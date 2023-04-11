from collections import deque

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