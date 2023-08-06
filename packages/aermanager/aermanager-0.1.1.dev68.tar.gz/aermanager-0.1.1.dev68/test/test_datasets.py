from pathlib import Path

HERE = Path(__file__).parent

# # To generate the dataset used for these tests:
# from aermanager.dataset_generator import gen_dataset_from_folders
# gen_dataset_from_folders(
#     source_path="data/",
#     destination_path="dataset_test",
#     compression=None,
#     crop_size=None,
#     hot_pixel_frequency=None,
#     time_window=None,
#     spike_count=5000,
# )


def test_frames():
    from aermanager.datasets import FramesDataset

    ds = FramesDataset(HERE / "dataset_test")
    assert len(ds) > 0
    data, label = ds[0]
    assert data.shape == (2, 240, 320)
    assert label == 0


def test_frames_transforms():
    from aermanager.datasets import FramesDataset

    ds = FramesDataset(HERE / "dataset_test",
                       transform=lambda fr: fr.sum(0, keepdims=True),
                       target_transform=lambda l: str(l))
    assert len(ds) > 0
    data, label = ds[0]
    assert data.shape == (1, 240, 320)
    assert label == "0"


def test_spiketrains():
    from aermanager.datasets import SpikeTrainDataset

    ds = SpikeTrainDataset(HERE / "dataset_test")
    assert len(ds) > 0
    data, label = ds[0]
    assert data.shape == (5000, )
    assert label == 0
