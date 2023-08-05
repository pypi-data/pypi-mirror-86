import torch

from ranking_metrics_torch.common import _check_inputs
from ranking_metrics_torch.common import _extract_topk
from ranking_metrics_torch.common import _create_output_placeholder
from ranking_metrics_torch.common import _mask_with_nans


def precision_at(
    ks: torch.Tensor, scores: torch.Tensor, labels: torch.Tensor
) -> torch.Tensor:
    """Compute precision@K for each of the provided cutoffs

    Returns NaN when there are no relevant items present in the labels.

    Args:
        ks (torch.Tensor or list): list of cutoffs
        scores (torch.Tensor): predicted item scores
        labels (torch.Tensor): true item labels

    Returns:
        torch.Tensor: list of precisions at cutoffs
    """

    ks, scores, labels = _check_inputs(ks, scores, labels)
    _, _, topk_labels = _extract_topk(ks, scores, labels)
    precisions = _create_output_placeholder(scores, ks)

    for column, k in enumerate(ks):
        precisions[:, column] = torch.sum(topk_labels[:, : int(k)], dim=1) / float(k)

    return _mask_with_nans(precisions, labels)


def recall_at(
    ks: torch.Tensor, scores: torch.Tensor, labels: torch.Tensor
) -> torch.Tensor:
    """Compute recall@K for each of the provided cutoffs

    Args:
        ks (torch.Tensor or list): list of cutoffs
        scores (torch.Tensor): predicted item scores
        labels (torch.Tensor): true item labels

    Returns:
        torch.Tensor: list of recalls at cutoffs
    """

    ks, scores, labels = _check_inputs(ks, scores, labels)
    _, _, topk_labels = _extract_topk(ks, scores, labels)
    recalls = _create_output_placeholder(scores, ks)

    # Compute recalls at K
    num_relevant = torch.sum(labels, dim=1)
    rel_indices = (num_relevant != 0).nonzero(as_tuple=False)

    if rel_indices.shape[0] > 0:
        for index, k in enumerate(ks):
            rel_labels = topk_labels[rel_indices, : int(k)].squeeze()
            rel_count = num_relevant[rel_indices].squeeze()

            recalls[rel_indices, index] = torch.div(
                torch.sum(rel_labels, dim=1), rel_count
            ).reshape(len(rel_indices), 1)

    return _mask_with_nans(recalls, labels)
