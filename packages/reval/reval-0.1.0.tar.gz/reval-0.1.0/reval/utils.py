import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import matthews_corrcoef, accuracy_score, f1_score, \
    precision_score, recall_score


def kuhn_munkres_algorithm(true_lab, pred_lab):
    """
    Function that implements the Kuhn-Munkres algorithm method.
    It selects the best label permutation of the
    predicted labels that minimizes the
    misclassification error when compared to the true labels.
    In order to allow for the investigation
    of replicability of findings between training and test sets,
    in the context of reval we permute
    clustering labels to match classification labels,
    in order to retain the label organization
    based on training dataset. This because otherwise we would loose the
    correspondence between training and test
    sets labels.

    :param true_lab: classification algorithm labels (for reval).
    :type true_lab: ndarray, (n_samples,)
    :param pred_lab: clustering algorithm labels (for reval).
    :type pred_lab: ndarray, (n_samples,)
    :return: permuted labels that minimize the misclassification error.
    :rtype: ndarray, (n_samples,)
    """
    if not (isinstance(true_lab, np.ndarray) and isinstance(pred_lab, np.ndarray)):
        true_lab, pred_lab = np.array(true_lab), np.array(pred_lab)
    if (true_lab.dtype == 'int' or true_lab.dtype == 'int32') and (
            pred_lab.dtype == 'int' or pred_lab.dtype == 'int32'):
        wmat = _build_weight_mat(true_lab, pred_lab)
        new_pred_lab = list(linear_sum_assignment(wmat)[1])
        try:
            pred_perm = np.array([new_pred_lab.index(i) for i in pred_lab])
            return pred_perm
        # Catch the case in which predicted array has more unique labels than true array. Raise ValueError
        # if input has length 1.
        except ValueError:
            if len(true_lab) == 1 or len(pred_lab) == 1:
                raise ValueError("Dimensions of input array should be greater than 1.")
            # True labels are less than predicted labels. Permuting only the available labels.
            else:
                pred_perm = np.array([], dtype=int)
                for i in pred_lab:
                    if len(new_pred_lab) <= i or i < 0:
                        pred_perm = np.append(pred_perm, i)
                    else:
                        pred_perm = np.append(pred_perm, new_pred_lab.index(i))
                return pred_perm
    else:
        raise TypeError(f'Input variables should be array-like structures of integers.'
                        f' Received ({true_lab.dtype}, {pred_lab.dtype})')


def _build_weight_mat(true_lab, pred_lab):
    """
    This private function allows to build a weight matrix to select the best permutation of
    predicted labels that minimizes the misclassification error when compared to true labels.

    :param true_lab: clustering labels, (n_samples,).
    :type true_lab: ndarray
    :param pred_lab: classification labels, (n_samples,).
    :type pred_lab: ndarray
    :return: weight matrix (number of true classes, number of true classes).
    :rtype: ndarray
    """
    if not (isinstance(true_lab, np.ndarray) and isinstance(pred_lab, np.ndarray)):
        raise TypeError("Numpy array required.")
    nclass, nobs = len(set(true_lab)), len(true_lab)
    wmat = np.zeros((nclass, nclass))
    for lab in range(nclass):
        for plab in range(lab, nclass):
            n_intersec = len(set(np.flatnonzero(true_lab == lab)).intersection(
                set(np.flatnonzero(pred_lab == plab))))
            w = (nobs - n_intersec) / nobs
            if lab == plab:
                wmat[lab, plab] = w
            else:
                wmat[lab, plab] = w
                n_intersec = len(set(np.flatnonzero(true_lab == plab)).intersection(
                    set(np.flatnonzero(pred_lab == lab))))
                w = (nobs - n_intersec) / nobs
                wmat[plab, lab] = w
    return wmat


def compute_metrics(class_labels, clust_labels, perm=False):
    """
    Function that computes useful classification metrics. If needed the
    clustering labels are permuted with :reval.utils.kuhn_munkres_algorithm:
    The function returns a dictionary with ACC, MCC, F1, precision, recall as keys
    for accuracy, Matthews correlation coefficient, F1 score, precision, and recall,
    respectively.

    :param class_labels: labels returned by the classifier.
    :type class_labels: array-like
    :param clust_labels: labels returned by the clustering.
    :type clust_labels: array-like
    :param perm: flag to enable permutation of clustering labels, default False.
    :type perm: bool
    :return: dictionary of scores.
    :rtype: dict
    """
    if perm:
        perm_clust_labels = kuhn_munkres_algorithm(class_labels, clust_labels)
    else:
        perm_clust_labels = clust_labels
    if len(set(class_labels)) == 2 and len(set(perm_clust_labels)) == 2:
        scores = {'ACC': accuracy_score(class_labels, perm_clust_labels),
                  'MCC': matthews_corrcoef(class_labels, perm_clust_labels),
                  'F1': f1_score(class_labels, perm_clust_labels),
                  'precision': precision_score(class_labels, perm_clust_labels),
                  'recall': recall_score(class_labels, perm_clust_labels)}
    else:
        scores = {'ACC': accuracy_score(class_labels, perm_clust_labels),
                  'MCC': matthews_corrcoef(class_labels, perm_clust_labels),
                  'F1': f1_score(class_labels, perm_clust_labels, average='macro'),
                  'precision': precision_score(class_labels, perm_clust_labels,
                                               average='macro', zero_division=0),
                  'recall': recall_score(class_labels, perm_clust_labels, average='macro',
                                         zero_division=0)}
    return scores
