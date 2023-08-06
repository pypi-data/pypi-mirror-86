import torch
from seqeval.metrics import f1_score, accuracy_score, precision_score, recall_score
from arkab.torch.tensor import count_zero, is_zero
from rich.console import Console
import json

logger = Console()


def _ner_metrics(golden_label: list, prediction: list) -> dict:
    """
    Convient metrics for NER tasks

    :param golden_label: the true label sequence, 2d with [N, length]
    :param prediction: prediction output by your model
    :return: dict type; including F1, Precision, Recall, Acc
    """
    result = dict()
    result['F1'] = f1_score(y_pred=prediction, y_true=golden_label)
    result['Precision'] = precision_score(y_true=golden_label, y_pred=prediction)
    result['Recall'] = recall_score(y_pred=prediction, y_true=golden_label)
    result['Acc'] = accuracy_score(y_pred=prediction, y_true=golden_label)
    return result


def ner_metrics(golden_labels: torch.Tensor,
                predictions: torch.Tensor,
                debug: bool = False):
    """
    NER metrics

    :param golden_labels: Tensor
    :param predictions: Tensor
    :param debug: Bool, if true debug informations.
    :return:
    """
    assert golden_labels.dim() == predictions.dim(), \
        f"golden_labels dimensions should be same as predictions, but got predictions dim " \
        f"{predictions.dim()} and golden_labels dim {golden_labels.dim()}"
    assert golden_labels.dim() == 2, f"This metrics is for 2-d data shape like [N, seq_length]"
    if debug:
        logger.log(f"{is_zero(predictions)=}")
        logger.log(f"{count_zero(predictions)=}")
    golden_list = golden_labels.cpu().tolist()
    preds = predictions.cpu().tolist()
    return _ner_metrics(golden_list, preds)


class NERMetricBase:
    f1: float
    precision: float
    recall: float

    def __lt__(self, other):
        if not isinstance(other, NERMetricBase):
            return NotImplemented
        if self.f1 < other.f1:
            return True
        if self.recall < other.recall and self.precision < other.precision:
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, NERMetricBase):
            raise NotImplemented
        return self.recall == other.recall and self.f1 == other.f1 and self.precision == other.precision

    def __str__(self):
        res = dict()
        res['F1'] = f"{self.f1:.3}"
        res['Recall'] = f"{self.recall:.3f}"
        res['Precision'] = f"{self.precision:.3f}"
        result_str = json.dumps(res)
        return result_str
