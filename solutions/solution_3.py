import numpy as np
from solutions.file_io import read_corrupted_ledger_file, write_file
from solutions.file_io import batch_stream
from solutions.max_like import find_best_perm, orderings
# Over an hour
# 97.78753713962284 %
# Another hour or so to add the priors for solution 4


debug = False
debug_prob_min = 0.99
probability_certainty = 0.9999


def count_n_same(list_1, list_2):
    return sum([l_1 == l_2 for l_1, l_2 in zip(list_1, list_2)])


def make_index_prior(index_best):
    # alpha is probability of not mutating, a guess
    alpha = 0.85
    ep = 1e-10
    indices = list(range(len(orderings)))
    prior = []
    for index in indices:
        if index == index_best:
            prior.append(alpha)
        else:
            ordering = orderings[index]
            ordering_best = orderings[index_best]

            if count_n_same(ordering, ordering_best) == 1:
                prior.append((1-alpha-ep)/3.0)
            else:
                prior.append(ep)
    return prior


def get_priors():
    return [make_index_prior(i) for i in range(len(orderings))]


def run_solution_3(use_priors=False):
    priors = None
    if use_priors:
        priors = get_priors()

    corrupted = read_corrupted_ledger_file()
    corrupted_batches = list(batch_stream(corrupted, 3))

    data_fixed = []
    index_prior = None
    num_uncertain = 0
    for batch_number, rows_list in enumerate(corrupted_batches):
        values_list = [list(line.values()) for line in rows_list]
        row_fixed_list, probability, index_best = find_best_perm(values_list, index_prior=index_prior)
        data_fixed.extend(row_fixed_list)

        num_uncertain += 1 * (probability < debug_prob_min)

        if use_priors and probability >= probability_certainty:
            index_prior = priors[index_best]
        else:
            index_prior = None

        if debug and probability < debug_prob_min:
            ok = input('OK?')
            if ok == 'q':
                return

    print('num_uncertain: %s' % num_uncertain)

    if use_priors:
        write_file(data_fixed, 'data/ledger_fixed_4.csv')
    else:
        write_file(data_fixed, 'data/ledger_fixed_3.csv')
