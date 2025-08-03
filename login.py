from menu import menu
# importa as funções do menu
from typing import Dict, List #permite que qualquer valor (e vários valores diferentes) seja adicionado a um dicionário sem muito segredo

class Login: # a classe que define as características para o login

    # Dicionário com os dados dos professores (turma, disciplina, etc)
    professores: Dict[int, Dict[str, any]] = {
        2023006: {
            "Professor": "Roberto Silva",
            "Cod_Professor": 6,
            "Disciplina": "Educação Física",
            "Cod_Disciplina": 10,
            "Turma": "3-B",
            "Cod_Turma": 31
        },
        2023005: {
            "Professor": "Patrícia Fernandes",
            "Cod_Professor": 5,
            "Disciplina": "Ciências",
            "Cod_Disciplina": 9,
            "Turma": "3-A",
            "Cod_Turma": 30
        },
        2023004: {
            "Professor": "Marcos Antônio",
            "Cod_Professor": 4,
            "Disciplina": "Geografia",
            "Cod_Disciplina": 8,
            "Turma": "2-B",
            "Cod_Turma": 21
        },
        2023003: {
            "Professor": "Ana Lúcia",
            "Cod_Professor": 3,
            "Disciplina": "História",
            "Cod_Disciplina": 7,
            "Turma": "2-A",
            "Cod_Turma": 20
        }
    }

    def __init__(self, matricula, senha):
        self.matricula = None #
        self.senha = senha
        self.horario_final = None #
        self.dias_preferidos = []
        self.horarios_preferidos = []
        # o "self.dias_preferidos" e o "self.horarios_preferidos" vão guardar as escolhas que os usuários fizeram de dias e horarios que são melhores pra cada um


    def login(self):
        print("\n---- SISTEMA DE GERENCIAMENTO DE HORÁRIOS ----")
        print("Por favor, faça login\n")

        while True:
            matricula = int(input("Matricula: "))
            senha = input("Senha: ")
            # O usuário digita sua matrícula (que só pode ser números inteiros) e a senha

            if senha != "12345":
                print("Senha incorreta! Tente novamente.")
                return False # se a senha não for digitada corretamente o retorno será dado como "falso" ou seja o login dará errado

            if matricula not in self.professores:
                print("Essa matrícula é invalida! Tente novamente.")
                return False # se a matrícula não estiver registrada o login dará errado

            self.matricula = matricula
            print(f"\nOlá, {self.professores[matricula]['Professor']}!")
            return True # se a matrícula estiver dentro do "registro de matriculas o login dará certo e o usuário será direcionado para o menu de opções