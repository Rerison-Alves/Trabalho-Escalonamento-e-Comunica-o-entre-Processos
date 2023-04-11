from escalonador import Processo
from escalonador import EscalonadorRoundRobin
import graphicsprinter as gp

# Teste da simulação
if __name__ == '__main__':
    quantums = range(1, 31)
    # Listas para armazenar os resultados de cada simulação
    tempos_medios_espera = []
    tempos_medios_retorno = []
    vazoes = []
    # teste de simulações
    for quantum in quantums:
        processos = [Processo(1, 10), Processo(2, 5), Processo(3, 8), Processo(4, 7)]

        for p in processos:
            p.burst += 1  # adiciona 1 unidade de tempo para mudança de contexto
        escalonador = EscalonadorRoundRobin(quantum)

        for p in processos:
            escalonador.adicionar_processo(p)
        escalonador.executar_todos()

        tempos_medios_espera.append(escalonador.tempo_medio_espera())
        tempos_medios_retorno.append(escalonador.tempo_medio_retorno())
        vazoes.append(escalonador.vazao())

        print(f'Tempo médio de espera no quantum {quantum}: {escalonador.tempo_medio_espera()}')
        print(f'Tempo médio de retorno no quantum {quantum}: {escalonador.tempo_medio_retorno()}')
        print(f'Vazão no quantum {quantum}: {escalonador.vazao()} processos por unidade de tempo')

    # Imprime os resultados
    gp.printer(quantums, tempos_medios_espera, tempos_medios_retorno, vazoes)
