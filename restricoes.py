from matrizGeradora import distribuir_disciplinas, dias, horarios  # Pega funções e variáveis do arquivo que gera horários
import random  # Importa biblioteca para números aleatórios
import numpy as np  # Importa biblioteca para trabalhar com matrizes

class ValidadorHorarios:  # Cria uma classe para verificar se os horários estão bons
    def __init__(self):  # Método que roda quando criamos um validador
        self.horarios_manha = [0, 1, 2, 3, 4, 5]  # Horários da manhã (índices 0 a 5)
        self.horarios_tarde = [6, 7, 8, 9]  # Horários da tarde (índices 6 a 9)
        self.todas_matrizes_globais = []  # Lista vazia para guardar todos os horários gerados

    def inicializar_dados(self, todas_matrizes):  # Método para receber todos os horários gerados
        self.todas_matrizes_globais = todas_matrizes  # Guarda os horários para poder verificar depois

    def validar_carga_horaria_disciplinas(self, matriz, df):  # Verifica se todas as matérias têm o número certo de aulas
        """Verificação MUITO IMPORTANTE - tem que estar perfeita"""  # Explicação
        erros = []  # Lista vazia para guardar erros encontrados
        total_aulas_necessarias = 0  # Contador para o total de aulas que são necessárias

        for _, row in df.iterrows():  # Para cada matéria no arquivo CSV
            codigo_disciplina = row["Código da Disciplina"]  # Pega o código da matéria
            aulas_necessarias = int(row["Total de Aulas Semanais"])  # Pega quantas aulas esta matéria precisa
            total_aulas_necessarias += aulas_necessarias  # Soma ao total geral

            # Conta quantas aulas desta matéria foram colocadas no horário
            aulas_alocadas = np.count_nonzero(matriz == codigo_disciplina)

            if aulas_alocadas != aulas_necessarias:  # Se o número de aulas não está certo
                disciplina_nome = row["Disciplina"]  # Pega o nome da matéria
                erros.append(  # Adiciona um erro na lista
                    f"CARGA HORÁRIA: {disciplina_nome} → {aulas_alocadas}/{aulas_necessarias} aulas"  # Mensagem do erro
                )

        # Conta o total de aulas que foram colocadas no horário
        total_aulas_alocadas = np.count_nonzero(matriz != 0)
        if total_aulas_alocadas != total_aulas_necessarias:  # Se o total não está certo
            erros.append(f"TOTAL: {total_aulas_alocadas}/{total_aulas_necessarias} aulas")  # Adiciona erro

        return erros  # Retorna a lista de erros

    def validar_professor_duas_turmas_mesmo_horario(self, matriz_atual, professores_atual, curso_atual, serie_atual, turma_atual):  # Verifica se um professor está em duas turmas ao mesmo tempo
        """Verificação MUITO IMPORTANTE - não pode acontecer"""  # Explicação
        erros = []  # Lista vazia para erros

        for dia_idx in range(len(dias)):  # Para cada dia da semana
            for horario_idx in range(len(horarios)):  # Para cada horário
                cod_disc_atual = matriz_atual[dia_idx, horario_idx]  # Pega a matéria neste horário
                if cod_disc_atual != 0 and cod_disc_atual != '0':  # Se tem aula neste horário
                    professor_atual = professores_atual.get(cod_disc_atual)  # Pega o professor desta aula

                    if professor_atual:  # Se encontrou o professor
                        # Verifica todas as outras turmas
                        for curso, serie, turma, matriz, professores, df in self.todas_matrizes_globais:
                            # Pula a turma atual (não compara com ela mesma)
                            if curso == curso_atual and serie == serie_atual and turma == turma_atual:
                                continue  # Vai para a próxima turma

                            cod_disc_outra = matriz[dia_idx, horario_idx]  # Pega a matéria da outra turma no mesmo horário
                            if cod_disc_outra != 0 and cod_disc_outra != '0':  # Se a outra turma tem aula neste horário
                                professor_outra = professores.get(cod_disc_outra)  # Pega o professor da outra turma
                                if professor_atual == professor_outra:  # Se é o mesmo professor
                                    erros.append(  # Adiciona erro
                                        f"PROFESSOR CONFLITO: {professor_atual} em {turma_atual} e {turma}"  # Mensagem
                                    )
        return erros  # Retorna lista de erros

    def validar_eficiencia_manha(self, matriz, df):  # Verifica se a manhã está bem aproveitada
        """Verificação de QUALIDADE: Manhã deve estar bem aproveitada"""  # Explicação
        erros = []  # Lista vazia

        # Conta aulas na manhã e tarde
        aulas_manha = sum(1 for dia in range(len(dias)) for hora in self.horarios_manha if matriz[dia, hora] != 0)
        aulas_tarde = sum(1 for dia in range(len(dias)) for hora in self.horarios_tarde if matriz[dia, hora] != 0)
        capacidade_manha = len(dias) * len(self.horarios_manha)  # Calcula quantas aulas cabem na manhã

        vagas_manha_vazias = capacidade_manha - aulas_manha  # Calcula quantos horários ficaram vazios na manhã

        # Só é problema se tem aulas na tarde E muitos horários vazios na manhã
        if aulas_tarde > 0 and vagas_manha_vazias > 3:  # Se tem mais de 3 horários vazios na manhã e aulas na tarde
            eficiencia = (aulas_manha / capacidade_manha) * 100  # Calcula percentual de aproveitamento
            erros.append(f"EFICIÊNCIA MANHÃ: {eficiencia:.1f}% ({vagas_manha_vazias} vagas)")  # Adiciona erro

        return erros  # Retorna lista

    def validar_todas_restricoes(self, matriz, professores, df, curso, serie, turma):  # Verifica tudo
        erros = []  # Lista para todos os erros

        # 1. Verifica se todas as matérias têm o número certo de aulas
        erros.extend(self.validar_carga_horaria_disciplinas(matriz, df))

        # 2. Verifica se nenhum professor está em duas turmas ao mesmo tempo
        erros.extend(self.validar_professor_duas_turmas_mesmo_horario(matriz, professores, curso, serie, turma))

        # 3. Verifica se a manhã está bem aproveitada
        erros.extend(self.validar_eficiencia_manha(matriz, df))

        # Calcula uma pontuação (quanto menor, melhor)
        pontuacao = len(erros)  # Começa com o número de erros
        for erro in erros:  # Para cada erro
            if "CARGA HORÁRIA" in erro:  # Se é erro de carga horária (MUITO GRAVE)
                pontuacao += 1000  # Adiciona muito ponto (queremos evitar isso)
            elif "PROFESSOR CONFLITO" in erro:  # Se é erro de professor em dois lugares
                pontuacao += 500  # Adiciona muitos pontos (muito grave)
            elif "EFICIÊNCIA" in erro:  # Se é só questão de eficiência
                pontuacao += 10  # Adiciona poucos pontos (não é tão grave)

        return erros, pontuacao  # Retorna erros e pontuação

