from menu import menu
# importa as funções do menu

class Login: # a classe que define as características para o login
    def __init__(self, matricula, senha):
        self.matricula = matricula
        self.senha = senha
        self.dias_preferidos = []
        self.horarios_preferidos = []
        # o "self.dias_preferidos" e o "self.horarios_preferidos" vão guardar as escolhas que os usuários fizeram de dias e horarios que são melhores pra cada um


    def login(self):
        if self.senha != 12345: # a senha, nesse caso eu defini como algo fixo, que o usuário não pode mudar, se o usuário não digitar "12345" da "return False", ou seja, erro e o "código recomeça"
            print("Senha incorreta! Tente novamente.")
            return False

        matriculas_aceitas = [8427, 4827, 5634, 9872] # basicamente a mesma coisa com as matrículas, já temos matrículas registradas e se algum usuário digita uma que "não existe" nesse sistema da "return False" e o "código recomeça"
        if self.matricula not in matriculas_aceitas:
            print("Essa matrícula não é válida! Tente novamente.")
            return False

        return True # caso a senha e a matrícula sejam válidas o usuário vai pro menu de opções, o "return True" é para dizer que essas informações são válidas e que o usuário pode prosseguir