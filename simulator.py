import cenario1
import cenario2
import cenario3

from util import parse_arguments

def main():
    args = parse_arguments()

    cenario_mapping = {
        '1': cenario1,
        '2': cenario2,
        '3': cenario3,
    }

    cenario = cenario_mapping[args.cenario]
    cenario.main(args)

if __name__ == '__main__':
    main()