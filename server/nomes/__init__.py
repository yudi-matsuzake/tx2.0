import random

nomes = []
sobrenomes = []

with open('nomes/nomes.txt', 'r') as nomesfile:
    for line in nomesfile:
        nomes.append(line.strip())

with open('nomes/sobrenomes.txt', 'r') as nomesfile:
    for line in nomesfile:
        sobrenomes.append(line.strip())

def nome_aleatorio():
    firstname = random.choice(nomes)
    n_name = random.randint(1, 3)

    lastname = ''
    for i in range(n_name):
        lastname += ' ' + random.choice(sobrenomes)

    return firstname + lastname
