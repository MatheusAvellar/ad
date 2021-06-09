import argparse
import numpy as np


def write_csv(*args):
    # tempo;cache;cid;tipo_requisicao;n_requisicoes_pendentes
    csv_str = ';'.join(args)
    print(csv_str)

def write_log(tempo='0', cache='0', cid='0', tipo_requisicao='hit', n_requisicoes_pendentes='0'):
    write_csv(str(tempo), str(cache), str(cid), tipo_requisicao, str(n_requisicoes_pendentes))

# [Ref] https://stackoverflow.com/c/ad-2020-2/a/64/9
def confidence_interval(data):
    media = np.mean(data)
    z = 1.96
    std_err = np.std(data)/np.sqrt(len(data))
    intervalo_de_confianca = (media - z * std_err, media + z * std_err)
    return intervalo_de_confianca

def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulador de Caching em Redes com Perdas e Atrasos')

    parser.add_argument('-c', '--cenario', type=str, default='1',
                        help='Cenário a ser simulado [1|2|3|4]', dest='cenario')
    parser.add_argument('-t', '--cache', type=str, default='FIFO',
                        help='Tipo de cache a ser utilizada [FIFO|LRU|RAND|STATIC]', dest='cache')
    parser.add_argument('-n', '--sims', type=int, default=1000,
                        help='Número de simulações a serem executadas', dest='n_sims')
    parser.add_argument('-r', '--rounds', type=int, default=50,
                        help='Número de rodadas a serem realizadas', dest='n_rounds')

    parser.add_argument('-l', '--lambda', type=int, default=1,
                        help='Lambda', dest='lambda_')
    parser.add_argument('-N', '--contents', type=int, default=3,
                        help='Número de conteúdos a serem processados', dest='N')
    parser.add_argument('-e', '--events', type=int, default=100,
                        help='Número de eventos a ocorrerem antes da simulação acabar', dest='n_events')
    parser.add_argument('-cs', '--cache-size', type=int, default=2,
                        help='Tamanho da cache', dest='cache_size')

    parser.add_argument('-p', type=float, default=1,
                        help='Probabilidade da requisição chegar a cache', dest='p')

    return parser.parse_args()