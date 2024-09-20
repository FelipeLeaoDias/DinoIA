import math
import json
from dinogame import DinoGame, ACTION_UP, ACTION_DOWN


with open("src/app/best_agentMC.json", "r") as infile:
    data = json.load(infile)
DINOAGENT = data['b_agent']
FPS = 0

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

# Tomada de Decisão
def choose_action(state, weights):
    action_score = forward_pass(state, weights)
    
    if action_score > 0:
        return ACTION_UP
    else:
        return ACTION_DOWN

while (True):
    game = DinoGame(FPS)
    while not game.game_over:  # O loop continua até que todos os dinossauros estejam mortos
                action = choose_action(game.get_state(), DINOAGENT)
                game.step(action)
                
    scores = game.get_scores()
    print(f"Pontuação: {scores}")
