import psycopg2
import psycopg2.extras
import os

# Credenciais para conexão com o banco de dados
APP_DB_USER = "SCC541_Murilo_Rossi"
APP_DB_PASSWORD = "grupo10_Murilo_2025"
APP_DB_NAME = "SCC541_Grupo10"
APP_DB_HOST = "143.107.183.82"
APP_DB_PORT = "5432"

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.id_driver_count = None
        self.id_constructor_count = None
        # Define o caminho para a pasta de scripts SQL
        self._sql_path = os.path.join(os.path.dirname(__file__), 'sql-commands')

    def _read_sql_file(self, filename):
        """Lê um arquivo .sql do diretório de comandos e retorna seu conteúdo."""
        try:
            with open(os.path.join(self._sql_path, filename), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"ERRO CRÍTICO: Arquivo SQL não encontrado: {filename}")
            return None
        except Exception as e:
            print(f"ERRO CRÍTICO: Falha ao ler o arquivo SQL {filename}: {e}")
            return None

    def connect(self):
        """
        Conecta ao banco de dados com credenciais fixas.
        Este método deve ser chamado uma vez para estabelecer a conexão da aplicação.
        A autenticação SCRAM-SHA-256 ocorre aqui, entre a aplicação e o servidor DB.
        """
        if self.conn:
            return True # Já está conectado
        try:
            self.conn = psycopg2.connect(
                dbname=APP_DB_NAME,
                user=APP_DB_USER,
                password=APP_DB_PASSWORD,
                host=APP_DB_HOST,
                port=APP_DB_PORT,
            )
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # print(f"Conectado com sucesso ao banco '{APP_DB_NAME}' como '{APP_DB_USER}'.")
            self.update_id_counts()
            return True
        except psycopg2.Error as e:
            print(f"ERRO CRÍTICO: Não foi possível conectar ao banco de dados: {e}")
            self.conn = None
            self.cursor = None
            return False

    def update_id_counts(self):
        """
        Carrega os valores de DriverCount e ConstructorCount da tabela ID_Counts
        do banco de dados e os armazena nos atributos da classe.
        """
        sql_query = self._read_sql_file('update_id_counts.sql')
        if not sql_query: return

        self.cursor.execute(sql_query)
        counts = self.cursor.fetchone()

        if counts:
            self.id_driver_count = counts['drivercount']
            self.id_constructor_count = counts['constructorcount']
            print(f"Contagens de IDs carregadas do DB: Drivers={self.id_driver_count}, Constructors={self.id_constructor_count}")
        else:
            print("Aviso: Tabela ID_Counts vazia ou não encontrada. Contagens não carregadas.")

    def validate_app_user(self, login, password):
        """
        Valida as credenciais do usuário da aplicação contra a tabela USERS.
        Este método NÃO realiza uma nova conexão ao banco.
        """
        sql_query = self._read_sql_file('validate_app_user.sql')
        if not sql_query: return None

        try:
            params = (login, password)
            self.cursor.execute(sql_query, params)
            user_data = self.cursor.fetchone()
            return user_data
        except psycopg2.Error as e:
            print(f"Erro ao validar usuário: {e}")
            return None

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Desconectado do banco de dados.")

    def execute_query(self, query, params=None):
        """Executa uma query SELECT e retorna todos os resultados."""
        if not query: return None
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Erro ao executar query: {e}\nQuery: {query}\nParams: {params}")
            self.conn.rollback()
            return None

    def execute_non_query(self, query, params=None):
        """Executa uma query INSERT, UPDATE, DELETE e retorna o número de linhas afetadas."""
        if not query: return None
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except psycopg2.Error as e:
            print(f"Erro ao executar non-query: {e}\nQuery: {query}\nParams: {params}")
            self.conn.rollback()
            return None

    def execute_many_non_query(self, query, params_list=None):
        """Executa uma query INSERT, UPDATE, DELETE para múltiplos registros."""
        if not query: return None
        try:
            psycopg2.extras.execute_batch(self.cursor, query, params_list)
            self.conn.commit()
            return self.cursor.rowcount
        except psycopg2.Error as e:
            print(f"Erro ao executar execute_many_non_query: {e}\nQuery: {query}")
            self.conn.rollback()
            return None

    def log_user_activity(self, user_id, event_type="login"):
        """
        Registra uma atividade do usuário (login/logout) na tabela Users_Log.
        Usa as funções CURRENT_DATE e CURRENT_TIME do PostgreSQL para os registros.
        """
        sql_query = self._read_sql_file('log_user_activity.sql')
        params = (user_id, event_type)
        self.execute_non_query(sql_query, params)

    # --- Ações do Administrador ---

    def admin_cadastrar_escuderia(self, constructor_ref, name, nationality, url):
        """
        Admin cadastra uma nova escuderia.
        A trigger 'constructors_sync_users_trigger' no banco de dados irá:
        1. Criar o usuário correspondente na tabela USERS.
        2. Cancelar a inserção se o login (baseado em constructor_ref) já existir.
        """
        sql_query = self._read_sql_file('admin_cadastrar_escuderia.sql')
        params = (self.id_constructor_count + 1, constructor_ref, name, nationality, url)
        self.id_constructor_count += 1
        print(self.id_constructor_count)
        return self.execute_non_query(sql_query, params)

    def admin_cadastrar_piloto(self, driver_ref, number, code, forename, surname, dob, nationality, url):
        """
        Admin cadastra um novo piloto.
        A trigger 'driver_sync_users_trigger' no banco de dados irá:
        1. Criar o usuário correspondente na tabela USERS.
        2. Cancelar a inserção se o login (baseado em driver_ref) já existir.
        """
        sql_query = self._read_sql_file('admin_cadastrar_piloto.sql')
        params = (self.id_driver_count + 1, driver_ref, number, code, forename, surname, dob, nationality, url)
        return self.execute_non_query(sql_query, params)

    # --- Dashboard do Administrador ---

    def admin_get_dashboard_counts(self):
        """Busca contagens para o dashboard do admin."""
        sql_query = self._read_sql_file('admin_get_dashboard_counts.sql')
        return self.execute_query(sql_query)

    def admin_get_corridas_ano_corrente(self):
        """
        Busca corridas do ano corrente.
        CORRIGIDO: O número de voltas é obtido a partir do máximo de voltas na tabela Results.
        """
        sql_query = self._read_sql_file('admin_get_corridas_ano_corrente.sql')
        return self.execute_query(sql_query)

    def admin_get_escuderias_pontos_ano_corrente(self):
        """Busca escuderias e seus pontos no ano corrente."""
        sql_query = self._read_sql_file('admin_get_escuderias_pontos_ano_corrente.sql')
        return self.execute_query(sql_query)

    def admin_get_pilotos_pontos_ano_corrente(self):
        """Busca pilotos e seus pontos no ano corrente."""
        sql_query = self._read_sql_file('admin_get_pilotos_pontos_ano_corrente.sql')
        return self.execute_query(sql_query)

    # --- Relatórios do Administrador ---

    def admin_report_resultados_por_status(self):
        """Relatório Admin 1: Quantidade de resultados por status."""
        sql_query = self._read_sql_file('admin_report_resultados_por_status.sql')
        return self.execute_query(sql_query)

    def admin_report_aeroportos_proximos(self, nome_cidade_param):
        """
        Relatório Admin 2: Aeroportos próximos a uma cidade.
        Não deu certo no banco do projeto pois não há a permissão para instalar a extensão.
        """
        sql_query = self._read_sql_file('admin_report_aeroportos_proximos.sql')
        return self.execute_query(sql_query, (f'%{nome_cidade_param}%',))

    def admin_report_escuderias_corridas_circuitos(self):
        """Relatório Admin 3: Relatório em múltiplos níveis."""
        results = {}
        
        # Cada consulta agora vem de um arquivo SQL dedicado.
        results["escuderias_com_pilotos"] = self.execute_query(self._read_sql_file('admin_report_escuderias_com_pilotos.sql'))
        results["total_corridas"] = self.execute_query(self._read_sql_file('admin_report_total_corridas.sql'))
        results["corridas_por_circuito"] = self.execute_query(self._read_sql_file('admin_report_corridas_por_circuito.sql'))
        results["detalhe_corridas_circuito"] = self.execute_query(self._read_sql_file('admin_report_detalhe_corridas_circuito.sql'))
        
        return results

    # --- Ações da Escuderia ---

    def escuderia_consultar_piloto_por_forename(self, constructor_id_logado, forename_piloto):
        """
        Busca pilotos pelo primeiro nome (Forename) que já participaram de corridas
        pela escuderia logada.
        """
        sql_query = self._read_sql_file('escuderia_consultar_piloto_por_forename.sql')
        params = (constructor_id_logado, f'%{forename_piloto}%')
        return self.execute_query(sql_query, params)

    def escuderia_dashboard_get_info(self, constructor_id_logado):
        """Busca informações agregadas para o dashboard da escuderia."""
        dashboard_data = {}
        params = (constructor_id_logado,)

        # Nome da Escuderia
        sql_nome = self._read_sql_file('escuderia_dashboard_get_nome.sql')
        nome_res = self.execute_query(sql_nome, params)
        dashboard_data["nome_escuderia"] = nome_res[0]['name'] if nome_res else "N/D"

        # Quantidade de vitórias
        sql_vitorias = self._read_sql_file('escuderia_dashboard_get_vitorias.sql')
        vitorias_res = self.execute_query(sql_vitorias, params)
        dashboard_data["vitorias"] = vitorias_res[0]['vitorias'] if vitorias_res else 0

        # Quantidade de pilotos diferentes
        sql_pilotos = self._read_sql_file('escuderia_dashboard_get_qtd_pilotos.sql')
        pilotos_res = self.execute_query(sql_pilotos, params)
        dashboard_data["qtd_pilotos"] = pilotos_res[0]['qtd_pilotos'] if pilotos_res else 0

        # Primeiro e último ano
        sql_anos = self._read_sql_file('escuderia_dashboard_get_anos.sql')
        anos_res = self.execute_query(sql_anos, params)
        if anos_res and anos_res[0]:
            dashboard_data["primeiro_ano"] = anos_res[0]['primeiro_ano']
            dashboard_data["ultimo_ano"] = anos_res[0]['ultimo_ano']
        else:
            dashboard_data["primeiro_ano"] = "N/A"
            dashboard_data["ultimo_ano"] = "N/A"

        return dashboard_data

    # --- Relatórios da Escuderia (Funções PL/SQL) ---

    def escuderia_report_pilotos_vitorias(self, constructor_id_logado):
        """Relatório Escuderia 4: Lista pilotos da escuderia e suas vitórias."""
        sql_query = self._read_sql_file('escuderia_report_pilotos_vitorias.sql')
        return self.execute_query(sql_query, (constructor_id_logado,))

    def escuderia_report_resultados_por_status(self, constructor_id_logado):
        """Relatório Escuderia 5: Quantidade de resultados por status da escuderia."""
        sql_query = self._read_sql_file('escuderia_report_resultados_por_status.sql')
        return self.execute_query(sql_query, (constructor_id_logado,))

    # --- Funções para o Dashboard do Piloto ---

    def piloto_dashboard_get_info(self, driver_id_logado):
        """Busca informações agregadas para o dashboard do piloto."""
        dashboard_data = {}
        params = (driver_id_logado,)

        # Nome do piloto e escuderia mais recente
        sql_piloto_info = self._read_sql_file('piloto_dashboard_get_piloto_info.sql')
        info_res = self.execute_query(sql_piloto_info, params)
        if info_res:
            dashboard_data["nome_piloto"] = info_res[0]['nome_piloto']
            dashboard_data["nome_escuderia"] = info_res[0]['nome_escuderia'] or "N/A"
        else:
            dashboard_data["nome_piloto"] = "N/D"
            dashboard_data["nome_escuderia"] = "N/A"

        # Primeiro e último ano
        sql_anos = self._read_sql_file('piloto_dashboard_get_anos.sql')
        anos_res = self.execute_query(sql_anos, params)
        if anos_res and anos_res[0]:
            dashboard_data["primeiro_ano"] = anos_res[0]['primeiro_ano']
            dashboard_data["ultimo_ano"] = anos_res[0]['ultimo_ano']
        else:
            dashboard_data["primeiro_ano"] = "N/A"
            dashboard_data["ultimo_ano"] = "N/A"

        # Estatísticas por ano e circuito
        sql_stats = self._read_sql_file('piloto_dashboard_get_stats_ano_circuito.sql')
        dashboard_data["stats_ano_circuito"] = self.execute_query(sql_stats, params)

        return dashboard_data

    # --- Relatórios do Piloto (Funções PL/SQL) ---

    def piloto_report_pontos_por_ano_corrida(self, driver_id_logado):
        """Relatório Piloto 6: Pontos obtidos por ano e corrida."""
        sql_query = self._read_sql_file('piloto_report_pontos_por_ano_corrida.sql')
        return self.execute_query(sql_query, (driver_id_logado,))

    def piloto_report_resultados_por_status(self, driver_id_logado):
        """Relatório Piloto 7: Quantidade de resultados por status do piloto."""
        sql_query = self._read_sql_file('piloto_report_resultados_por_status.sql')
        return self.execute_query(sql_query, (driver_id_logado,))