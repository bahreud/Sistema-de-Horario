from menu import menu
# importa as funções do menu
from typing import Dict, List
# Deixa que usemos diferentes valores dentro de dicionários, listas, etc

class Login: # a classe que define as características para o login
    # Dicionário dentro de uma lista com os dados dos professores (turma, disciplina, etc)
    professores: List[Dict[str, any]] = [
        {
            "Professor": "Roberto Silva",
            "Cod_Professor": 2023006,
            "Disciplina": "Educação Física",
            "Cod_Disciplina": 10,
            "Turma": "3-B",
            "Cod_Turma": 31
        },
        {
            "Professor": "Patrícia Fernandes",
            "Cod_Professor": 2023005,
            "Disciplina": "Ciências",
            "Cod_Disciplina": 9,
            "Turma": "3-A",
            "Cod_Turma": 30
        },
        {
            "Professor": "Marcos Antônio",
            "Cod_Professor": 2023004,
            "Disciplina": "Geografia",
            "Cod_Disciplina": 8,
            "Turma": "2-B",
            "Cod_Turma": 21
        },
        {
            "Professor": "Ana Lúcia",
            "Cod_Professor": 2023003,
            "Disciplina": "História",
            "Cod_Disciplina": 7,
            "Turma": "2-A",
            "Cod_Turma": 20
        }
    ]



    def __init__(self, matricula, senha):
        self.matricula = matricula
        self.senha = senha
        self.horario_final = None
        self.dias_preferidos = []
        self.horarios_preferidos = []
        # o "self.dias_preferidos" e o "self.horarios_preferidos" vão guardar as escolhas que os usuários fizeram de dias e horarios que são melhores pra cada um
        self.horarios_numericos = []  # Lista vazia para verificação de conflitos entre os horários em formato numérico

    def login(self): # Método Login que basicamente define tudo para que o usuário consiga fazer login
        print("\n---- SISTEMA DE GERENCIAMENTO DE HORÁRIOS ----")
        print("Por favor, faça login\n")

        while True:
            matricula = int(input("Matricula: "))
            senha = input("Senha: ")

            if senha != "12345": # a senha não pode ser diferente desse valor
                print("Senha incorreta! Tente novamente.")
                return False # caso contrário o programa retorna que isso é falso

            for prof in self.professores:
                if prof["Cod_Professor"] == matricula: # se a matrícula do professor estiver registrada o professor consegue entrar
                    self.matricula = matricula
                    print(f"\nOlá, {prof['Professor']}")
                    return True

            print("Essa matrícula é inválida! Tente novamente.")
            return False