import numpy as np
from itertools import permutations
from solutions import likelihoods


field_names = ['customer_id', 'age', 'amount']
debug = False


def permutations_of_3():
    return list(permutations([0, 1, 2]))


orderings = permutations_of_3()


prob_funcs = {'age': likelihoods.like_age,
              'amount': likelihoods.like_amount,
              'customer_id': likelihoods.like_cust_id}


def total_like_for_ordering(values_lists, ordering, debug=False):
    if debug:
        print('ordering', ordering)

    total_likelihood = 1.0

    for values in values_lists:
        values_reordered = [values[o] for o in ordering]
        probs = [prob_funcs[f](v) for f, v in zip(field_names, values_reordered)]
        prob_all_cols = probs[0] * probs[1] * probs[2]
        total_likelihood *= prob_all_cols

        row = {f: v for f, v in zip(field_names, values_reordered)}
        if debug:
            print('--------------')
            print(row)
            print('probs', probs)
            print('prob_all_cols', prob_all_cols)

    if debug:
        print('\nTotal like:', total_likelihood)

    return total_likelihood


def reordered_row(values_lists, index_best):
    ordering_best = orderings[index_best]
    values_reordered_list = [[values[o] for o in ordering_best] for values in values_lists]

    return [{f: v for f, v in zip(field_names, vals)} for vals in values_reordered_list]


def find_best_perm(values_lists, index_prior=None):
    like = [total_like_for_ordering(values_lists, ordering, debug=debug)
            for ordering in orderings]

    if index_prior is not None:
        # use the priors if you have any
        like = list(np.array(like) * np.array(index_prior))

    index_best = np.argmax(like)
    max_like = like[index_best]
    reordered = reordered_row(values_lists, index_best)
    probability = max_like/sum(like)

    if debug and probability:
        print(90 * '#')
        print('val lists')
        print(values_lists)

        print('index_best: %s, max_like: %s, probability: %s' % (index_best, max_like, probability))
        for row in reordered:
            print(row)

    return reordered, probability, index_best
