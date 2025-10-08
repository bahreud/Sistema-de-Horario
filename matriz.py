import numpy as np
import random
from csvpandas import horarioINFO as info, horarioADM as adm, horarioAGRO as agro

# === Renomear colunas para português (caso estejam em inglês) ===
def padronizar_colunas(df):
    return df.rename(columns={
        "Discipline_Code": "Código da Disciplina",
        "Total_Semanal": "Total de Aulas Semanais"
    })

info = padronizar_colunas(info)
adm = padronizar_colunas(adm)
agro = padronizar_colunas(agro)

# === Criar dicionários que ligam código da disciplina → professor ===
professores_info = dict(zip(info["Código da Disciplina"], info["Professor"]))
professores_adm = dict(zip(adm["Código da Disciplina"], adm["Professor"]))
professores_agro = dict(zip(agro["Código da Disciplina"], agro["Professor"]))

# === Definir dias e horários ===
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50",
    "10:50-11:40", "11:40-12:30", "13:50-14:40",
    "14:40-15:30", "15:50-16:40", "16:40-17:30"
]

# === Função que distribui disciplinas automaticamente ===
def distribuir_disciplinas(df):
    matriz = np.zeros((len(dias), len(horarios)), dtype=int)
    for _, row in df.iterrows():
        codigo = int(row["Código da Disciplina"])
        aulas = int(row["Total de Aulas Semanais"])

        # Encontra posições vazias na matriz
        livres = [(i, j) for i in range(len(dias)) for j in range(len(horarios)) if matriz[i, j] == 0]
        if len(livres) == 0:
            break
        if len(livres) < aulas:
            aulas = len(livres)  # evita erro caso falte espaço

        # Escolhe posições aleatórias
        escolhidos = random.sample(livres, aulas)

        # Preenche as células com o código da disciplina
        for (i, j) in escolhidos:
            matriz[i, j] = codigo
    return matriz

# === Criar as matrizes para cada curso ===
matriz_info = distribuir_disciplinas(info)
matriz_adm = distribuir_disciplinas(adm)
matriz_agro = distribuir_disciplinas(agro)

# === Função para mostrar a matriz com nomes de professores ===
def mostrar_matriz(nome_curso, matriz, professores):
    print(f"\n MATRIZ DO CURSO: {nome_curso}")
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
                # Exibir código + nome do professor
                texto = f"{valor}-{nome_prof[:8]}"
                print(f"{texto:<15}", end="")
        print()  # quebra de linha ao final do dia

# === Exibir todas as matrizes ===
mostrar_matriz("Informática", matriz_info, professores_info)
mostrar_matriz("Administração", matriz_adm, professores_adm)
mostrar_matriz("Agropecuária", matriz_agro, professores_agro)
