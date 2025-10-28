from matrizGeradora import distribuir_disciplinas, dias, horarios


class ValidadorHorarios:
    def __init__(self):
        self.vagos_permitidos = [3, 4, 7, 8]
        self.professores_por_disciplina = {}
        self.carga_horaria_professores = {}
        self.todas_matrizes_globais = []

    def inicializar_dados(self, todas_matrizes):
        self.professores_por_disciplina = {}
        self.carga_horaria_professores = {}
        self.todas_matrizes_globais = todas_matrizes

        for curso, serie, turma, matriz, professores, df in todas_matrizes:
            for _, row in df.iterrows():
                cod_disc = row["Código da Disciplina"]
                professor = row["Professor"]
                self.professores_por_disciplina[cod_disc] = professor

                if professor not in self.carga_horaria_professores:
                    self.carga_horaria_professores[professor] = 0
                self.carga_horaria_professores[professor] += int(row["Total de Aulas Semanais"])

    def validar_professor_duplicado_mesmo_horario(self, matriz, professores):
        erros = []
        for dia_idx in range(len(dias)):
            professores_vistos = set()
            for horario_idx in range(len(horarios)):
                cod_disc = matriz[dia_idx, horario_idx]
                if cod_disc != 0 and cod_disc != '0':
                    professor = professores.get(cod_disc, "Desconhecido")
                    if professor in professores_vistos:
                        erros.append(
                            f"Professor {professor} em dois horários simultâneos: "
                            f"{dias[dia_idx]} no horário {horarios[horario_idx]}"
                        )
                    professores_vistos.add(professor)
        return erros

    def validar_professor_mesmo_horario_outras_turmas(self, matriz_atual, professores_atual, curso_atual, serie_atual,
                                                      turma_atual):
        erros = []
        for dia_idx in range(len(dias)):
            for horario_idx in range(len(horarios)):
                cod_disc_atual = matriz_atual[dia_idx, horario_idx]
                if cod_disc_atual != 0 and cod_disc_atual != '0':
                    professor_atual = professores_atual.get(cod_disc_atual)

                    for curso, serie, turma, matriz, professores, df in self.todas_matrizes_globais:
                        if curso == curso_atual and serie == serie_atual and turma == turma_atual:
                            continue

                        cod_disc_outra = matriz[dia_idx, horario_idx]
                        if cod_disc_outra != 0 and cod_disc_outra != '0':
                            professor_outra = professores.get(cod_disc_outra)
                            if professor_atual == professor_outra:
                                erros.append(
                                    f"Professor {professor_atual} em mesma hora em {turma_atual} e {turma}"
                                )
        return erros

    def validar_horarios_vagos(self, matriz):
        erros = []
        for dia_idx in range(len(dias)):
            for horario_idx in range(len(horarios)):
                if (matriz[dia_idx, horario_idx] == 0 or matriz[
                    dia_idx, horario_idx] == '0') and horario_idx not in self.vagos_permitidos:
                    erros.append(
                        f"Horário vago não permitido: {dias[dia_idx]} no horário {horarios[horario_idx]}"
                    )
        return erros

    def validar_ultimo_manha_primeiro_tarde(self, matriz, professores):
        erros = []
        ultimo_manha = 4
        primeiro_tarde = 5

        for dia_idx in range(len(dias)):
            professor_ultimo_manha = None
            professor_primeiro_tarde = None

            cod_manha = matriz[dia_idx, ultimo_manha]
            if cod_manha != 0 and cod_manha != '0':
                professor_ultimo_manha = professores.get(cod_manha)

            cod_tarde = matriz[dia_idx, primeiro_tarde]
            if cod_tarde != 0 and cod_tarde != '0':
                professor_primeiro_tarde = professores.get(cod_tarde)

            if (professor_ultimo_manha and professor_primeiro_tarde and
                    professor_ultimo_manha == professor_primeiro_tarde):
                erros.append(
                    f"Professor {professor_ultimo_manha} leciona no último horário da manhã "
                    f"e primeiro da tarde na {dias[dia_idx]}"
                )
        return erros

    def validar_dois_turnos_por_dia(self, matriz, professores):
        erros = []
        turnos = {
            "manhã": [0, 1, 2, 3, 4],
            "tarde": [5, 6, 7, 8]
        }

        for dia_idx in range(len(dias)):
            professores_turnos = {}

            for turno, horarios_turno in turnos.items():
                for horario_idx in horarios_turno:
                    cod_disc = matriz[dia_idx, horario_idx]
                    if cod_disc != 0 and cod_disc != '0':
                        professor = professores.get(cod_disc)
                        if professor:
                            if professor not in professores_turnos:
                                professores_turnos[professor] = set()
                            professores_turnos[professor].add(turno)

            for professor, turnos_atuando in professores_turnos.items():
                if len(turnos_atuando) > 2:
                    erros.append(
                        f"Professor {professor} atua em {len(turnos_atuando)} turnos "
                        f"na {dias[dia_idx]}: {', '.join(turnos_atuando)}"
                    )
        return erros

    def validar_aulas_por_dia_professor(self, matriz, professores, df):
        erros = []

        disciplinas_curso = set(df[df["Código da Disciplina"].str.startswith("dis0")]["Código da Disciplina"])
        professores_curso = set()

        for cod_disc in disciplinas_curso:
            if cod_disc in professores:
                professores_curso.add(professores[cod_disc])

        for dia_idx in range(len(dias)):
            aulas_por_professor = {}

            for horario_idx in range(len(horarios)):
                cod_disc = matriz[dia_idx, horario_idx]
                if cod_disc != 0 and cod_disc != '0':
                    professor = professores.get(cod_disc)
                    if professor:
                        if professor not in aulas_por_professor:
                            aulas_por_professor[professor] = 0
                        aulas_por_professor[professor] += 1

            for professor, aulas_dia in aulas_por_professor.items():
                if professor in professores_curso:
                    if aulas_dia < 2:
                        erros.append(
                            f"Professor do curso {professor} com apenas {aulas_dia} aulas na {dias[dia_idx]} (mínimo: 2)")
                    if aulas_dia > 4:
                        erros.append(
                            f"Professor do curso {professor} com {aulas_dia} aulas na {dias[dia_idx]} (máximo: 4)")
                else:
                    if aulas_dia > 2:
                        erros.append(
                            f"Professor comum {professor} com {aulas_dia} aulas na {dias[dia_idx]} (máximo: 2)")

        return erros

    def validar_carga_horaria_professores(self):
        erros = []
        limite_professor_curso = 20
        limite_professor_comum = 16

        for professor, carga in self.carga_horaria_professores.items():
            if any(professor in [p for p in profs.values()] for _, _, _, _, profs, _ in self.todas_matrizes_globais):
                if carga > limite_professor_curso:
                    erros.append(f"Professor {professor} excede carga horária: {carga} > {limite_professor_curso}")
            else:
                if carga > limite_professor_comum:
                    erros.append(
                        f"Professor comum {professor} excede carga horária: {carga} > {limite_professor_comum}")

        return erros

    def validar_todas_restricoes(self, matriz, professores, df, curso, serie, turma):
        erros = []

        erros.extend(self.validar_professor_duplicado_mesmo_horario(matriz, professores))
        erros.extend(self.validar_professor_mesmo_horario_outras_turmas(matriz, professores, curso, serie, turma))
        erros.extend(self.validar_horarios_vagos(matriz))
        erros.extend(self.validar_ultimo_manha_primeiro_tarde(matriz, professores))
        erros.extend(self.validar_dois_turnos_por_dia(matriz, professores))
        erros.extend(self.validar_aulas_por_dia_professor(matriz, professores, df))


        pontuacao = len(erros)

        for erro in erros:
            if "horário vago não permitido" in erro.lower():
                pontuacao += 2
            elif "professor em dois horários simultâneos" in erro.lower():
                pontuacao += 3

        return erros, pontuacao


