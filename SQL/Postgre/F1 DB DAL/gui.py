import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, font
from datetime import datetime

# --- Paleta de Cores ---
COLOR_BACKGROUND = "#2E3033"
COLOR_WIDGET_BG = "#3F4145"
COLOR_TEXT = "#EAEAEA"
COLOR_ACCENT = "#4A6984"
COLOR_ACCENT_ACTIVE = "#5F85A6"
COLOR_HEADER = "#3A506B"

# --- Constantes da Interface ---
PAD_X = 12
PAD_Y = 6
INPUT_WIDTH = 30

# --- Janela Auxiliar para Exibição de Relatórios ---
class ReportWindow(tk.Toplevel):
    def __init__(self, parent, title, columns_map, data_rows, column_widths=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("900x500")
        self.configure(background=COLOR_BACKGROUND)

        # Frame para Treeview e Scrollbars
        frame = ttk.Frame(self, style="TFrame")
        frame.pack(expand=True, fill="both", padx=PAD_X, pady=PAD_Y)

        # Treeview (usa o estilo definido na App)
        self.tree = ttk.Treeview(frame, columns=list(columns_map.keys()), show="headings")

        for db_col, display_col in columns_map.items():
            self.tree.heading(db_col, text=display_col)
            col_width = 120  # Default
            if column_widths and db_col in column_widths:
                col_width = column_widths[db_col]
            self.tree.column(db_col, width=col_width, anchor='w', stretch=tk.YES)

        # Scrollbars (usam o estilo definido na App)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(expand=True, fill="both")

        if data_rows:
            for row in data_rows:
                if isinstance(row, dict) or hasattr(row, 'keys'):
                    values_to_insert = [row.get(key, "") for key in columns_map.keys()]
                else:
                    values_to_insert = row
                self.tree.insert("", "end", values=values_to_insert)
        else:
            self.tree.insert("", "end", values=(["Nenhum dado encontrado"] * len(columns_map)))

        # Botão Fechar
        close_button = ttk.Button(self, text="Fechar", command=self.destroy, style="TButton")
        close_button.pack(pady=PAD_Y*2)
        self.grab_set()
        self.focus_set()

class App:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager
        self.current_user_type = None
        self.current_user_id = None
        self.current_original_id = None
        self.current_user_login = None

        self.setup_style()

        self.root.title("FIA F1 - Ferramenta de Análise de Dados")
        self.root.geometry("450x300")
        self.root.configure(background=COLOR_BACKGROUND)

        self._main_frame = None
        self.show_login_screen()

    def setup_style(self):
        """Configura um tema moderno e customizado para a aplicação."""
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam") # Base para customização

        # --- Definições de Fontes ---
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        self.header_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")

        # --- Configurações Gerais do Tema ---
        self.style.configure(".",
                             background=COLOR_BACKGROUND,
                             foreground=COLOR_TEXT,
                             font=self.default_font,
                             borderwidth=0,
                             focuscolor=COLOR_ACCENT) # Remove cor de foco padrão

        # --- Estilos de Widgets Específicos ---
        self.style.configure("TFrame", background=COLOR_BACKGROUND)
        self.style.configure("TLabel", background=COLOR_BACKGROUND, foreground=COLOR_TEXT)
        self.style.configure("Header.TLabel", font=self.header_font, foreground=COLOR_ACCENT_ACTIVE)

        self.style.configure("TButton",
                             background=COLOR_ACCENT,
                             foreground=COLOR_TEXT,
                             font=("Segoe UI", 10, "bold"),
                             padding=(10, 5),
                             relief="flat",
                             borderwidth=0)
        self.style.map("TButton",
                       background=[("active", COLOR_ACCENT_ACTIVE), ("disabled", COLOR_WIDGET_BG)])

        self.style.configure("TEntry",
                             fieldbackground=COLOR_WIDGET_BG,
                             foreground=COLOR_TEXT,
                             insertcolor=COLOR_TEXT, # Cor do cursor
                             borderwidth=1,
                             relief="flat")

        self.style.configure("TLabelframe", background=COLOR_BACKGROUND, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label",
                             background=COLOR_BACKGROUND,
                             foreground=COLOR_TEXT,
                             font=("Segoe UI", 11, "bold"))

        # Estilo da Tabela/Treeview
        self.style.configure("Treeview",
                             background=COLOR_WIDGET_BG,
                             fieldbackground=COLOR_WIDGET_BG,
                             foreground=COLOR_TEXT,
                             rowheight=25,
                             relief="flat")
        self.style.map("Treeview",
                       background=[("selected", COLOR_ACCENT)])

        # Estilo do Cabeçalho da Tabela
        self.style.configure("Treeview.Heading",
                             background=COLOR_HEADER,
                             foreground=COLOR_TEXT,
                             font=("Segoe UI", 10, "bold"),
                             relief="flat")
        self.style.map("Treeview.Heading",
                       background=[("active", COLOR_ACCENT_ACTIVE)])

    def _clear_main_frame(self):
        if self._main_frame:
            self._main_frame.destroy()
        self._main_frame = ttk.Frame(self.root, style="TFrame")
        self._main_frame.pack(expand=True, fill="both", padx=PAD_X, pady=PAD_Y)

    # --- Tela de Login ---
    def show_login_screen(self):
        self._clear_main_frame()
        self.root.geometry("450x300")
        self.root.title("FIA F1 - Login")

        login_frame = ttk.LabelFrame(self._main_frame, text="Autenticação de Usuário", style="TLabelframe")
        login_frame.pack(expand=True, padx=20, pady=20)

        # --- Campos de Login ---
        ttk.Label(login_frame, text="Login:").grid(row=0, column=0, padx=PAD_X, pady=PAD_Y*2, sticky="w")
        self.login_entry = ttk.Entry(login_frame, width=INPUT_WIDTH)
        self.login_entry.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y*2)
        self.login_entry.insert(0, "admin")

        ttk.Label(login_frame, text="Senha:").grid(row=1, column=0, padx=PAD_X, pady=PAD_Y*2, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=INPUT_WIDTH)
        self.password_entry.grid(row=1, column=1, padx=PAD_X, pady=PAD_Y*2)
        self.password_entry.insert(0, "admin")
        
        # --- Botão de Login ---
        login_button = ttk.Button(login_frame, text="Entrar", command=self.attempt_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=(20, PAD_Y))

        self.login_entry.focus_set()

    # --- Lógica de Login ---
    def attempt_login(self):
        # Passo 1: Garantir que a aplicação está conectada ao banco de dados.
        if not self.db.connect():
            messagebox.showerror("Erro de Conexão",
                                 "Não foi possível conectar ao banco de dados usando as credenciais da aplicação. Verifique as configurações em db_manager.py e se o servidor PostgreSQL está no ar.")
            return

        # Passo 2: Pegar as credenciais da tela.
        login = self.login_entry.get()
        password = self.password_entry.get()
        if not login or not password:
            messagebox.showwarning("Entrada Inválida", "Os campos de login e senha não podem estar vazios.")
            return

        # Passo 3: Validar as credenciais contra a tabela USERS.
        user_details = self.db.validate_app_user(login, password)

        # Passo 4: Processar o resultado da validação.
        if user_details:
            # Login bem-sucedido! Armazenar dados da sessão.
            self.current_user_id = user_details['userid']
            self.current_user_type = user_details['tipo']
            self.current_original_id = user_details['idoriginal']
            self.current_user_login = login

            # Registrar a atividade de login
            self.db.log_user_activity(self.current_user_id, "login")
            
            # Ir para o dashboard
            self.show_dashboard_screen()
        else:
            # Login falhou.
            messagebox.showerror("Acesso Negado", "Login ou senha inválidos.")
            # A aplicação continua conectada ao banco, pronta para outra tentativa.

    def logout(self):
        # A conexão com o banco permanece ativa, apenas a sessão do usuário da aplicação é encerrada.
        if self.db and self.current_user_id:
            self.db.log_user_activity(self.current_user_id, "logout")

        # Limpar variáveis da sessão
        self.current_user_type = None
        self.current_user_id = None
        self.current_original_id = None
        self.current_user_login = None
        
        # Voltar para a tela de login
        self.show_login_screen()

    # --- Tela do Dashboard ---
    def show_dashboard_screen(self):
        self._clear_main_frame()
        self.root.geometry("900x700")
        self.root.title(f"FIA F1 - Dashboard ({self.current_user_type})")

        header_frame = ttk.Frame(self._main_frame)
        header_frame.pack(fill="x", pady=PAD_Y, anchor="n")
        
        user_label = f"Usuário: {self.current_user_login} ({self.current_user_type})"
        ttk.Label(header_frame, text=user_label, font=self.header_font).pack(side="left")
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side="right")

        ttk.Separator(self._main_frame, orient="horizontal").pack(fill="x", pady=PAD_Y*2)

        dashboard_content_frame = ttk.Frame(self._main_frame)
        dashboard_content_frame.pack(expand=True, fill="both")

        # Botão centralizado para Relatórios
        report_button_frame = ttk.Frame(self._main_frame)
        report_button_frame.pack(pady=PAD_Y*2, fill="x")
        ttk.Button(report_button_frame, text="Abrir Central de Relatórios", command=self.show_reports_selection_screen).pack()

        # Carrega o dashboard específico do tipo de usuário
        user_dashboards = {
            'Administrador': self.setup_admin_dashboard,
            'Escuderia': self.setup_escuderia_dashboard,
            'Piloto': self.setup_piloto_dashboard
        }
        dashboard_func = user_dashboards.get(self.current_user_type, lambda p: ttk.Label(p, text="Tipo de usuário desconhecido.").pack())
        dashboard_func(dashboard_content_frame)

    # --- Função utilitária para exibir Treeviews ---
    def _display_data_in_treeview(self, parent_frame, title, columns_map, data_rows, height=2):
        frame = ttk.LabelFrame(parent_frame, text=title)
        frame.pack(pady=PAD_Y, padx=PAD_X, fill="x", expand=True)

        tree = ttk.Treeview(frame, columns=list(columns_map.keys()), show="headings", height=height)
        
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for db_col, display_col in columns_map.items():
            tree.heading(db_col, text=display_col)
            tree.column(db_col, width=50, anchor='w')

        if data_rows:
            for row_data in data_rows:
                values = [row_data.get(key, 'N/A') for key in columns_map.keys()]
                tree.insert("", "end", values=values)
        else:
            tree.insert("", "end", values=(["N/D"] * len(columns_map)))
        return tree

    # --- Dashboards Específicos ---
    def setup_admin_dashboard(self, parent_frame):
        # Ações
        actions_frame = ttk.LabelFrame(parent_frame, text="Ações do Administrador")
        actions_frame.pack(pady=PAD_Y, fill="x")
        ttk.Button(actions_frame, text="Cadastrar Nova Escuderia", command=self.show_cadastrar_escuderia_form).pack(side="left", padx=PAD_X)
        ttk.Button(actions_frame, text="Cadastrar Novo Piloto", command=self.show_cadastrar_piloto_form).pack(side="left", padx=PAD_X)

        # Resumo
        summary_frame = ttk.LabelFrame(parent_frame, text="Resumo Geral")
        summary_frame.pack(pady=PAD_Y, fill="x")
        counts = self.db.admin_get_dashboard_counts()
        if counts and counts[0]:
            data = counts[0]
            info_text = (f"Pilotos: {data.get('total_pilotos', 'N/D')} | "
                         f"Escuderias: {data.get('total_escuderias', 'N/D')} | "
                         f"Temporadas: {data.get('total_temporadas', 'N/D')}")
            ttk.Label(summary_frame, text=info_text).pack(anchor="w", padx=PAD_X, pady=PAD_Y)
        
        # Tabelas do Dashboard
        cols_corridas = {"nomecorrida": "Nome da Corrida", "totalvoltas": "Total de Voltas", "tempo": "Tempo"}
        self._display_data_in_treeview(parent_frame, "Corridas do Ano Corrente", cols_corridas, self.db.admin_get_corridas_ano_corrente())
        
        cols_escuderias = {"nomeescuderia": "Escuderia", "totalpontos": "Pontos"}
        self._display_data_in_treeview(parent_frame, "Pontos de Escuderias (Ano Corrente)", cols_escuderias, self.db.admin_get_escuderias_pontos_ano_corrente())
        
        cols_pilotos = {"nomepiloto": "Piloto", "totalpontos": "Pontos"}
        self._display_data_in_treeview(parent_frame, "Pontos de Pilotos (Ano Corrente)", cols_pilotos, self.db.admin_get_pilotos_pontos_ano_corrente())

    def setup_escuderia_dashboard(self, parent_frame):
        # Ações
        actions_frame = ttk.LabelFrame(parent_frame, text="Ações da Escuderia")
        actions_frame.pack(pady=PAD_Y, fill="x")
        ttk.Button(actions_frame, text="Consultar Piloto", command=self.show_escuderia_consultar_piloto_form).pack(side="left", padx=PAD_X)
        ttk.Button(actions_frame, text="Inserir Pilotos de Arquivo", command=self.show_escuderia_inserir_piloto_arquivo).pack(side="left", padx=PAD_X)

        # Resumo
        data = self.db.escuderia_dashboard_get_info(self.current_original_id)
        if data:
            summary_frame = ttk.LabelFrame(parent_frame, text=f"Resumo: {data.get('nome_escuderia', 'N/D')}")
            summary_frame.pack(pady=PAD_Y, fill="x", expand=True)
            info_text = (f"Total de Vitórias: {data.get('vitorias', 'N/D')} | "
                         f"Pilotos Distintos: {data.get('qtd_pilotos', 'N/D')} | "
                         f"Anos de Atividade: {data.get('primeiro_ano', 'N/A')} - {data.get('ultimo_ano', 'N/A')}")
            ttk.Label(summary_frame, text=info_text).pack(anchor="w", padx=PAD_X, pady=PAD_Y)

    def setup_piloto_dashboard(self, parent_frame):
        data = self.db.piloto_dashboard_get_info(self.current_original_id)
        if data:
            summary_frame = ttk.LabelFrame(parent_frame, text=f"Resumo: {data.get('nome_piloto', 'N/D')}")
            summary_frame.pack(pady=PAD_Y, fill="x")
            
            info_text_1 = f"Escuderia (mais recente): {data.get('nome_escuderia', 'N/A')}"
            info_text_2 = f"Anos de Atividade: {data.get('primeiro_ano', 'N/A')} - {data.get('ultimo_ano', 'N/A')}"
            ttk.Label(summary_frame, text=info_text_1).pack(anchor="w", padx=PAD_X)
            ttk.Label(summary_frame, text=info_text_2).pack(anchor="w", padx=PAD_X)

            cols_stats = {"ano": "Ano", "nome_circuito": "Circuito", "qtd_pontos": "Pontos", "qtd_vitorias": "Vitórias", "qtd_corridas": "Corridas"}
            self._display_data_in_treeview(parent_frame, "Desempenho por Ano e Circuito", cols_stats, data.get("stats_ano_circuito"), height=15)
    
    # --- Formulários e Ações ---
    # Os métodos para formulários e relatórios permanecem os mesmos, mas agora usarão
    # o novo tema definido. Aqui está uma versão de um deles como exemplo da adaptação.
    def show_cadastrar_escuderia_form(self):
        win = tk.Toplevel(self.root)
        win.title("Cadastrar Nova Escuderia")
        win.geometry("450x300")
        win.configure(background=COLOR_BACKGROUND)
        win.grab_set()

        frame = ttk.LabelFrame(win, text="Dados da Escuderia", padding=PAD_X*2)
        frame.pack(expand=True, fill="both", padx=PAD_X, pady=PAD_Y)

        fields = {
            "ConstructorRef:": ttk.Entry(frame, width=INPUT_WIDTH),
            "Nome:": ttk.Entry(frame, width=INPUT_WIDTH),
            "Nacionalidade:": ttk.Entry(frame, width=INPUT_WIDTH),
            "URL:": ttk.Entry(frame, width=INPUT_WIDTH)
        }

        for i, (label_text, entry_widget) in enumerate(fields.items()):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky="w", pady=PAD_Y)
            entry_widget.grid(row=i, column=1, pady=PAD_Y, padx=PAD_X)
        
        ref_entry, name_entry, nat_entry, url_entry = fields.values()

        def save_escuderia():
            # (Lógica de salvamento permanece a mesma)
            ref, name, nationality, url = ref_entry.get(), name_entry.get(), nat_entry.get(), url_entry.get()
            if not all([ref, name, nationality, url]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=win)
                return
            try:
                if self.db.admin_cadastrar_escuderia(ref, name, nationality, url) is not None:
                    messagebox.showinfo("Sucesso", "Escuderia cadastrada!", parent=win)
                    win.destroy()
                    self.show_dashboard_screen()
                else:
                    messagebox.showerror("Erro", "Falha ao cadastrar. Verifique console.", parent=win)
            except Exception as e:
                messagebox.showerror("Erro Crítico", f"Erro: {e}", parent=win)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=PAD_Y*2)
        ttk.Button(button_frame, text="Salvar Escuderia", command=save_escuderia).pack()
        ref_entry.focus_set()

    def show_cadastrar_piloto_form(self):
        win = tk.Toplevel(self.root)
        win.title("Cadastrar Novo Piloto")
        win.geometry("500x450") # Aumenta um pouco a altura para o novo campo
        win.configure(background=COLOR_BACKGROUND)
        win.grab_set()

        frame = ttk.LabelFrame(win, text="Dados do Piloto", padding=PAD_X*2)
        frame.pack(expand=True, fill="both", padx=PAD_X, pady=PAD_Y)

        # Dicionário de campos, agora incluindo a URL
        fields = {
            "DriverRef:": ttk.Entry(frame, width=INPUT_WIDTH),
            "Número (opcional):": ttk.Entry(frame, width=INPUT_WIDTH),
            "Código (3 letras):": ttk.Entry(frame, width=INPUT_WIDTH),
            "Nome (Forename):": ttk.Entry(frame, width=INPUT_WIDTH),
            "Sobrenome (Surname):": ttk.Entry(frame, width=INPUT_WIDTH),
            "Data de Nasc. (YYYY-MM-DD):": ttk.Entry(frame, width=INPUT_WIDTH),
            "Nacionalidade:": ttk.Entry(frame, width=INPUT_WIDTH),
            "URL (do piloto):": ttk.Entry(frame, width=INPUT_WIDTH) # <<< CAMPO ADICIONADO
        }

        # Posiciona os widgets na janela
        for i, (label_text, entry_widget) in enumerate(fields.items()):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky="w", pady=PAD_Y)
            entry_widget.grid(row=i, column=1, pady=PAD_Y, padx=PAD_X)
        
        # Desempacota os widgets em variáveis para fácil acesso
        entries = list(fields.values())

        def save_piloto():
            # Coleta os valores de todos os campos
            values = [e.get() for e in entries]
            driver_ref, number_str, code, forename, surname, dob_str, nationality, url = values

            # Validação dos campos obrigatórios
            if not all([driver_ref, forename, surname, dob_str, nationality, url]):
                messagebox.showerror("Erro", "Todos os campos, incluindo a URL, são obrigatórios.", parent=win)
                return

            try:
                # Valida o formato da data
                datetime.strptime(dob_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erro de Formato", "Data de Nascimento deve estar no formato YYYY-MM-DD.", parent=win)
                return

            number = int(number_str) if number_str and number_str.isdigit() else None
            
            # Trata a URL: se o usuário deixar em branco, passamos None para o banco
            # (se a constraint UNIQUE permitir múltiplos NULLs, caso contrário, deve ser preenchido)
            final_url = url if url else None

            try:
                # Chama a função do db_manager com o novo parâmetro 'url'
                result = self.db.admin_cadastrar_piloto(driver_ref, number, code, forename, surname, dob_str, nationality, final_url)
                
                if result is not None:
                    messagebox.showinfo("Sucesso", "Piloto cadastrado com sucesso!", parent=win)
                    win.destroy()
                    self.show_dashboard_screen()
                else:
                    messagebox.showerror("Erro de Cadastro", "Falha ao cadastrar piloto. Verifique o console para detalhes (possível login ou URL duplicada).", parent=win)
            
            except Exception as e:
                # Captura erros da trigger do banco (ex: login duplicado)
                messagebox.showerror("Erro Crítico", f"Erro ao salvar no banco de dados:\n{e}", parent=win)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=PAD_Y*2)
        ttk.Button(button_frame, text="Salvar Piloto", command=save_piloto).pack()
        
        # Coloca o foco no primeiro campo
        entries[0].focus_set()

    # --- Ações da Escuderia (Formulários) ---
    def show_escuderia_consultar_piloto_form(self):
        win = tk.Toplevel(self.root)
        win.title("Consultar Piloto da Escuderia por Nome")
        win.geometry("700x450")
        win.configure(background=COLOR_BACKGROUND)
        win.grab_set()

        # Frame para a entrada de dados
        input_frame = ttk.Frame(win, padding=PAD_X)
        input_frame.pack(fill="x", pady=PAD_Y)
        
        ttk.Label(input_frame, text="Primeiro Nome do Piloto:").pack(side="left", padx=(0, PAD_X))
        forename_entry = ttk.Entry(input_frame, width=INPUT_WIDTH)
        forename_entry.pack(side="left", fill="x", expand=True)
        
        # Frame para os resultados
        results_frame = ttk.Frame(win, padding=PAD_X)
        results_frame.pack(expand=True, fill="both")

        # Dicionário de colunas para o Treeview
        cols_pilotos = {
            "Nome Completo": "Nome Completo",
            "Data de Nascimento": "Data de Nascimento",
            "Nacionalidade": "Nacionalidade"
        }
        
        # Cria a Treeview usando a função auxiliar
        tree = self._display_data_in_treeview(results_frame, "Pilotos Encontrados", cols_pilotos, [], height=12)

        def search_piloto():
            forename = forename_entry.get()
            if not forename:
                messagebox.showwarning("Entrada Inválida", "Por favor, insira o primeiro nome do piloto para buscar.", parent=win)
                return

            # Limpa resultados anteriores
            for i in tree.get_children():
                tree.delete(i)
                
            # Busca os dados no banco
            data = self.db.escuderia_consultar_piloto_por_forename(self.current_original_id, forename)
            
            # Popula a tabela com os novos dados
            if data:
                for row in data:
                    # O DictCursor nos permite acessar as colunas pelo nome (alias) da query
                    values = [row["Nome Completo"], row["Data de Nascimento"], row["Nacionalidade"]]
                    tree.insert("", "end", values=values)
            else:
                tree.insert("", "end", values=(["Nenhum piloto encontrado."], "", ""))

        search_button = ttk.Button(input_frame, text="Buscar", command=search_piloto)
        search_button.pack(side="left", padx=PAD_X)
        
        forename_entry.focus_set()

    def show_escuderia_inserir_piloto_arquivo(self):
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de pilotos (.txt ou .csv)",
            filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")),
            parent=self.root
        )
        if not filepath:
            return

        # COMENTÁRIO: A lógica de processamento do arquivo e inserção deve ser robusta.
        # Cada linha do arquivo: Driverref, Number, Code, Forename, Surname, Date of Birth (YYYY-MM-DD), Nationality
        # Number e Code podem ser nulos.
        # Verificar se piloto já existe (nome e sobrenome). Se não, inserir.
        # A trigger de DRIVER deve criar o usuário em USERS.
        # Informar o resultado de cada piloto.

        pilotos_processados = [] # Lista para armazenar resultados (sucesso, falha, existente)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if not line or line.startswith("#"): # Ignorar linhas vazias ou comentários
                        continue

                    parts = [p.strip() for p in line.split(',')] # Assumindo CSV
                    if len(parts) < 5 or len(parts) > 7 : # Min: ref, fn, sn, dob, nat. Max: +num, +code
                         pilotos_processados.append(f"Linha {i+1}: Formato inválido (esperado 5-7 colunas) - '{line}'")
                         continue

                    # Preencher partes faltantes (number, code) com None se não fornecidas
                    driver_ref = parts[0]
                    forename = parts[1] # Ajustar índices conforme seu arquivo
                    surname = parts[2]
                    dob_str = parts[3]
                    nationality = parts[4]
                    number_str = parts[5] if len(parts) > 5 and parts[5] else None
                    code = parts[6] if len(parts) > 6 and parts[6] else None

                    # Validação básica
                    if not all([driver_ref, forename, surname, dob_str, nationality]):
                        pilotos_processados.append(f"Linha {i+1} ({forename} {surname}): Campos obrigatórios faltando.")
                        continue
                    try:
                        datetime.strptime(dob_str, '%Y-%m-%d')
                    except ValueError:
                        pilotos_processados.append(f"Linha {i+1} ({forename} {surname}): Formato de data inválido (use YYYY-MM-DD).")
                        continue

                    number = int(number_str) if number_str and number_str.isdigit() else None

                    # Verificar se piloto já existe
                    if self.db.escuderia_verificar_piloto_existente(forename, surname):
                        pilotos_processados.append(f"Piloto {forename} {surname}: Já existe no banco. Inserção cancelada.")
                        continue

                    # Inserir novo piloto
                    try:
                        if self.db.escuderia_inserir_novo_piloto(driver_ref, number, code, forename, surname, dob_str, nationality) is not None:
                            pilotos_processados.append(f"Piloto {forename} {surname}: Cadastrado com sucesso (usuário criado via trigger).")
                        else:
                             pilotos_processados.append(f"Piloto {forename} {surname}: Falha ao cadastrar (verifique console/trigger).")
                    except Exception as e_insert:
                         pilotos_processados.append(f"Piloto {forename} {surname}: Erro crítico no cadastro - {e_insert}")

            # Mostrar resultados
            results_text = "\n".join(pilotos_processados)
            if not results_text: results_text = "Nenhum piloto processado ou arquivo vazio."

            result_win = tk.Toplevel(self.root)
            result_win.title("Resultado da Importação de Pilotos")
            result_win.geometry("700x400")
            text_area = tk.Text(result_win, wrap="word", height=20, width=80)
            text_area.pack(padx=PAD_X, pady=PAD_Y, expand=True, fill="both")
            text_area.insert("1.0", results_text)
            text_area.config(state="disabled")
            ttk.Button(result_win, text="OK", command=result_win.destroy).pack(pady=PAD_Y)
            result_win.grab_set()

        except Exception as e:
            messagebox.showerror("Erro ao Processar Arquivo", f"Ocorreu um erro: {e}", parent=self.root)

    # --- Tela de Seleção de Relatórios ---
    def show_reports_selection_screen(self):
        reports_win = tk.Toplevel(self.root)
        reports_win.title(f"Relatórios Disponíveis - {self.current_user_type}")
        reports_win.geometry("500x400")
        reports_win.grab_set()

        frame = ttk.Frame(reports_win, padding=PAD_X)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Selecione um relatório:", font=("Arial", 14)).pack(pady=PAD_Y*2)

        if self.current_user_type == 'Administrador':
            ttk.Button(frame, text="Relatório 1: Resultados por Status", command=self.admin_show_report_resultados_status).pack(fill="x", pady=PAD_Y)
            ttk.Button(frame, text="Relatório 2: Aeroportos Próximos", command=self.admin_show_report_aeroportos_input).pack(fill="x", pady=PAD_Y)
            ttk.Button(frame, text="Relatório 3: Escuderias, Corridas e Circuitos", command=self.admin_show_report_escuderias_corridas).pack(fill="x", pady=PAD_Y)
        elif self.current_user_type == 'Escuderia':
            ttk.Button(frame, text="Relatório 4: Pilotos da Escuderia e Vitórias", command=self.escuderia_show_report_pilotos_vitorias).pack(fill="x", pady=PAD_Y)
            ttk.Button(frame, text="Relatório 5: Resultados por Status (Escuderia)", command=self.escuderia_show_report_status).pack(fill="x", pady=PAD_Y)
        elif self.current_user_type == 'Piloto':
            ttk.Button(frame, text="Relatório 6: Pontos por Ano e Corrida", command=self.piloto_show_report_pontos_ano_corrida).pack(fill="x", pady=PAD_Y)
            ttk.Button(frame, text="Relatório 7: Resultados por Status (Piloto)", command=self.piloto_show_report_status).pack(fill="x", pady=PAD_Y)
        else:
            ttk.Label(frame, text="Nenhum relatório disponível para este tipo de usuário.").pack()

        ttk.Button(frame, text="Fechar", command=reports_win.destroy).pack(pady=PAD_Y*3, side="bottom")

    # --- Funções para Exibir Relatórios Específicos ---

    # Relatórios do Admin
    def admin_show_report_resultados_status(self):
        data = self.db.admin_report_resultados_por_status()
        # As chaves do dicionário agora correspondem exatamente aos aliases da query SQL
        cols = {"Nome do Status": "Nome do Status", "Quantidade": "Quantidade"}
        ReportWindow(self.root, "Admin - Relatório: Resultados por Status", cols, data)

    def admin_show_report_aeroportos_input(self):
        cidade = simpledialog.askstring("Entrada para Relatório", "Digite o nome da cidade:", parent=self.root)
        if cidade:
            data = self.db.admin_report_aeroportos_proximos(cidade)
            cols = {
                "Nome da Cidade": "Cidade Pesquisada",
                "Código IATA": "Código IATA",
                "Nome do Aeroporto": "Nome do Aeroporto",
                "Cidade do Aeroporto": "Cidade do Aeroporto",
                "Distância (Km)": "Distância (Km)",
                "Tipo do Aeroporto": "Tipo do Aeroporto"
            }
            column_widths = {"Nome do Aeroporto": 250, "Distância (Km)": 100}
            ReportWindow(self.root, f"Admin - Relatório: Aeroportos Próximos a '{cidade}'", cols, data, column_widths)

    def admin_show_report_escuderias_corridas(self):
        report_data = self.db.admin_report_escuderias_corridas_circuitos()

        # Nível 0: Escuderias e Qtd. Pilotos
        cols_esc_pilotos = {"Nome da Escuderia": "Nome da Escuderia", "Qtd. Pilotos": "Qtd. Pilotos"}
        ReportWindow(self.root, "Admin - Relatório: Escuderias e Qtd. de Pilotos", cols_esc_pilotos, report_data.get("escuderias_com_pilotos"))

        # Nível 1: Total de Corridas (mostrado em uma messagebox)
        total_corridas_data = report_data.get("total_corridas")
        total = total_corridas_data[0]['total_corridas'] if total_corridas_data else "N/D"
        messagebox.showinfo("Admin - Relatório", f"Total de corridas cadastradas: {total}", parent=self.root)

        # Nível 2: Corridas por Circuito (stats voltas)
        cols_circuito_stats = {
            "Circuito": "Circuito", "Qtd. Corridas": "Qtd. Corridas",
            "Mín. Voltas": "Mín. Voltas", "Média Voltas": "Média Voltas", "Máx. Voltas": "Máx. Voltas"
        }
        ReportWindow(self.root, "Admin - Relatório: Corridas por Circuito (Estatísticas)",
                    cols_circuito_stats, report_data.get("corridas_por_circuito"))

        # Nível 3: Detalhe de Corridas por Circuito
        cols_detalhe_corrida = {
            "Circuito": "Circuito", "Nome da Corrida": "Nome da Corrida", "Ano": "Ano",
            "Voltas": "Voltas", "Tempo Total": "Tempo Total"
        }
        ReportWindow(self.root, "Admin - Relatório: Detalhe de Corridas por Circuito",
                    cols_detalhe_corrida, report_data.get("detalhe_corridas_circuito"))


    # Relatórios da Escuderia
    def escuderia_show_report_pilotos_vitorias(self):
        data = self.db.escuderia_report_pilotos_vitorias(self.current_original_id)
        cols = {"Nome Completo do Piloto": "Nome Completo do Piloto", "Quantidade de Vitórias": "Quantidade de Vitórias"}
        ReportWindow(self.root, "Escuderia - Relatório: Pilotos e Vitórias", cols, data)

    def escuderia_show_report_status(self):
        data = self.db.escuderia_report_resultados_por_status(self.current_original_id)
        cols = {"Status": "Status", "Quantidade": "Quantidade"}
        ReportWindow(self.root, "Escuderia - Relatório: Resultados por Status", cols, data)

    # Relatórios do Piloto
    def piloto_show_report_pontos_ano_corrida(self):
        data = self.db.piloto_report_pontos_por_ano_corrida(self.current_original_id)
        cols = {"Ano": "Ano", "Nome da Corrida": "Nome da Corrida", "Pontos Obtidos": "Pontos Obtidos"}
        ReportWindow(self.root, "Piloto - Relatório: Pontos por Ano e Corrida", cols, data)

    def piloto_show_report_status(self):
        data = self.db.piloto_report_resultados_por_status(self.current_original_id)
        cols = {"Status": "Status", "Quantidade": "Quantidade"}
        ReportWindow(self.root, "Piloto - Relatório: Resultados por Status", cols, data)
