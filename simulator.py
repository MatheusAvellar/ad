import cenario1
import cenario2
import cenario3

from util import parse_arguments

def main():
    args = parse_arguments()

    print(args)
    cenario_mapping = {
        '1': cenario1,
        '2': cenario2,
        '3': cenario3,
    }

    cenario = cenario_mapping[args.cenario]
    cenario.run_simulation(args.cache, n_sims=args.n_sims, n_rounds=args.n_rounds)

if __name__ == '__main__':
    main()