validador = ValidadorHorarios()


def validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma):
    professores = dict(zip(df["Código da Disciplina"], df["Professor"]))
    return validador.validar_todas_restricoes(matriz, professores, df, curso, serie, turma)


def validar_restricoes(matriz, df, curso, serie, turma):
    professores = dict(zip(df["Código da Disciplina"], df["Professor"]))
    erros, _ = validador.validar_todas_restricoes(matriz, professores, df, curso, serie, turma)
    return erros


def autoajustar_matriz_com_pontuacao(matriz, df, curso, serie, turma, max_tentativas=30):
    print("Aplicando autoajuste...")

    melhor_matriz = matriz
    melhor_pontuacao = float('inf')
    melhor_erros = []

    for tentativa in range(max_tentativas):
        erros, pontuacao = validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma)

        if pontuacao < melhor_pontuacao:
            melhor_matriz = matriz.copy()
            melhor_pontuacao = pontuacao
            melhor_erros = erros.copy()

        if pontuacao == 0:
            print(f"✓ Matriz PERFEITA encontrada na tentativa {tentativa + 1}")
            return matriz, True, pontuacao

        matriz, professores = distribuir_disciplinas(df)

        if tentativa % 10 == 0:
            print(f"Tentativa {tentativa + 1}: Melhor pontuação = {melhor_pontuacao}")

    print(f"Melhor matriz encontrada com pontuação {melhor_pontuacao} (violações: {len(melhor_erros)})")
    return melhor_matriz, False, melhor_pontuacao


def autoajustar_matriz(matriz, df, curso, serie, turma, max_tentativas=20):
    matriz_ajustada, sucesso, pontuacao = autoajustar_matriz_com_pontuacao(matriz, df, curso, serie, turma,
                                                                           max_tentativas)
    return matriz_ajustada, sucesso

def inicializar_validador(todas_matrizes):
    validador.inicializar_dados(todas_matrizes)

def validar_restricoes_globais():
    return validador.validar_carga_horaria_professores()