# Cria um validador que pode ser usado por todo o programa
validador = ValidadorHorarios()

def validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma):  # Função para validar e dar pontuação
    professores = dict(zip(df["Código da Disciplina"], df["Professor"]))  # Cria lista de professores
    return validador.validar_todas_restricoes(matriz, professores, df, curso, serie, turma)  # Chama o validador

def validar_restricoes(matriz, df, curso, serie, turma):  # Função para validar sem pontuação
    professores = dict(zip(df["Código da Disciplina"], df["Professor"]))  # Cria lista de professores
    erros, _ = validador.validar_todas_restricoes(matriz, professores, df, curso, serie, turma)  # Valida ignorando pontuação
    return erros  # Retorna só os erros

def autoajustar_matriz_com_pontuacao(matriz, df, curso, serie, turma, max_tentativas=100):  # Tenta melhorar o horário
    """Tenta ajustar automaticamente o horário para ficar melhor"""  # Explicação
    print("🔄 Autoajuste priorizando carga horária...")  # Mensagem

    melhor_matriz = matriz.copy()  # Faz uma cópia do horário original
    melhor_pontuacao = float('inf')  # Começa com uma pontuação muito ruim

    for tentativa in range(max_tentativas):  # Tenta várias vezes melhorar
        # Gera um novo horário para esta turma
        nova_matriz, professores = distribuir_disciplinas(df, curso, serie, turma)
        # Verifica se este novo horário é bom
        erros, pontuacao = validar_restricoes_com_pontuacao(nova_matriz, df, curso, serie, turma)

        if pontuacao < melhor_pontuacao:  # Se este horário é melhor que o anterior
            melhor_matriz = nova_matriz.copy()  # Guarda este horário como o melhor
            melhor_pontuacao = pontuacao  # Guarda esta pontuação como a melhor

            if tentativa % 10 == 0:  # A cada 10 tentativas
                print(f"   Tentativa {tentativa + 1}: Pontuação = {melhor_pontuacao}")  # Mostra progresso

        if pontuacao == 0:  # Se encontrou um horário perfeito
            print(f"   ✅ HORÁRIO PERFEITO na tentativa {tentativa + 1}")  # Comemora!
            return melhor_matriz, True, pontuacao  # Retorna o horário perfeito

    print(f"   Melhor encontrado: pontuação {melhor_pontuacao}")  # Mostra o melhor que conseguiu
    return melhor_matriz, False, melhor_pontuacao  # Retorna o melhor horário encontrado

def autoajustar_matriz(matriz, df, curso, serie, turma, max_tentativas=20):  # Versão simples do ajuste
    matriz_ajustada, sucesso, pontuacao = autoajustar_matriz_com_pontuacao(matriz, df, curso, serie, turma, max_tentativas)  # Chama a versão completa
    return matriz_ajustada, sucesso  # Retorna só o horário e se conseguiu

def inicializar_validador(todas_matrizes):  # Função para preparar o validador
    validador.inicializar_dados(todas_matrizes)  # Passa todos os horários para o validador

def validar_restricoes_globais():  # Função para verificar problemas entre todas as turmas (ainda não faz nada)
    return []  # Retorna lista vazia (não implementada ainda)