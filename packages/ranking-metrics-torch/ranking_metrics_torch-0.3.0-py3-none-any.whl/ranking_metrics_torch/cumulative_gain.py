import torch

from ranking_metrics_torch.common import _check_inputs
from ranking_metrics_torch.common import _create_output_placeholder
from ranking_metrics_torch.common import _extract_topk
from ranking_metrics_torch.common import _mask_with_nans


def dcg_at(
    ks: torch.Tensor, scores: torch.Tensor, labels: torch.Tensor, log_base: int = 2
) -> torch.Tensor:
    """Compute discounted cumulative gain at K for provided cutoffs (ignoring ties)

    Args:
        ks (torch.Tensor or list): list of cutoffs
        scores (torch.Tensor): predicted item scores
        labels (torch.Tensor): true item labels

    Returns:
        torch.Tensor: list of discounted cumulative gains at cutoffs
    """
    ks, scores, labels = _check_inputs(ks, scores, labels)
    topk_scores, topk_indices, topk_labels = _extract_topk(ks, scores, labels)
    dcgs = _create_output_placeholder(scores, ks)

    # Compute discounts
    discount_positions = torch.arange(
        ks.max().item(), device=scores.device, dtype=torch.float64
    )

    discount_log_base = torch.log(
        torch.tensor([log_base], device=scores.device, dtype=torch.float64)
    ).item()

    discounts = 1 / (torch.log(discount_positions + 2) / discount_log_base)

    # Compute DCGs at K
    for index, k in enumerate(ks):
        dcgs[:, index] = torch.sum(
            (topk_labels[:, :k] * discounts[:k].repeat(topk_labels.shape[0], 1)), dim=1
        )

    return _mask_with_nans(dcgs, labels)


def ndcg_at(
    ks: torch.Tensor, scores: torch.Tensor, labels: torch.Tensor, log_base: int = 2
) -> torch.Tensor:
    """Compute normalized discounted cumulative gain at K for provided cutoffs (ignoring ties)

    Args:
        ks (torch.Tensor or list): list of cutoffs
        scores (torch.Tensor): predicted item scores
        labels (torch.Tensor): true item labels

    Returns:
        torch.Tensor: list of discounted cumulative gains at cutoffs
    """
    ks, scores, labels = _check_inputs(ks, scores, labels)
    topk_scores, topk_indices, topk_labels = _extract_topk(ks, scores, labels)
    ndcgs = _create_output_placeholder(scores, ks)

    # Compute discounted cumulative gains
    gains = dcg_at(ks, topk_scores, topk_labels)
    normalizing_gains = dcg_at(ks, labels, labels)

    # Prevent divisions by zero
    relevant_pos = (normalizing_gains != 0).nonzero(as_tuple=True)
    irrelevant_pos = (normalizing_gains == 0).nonzero(as_tuple=True)

    gains[irrelevant_pos] = 0
    gains[relevant_pos] /= normalizing_gains[relevant_pos]

    return _mask_with_nans(gains, labels)
