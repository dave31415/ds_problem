from readers import read_ledger_file, read_corrupted_ledger_file
from plot_utils import add_hist_plot
from bokeh.plotting import figure, show, output_file
import numpy as np
import params


def make_histograms():
    output_file('junk.html')
    data = list(read_ledger_file())

    age = [int(i['age']) for i in data]
    amount = [int(i['amount']) for i in data]
    cust_id = [int(i['customer_id']) for i in data]

    fig = figure(width=900, height=600)
    x_range = [0, 5000]
    add_hist_plot(age, fig, x_range=x_range, n_bins=1000, color='blue', normalize=True)
    add_hist_plot(amount, fig, x_range=x_range, n_bins=300, color='red', normalize=True)

    norm = params.num_lines/x_range[1]
    add_hist_plot(cust_id, fig, x_range=x_range, n_bins=25, color='green', normalize=True, norm=norm)
    x = np.linspace(0, x_range[1], x_range[1])
    y = np.ones(x_range[1])/params.num_lines
    fig.line(x, y, color='black', alpha=0.6, line_dash='dashed')

    amount = np.sort(amount)
    cum_amount = np.cumsum(amount)
    x = amount
    y = cum_amount*0.01/cum_amount[-1]

    index = x < x_range[1]
    x = x[index]
    y = y[index]

    fig.line(x, y, color='gray', alpha=0.6, line_dash='dashed')
    fig.line(x_range, [0.005, 0.005], color='gray', alpha=0.6, line_dash='dotted')
    fig.circle(x, y, color='red', alpha=0.6, size=2)

    show(fig)


def make_histograms_corrupt():
    output_file('junk2.html')
    data = list(read_corrupted_ledger_file())

    amount = [int(i['amount']) for i in data]

    fig = figure(width=900, height=600)
    x_range = [0, 2000]
    add_hist_plot(amount, fig, x_range=x_range, n_bins=200, color='red', normalize=True)

    x = np.linspace(0, x_range[1], x_range[1])
    y = np.ones(x_range[1])/params.num_lines
    fig.line(x, y, color='black', alpha=0.6, line_dash='dashed')

    show(fig)


if __name__ == "__main__":
    make_histograms()
    make_histograms_corrupt()
