from readers import read_ledger_file
import numpy as np
from matplotlib import pylab as plt


def dist_plot(normed=True):
    num = 700
    range = (0, num)
    ledger = read_ledger_file()
    amount = np.array([int(i['amount']) for i in ledger])
    age = np.array([int(i['age']) for i in ledger])
    street_num = np.array([int(i['address_num']) for i in ledger])
    plt.clf()
    plt.hist(amount, num, range=range, alpha=0.3,
             normed=normed, label='Amount')
    plt.hist(age, num, range=range, alpha=0.3,
             normed=normed, label='Age')
    plt.hist(street_num, num, range=range, alpha=0.3,
             normed=normed, label='Street number')
    plt.legend()

