from csvpandas import horarioINFO as info, horarioADM as adm, horarioAGRO as agro
from matriz import gerar_matrizes_por_turma, dias, horarios
from restricoes import validar_restricoes, autoajustar_matriz

# Criar dicionários de professores
professores_info = dict(zip(info["Código da Disciplina"], info["Professor"]))
professores_adm = dict(zip(adm["Código da Disciplina"], adm["Professor"]))
professores_agro = dict(zip(agro["Código da Disciplina"], agro["Professor"]))

# Gera todas as matrizes
todas = []
todas += gerar_matrizes_por_turma(info, "Informática", professores_info)
todas += gerar_matrizes_por_turma(adm, "Administração", professores_adm)
todas += gerar_matrizes_por_turma(agro, "Agropecuária", professores_agro)

# Verificação geral
for curso, serie, turma, matriz, professores, df in todas:
    print(f"\n MATRIZ DO CURSO: {curso} | {serie} | Turma {turma}")
    print(f"{'Dia/Horário':<12}", end="")
    for h in horarios:
        print(f"{h:<15}", end="")
    print()
    for i, dia in enumerate(dias):
        print(f"{dia:<12}", end="")
        for j in range(len(horarios)):
            valor = matriz[i, j]
            if valor == 0:
                print(f"{'-':<15}", end="")
            else:
                nome_prof = professores.get(valor, "?")
                texto = f"{valor}-{nome_prof[:8]}"
                print(f"{texto:<15}", end="")
        print()

    print(f"\n Verificando restrições para {curso} | {serie} | Turma {turma}")
    erros = validar_restricoes(matriz, df)
    if erros:
        print("Tentando autoajuste...\n")
        matriz = autoajustar_matriz(matriz, df)
