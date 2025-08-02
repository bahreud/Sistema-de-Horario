contas = []
while True:
    def login():
        valida = [(input("Insira seu ID")), input("Insira sua senha: ")]
        for i in contas:
            if i == valida:
                return True


    def registro():
        conta = [(input("Escolha seu ID")), input("Escolha sua senha: ")]
        contas.append(conta)
        print("Conta registrada!")


    print("      Menu      "
          "\nselecione uma opção de 1 a 3:"
          "\n1 - Fazer Login"
          "\n2 - Resgistrar uma conta"
          "\n3 - Sair")
    resposta = int(input("Sua opção:"))

    if resposta == 2:
        registro()
    elif resposta == 3:
        break
    if resposta == 1:
        if login() == True:
            print("      Menu do Sistema de Horários"
                  "\n1 - Registrar Horário"
                  "\n2 - Sair")
            opcao = int(input("Sua opção: "))
            if opcao == 2:
                break
            elif opcao == 1:

                Segunda = int(input(""))

            elif opcao == 2:
                break

            else:
                print("Nenhum horário registrado ainda.\n")

ababababababa
