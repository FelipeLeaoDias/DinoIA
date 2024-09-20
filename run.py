import argparse
import subprocess

# Criando o parser
parser = argparse.ArgumentParser(description="Rodar diferentes agentes e treinos.")

# Adicionando opções para escolha do que rodar
parser.add_argument('--run', choices=['uc', 'mc'], help="Escolha qual agente rodar: 'uc' (Unica Camada) ou 'mc' (Multi Camadas)")
parser.add_argument('--train', action='store_true', help="Rodar o treino em vez do teste.")

# Parseando os argumentos
args = parser.parse_args()

# Verifica o input e decisão do que rodar, o treino ou o teste
if args.run == 'uc':
    if args.train:
        subprocess.run(['python', 'src/app/mainUC.py'])  # Rodar treino de UC
    else:
        subprocess.run(['python', 'src/app/testagentUC.py'])  # Rodar teste de UC
elif args.run == 'mc':
    if args.train:
        subprocess.run(['python', 'src/app/mainMC.py'])  # Rodar treino de MC
    else:
        subprocess.run(['python', 'src/app/testagentMC.py'])  # Rodar teste de MC
else:
    print("Nenhuma opção válida foi selecionada.")
