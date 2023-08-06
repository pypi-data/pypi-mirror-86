from typing import Literal, Tuple

from pytorch_pretrained_bert import BertModel, BertTokenizer

UNCASE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:\'"/\\|_@#$%^&*~`+-=<>()[]{} '
CASED_ALPHABAT = 'abcdefghijklmnopqrstuvwxyz'.upper() + UNCASE_ALPHABET
washing = {"“": '\"', "”": '\"'}


def load_bert(pretrain_path: str) -> Tuple[BertTokenizer, BertModel]:
    """Load bert tokenizer and model from given path
    Using pytorch_pretrained_bert

    :param pretrain_path: path contains bert pretrain contents
    :return: BertTokenizer, BertModel
    """
    tokenizer = BertTokenizer.from_pretrained(pretrain_path)
    model = BertModel.from_pretrained(pretrain_path)
    return tokenizer, model


class ChineseCharTokenizer:
    def __init__(self, bert_path: str):
        super(ChineseCharTokenizer, self).__init__()
        self.bert_tokenizer = BertTokenizer.from_pretrained(bert_path)

    def convert_sequence_to_id(self, sentence: str, padding_length: int = -1):
        """Convert Chinese sentence to id in bert model

        :param sentence:
        :param padding_length:
        :return:
        """
        sentence_char = list(sentence)
        sentence_char = [
            c.lower() if c in CASED_ALPHABAT else c for c in sentence_char]
        sentence_char = [washing[c] if c in washing.keys()
                         else c for c in sentence_char]
        if padding_length > 0:
            padding_list = ['[PAD]']
            padding_list = padding_list * padding_length
            sentence_char.extend(padding_list)
        sentence_idx = self.bert_tokenizer.convert_tokens_to_ids(sentence_char)
        assert len(sentence_idx) == len(sentence_char)
        return sentence_idx
