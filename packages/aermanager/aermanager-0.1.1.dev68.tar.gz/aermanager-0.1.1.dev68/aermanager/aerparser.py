"""
'aerparser' module contains the implementation of functions for parsing .aerdat files
"""

import os
import struct
import numpy as np
from dv import AedatFile
from collections.abc import Callable

events_struct = [("x", np.uint16), ("y", np.uint16), ("t", np.uint64), ("p", np.bool)]


def make_structured_array(x, y, t, p):
    """
    Make a structured array given lists of x, y, t, p

    Args:
        x: List of x values
        y: List of y values
        t: List of times
        p: List of polarities boolean
    Returns:
        xytp: numpy structured array
    """
    return np.fromiter(zip(x, y, t, p), dtype=events_struct)


def parse_header_from_file(filename):
    """
    Get the aedat file version and start index of the binary data.

    Args:

        filename (str):     The name of the .aedat file

    Returns:
        data_version (float):   The version of the .aedat file
        data_start (int):       The start index of the data
    """
    filename = os.path.expanduser(filename)
    assert os.path.isfile(filename), f"The .aedat file '{filename}' does not exist."
    f = open(filename, "rb")
    count = 1
    is_comment = "#" in str(f.read(count))

    while is_comment:
        # Read the rest of the line
        head = str(f.readline())
        if "!AER-DAT" in head:
            data_version = float(head[head.find("!AER-DAT") + 8: -5])
        is_comment = "#" in str(f.read(1))
        count += 1
    data_start = f.seek(-1, 1)
    f.close()
    return data_version, data_start


def get_aer_events_from_file(filename, data_version, data_start):
    """
    Get aer events from an aer file.

    Args:
        filename (str):         The name of the .aedat file
        data_version (float):   The version of the .aedat file
        data_start (int):       The start index of the data

    Returns:
         all_events:          Numpy structured array:
                                  ['address'] the address of a neuron which fires
                                  ['timeStamp'] the timeStamp in mus when a neuron fires
    """
    filename = os.path.expanduser(filename)
    assert os.path.isfile(filename), \
        "The .aedat file does not exist."
    f = open(filename, "rb")
    f.seek(data_start)

    if 2 <= data_version < 3:
        event_dtype = np.dtype([("address", ">u4"), ("timeStamp", ">u4")])
        all_events = np.fromfile(f, event_dtype)
    elif data_version > 3:
        event_dtype = np.dtype([("address", "<u4"), ("timeStamp", "<u4")])
        event_list = []
        while True:
            header = f.read(28)
            if not header or len(header) == 0:
                break

            # read header
            capacity = struct.unpack("I", header[16:20])[0]
            event_list.append(np.fromfile(f, event_dtype, capacity))
        all_events = np.concatenate(event_list)
    else:
        raise NotImplementedError()
    f.close()
    return all_events


def parse_aedat4(in_file):
    """
    Get the aer events from version 4 of .aedat file

    Args:
        in_file: str The name of the .aedat file
    Returns:
        shape (Tuple): Shape of the sensor (height, width)
        xytp:   numpy structured array of events
    """
    with AedatFile(in_file) as f:
        shape = f['events'].size
        x, y, t, p = [], [], [], []
        for packet in f.numpy_packet_iterator("events"):
            x.append(packet["x"])
            y.append(packet["y"])
            t.append(packet["timestamp"])
            p.append(packet["polarity"])
    x = np.hstack(x)
    y = np.hstack(y)
    t = np.hstack(t)
    p = np.hstack(p)
    xytp = make_structured_array(x, y, t, p)
    return shape, xytp


def parse_dvs_128(all_events):
    """
    Get the aer events from DVS with resolution of rows and cols are (128, 128)

    Args:
        all_events: events in numpy structure
    Returns:
        xytp: numpy structured array of events
    """
    all_addr = all_events["address"]
    t = all_events["timeStamp"]

    x = (all_addr >> 8) & 0x007F
    y = (all_addr >> 1) & 0x007F
    p = all_addr & 0x1

    xytp = make_structured_array(x, y, t, p)
    return xytp


