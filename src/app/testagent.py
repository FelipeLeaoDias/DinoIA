import random
from dinogame import DinoGame, ACTION_UP, ACTION_DOWN


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
    dinoagent = [-969.9747823465515, -650.32064247121, -162.86909870427598, 337.23620509601096, -67.69696867986943, 802.9135481475676, -132.73599107958, -124.19254050945483, 982.0102558513966, -981.1091337906228]
    while not game.game_over:  # O loop continua até que todos os dinossauros estejam mortos
                action = choose_action(game.get_state(), dinoagent)
                game.step(action)
                
    scores = game.get_scores()
    print(f"Pontuação: {scores}")
