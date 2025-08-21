# método que define o menu
def menu(user):
    def tem_conflito(horarios_existentes, novo_horario): # vai verificar se um novo horário que está sendo registrado vai ou não conflituar com um horário já existente
        novo_inicio, novo_fim = novo_horario # relaciona o começo de um horário com o fim dele (espero que dê pra entender)

        for existente_inicio, existente_fim in horarios_existentes: # verifica cada horário já selecionado até o momento
            if not (novo_fim <= existente_inicio or novo_inicio >= existente_fim): # define que: se o novo horário termina antes do outro começar e/ou o outro começa depois do existente terminar, então, os horários não dão conflito, se o novo horário não corresponder a nem uma dessas condições o código entende como conflito!
                return True
        return False

    while True:
        print("\n---- MENU DE OPÇÕES ----")
        print("1 - Registrar preferências de dias de aula")
        print("2 - Registrar preferências de horários de aula")
        print("3 - Sair e mostrar dados")
        op = input("\nEscolha uma opção: ") # usuário escolhe o que quer fazer

        if op == "1": # seleciona seus dias de preferência
            print("\nEscolha os dias da semana que pode dar aula:")
            print("1 - Segunda")
            print("2 - Terça")
            print("3 - Quarta")
            print("4 - Quinta")
            print("5 - Sexta")
            op_dias = input("Digite os dias em ordem de preferência (ex: 2,4,5): ")

            # dicionário que relaciona um número com um dia
            dias_semana = {
                "1": "Segunda",
                "2": "Terça",
                "3": "Quarta",
                "4": "Quinta",
                "5": "Sexta"
            }

            # Se o dia selecionado estiver no dicionário de dias, o código aceita, se não o resultado sera KeyError (O valor escolhido é inválido)
            try:
                user.dias_preferidos = [dias_semana[num.strip()] for num in op_dias.split(",")]
                print("\nDias preferenciais registrados com sucesso!")
            except KeyError:
                print("\nErro: Algum dia selecionado é inválido. Use apenas números de 1 a 5 separados por vírgula.")
                continue


        elif op == "2": # o usuário escolhe seus horários de preferência
            print("\nEscolha os horários que pode dar aula:")
            print("1 - 7:10 às 8:00")
            print("2 - 8:00 às 8:50")
            print("3 - 8:50 às 9:40")
            print("4 - 9:55 às 10:45")
            print("5 - 10:45 às 11:35")
            print("6 - 11:35 às 12:25")
            op_horas = input("Digite os horários em ordem de prioridade (ex: 2,4,6): ")

            # dicionário que relaciona cada número com um horário
            horas_dia = {
                "1": "7:10 às 8:00",
                "2": "8:00 às 8:50",
                "3": "8:50 às 9:40",
                "4": "9:55 às 10:45",
                "5": "10:45 às 11:35",
                "6": "11:35 às 12:25"
            }

            # dicionário que relaciona horários com números decimais, isso é feito para que o código/computador consiga diferenciar cada um dos horários
            horarios_numericos = {
                "1": (7.17, 8.00),
                "2": (8.00, 8.50),
                "3": (8.50, 9.40),
                "4": (9.92, 10.45),
                "5": (10.45, 11.35),
                "6": (11.35, 12.25)
            }

            try: # parte do código que testa, para cada um dos horários que o usuário escolher se algum deles resulta em conflito
                horarios_selecionados = [] # verifica a lista com horários que não tem nem uma relação com os valores reais(os números decimais)
                horarios_numericos_selecionados = [] # verifica a lista de valores decimais

                for num in op_horas.split(","): # vai possibilitar/dividir o números que o usuário escolheu em ", " sem que de erro
                    num = num.strip() # para que o usuário consiga escrever os números como quiser (com espaço, sem, etc)
                    horario_str = horas_dia[num] # só converte os números selecionados com os horários que correspondem
                    horario_num = horarios_numericos[num] # a mesma coisa do de cima, mas esse é para os números decimais

                    if tem_conflito(horarios_numericos_selecionados, horario_num): # se o horário já tiver sido pego o código resulta em "conflito", se não ele continua
                        print(f"\nO horário {horario_str} conflita com horários já selecionados.")
                        continue

                    horarios_selecionados.append(horario_str) # se o usuário não escolheu nem um horário já pego, os horários selecionados são adiconados a lista de horários
                    horarios_numericos_selecionados.append(horario_num) # outra lista, mas essa armazena os horários já selecionados pra poder distinguir os escolhidos dos não escolhidos

                # cria a relação dos horários selecionados com os preferidos e entre os números decimais escolhidos com o dicionário deles
                user.horarios_preferidos = horarios_selecionados
                user.horarios_numericos = horarios_numericos_selecionados
                print("\nHorários preferenciais registrados com sucesso!")

            except KeyError: # se algum horário tiver sido selecionado e ele não está registrado da erro
                print(
                    "\nErro: Algum horário selecionado é inválido. Use apenas números de 1 a 6 separados por vírgula.")
                continue


        elif op == "3": # dá todos os dados já registrados sobre tal usuário
            # encontra o primeiro professor na lista de dados que corresponde a tal matrícula, se ele não encontrar nem um, o código retorna "None"
            dados = next((prof for prof in user.professores if prof["Cod_Professor"] == user.matricula), None)

            if dados is None: # se o código não conseguir achar nem um dado do professor, ele mostra isso:
                print("\nErro: Dados do professor não encontrados!")
                continue

            print("\n---- DADOS DO PROFESSOR ----")
            print(f"Código do professor: {dados['Cod_Professor']}")
            print(f"Nome: {dados['Professor']}")
            print(f"Matéria: {dados['Disciplina']}")
            print(f"Turma: {dados['Turma']} (Código: {dados['Cod_Turma']})")
            print("Dias preferidos:", ", ".join(user.dias_preferidos) if user.dias_preferidos else "Não informados")
            print("Horários preferidos:",
                  ", ".join(user.horarios_preferidos) if user.horarios_preferidos else "Não informados")
            break # finaliza o loop do menu

        else:
            print("\nOpção inválida. Digite 1, 2 ou 3.") # caso o usuário escolha uma opção inválida