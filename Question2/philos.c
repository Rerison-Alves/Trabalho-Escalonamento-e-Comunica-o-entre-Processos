#include <assert.h>
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define PHILOS 3 // Define o número de filósofos
#define FOOD 100 // Define a quantidade de comida disponível na mesa

void *philosopher(void *id); // Declaração da função que representa o
                             // comportamento dos filósofos
void grab_chopstick(
    int, int,
    char *); // Declaração da função que simula um filósofo pegando um hashi
void down_chopsticks(int, int); // Declaração da função que simula um filósofo
                                // colocando os hashis na mesa
int food_on_table(); // Declaração da função que simula a verificação de comida
                     // na mesa

pthread_mutex_t chopstick[PHILOS]; // Declaração dos hashis (mutexes) que os
                                   // filósofos compartilham
pthread_t philo[PHILOS];           // Declaração dos filósofos (threads)
pthread_mutex_t food_lock; // Declaração do mutex para controlar a quantidade de
                           // comida na mesa
pthread_mutex_t
    print_lock; // Declaração do mutex para controlar a impressão na tela

int main(int argn, char **argv) {
  int i, j;

  pthread_mutex_init(
      &food_lock,
      NULL); // Inicializa o mutex para controlar a quantidade de comida na mesa
  pthread_mutex_init(
      &print_lock,
      NULL); // Inicializa o mutex para controlar a impressão na tela
  for (i = 0; i < PHILOS; i++) {
    pthread_mutex_init(&chopstick[i], NULL); // Inicializa os hashis
  }

    for (i = 0; i < PHILOS; i++) {
      pthread_create(&philo[i], NULL, philosopher,
                     (void *)i); // Cria as threads para os filósofos
    }
    for (i = 0; i < PHILOS; i++) {
      pthread_join(philo[i], NULL); // Aguarda todas as threads finalizarem
    }
  

  return 0;
}
void *philosopher(void *num) {
  int id;
  int left_chopstick, right_chopstick, f;
  int eat_count = 0; // Inicializa o contador de quantas vezes o filósofo comeu

  id = (int)num; // Conversão do ponteiro genérico para um inteiro
  printf("Filosofo %d parou de pensar e esta pronto para comer.\n", id);
  right_chopstick = id;    // Define qual hashi fica à direita do filósofo
  left_chopstick = id + 1; // Define qual hashi fica à esquerda do filósofo

  if (left_chopstick ==
      PHILOS) { // Se o hashi à esquerda for o último, volta para o primeiro
    left_chopstick = 0;
  }

  while ((f = food_on_table())) { // Enquanto houver comida na mesa, o filósofo
                                  // continua comendo

    if (id == 0) { // Se o filósofo for o de id 0, ele pega primeiro o hashi da
                   // esquerda

      grab_chopstick(id, left_chopstick, "left ");
      grab_chopstick(id, right_chopstick, "right ");

    } else { // Outros filósofos pegam o hashi da direita primeiro
      grab_chopstick(id, right_chopstick, "right ");
      grab_chopstick(id, left_chopstick, "left");
    }
    printf("Philosopher %d: eating.\n", id);
    down_chopsticks(left_chopstick,
                    right_chopstick); // O filósofo libera os hashis
    eat_count++; // Incrementa o contador de quantas vezes o filósofo comeu
  }

  printf("Philosopher %d is done eating.\n", id); // Acabou de comer
  printf("Philosopher %d ate %d times.\n", id,
         eat_count); // Imprime quantas vezes o filósofo comeu
  return (NULL);
}
// função para verificar se há comida na mesa
int food_on_table() {
  static int food = FOOD;
  int myfood;
  pthread_mutex_lock(
      &food_lock); // trava o mutex da comida para garantir que apenas um
                   // filósofo acesse a variável food por vez
  if (food > 0) {
    food--;
  }
  myfood = food;
  pthread_mutex_unlock(&food_lock); // libera o mutex da comida
  return myfood;
}
// função para pegar um hashi
void grab_chopstick(int phil, int c, char *hand) {
  int result;

  pthread_mutex_lock(&print_lock);
  printf("Philosopher %d: tries to get %s chopstick %d\n", phil, hand, c);
  pthread_mutex_unlock(&print_lock);

  while (1) {
    result = pthread_mutex_trylock(&chopstick[c]);

    if (result == 0) {
      break;
    } else if (result == EBUSY) {
      pthread_mutex_unlock(&chopstick[(c + 1) % PHILOS]);
      usleep(rand() % 1000); // espera um pouco antes de tentar novamente
    } else {
      perror("pthread_mutex_trylock");
      exit(1);
    }
  }

  pthread_mutex_lock(&print_lock);
  printf("Philosopher %d: got %s chopstick %d\n", phil, hand, c);
  pthread_mutex_unlock(&print_lock);
}

// função para soltar os hashis
void down_chopsticks(int c1, int c2) {
  // libera o mutex do primeiro hashi
  pthread_mutex_unlock(&chopstick[c1]);
  // libera o mutex do segundo hashi
  pthread_mutex_unlock(&chopstick[c2]);
}
