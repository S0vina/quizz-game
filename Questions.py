import json

class perguntas:
    def __init__(self, js):
        self.js = js

    def carregar_perguntas(self, tema_escolhido): 
        with open(self.js, 'r', encoding='utf-8') as perguntas:
            todos_os_dados = json.load(perguntas)
    
    # Retorna a lista de perguntas do tema ou uma lista vazia se não existir
        return todos_os_dados.get(tema_escolhido, [])
