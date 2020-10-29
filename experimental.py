from readers import read_corrupted_ledger_file
from utils import batch_stream, get_temp_html
from plot_utils import add_hist_plot
from analysis import plot_likes
from bokeh.plotting import figure, show, output_file


field_names = ['customer_id', 'age', 'amount']


def get_amounts():
    ledger = read_corrupted_ledger_file()
    batches = list(batch_stream(ledger, 3))
    amount_list = []
    for batch in batches:
        cols = [[i[k] for i in batch] for k in field_names]
        has_zero = ['0' in col for col in cols]
        n_zero = sum(has_zero)
        assert n_zero <= 1
        if n_zero == 0:
            continue
        index = [i for i in range(3) if has_zero[i]]
        index = index[0]
        col = cols[index]
        amounts = [int(amount) for amount in col if amount != '0']
        amount_list.extend(amounts)

    x_range = [0, 5000]
    output_file(get_temp_html())
    fig = figure(width=800, height=500)

    add_hist_plot(amount_list, fig, n_bins=1000, x_range=x_range, normalize=True)
    plot_likes(x_range, fig)

    show(fig)

    return amount_list


if __name__ == "__main__":
    get_amounts()



