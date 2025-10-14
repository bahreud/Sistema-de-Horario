import numpy as np
import random
from csvpandas import horarioINFO as info, horarioADM as adm, horarioAGRO as agro

def padronizar_colunas(df):
    return df.rename(columns={
        "Discipline_Code": "Código da Disciplina",
        "Total_Semanal": "Total de Aulas Semanais"
    })

info = padronizar_colunas(info)
adm = padronizar_colunas(adm)
agro = padronizar_colunas(agro)

professores_info = dict(zip(info["Código da Disciplina"], info["Professor"]))
professores_adm = dict(zip(adm["Código da Disciplina"], adm["Professor"]))
professores_agro = dict(zip(agro["Código da Disciplina"], agro["Professor"]))

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50",
    "10:50-11:40", "11:40-12:30", "13:50-14:40",
    "14:40-15:30", "15:50-16:40", "16:40-17:30"
]

def distribuir_disciplinas(df):
    matriz = np.zeros((len(dias), len(horarios)), dtype=int)
    for _, row in df.iterrows():
        codigo = int(row["Código da Disciplina"])
        aulas = int(row["Total de Aulas Semanais"])

        livres = [(i, j) for i in range(len(dias)) for j in range(len(horarios)) if matriz[i, j] == 0]
        if len(livres) == 0:
            break
        if len(livres) < aulas:
            aulas = len(livres)

        escolhidos = random.sample(livres, aulas)

        for (i, j) in escolhidos:
            matriz[i, j] = codigo
    return matriz

def mostrar_matriz(nome_curso, serie, turma, matriz, professores):
    print(f"\n MATRIZ DO CURSO: {nome_curso} | {serie} | Turma {turma}")
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

def gerar_matrizes_por_turma(df, nome_curso, professores):
    if "Série" not in df.columns or "Turma" not in df.columns:
        print(f"O DataFrame de {nome_curso} não tem colunas 'Série' e 'Turma'.")
        return

    grupos = df.groupby(["Série", "Turma"])
    for (serie, turma), grupo in grupos:
        matriz = distribuir_disciplinas(grupo)
        mostrar_matriz(nome_curso, serie, turma, matriz, professores)

gerar_matrizes_por_turma(info, "Informática", professores_info)
gerar_matrizes_por_turma(adm, "Administração", professores_adm)
gerar_matrizes_por_turma(agro, "Agropecuária", professores_agro)
