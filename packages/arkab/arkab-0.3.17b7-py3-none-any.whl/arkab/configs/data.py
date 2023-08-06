from tap import Tap


class DataConfigBase(Tap):
    train_path: str  # train data path
    test_path: str  # test data path
    valid_path: str  # valid data path
    batch: int = 1  # batch size
