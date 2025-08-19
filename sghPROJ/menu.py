def menu(user): 
    while True:
        print("\n---- MENU DE OPÇÕES ----")
        print("1 - Registrar preferências de dias de aula")
        print("2 - Registrar preferências de horários de aula")
        print("3 - Sair e mostrar dados")
        op = input("\nEscolha uma opção: ")

        if op == "1":
            print("\nEscolha os dias da semana que pode dar aula:")
            print("1 - Segunda")
            print("2 - Terça")
            print("3 - Quarta")
            print("4 - Quinta")
            print("5 - Sexta")
            op_dias = input("Digite os dias em ordem de preferência (ex: 2,4,5): ")

            dias_semana = {
                "1": "Segunda",
                "2": "Terça",
                "3": "Quarta",
                "4": "Quinta",
                "5": "Sexta"
            }

            try:
                user.dias_preferidos = [dias_semana[num.strip()] for num in op_dias.split(",")]
                print("\nDias preferenciais registrados com sucesso!")
            except KeyError:
                print("\nErro: Algum dia selecionado é inválido. Use apenas números de 1 a 5 separados por vírgula.")
                continue

        elif op == "2":
            print("\nEscolha os horários que pode dar aula:")
            print("1 - 7:10 às 8:00")
            print("2 - 8:00 às 8:50")
            print("3 - 8:50 às 9:40")
            print("4 - 9:55 às 10:45")
            print("5 - 10:45 às 11:35")
            print("6 - 11:35 às 12:25")
            op_horas = input("Digite os horários em ordem de prioridade (ex: 2,4,6): ")

            horas_dia = {
                "1": "7:10 às 8:00",
                "2": "8:00 às 8:50",
                "3": "8:50 às 9:40",
                "4": "9:55 às 10:45",
                "5": "10:45 às 11:35",
                "6": "11:35 às 12:25"
            }

            try:
                user.horarios_preferidos = [horas_dia[num.strip()] for num in op_horas.split(",")]
                print("\nHorários preferenciais registrados com sucesso!")
            except KeyError:
                print("\nErro: Algum horário selecionado é inválido. Use apenas números de 1 a 6 separados por vírgula.")
                continue

        elif op == "3":
            try:
                dados = user.professores[user.matricula]
                
                print("\n---- DADOS DO PROFESSOR ----")
                print(f"Código do professor: {dados['Cod_Professor']}")
                print(f"Nome: {dados['Professor']}")
                print(f"Matéria: {dados['Disciplina']}")
                print(f"Turma: {dados['Turma']} (Código: {dados['Cod_Turma']})")
                print("Dias preferidos:", ", ".join(user.dias_preferidos) if user.dias_preferidos else "Não informados")
                print("Horários preferidos:", ", ".join(user.horarios_preferidos) if user.horarios_preferidos else "Não informados")
                break
                
            except AttributeError:
                print("\nErro: Nenhum professor logado corretamente.")
                break
            except KeyError:
                print("\nErro: Dados do professor não encontrados.")
                break

        else:
            print("\nOpção inválida. Digite 1, 2 ou 3.")
