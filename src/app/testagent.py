import random
from dinogame import DinoGame, ACTION_UP, ACTION_DOWN

FPS = 0
    #new_population.append([446.62672097774293, -934.2578733894258, -100.33945666994896, -610.1787183988849, -95.66858964780067, -26.46658966286691, 14.146118580399275, -297.0866625783599, 250.33537953596783, 283.6284980840978])
    #new_population.append([632.5458559288359, -625.0027796970503, -162.86909870427598, 337.23620509601096, -491.97789527506797, -473.401104405238, -22.10340021731531, -745.293100326201, 612.8061548750454, 990.4510769971735])
    #new_population.append([-969.9747823465515, -650.32064247121, -162.86909870427598, 337.23620509601096, -67.69696867986943, 802.9135481475676, -132.73599107958, -124.19254050945483, 982.0102558513966, -981.1091337906228])

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
    dinoagent = [-641.7001178594481, -940.4473597770137, -425.42063527206994, 997.8676675792362, 657.2565969585264, 333.4801124278242, -79.155749425718, -119.33917606039836, 735.5958131726372, -923.7118141608858]

    while not game.game_over:  # O loop continua até que todos os dinossauros estejam mortos
                action = choose_action(game.get_state(), dinoagent)
                game.step(action)
                
    scores = game.get_scores()
    print(f"Pontuação: {scores}")
