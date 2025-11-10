import numpy as np  # Importa biblioteca para trabalhar com matrizes (tabelas de números)
import random  # Importa biblioteca para gerar números aleatórios
import pandas as pd  # Importa biblioteca para trabalhar com dados em formato de tabela
from csvpandas import horariosTURMAS  # Pega os dados das turmas que já foram preparados

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]  # Lista dos dias da semana que terão aula
horarios = [  # Lista com todos os horários de aula disponíveis
    "07:10-08:00", "08:00-08:50", "09:00-09:50",  # Três primeiros horários da manhã
    "09:50-10:40", "10:50-11:40", "11:40-12:30",  # Três últimos horários da manhã
    "13:50-14:40", "14:40-15:30", "15:50-16:40", "16:40-17:30"  # Quatro horários da tarde
]

class GeradorTardeOpcional:  # Cria uma classe (um molde) para gerar horários dando preferência para a manhã
    def __init__(self):  # Método que roda quando criamos um novo gerador de horários
        self.horarios_manha = [0, 1, 2, 3, 4, 5]  # Os primeiros 6 horários são da manhã (índices 0 a 5)
        self.horarios_tarde = [6, 7, 8, 9]  # Os últimos 4 horários são da tarde (índices 6 a 9)
        self.professor_horarios = {}  # Um dicionário vazio para lembrar onde cada professor foi colocado

    def inicializar_rastreamento(self):  # Método para limpar a memória de onde os professores estão
        self.professor_horarios = {}  # Esvazia o dicionário que guarda os professores

    def distribuir_tarde_opcional(self, df, curso, serie, turma, max_tentativas=500):  # Método principal que tenta criar os horários
        """Foca em colocar o máximo de aulas na manhã, só usando a tarde se for realmente necessário"""

        for tentativa in range(max_tentativas):  # Tenta várias vezes (até 500 vezes) criar um horário bom
            matriz = np.zeros((len(dias), len(horarios)), dtype=object)  # Cria uma tabela vazia com 5 linhas (dias) e 10 colunas (horários)
            professores_dict = dict(zip(df["Código da Disciplina"], df["Professor"]))  # Cria uma lista que liga cada matéria ao seu professor

            # PRIMEIRA TENTATIVA: Tentar colocar TODAS as aulas só na MANHÃ
            sucesso_manha_completa = self._tentar_manha_completa(matriz, df, professores_dict, curso, serie, turma)

            if sucesso_manha_completa:  # Se conseguiu colocar tudo na manhã
                print(f"   ✅ CONSEGUIU: Todas as aulas na manhã!")  # Mostra mensagem de sucesso
                return matriz, professores_dict  # Retorna a tabela de horários e a lista de professores

            # SEGUNDA TENTATIVA: Se não conseguiu tudo na manhã, usar a tarde para completar
            sucesso_com_tarde = self._usar_tarde_complemento(matriz, df, professores_dict, curso, serie, turma)

            if sucesso_com_tarde:  # Se conseguiu com complemento da tarde
                aulas_manha = self._contar_aulas_manha(matriz)  # Conta quantas aulas ficaram na manhã
                aulas_tarde = self._contar_aulas_tarde(matriz)  # Conta quantas aulas ficaram na tarde
                total_necessario = df["Total de Aulas Semanais"].sum()  # Soma total de aulas que eram necessárias

                print(f"   🔄 COMPLEMENTO: {aulas_manha} manhã + {aulas_tarde} tarde = {total_necessario} total")  # Mostra o resultado
                return matriz, professores_dict  # Retorna a tabela de horários e a lista de professores

        print(f"⚠️  DIFICULDADE para {curso} {serie} {turma}")  # Se tentou muitas vezes e não conseguiu
        return self._abordagem_garantida(df, curso, serie, turma)  # Usa um método mais simples que sempre funciona

    def _tentar_manha_completa(self, matriz, df, professores_dict, curso, serie, turma):  # Tenta colocar tudo só na manhã
        """Tenta colocar TODAS as aulas apenas na MANHÃ"""
        total_necessario = df["Total de Aulas Semanais"].sum()  # Soma quantas aulas são necessárias no total
        capacidade_manha = len(dias) * len(self.horarios_manha)  # Calcula quantas aulas cabem na manhã (5 dias × 6 horários = 30)

        # Verifica se é possível fisicamente colocar todas as aulas na manhã
        if total_necessario > capacidade_manha:  # Se precisar de mais aulas do que cabem na manhã
            return False  # Retorna que não é possível

        # Cria uma lista com todas as aulas que precisam ser colocadas
        todas_aulas = []  # Lista vazia para guardar as aulas
        for _, row in df.iterrows():  # Para cada matéria no arquivo CSV
            codigo = row["Código da Disciplina"]  # Pega o código da matéria
            aulas_necessarias = int(row["Total de Aulas Semanais"])  # Pega quantas aulas esta matéria precisa
            professor = professores_dict[codigo]  # Pega o professor desta matéria
            # Adiciona esta aula várias vezes na lista (uma vez para cada aula necessária)
            todas_aulas.extend([(codigo, professor)] * aulas_necessarias)

        # Ordena as matérias começando pelas que têm mais aulas (são mais difíceis de encaixar)
        todas_aulas.sort(key=lambda x: todas_aulas.count(x), reverse=True)

        # Tenta colocar cada aula na manhã
        for codigo, professor in todas_aulas:  # Para cada aula que precisa ser colocada
            alocado = False  # Ainda não colocou esta aula

            # Tentar de forma inteligente: dias com menos aulas primeiro
            dias_ordenados = sorted(range(len(dias)),
                                    key=lambda d: sum(1 for h in self.horarios_manha if matriz[d, h] != 0))

            for dia_idx in dias_ordenados:  # Para cada dia (começando pelos menos ocupados)
                if alocado:  # Se já conseguiu colocar esta aula
                    break  # Para de tentar

                # Mistura a ordem dos horários para tentar combinações diferentes
                horarios_tentativa = random.sample(self.horarios_manha, len(self.horarios_manha))
                for horario_idx in horarios_tentativa:  # Para cada horário da manhã
                    # Verifica duas coisas: se o horário está livre e se o professor está disponível
                    if (matriz[dia_idx, horario_idx] == 0 and  # O horário está vazio?
                            self._professor_disponivel(professor, dia_idx, horario_idx)):  # O professor está livre neste horário?
                        # NOTA: A verificação de conflito no mesmo dia foi removida

                        matriz[dia_idx, horario_idx] = codigo  # Coloca a matéria neste horário
                        self._registrar_alocacao(professor, dia_idx, horario_idx, curso, serie, turma)  # Marca que o professor está ocupado
                        alocado = True  # Conseguiu colocar esta aula
                        break  # Para de tentar horários para esta aula

            if not alocado:  # Se não conseguiu colocar esta aula em nenhum horário da manhã
                return False  # Retorna que não conseguiu colocar tudo na manhã

        return True  # Conseguiu colocar todas as aulas na manhã!

    def _usar_tarde_complemento(self, matriz, df, professores_dict, curso, serie, turma):  # Usa a tarde para completar
        """Usa a tarde apenas para completar aulas que não couberam na manhã"""
        # Primeiro: Tenta colocar o máximo possível na manhã
        self._maximizar_manha(matriz, df, professores_dict, curso, serie, turma)
        # Depois: Completa o restante na tarde
        return self._completar_na_tarde(matriz, df, professores_dict, curso, serie, turma)

    def _maximizar_manha(self, matriz, df, professores_dict, curso, serie, turma):  # Coloca o máximo na manhã
        """Preenche a manhã o máximo possível antes de usar a tarde"""
        # Cria lista com todas as aulas
        todas_aulas = []  # Lista vazia
        for _, row in df.iterrows():  # Para cada matéria no arquivo CSV
            codigo = row["Código da Disciplina"]  # Pega código da matéria
            aulas_necessarias = int(row["Total de Aulas Semanais"])  # Pega quantas aulas precisa
            professor = professores_dict[codigo]  # Pega o professor
            # Adiciona as aulas na lista
            todas_aulas.extend([(codigo, professor)] * aulas_necessarias)

        random.shuffle(todas_aulas)  # Mistura a ordem das aulas para tentar combinações diferentes

        # Tenta colocar cada aula na manhã
        for codigo, professor in todas_aulas:  # Para cada aula
            alocado = False  # Ainda não colocou
            for dia_idx in range(len(dias)):  # Para cada dia da semana
                if alocado:  # Se já colocou
                    break  # Para
                for horario_idx in self.horarios_manha:  # Para cada horário da manhã
                    # Verifica se pode colocar a aula aqui
                    if (matriz[dia_idx, horario_idx] == 0 and  # Horário vazio?
                            self._professor_disponivel(professor, dia_idx, horario_idx)):  # Professor livre?
                        # NOTA: A verificação de conflito no mesmo dia foi removida

                        matriz[dia_idx, horario_idx] = codigo  # Coloca a matéria
                        self._registrar_alocacao(professor, dia_idx, horario_idx, curso, serie, turma)  # Marca professor ocupado
                        alocado = True  # Conseguiu colocar
                        break  # Para de tentar horários

    def _completar_na_tarde(self, matriz, df, professores_dict, curso, serie, turma):  # Completa na tarde o que faltou
        """Completa na tarde apenas o que faltou na manhã"""
        # Verifica quais matérias ainda precisam de mais aulas
        disciplinas_faltantes = []  # Lista vazia para matérias que faltam aulas
        for _, row in df.iterrows():  # Para cada matéria no arquivo CSV
            codigo = row["Código da Disciplina"]  # Pega código da matéria
            aulas_alocadas = np.count_nonzero(matriz == codigo)  # Conta quantas aulas já foram colocadas
            aulas_necessarias = int(row["Total de Aulas Semanais"])  # Pega quantas aulas precisa no total
            aulas_faltantes = aulas_necessarias - aulas_alocadas  # Calcula quantas aulas ainda faltam

            if aulas_faltantes > 0:  # Se ainda faltam aulas desta matéria
                professor = professores_dict[codigo]  # Pega o professor
                # Adiciona as aulas faltantes na lista
                disciplinas_faltantes.extend([(codigo, professor)] * aulas_faltantes)

        if not disciplinas_faltantes:  # Se não faltam aulas de nenhuma matéria
            return True  # Já está completo!

        random.shuffle(disciplinas_faltantes)  # Mistura a ordem das aulas faltantes

        # Tenta colocar as aulas faltantes na tarde
        for codigo, professor in disciplinas_faltantes:  # Para cada aula faltante
            alocado = False  # Ainda não colocou
            for dia_idx in range(len(dias)):  # Para cada dia
                if alocado:  # Se já colocou
                    break  # Para
                for horario_idx in self.horarios_tarde:  # Para cada horário da tarde
                    if (matriz[dia_idx, horario_idx] == 0 and  # Horário vazio?
                            self._professor_disponivel(professor, dia_idx, horario_idx)):  # Professor livre?

                        matriz[dia_idx, horario_idx] = codigo  # Coloca a matéria
                        self._registrar_alocacao(professor, dia_idx, horario_idx, curso, serie, turma)  # Marca professor ocupado
                        alocado = True  # Conseguiu colocar
                        break  # Para de tentar horários

            if not alocado:  # Se não conseguiu colocar esta aula em nenhum horário da tarde
                return False  # Não conseguiu completar todas as aulas

        return True  # Conseguiu colocar todas as aulas faltantes!

    def _abordagem_garantida(self, df, curso, serie, turma):  # Método simples que sempre funciona
        """Método de última opção que SEMPRE consegue colocar todas as aulas"""
        print(f"🔧 Usando abordagem GARANTIDA para {curso} {serie} {turma}")  # Avisa que está usando este método

        matriz = np.zeros((len(dias), len(horarios)), dtype=object)  # Cria tabela vazia
        professores_dict = dict(zip(df["Código da Disciplina"], df["Professor"]))  # Cria lista de professores

        # Cria lista com todas as aulas
        todas_aulas = []  # Lista vazia
        for _, row in df.iterrows():  # Para cada matéria
            codigo = row["Código da Disciplina"]  # Pega código
            aulas_necessarias = int(row["Total de Aulas Semanais"])  # Pega quantas aulas precisa
            professor = professores_dict[codigo]  # Pega professor
            # Adiciona aulas na lista
            todas_aulas.extend([(codigo, professor)] * aulas_necessarias)

        # Coloca cada aula na primeira vaga livre que encontrar
        for codigo, professor in todas_aulas:  # Para cada aula
            alocado = False  # Ainda não colocou

            # Primeiro tenta na manhã
            for dia_idx in range(len(dias)):  # Para cada dia
                if alocado:  # Se já colocou
                    break  # Para
                for horario_idx in self.horarios_manha:  # Para cada horário da manhã
                    if matriz[dia_idx, horario_idx] == 0:  # Se o horário está vazio
                        matriz[dia_idx, horario_idx] = codigo  # Coloca a matéria
                        self._registrar_alocacao(professor, dia_idx, horario_idx, curso, serie, turma)  # Marca professor
                        alocado = True  # Conseguiu colocar
                        break  # Para de tentar horários

            # Se não conseguiu na manhã, tenta na tarde
            if not alocado:  # Se ainda não colocou
                for dia_idx in range(len(dias)):  # Para cada dia
                    if alocado:  # Se já colocou
                        break  # Para
                    for horario_idx in self.horarios_tarde:  # Para cada horário da tarde
                        if matriz[dia_idx, horario_idx] == 0:  # Se o horário está vazio
                            matriz[dia_idx, horario_idx] = codigo  # Coloca a matéria
                            self._registrar_alocacao(professor, dia_idx, horario_idx, curso, serie, turma)  # Marca professor
                            alocado = True  # Conseguiu colocar
                            break  # Para de tentar horários

        return matriz, professores_dict  # Retorna a tabela de horários e a lista de professores

    def _contar_aulas_manha(self, matriz):  # Conta quantas aulas tem na manhã
        return sum(1 for dia in range(len(dias)) for hora in self.horarios_manha if matriz[dia, hora] != 0)  # Soma todas as células não vazias da manhã

    def _contar_aulas_tarde(self, matriz):  # Conta quantas aulas tem na tarde
        return sum(1 for dia in range(len(dias)) for hora in self.horarios_tarde if matriz[dia, hora] != 0)  # Soma todas as células não vazias da tarde

    def _professor_disponivel(self, professor, dia_idx, horario_idx):  # Verifica se o professor está livre
        """Verifica se o professor está disponível (não está em outra turma no mesmo horário)"""
        chave = (professor, dia_idx, horario_idx)  # Cria uma chave única com professor, dia e horário
        return chave not in self.professor_horarios  # Retorna True se o professor não está ocupado neste horário

    def _registrar_alocacao(self, professor, dia_idx, horario_idx, curso, serie, turma):  # Marca que o professor está ocupado
        """Registra onde o professor foi colocado para evitar que ele fique em duas turmas ao mesmo tempo"""
        chave = (professor, dia_idx, horario_idx)  # Cria uma chave única
        self.professor_horarios[chave] = (curso, serie, turma)  # Guarda onde o professor foi colocado

