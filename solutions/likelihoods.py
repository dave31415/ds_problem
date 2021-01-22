import numpy as np


def like_cust_id(_):
    # constant
    return 1 / 27989.0


def like_age(xx):
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
    x = int(xx)
    if x < 0:
        return 0

    if x == 0:
        return 0.02

    if x > 1000:
        return 1e-20

    pi = 3.14159
    mu = 5.0
    sig = 1.8
    norm = 1.0 / (np.sqrt(2 * pi) * sig * x)
    u = ((np.log(x) - mu) / sig) ** 2
    u = min(u, 100)
    result = norm * np.exp(-0.5 * u)
    return result