def parse_dvs_ibm(all_events):
    """
    Get the aer events from DVS with ibm gesture dataset

    Args:
        all_events: events in numpy structure
    Returns:
        xytp: numpy structured array of events
    """
    all_addr = all_events["address"]
    t = all_events["timeStamp"]

    # x = (all_addr >> 17) & 0x007F
    # y = (all_addr >> 2) & 0x007F
    # p = (all_addr >> 1) & 0x1

    x = (all_addr >> 17) & 0x00001FFF
    y = (all_addr >> 2) & 0x00001FFF
    p = (all_addr >> 1) & 0x00000001

    xytp = make_structured_array(x, y, t, p)
    return xytp


def parse_dvs_red(all_events):
    """
    Get the aer events from DVS with resolution of (260, 346)
    Args:

        all_events: events in numpy structure

    Returns:

        xytp: numpy structured array of events
    """
    all_addr = all_events["address"]
    t = all_events["timeStamp"]

    x = (all_addr >> 17) & 0x7FFF
    y = (all_addr >> 2) & 0x7FFF
    p = (all_addr >> 1) & 0x1

    xytp = make_structured_array(x, y, t, p)
    return xytp


def parse_dvs_346mini(all_events):
    """
    Get the aer events from DVS with resolution of (132,104)

    Args:
        all_events: events in numpy structure
    Returns:
        xytp: numpy structure of xytp

    """
    all_addr = all_events["address"]
    t = all_events["timeStamp"]

    x = (all_addr >> 22) & 0x01FF
    y = (all_addr >> 12) & 0x03FF
    p = (all_addr >> 11) & 0x1

    xytp = make_structured_array(x, y, t, p)
    return xytp


def parse_dvs(all_events, dvs_model):
    """
    Parse data from raw address and timeStamp to x, y, t, p.

    Args:
        all_events:
            Numpy structured array
            ['address'] the address of a neuron which fires
            ['timeStamp'] the timeStamp in mus when a neuron fires

        dvs_model  (str):
            Name of the DVS model. Currently only 3 supported:
            'DVS128': resolution of rows and cols are (128, 128)
            'mini346': resolution of rows and cols are (260, 346)
            'redV3': resolution of rows and cols are (132,104)

    Returns:
        shape (tuple):
            (height, width) of the sensor array
        aer_data (np.ndarray):
            Structured Numpy array of Class DvsData where nsOutputData.data is:
            ["x"]: int Row ID of a spike
            ["y"]: int Column ID of a spike
            ["p"]: bool 'On' (polarity=0) or 'Off' (polarity=1)
            Channel of a spike
            ["t"]: float Timestamp of a spike in ms
    """

    if dvs_model == "DVS128":
        shape = (128, 128)
        aer_data = parse_dvs_128(all_events)
    elif dvs_model == "mini346":
        shape = (260, 346)
        aer_data = parse_dvs_346mini(all_events)
    elif dvs_model == "redV3":
        shape = (132, 104)
        aer_data = parse_dvs_red(all_events)
    elif dvs_model == "ibm":
        shape = (128, 128)
        aer_data = parse_dvs_ibm(all_events)
    elif Callable(dvs_model):
        shape, aer_data = dvs_model(all_events)
    else:
        raise NotImplementedError("DVS model not recognized.")
    return shape, aer_data


def load_events_from_file(filename, dvs_model):
    """
    Load_events_from_file(filename, dvs_model) - Method, convert .aedat file into Numpy Sturctured array of Class DvsData

    Args:
        filename (str):
            The name of the .aedat file

        dvs_model (str):
            Name of the DVS model. Currently only 3 supported:
            'DVS128': resolution of rows and cols are (128, 128)
            'mini346': resolution of rows and cols are (260, 346)
            'redV3': resolution of rows and cols are (132,104)

    Returns:
        shape (Tuple):
            (height, width) or None if it cannot be inferred
        aer_data:
            Structured Numpy array of Class DvsData where aer_data.data is:
            ["x"]: int Row ID of a spike
            ["y"]: int Column ID of a spike
            ["polarity"]: bool 'On' (polarity=0) or 'Off' (polarity=1)
            Channel of a spike
            ["timeStamp"]: float Timestamp of a spike in ms
    """
    data_version, data_start = parse_header_from_file(filename)

    if data_version >= 4:
        shape, aer_data = parse_aedat4(filename)
    else:
        if not dvs_model:
            raise ValueError("A DVS Model must be specified for older aedat files.")
        all_events = get_aer_events_from_file(filename, data_version, data_start)
        shape, aer_data = parse_dvs(all_events, dvs_model)

    return shape, aer_data
