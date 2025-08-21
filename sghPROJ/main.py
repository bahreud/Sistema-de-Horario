from login import Login  # sua classe Login com professores
from menu import menu    # a função menu separada

if __name__ == "__main__": # define que o código só vai rodar/mostrar no terminal se você usar esse arquivo, ou seja, isso define que o código só vai rodar se o arquivo main.py for executado
    user = Login(matricula=0, senha="")  # Valores iniciais quaisquer
    if user.login(): # se o Login der certo, então o código executa o Menu!
        menu(user)