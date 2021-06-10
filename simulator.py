import cenario1
import cenario2
import cenario3
import cenario4
import cenario_extra

from util import parse_arguments

def main():
    args = parse_arguments()

    cenario_mapping = {
        '1': cenario1,
        '2': cenario2,
        '3': cenario3,
        '4': cenario4,
        'x': cenario_extra,
    }

    cenario = cenario_mapping[args.cenario]
    means = cenario.main(args)
    if args.plot:
        import numpy as np
        from scipy.stats import norm
        import matplotlib.pyplot as plt

        # Fit a normal distribution to the data:
        mu, std = norm.fit(means)

        # Plot the histogram.
        plt.hist(means, bins=8, density=True, alpha=0.6, color='g')

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
        plt.title(title)

        plt.show()

if __name__ == '__main__':
    main()