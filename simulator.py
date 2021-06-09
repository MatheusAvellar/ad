import cenario1
import cenario2
import cenario3
import cenario_extra

from util import parse_arguments

def main():
    args = parse_arguments()

    cenario_mapping = {
        '1': cenario1,
        '2': cenario2,
        '3': cenario3,
        'x': cenario_extra,
    }

    cenario = cenario_mapping[args.cenario]
    cenario.main(args)

if __name__ == '__main__':
    main()