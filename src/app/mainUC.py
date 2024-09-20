import random
import json
import math

from dinogame import MultiDinoGame, ACTION_UP, ACTION_DOWN

# Configurações do Algoritmo Genético
POPULATION_SIZE = 300
GENERATIONS = 500
MUTATION_RATE = 0.3
FPS = 0
WEIGHT_RANGE = (-1000, 1000)

# Função para gerar pesos aleatórios
def generate_weights():
    return [random.uniform(*WEIGHT_RANGE) for _ in range(10)] 


# Função para mutar pesos
def mutate(weights):
    return [w if random.random() > MUTATION_RATE else random.uniform(*WEIGHT_RANGE) for w in weights]


# Função de seleção e reprodução
def evolve_population(population, best_individual):
    new_population = [best_individual]  # Mantém o melhor indivíduo sem mutação

    print(best_individual)
    for _ in range(POPULATION_SIZE - 1):
        mutated_weights = mutate(best_individual[:])  # Aplica mutação ao melhor indivíduo
        new_population.append(mutated_weights)
    return new_population


def tanh(x):
    # Limita o valor de x para evitar estouro numérico
    if x > 20:
        return 1
    elif x < -20:
        return -1
    else:
        return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))


def choose_action(state, weights):
    weighted_sum = sum(s * w for s, w in zip(state, weights))
    action_score = tanh(weighted_sum)

    if action_score > 0:
        return ACTION_UP
    else:
        return ACTION_DOWN


# Função principal
def main():
    game = MultiDinoGame(POPULATION_SIZE, FPS)
    population = [generate_weights() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        game.reset()
        alive = [True] * POPULATION_SIZE  # Mantém controle dos dinos vivos
        scores = [0] * POPULATION_SIZE

        while not game.game_over:  # O loop continua até que todos os dinossauros estejam mortos
            states = game.get_state()
            actions = []

            # Choose_action
            for i in range(POPULATION_SIZE):
                action = choose_action(states[i], population[i])
                actions.append(action)
            game.step(actions)
            scores = game.get_scores()

            # Limite de pontos para pegar o melhor score
            if 15000 < max(scores):
                game.game_over = True
                best_index = scores.index(max(scores))
                best_agent = population[best_index]
                json_dict = {'b_agent': best_agent}
                with open("best_agentUC.json", "w+") as outfile:
                    json.dump(json_dict, outfile)
                break

            # Atualiza o status de vivos/mortos
            for i in range(POPULATION_SIZE):
                if alive[i] and game.player_dinos[i].is_dead:  # Verifica se o dinossauro está morto
                    alive[i] = False

            # Verifica se todos os dinossauros estão mortos
            if not any(alive):
                game.game_over = True
                break
        
        # Pega o melhor individuo para evolução
        best_index = scores.index(max(scores))
        best_individual = population[best_index]
        print(f"Geração {generation + 1} - Melhor Pontuação: {max(scores)}")

        # Evolui a população
        population = evolve_population(population, best_individual)
    game.close()
if __name__ == "__main__":
    main()
