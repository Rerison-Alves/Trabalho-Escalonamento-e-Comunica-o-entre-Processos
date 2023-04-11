from collections import deque
import seaborn as sns
import matplotlib.pyplot as plt

class Processo:
    def __init__(self, id, burst):
        self.id = id
        self.burst = burst
        self.tempo_espera = 0
        self.tempo_retorno = 0

    def __repr__(self):
        return f'P{self.id}({self.burst})'

class EscalonadorRoundRobin:
    def __init__(self, quantum):
        self.quantum = quantum
        self.lista_prontos = deque()
        self.lista_concluidos = []
        self.tempo_atual = 0
        self.tempo_executado = 0

    def adicionar_processo(self, processo):
        self.lista_prontos.append(processo)

    def executar(self):
        if len(self.lista_prontos) == 0:
            return

        processo = self.lista_prontos.popleft()
        if processo.burst > self.quantum:
            self.tempo_atual += self.quantum + 1
            processo.burst -= self.quantum
            self.lista_prontos.append(processo)
        else:
            self.tempo_atual += processo.burst + 1
            self.tempo_executado += processo.burst
            processo.tempo_espera = self.tempo_executado - processo.burst
            processo.tempo_retorno = self.tempo_executado
            self.lista_concluidos.append(processo)

    def executar_todos(self):
        while len(self.lista_prontos) > 0:
            self.executar()

    def tempo_medio_espera(self):
        return sum(p.tempo_espera for p in self.lista_concluidos) / len(self.lista_concluidos)

    def tempo_medio_retorno(self):
        return sum(p.tempo_retorno for p in self.lista_concluidos) / len(self.lista_concluidos)

    def vazao(self):
        return len(self.lista_concluidos) / self.tempo_atual


# Teste da simulação
if __name__ == '__main__':
     quantums = range(1,31)
    # Listas para armazenar os resultados de cada simulação
    tempos_medios_espera = []
    tempos_medios_retorno = []
    vazoes = []
    #teste de simulações
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

    # Plotar gráfico de tempo médio de espera
    sns.lineplot(x=quantums, y=tempos_medios_espera)
    plt.title('Tempo médio de espera para diferentes valores de quantum')
    plt.xlabel('Quantum')
    plt.ylabel('Tempo médio de espera')
    plt.show()

    # Plotar gráfico de tempo médio de retorno
    sns.lineplot(x=quantums, y=tempos_medios_retorno)
    plt.title('Tempo médio de retorno para diferentes valores de quantum')
    plt.xlabel('Quantum')
    plt.ylabel('Tempo médio de retorno')
    plt.show()

    # Plotar gráfico de vazão
    sns.lineplot(x=quantums, y=vazoes)
    plt.title('Vazão para diferentes valores de quantum')
    plt.xlabel('Quantum')
    plt.ylabel('Vazão')
    plt.show()
