import json
from dinogame import DinoGame, ACTION_UP, ACTION_DOWN

with open("best_agentUC.json", "r") as infile:
    data = json.load(infile)
DINOAGENT = data['b_agent']
FPS = 0

# Função de decisão da ação com base nos pesos e no estado do jogo
def choose_action(state, weights):

    # Calcula a soma ponderada
    weighted_sum = sum(s * w for s, w in zip(state, weights))
    
    # Decisão da ação com base na soma ponderada
    if weighted_sum > 0:
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
