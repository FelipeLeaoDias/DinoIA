import random
from chrome_trex import MultiDinoGame, ACTION_UP, ACTION_DOWN

# Configurações do Algoritmo Genético
POPULATION_SIZE = 70
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
    #new_population.append([446.62672097774293, -934.2578733894258, -100.33945666994896, -610.1787183988849, -95.66858964780067, -26.46658966286691, 14.146118580399275, -297.0866625783599, 250.33537953596783, 283.6284980840978])
    new_population.append([632.5458559288359, -625.0027796970503, -162.86909870427598, 337.23620509601096, -491.97789527506797, -473.401104405238, -22.10340021731531, -745.293100326201, 612.8061548750454, 990.4510769971735])
    new_population.append([-969.9747823465515, -650.32064247121, -162.86909870427598, 337.23620509601096, -67.69696867986943, 802.9135481475676, -132.73599107958, -124.19254050945483, 982.0102558513966, -981.1091337906228])

    print(best_individual)
    for _ in range(POPULATION_SIZE - 3):
        mutated_weights = mutate(best_individual[:])  # Aplica mutação ao melhor indivíduo
        new_population.append(mutated_weights)
    return new_population


# Função de decisão da ação com base nos pesos e no estado do jogo
def choose_action(state, weights):

    # Calcula a soma ponderada
    weighted_sum = sum(s * w for s, w in zip(state, weights))
    
    # Decisão da ação com base na soma ponderada
    if weighted_sum > 0:
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
            for i in range(POPULATION_SIZE):
                if alive[i]:  # Só decide ação para dinos vivos
                    action = choose_action(states[i], population[i])
                    actions.append(action)
                else:
                    actions.append(ACTION_DOWN)  # Ação neutra para dinos mortos
            
            game.step(actions)
            scores = game.get_scores()

            # Atualiza o status de vivos/mortos
            for i in range(POPULATION_SIZE):
                if alive[i] and game.player_dinos[i].is_dead:  # Verifica se o dinossauro está morto
                    alive[i] = False

            # Verifica se todos os dinossauros estão mortos
            if not any(alive):
                game.game_over = True
                break

        # Seleciona os 4 melhores dinossauros com base nas pontuações
        best_index = scores.index(max(scores))
        best_individual = population[best_index]
        print(f"Geração {generation + 1} - Melhor Pontuação: {max(scores)}")

        # Evolui a população
        population = evolve_population(population, best_individual)

    game.close()

if __name__ == "__main__":
    main()