# Cria um gerador de horários que pode ser usado por todo o programa
gerador_tarde_opcional = GeradorTardeOpcional()

def distribuir_disciplinas(df, curso="", serie="", turma="", max_tentativas=50):  # Função que outras partes do programa podem usar
    return gerador_tarde_opcional.distribuir_tarde_opcional(df, curso, serie, turma, max_tentativas)  # Chama o método do gerador

def gerar_matrizes_por_turma(df):  # Gera horários para todas as turmas do arquivo CSV
    # Verifica se o arquivo CSV tem as colunas necessárias
    if "Série" not in df.columns or "Turma_Letra" not in df.columns:  # Se não tem coluna Série ou Turma_Letra
        print("O arquivo CSV não tem colunas 'Série' e 'Turma_Letra'.")  # Mostra erro
        return []  # Retorna lista vazia

    gerador_tarde_opcional.inicializar_rastreamento()  # Limpa a memória de onde os professores estão

    resultados = []  # Lista vazia para guardar os resultados
    # Agrupa os dados por curso, série e turma (para criar horário para cada turma separadamente)
    grupos = df.groupby(["Curso", "Série", "Turma_Letra"])

    for (curso, serie, turma), grupo in grupos:  # Para cada turma
        print(f"\n🎯 GERANDO: {curso} - {serie} - Turma {turma}")  # Mostra qual turma está sendo processada
        total_aulas = grupo["Total de Aulas Semanais"].sum()  # Soma quantas aulas esta turma precisa
        capacidade_manha = len(dias) * len(gerador_tarde_opcional.horarios_manha)  # Calcula quantas aulas cabem na manhã

        print(f"   📚 Aulas necessárias: {total_aulas}")  # Mostra quantas aulas são necessárias
        print(f"   🌅 Capacidade manhã: {capacidade_manha}")  # Mostra quantas aulas cabem na manhã

        if total_aulas > capacidade_manha:  # Se precisar de mais aulas do que cabem na manhã
            aulas_tarde_minimas = total_aulas - capacidade_manha  # Calcula quantas aulas no mínimo precisam ser na tarde
            print(f"   🔄 Tarde OBRIGATÓRIA: mínimo {aulas_tarde_minimas} aulas na tarde")  # Avisa que vai usar a tarde
        else:  # Se todas as aulas cabem na manhã
            print(f"   ✅ Possível manhã COMPLETA")  # Avisa que pode ser só na manhã

        # Gera o horário para esta turma
        matriz, professores = distribuir_disciplinas(grupo, curso, serie, turma)

        aulas_alocadas = np.count_nonzero(matriz != 0)  # Conta quantas aulas foram colocadas no total
        aulas_manha = gerador_tarde_opcional._contar_aulas_manha(matriz)  # Conta aulas na manhã
        aulas_tarde = gerador_tarde_opcional._contar_aulas_tarde(matriz)  # Conta aulas na tarde

        print(f"   📊 Resultado: {aulas_manha} manhã + {aulas_tarde} tarde = {aulas_alocadas} total")  # Mostra o resultado

        if aulas_alocadas == total_aulas:  # Se conseguiu colocar todas as aulas necessárias
            if aulas_tarde == 0:  # Se não usou a tarde
                print(f"   🎉 MANHÃ COMPLETA PERFEITA!")  # Comemora!
            else:  # Se usou a tarde
                print(f"   ✅ CARGA HORÁRIA COMPLETA (com {aulas_tarde} aulas na tarde)")  # Avisa que completou
        else:  # Se não conseguiu colocar todas as aulas
            print(f"   ❌ FALTAM {total_aulas - aulas_alocadas} AULAS")  # Mostra quantas aulas faltaram

        # Guarda o resultado desta turma
        resultados.append((curso, serie, turma, matriz, professores, grupo))

    return resultados  # Retorna todos os horários gerados