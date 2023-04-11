import seaborn as sns
import matplotlib.pyplot as plt


def printer(quantums, tempos_medios_espera, tempos_medios_retorno, vazoes):
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
