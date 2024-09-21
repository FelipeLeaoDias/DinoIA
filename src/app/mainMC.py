import random
import json
import math
import copy
from dinogame import MultiDinoGame, ACTION_UP, ACTION_DOWN

# Configurações do Algoritmo Genético
POPULATION_SIZE = 150
GENERATIONS = 500
MUTATION_RATE = 0.3
FPS = 0
WEIGHT_RANGE = (-1000, 1000)
INPUT_SIZE = 10  # DY, X1, Y1, H1, W1, X2, Y2, H2, W2, GS
HIDDEN_SIZE = 5  # Tamanho da camada oculta
OUTPUT_SIZE = 1  # Um único neurônio para decidir entre ACTION_UP ou ACTION_DOWN


# Função para gerar pesos aleatórios
def generate_weights():
    # Pesos para a primeira camada (input -> hidden)
    weights_input_hidden = [[random.uniform(*WEIGHT_RANGE) for _ in range(INPUT_SIZE)] for _ in range(HIDDEN_SIZE)]
    # Pesos para a segunda camada (hidden -> output)
    weights_hidden_output = [random.uniform(*WEIGHT_RANGE) for _ in range(HIDDEN_SIZE)]
    return {'input_hidden': weights_input_hidden, 'hidden_output': weights_hidden_output}


def tanh(x):
    # Limita o valor de x para evitar estouro numérico
    if x > 20:
        return 1
    elif x < -20:
        return -1
    else:
        return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))


def forward_pass(state, weights):
    # Cálculo da ativação da primeira camada (input -> hidden)
    hidden_activations = []
    for neuron_weights in weights['input_hidden']:
        weighted_sum = sum(s * w for s, w in zip(state, neuron_weights))
        hidden_activations.append(tanh(weighted_sum))  # Aplicar função de ativação 'tanh'

    # Cálculo da ativação da camada de saída (hidden -> output)
    output_weighted_sum = sum(h * w for h, w in zip(hidden_activations, weights['hidden_output']))
    action_score = tanh(output_weighted_sum)  # Aplicar 'tanh' na saída

    return action_score


# Função para mutar pesos
def mutate(weights):
    mutated_weights = {
        'input_hidden': [[w if random.random() > MUTATION_RATE else random.uniform(*WEIGHT_RANGE)
                          for w in neuron_weights]
                         for neuron_weights in weights['input_hidden']],
        'hidden_output': [w if random.random() > MUTATION_RATE else random.uniform(*WEIGHT_RANGE)
                          for w in weights['hidden_output']]
    }
    return mutated_weights


# Função de evolução (Seleção e Mutação)
def evolve_population(population, best_individual):
    new_population = [best_individual]  # Mantém o melhor indivíduo sem mutação
    #print(best_individual)
    for _ in range(POPULATION_SIZE - 1):
        # Fazer uma cópia profunda do melhor indivíduo antes de mutar
        mutated_weights = mutate(copy.deepcopy(best_individual))  
        new_population.append(mutated_weights)
    
    return new_population


# Tomada de Decisão
def choose_action(state, weights):
    action_score = forward_pass(state, weights)
    
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
            if 5000 < max(scores):
                print("Agente Dino Infinito Encontrado!")
                game.game_over = True
                best_index = scores.index(max(scores))
                best_agent = population[best_index]
                json_dict = {'b_agent': best_agent}
                with open("best_agentMC.json", "w+") as outfile:
                    json.dump(json_dict, outfile)
                print("Melhor agente salvo!")
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