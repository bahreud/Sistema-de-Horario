from login import Login  # sua classe Login com professores
from menu import menu    # a função menu separada

if __name__ == "__main__":
    user = Login(matricula=None, senha=None)
    if user.login():
        menu(user)