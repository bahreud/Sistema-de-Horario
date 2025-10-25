import numpy as np
from matriz import distribuir_disciplinas

# --- CONFIGURAÇÕES ---
vagos_permitidos = [3, 4, 7, 8]  # índices permitidos (0-indexed)
# 3 e 4 -> manhã (10:50-11:40 e 11:40-12:30)
# 7 e 8 -> tarde (15:50-16:40 e 16:40-17:30)


def validar_restricoes(matriz, df):
    """Verifica restrições fundamentais e de eficiência."""
    erros = []
    professores = dict(zip(df["Código da Disciplina"], df["Professor"]))

    # Restrições Fundamentais ---------------------------
    # Nenhum professor pode estar em dois lugares ao mesmo tempo
    for dia_idx in range(matriz.shape[0]):
        vistos = set()
        for col in range(matriz.shape[1]):
            cod = matriz[dia_idx, col]
            if cod == 0:
                continue
            prof = professores.get(cod)
            if prof in vistos:
                erros.append(f"Professor {prof} em 2 lugares no mesmo horário (dia {dia_idx + 1}).")
            vistos.add(prof)

    # Horários vagos apenas nos permitidos
    for dia_idx in range(matriz.shape[0]):
        for col in range(matriz.shape[1]):
            if matriz[dia_idx, col] == 0 and col not in vagos_permitidos:
                erros.append(f"Horário vago não permitido no dia {dia_idx + 1}, horário {col + 1}.")

    # Restrições de Eficiência --------------------------
    # Evitar buracos antes do intervalo
    for dia_idx in range(matriz.shape[0]):
        horarios = matriz[dia_idx]
        for i in range(len(horarios) - 1):
            if horarios[i] == 0 and horarios[i + 1] != 0 and i not in vagos_permitidos:
                erros.append(f"Horário vago antes de aula no dia {dia_idx + 1}, horário {i + 1}.")

    # Aulas consecutivas (se possível)
    # Aqui apenas emitimos um aviso, não é erro
    for dia_idx in range(matriz.shape[0]):
        horarios = matriz[dia_idx]
        for i in range(len(horarios) - 1):
            if horarios[i] != 0 and horarios[i + 1] == 0:
                pass  # eficiência opcional

    # Resultado final
    if erros:
        print("\n Restrições violadas:")
        for e in erros:
            print(f" - {e}")
    else:
        print("Todas as restrições foram atendidas.")

    return erros


def autoajustar_matriz(matriz, df):
    """Tenta corrigir a matriz caso haja violações."""
    print("Aplicando autoajuste...")
    erros = validar_restricoes(matriz, df)

    # Tenta redistribuir se houver erros
    if erros:
        matriz_corrigida = distribuir_disciplinas(df)
        print("Nova matriz gerada após ajuste.")
        return matriz_corrigida
    return matriz

