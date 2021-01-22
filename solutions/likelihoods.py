"""
Here we define out likelihood functions or rather a good guess at them
Most important is that
1) customer_id likelihood is a constant function
2) likelihood for age rules out ages outside the range [18,100 (or so)]
3) Amount does not rule out [0,18] and gives some preference to smaller values
over bigger ones. You know for example that the average amount is roughly 7 million/10,000 = 700.

If you have at least modeled those conditions into the likelihoods, you do surprisingly well.
If you work harder to determine better what they are, you can improve on it.

How can you learn more about these individual distributions since
making a histogram of the numbers in any columns will show just the
superposition of them?

It's reasonable to assume that customer_ids are just
incrementing numbers and therefor have a uniform distribution. That
seems consistent with how the histograms look. It turns out to be true.

Separating the age dist from the amount dist is harder but not impossible.
For example, the number 0 is not uncommon at that must almost always be amount.
At worse, one of those could be customer_id. So whenever you find a row with a 0, you
know that column is amount and so the other two rows in that column must be samples from
the amount distribution. Make a histogram of those and you will see a single-model function
which looks (and actually is) a log-normal distribution superposed with a spike at 0. That
allows you to model the amount distribution.

If you histogram the other numbers in those same buffers, you will know they must be
a superposition of age and customer_id and you know customer_id is very likely uniform.
This demonstrates that the age distribution looks like (and actually is) a half normal
distribution centered on age 18.

There are other ways to extract this information and come to the same conclusions by
performing similar experiments. You can if you wish create various tests to make sure
the distributions were not specifically designed to fool you (i.e. bimodal distributions sharing
a similar peak) but the simplest explanation happens to be correct. There is enough information
to rule out these more bizarre possibilities.
"""

import numpy as np


def like_cust_id(_):
    """
    constant function
    The exact number you out into here is not that important
    the largest value seen in the data is very likely the top end of customer id
    """
    return 1 / 27989.0


def like_age(xx):
    """
    A half Gaussian centered at 18
    Zero outside the range [0, 120].
    The 120 is just a reasonable guess. 18 is given as a lower limit.
    :param xx: The point to evaluate at
    :return: likelihood
    """
    x = int(xx)
    if x < 18:
        return 0

    if x > 120:
        return 0

    x = int(xx)

    pi = 3.14159
    mu = 18.0
    sig = 17.0
    norm = 2.0 / (np.sqrt(2 * pi) * sig)
    u = ((x - mu) / sig) ** 2
    u = min(u, 100)
    result = norm * np.exp(-0.5 * u)
    return result


def like_amount(xx):
    """
    A log-normal distribution
    You can fiddle with the parameters until it seems to fit the data.
    You still get a good solution when these parameters are off by quite a bit.
    :param xx:
    :return:
    """
    x = int(xx)
    if x < 0:
        return 0

    if x == 0:
        # this models a spike at 0
        return 0.02

    if x > 4000:
        # make it constant but small at very high values rather
        # than evaluating the log-normal there. There is really no
        # great way to check the tails all that well.
        # any points greater than this max-value will get
        # assigned customer-id with almost certainty
        return 1e-20

    # otherwise, a regular log-normal distribution
    pi = 3.14159
    mu = 5.0
    sig = 1.8
    norm = 1.0 / (np.sqrt(2 * pi) * sig * x)
    u = ((np.log(x) - mu) / sig) ** 2
    u = min(u, 100)
    result = norm * np.exp(-0.5 * u)
    return result

