def menu(login_instance): # função do menu, que tem todas as opções após o login
    while True:
        print("---- MENU DE OPÇÕES ----")
        print("1 - Registrar preferências de dias de aula;")
        print("2 - Registrar preferências de horários de aula;")
        print("3 - Sair")
        op = input("Escolha uma opção: ")
        # todas as opções que o usuário pode escolher

        if op == "3": # sai do menu de escolhas
            break

        if op == "1": # pede ao usuário quais os dias são melhor para ele, cada número na lista corresponde a um dia, se o usuàrio no final colocar: 1, 2, 3 ele basicamente tá dizendo que o melhor dia pra ele dar aula é segunda, o segundo melhor seria terça e o terceiro melhor, quarta, e assim vai
            print("Escolha os dias da semana que pode dar aula: ")
            print("1 - Segunda;")
            print("2 - Terça;")
            print("3 - Quarta;")
            print("4 - Quinta;")
            print("5 - Sexta;")
            op_dias = input("Digite os dias da semana que escolheu em ordem de preferência (ex: 2, 4, 5): ")

            # dicionário que relaciona cada número com tal dia
            dias_semana = {
                "1": "Segunda",
                "2": "Terça",
                "3": "Quarta",
                "4": "Quinta",
                "5": "Sexta"
            }

            #vai criar uma lista com os números/dias que o usuário escolheu na ordem de prioridade definida e separar com uma vírgula (por isso o "op_dias.split(".")". Basicamente é isso
            dias_escolhidos = [dias_semana[num.strip()] for num in op_dias.split(",")]

        if op == "2": # pergunta ao usuário quais os melhores horários para ele
            print("Escolha os horários que pode dar aula:")
            print("1 - 7:10 às 8:00")
            print("2 - 8:00 às 8:50")
            print("3 - 8:50 às 9:40")
            print("4 - 9:55 às 10:45")
            print("5 - 10:45 às 11:35")
            print("6 - 11:35 à 12:25")
            op_horas = input("Digite em ordem de prioridade os horários que escolheu: ")

            # dicionário que relaciona tal número com tal horário
            horas_dia = {
                "1": "7:10 às 8:00",
                "2": "8:00 às 8:50",
                "3": "8:50 às 9:40",
                "4": "9:55 às 10:45",
                "5": "10:45 às 11:35",
                "6": "11:35 à 12:25"
            }

            # mesma coisa do de cima, cria uma lista com os horários que o usuário escolheu e os organiza por prioridade separando eles com vírgula
            horarios_escolhidos = [horas_dia[num.strip()] for num in op_horas.split(",")]
