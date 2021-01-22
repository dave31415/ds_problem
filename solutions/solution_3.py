import numpy as np
from solutions.file_io import read_corrupted_ledger_file, write_file
from solutions.file_io import batch_stream
from solutions.max_like import find_best_perm, orderings, make_index_prior
# Over an hour to implement (prior to additional refactoring)
# 97.78753713962284 %
# Another hour or so to add the priors for solution 4


debug = False
debug_prob_min = 0.99

# good enough certainty to apply the prior to next buffer as if prob=1
# turns out to be insensitive to this
probability_certainty = 0.9999


def get_priors():
    return [make_index_prior(i) for i in range(len(orderings))]


def run_solution_3(use_priors=False):
    """
    This is a maximum likelihood technique. Using priors was added later
    and that defines solution 4.
    The idea is that there are 6 possible assignments for the the three columns.
    For each assigmennt we, can calculate the likelihood if we had likelihood functions
    for each of the data fields (customer_id, age,amount). The likelihood of the
    assignment is just the product of each of those likelihood functions evaluated at
    the assigned line values.
    Example: if the numbers are 12, 55, 676 and the assignment we are considering is
    (age, amount, customer_id), the likelihood is
    Likelihood_age(12) * Likelihood_amount(55) * Likelihood_cust_id(676)
    This will ber zero because  Likelihood_age(12) is zero. The probablility of the age
    being 12 is zero as per the problem statement.
    For the assignment  (amount, age, customer_id), it is
    Likelihood_amount(12) * Likelihood_age(55) * Likelihood_cust_id(676)
    This is now non-zero.
    Likelihood_cust_id(x) is just a constant since it is a uniform distribution
    We now just have to model the distributions: Likelihood_age(x) and Likelihood_amount(x)
    :param use_priors: If true, it will impose the condition that contiguous buffer regions
    must have assignments where no more than one swap has happened. That is, one
    the column assignments must stay put.
    Therefore if we know for sure that one buffer has the assigment
    (age, amount, customer_id), for the next buffer, we can rule out two of
    the assignments. That is, we can give those assignments a "prior" of zero.
    That essentially makes this a Bayesian method. In some cases this can help.

    This approach assumes that we know for sure that the first assignment is correct
    before creating a prior for the next one. While we can usually not be sure, in
    many cases we certain enough to use that approximation.

    A better and more general technique would try to apply priors to all contiguous
    buffers simultaneously and determine the maxmium a posteori solution without requiring
    certainty about one buffer before looking at the next. For example, imagine there are just
    two buffers. There are 6 assignments for the first one and 6 for the second so 6*6 = 36
    total assignments. But there are really only 6*4=24 that are feasible due to this condition.
    If there are three buffers, there are 6*4*4 = 96. In general 6*(4^(N-1)) possible
    assignments with N buffers. Obviously we have an exponentially
    increasing sized parameter space so this seems hopeless.
    Yet, there is a miraculous way of making this tractable which makes use
    of the Viterbi algorithm. That is, we can reduce the number of joint assignment that
    need to be checked to be O(N). It uses a forward pass and a backwards pass. The
    algorithm has actually been discovered many different times and has many different names.
    We have not implemented the Viterbi algorithm version here but we have done so with an
    earlier version of this problem. In practice, it's unlikely to work much better or
    any better than this simpler version using the prior.

    Not using the prior and setting the buffer size to 3 just reduces this to solution 2
    which ignores the buffer and just tries to get each line correct. Since this combines
    information within a buffer it works much better.
    :return:
    """
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
