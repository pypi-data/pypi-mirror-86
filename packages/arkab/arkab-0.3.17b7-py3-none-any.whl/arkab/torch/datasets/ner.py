import torch as th
from torch.utils.data import Dataset
from typing import Dict, List

Dicts = List[Dict]


class NERDatasetBase(Dataset):
    def __init__(self, data_source: Dicts, sent_key: str = 'sentence', tag_key: str = 'label'):
        self.dataSource = data_source
        self.length = len(self.dataSource)
        self.sent_key = sent_key
        self.tag_key = tag_key

    def get_pairs(self, index: int):
        """Return an sentence-tags pair

        :param index: index same as __getitem__
        :return: sentence, tags_of_sent
        """
        item = self.dataSource[index]
        sentence_ids = item[self.sent_key]
        label_ids = item[self.tag_key]
        return th.tensor(sentence_ids), th.tensor(label_ids)

    def prepare_others(self, index: int):
        """Other contents for return; if you want to use, you need to override this.

        :param index: same as __getitem__
        :return: tuple type of other things
        """
        return None
