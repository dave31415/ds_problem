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


def find_best_perm(values_lists):
    values_reordered = None
    probs = None

    if debug:
        print('##############')

    like = []
    for ordering in orderings:
        total_likelihood = 1.0
        for values in values_lists:
            values_reordered = [values[o] for o in ordering]
            probs = [prob_funcs[f](v) for f, v in zip(field_names, values_reordered)]
            total_likelihood *= probs[0]*probs[1]*probs[2]

        like.append(total_likelihood)
        row = {f: v for f, v in zip(field_names, values_reordered)}
        if debug:
            print('--------------')
            print(row)
            print(probs)
            print(total_likelihood)

    index_best = np.argmax(like)
    if debug:
        print('index_best: %s' % index_best)

    ordering_best = orderings[index_best]
    values_reordered_list = [[values[o] for o in ordering_best] for values in values_lists]

    return [{f: v for f, v in zip(field_names, vals)} for vals in values_reordered_list]
