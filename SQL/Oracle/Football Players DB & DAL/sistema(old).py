import cx_Oracle

def conectar_banco():
    try:
        conn = cx_Oracle.connect(
            user="a9039361",
            password="6mm0BQvC9nm7xS",
            dsn="orclgrad1.icmc.usp.br:1521/pdb_elaine.icmc.usp.br"
        )
        print("Conexão com o banco estabelecida!")
        return conn
    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao conectar no banco de dados: {erro.message}")
        return None

def verificar_conexao(conn):
    try:
        if conn is None or conn.ping() is None:
            return False
        return True
    except cx_Oracle.DatabaseError:
        return False

def cadastrar_pessoa_e_endereco(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Pessoa ===")
        cpf = input("CPF (formato 000.000.000-00): ")
        data_nasc = input("Data de nascimento (DD-MM-AAAA): ")
        idade = int(input("Idade: "))
        nome = input("Nome: ")
        peso = float(input("Peso (kg): "))
        altura = int(input("Altura (cm): "))
        telefone = input("Telefone (opcional): ")

        sql_insert_pessoa = """
        INSERT INTO PESSOA (CPF, DATANASC, IDADE, NOME, PESO, ALTURA, TELEFONE)
        VALUES (:cpf, TO_DATE(:data_nasc, 'DD-MM-YYYY'), :idade, :nome, :peso, :altura, :telefone)
        """
        cursor.execute(sql_insert_pessoa, {
            "cpf": cpf,
            "data_nasc": data_nasc,
            "idade": idade,
            "nome": nome,
            "peso": peso,
            "altura": altura,
            "telefone": telefone or None
        })

        print("\n=== Cadastro de Endereço ===")
        cep = input("CEP: ")
        rua = input("Rua: ")
        numero = input("Número: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado (UF): ")

        sql_insert_endereco = """
        INSERT INTO ENDERECO (PESSOA, CEP, RUA, NUMERO, BAIRRO, CIDADE, ESTADO)
        VALUES (:cpf, :cep, :rua, :numero, :bairro, :cidade, :estado)
        """
        cursor.execute(sql_insert_endereco, {
            "cpf": cpf,
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        })

        print("\n=== Cadastro de Deficiências ===")
        possui_deficiencia = input("A pessoa possui deficiência? (S/N): ").strip().upper()
        while possui_deficiencia == "S":
            descricao_deficiencia = input("Descrição da deficiência: ")
            sql_insert_deficiencia = """
            INSERT INTO DEFICIENCIAS (PESSOA, DESCRICAO)
            VALUES (:cpf, :descricao)
            """
            cursor.execute(sql_insert_deficiencia, {
                "cpf": cpf,
                "descricao": descricao_deficiencia
            })
            possui_deficiencia = input("Deseja cadastrar outra deficiência? (S/N): ").strip().upper()

        if idade < 18:
            print("\n=== Cadastro de Responsável ===")
            cpf_responsavel = input("CPF do responsável (maior de idade, formato 000.000.000-00): ")
            sql_insert_maior = """
            INSERT INTO MAIOR_MENOR (CPF_MENOR, CPF_RESPONSAVEL)
            VALUES (:cpf, :cpf_responsavel)
            """
            cursor.execute(sql_insert_maior, {
                "cpf": cpf,
                "cpf_responsavel": cpf_responsavel
            })

        conn.commit()
        print("Cadastro de pessoa, endereço e deficiência realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao inserir dados: {erro.message}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_pessoa(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Pessoa ===")
        cpf = input("Digite o CPF da pessoa (formato 000.000.000-00): ")

        sql_consulta_pessoa = """
        SELECT NOME, DATANASC, IDADE, PESO, ALTURA, TELEFONE
        FROM PESSOA
        WHERE CPF = :cpf
        """
        cursor.execute(sql_consulta_pessoa, {"cpf": cpf})
        resultado = cursor.fetchone()

        if resultado:
            print("\n=== Dados da Pessoa ===")
            print(f"Nome: {resultado[0]}")
            print(f"Data de Nascimento: {resultado[1]}")
            print(f"Idade: {resultado[2]}")
            print(f"Peso: {resultado[3]}")
            print(f"Altura: {resultado[4]}")
            print(f"Telefone: {resultado[5]}")
        else:
            print("Pessoa não encontrada no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao consultar dados da pessoa: {erro.message}")
    finally:
        if cursor:
            cursor.close()

def buscar_endereco(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Endereço ===")
        cpf = input("Digite o CPF da pessoa (formato 000.000.000-00): ")

        sql_consulta_endereco = """
        SELECT CEP, RUA, NUMERO, BAIRRO, CIDADE, ESTADO
        FROM ENDERECO
        WHERE PESSOA = :cpf
        """
        cursor.execute(sql_consulta_endereco, {"cpf": cpf})
        resultado = cursor.fetchone()

        if resultado:
            print("\n=== Dados do Endereço ===")
            print(f"CEP: {resultado[0]}")
            print(f"Rua: {resultado[1]}")
            print(f"Número: {resultado[2]}")
            print(f"Bairro: {resultado[3]}")
            print(f"Cidade: {resultado[4]}")
            print(f"Estado: {resultado[5]}")
        else:
            print("Endereço não encontrado para o CPF informado.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao consultar dados do endereço: {erro.message}")
    finally:
        if cursor:
            cursor.close()

def cadastrar_diretor(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Diretor ===")
        cpf = input("CPF (formato 000.000.000-00): ")
        nome = input("Nome: ")
        data_nasc = input("Data de nascimento (DD-MM-AAAA): ")

        sql_insert_diretor = """
        INSERT INTO DIRETOR (CPF, NOME, DATANASC)
        VALUES (:cpf, :nome, TO_DATE(:data_nasc, 'DD-MM-YYYY'))
        """
        cursor.execute(sql_insert_diretor, {
            "cpf": cpf,
            "nome": nome,
            "data_nasc": data_nasc
        })

        conn.commit()
        print("Cadastro de diretor realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao inserir dados do diretor: {erro.message}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_diretor(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Diretor ===")
        cpf = input("Digite o CPF do diretor (formato 000.000.000-00): ")

        sql_consulta_diretor = """
        SELECT NOME, DATANASC
        FROM DIRETOR
        WHERE CPF = :cpf
        """
        cursor.execute(sql_consulta_diretor, {"cpf": cpf})
        resultado = cursor.fetchone()

        if resultado:
            print("\n=== Dados do Diretor ===")
            print(f"Nome: {resultado[0]}")
            print(f"Data de Nascimento: {resultado[1]}")
        else:
            print("Diretor não encontrado no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao consultar dados do diretor: {erro.message}")
    finally:
        if cursor:
            cursor.close()

def cadastrar_funcionario(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Funcionário ===")
        cpf = input("CPF (formato 000.000.000-00): ")
        nome = input("Nome: ")
        data_nasc = input("Data de nascimento (DD-MM-AAAA): ")
        tipo = input("Tipo (RESPONSAVEL ou PERSONAL): ").upper()
        unidade = input("Unidade (Cidade): ")

        sql_insert_funcionario = """
        INSERT INTO FUNCIONARIO (CPF, NOME, DATANASC, TIPO, UNIDADE)
        VALUES (:cpf, :nome, TO_DATE(:data_nasc, 'DD-MM-YYYY'), :tipo, :unidade)
        """
        cursor.execute(sql_insert_funcionario, {
            "cpf": cpf,
            "nome": nome,
            "data_nasc": data_nasc,
            "tipo": tipo,
            "unidade": unidade
        })

        conn.commit()
        print("Cadastro de funcionário realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao inserir dados do funcionário: {erro.message}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_funcionario(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Funcionário ===")
        cpf = input("Digite o CPF do funcionário (formato 000.000.000-00): ")

        sql_consulta_funcionario = """
        SELECT NOME, DATANASC, TIPO, UNIDADE
        FROM FUNCIONARIO
        WHERE CPF = :cpf
        """
        cursor.execute(sql_consulta_funcionario, {"cpf": cpf})
        resultado = cursor.fetchone()

        if resultado:
            print("\n=== Dados do Funcionário ===")
            print(f"Nome: {resultado[0]}")
            print(f"Data de Nascimento: {resultado[1]}")
            print(f"Tipo: {resultado[2]}")
            print(f"Unidade: {resultado[3]}")
        else:
            print("Funcionário não encontrado no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        print(f"Erro ao consultar dados do funcionário: {erro.message}")
    finally:
        if cursor:
            cursor.close()
def menu():
    conn = conectar_banco()
    if conn is None:
        return

    while True:
        print("\n=== Menu ===")
        print("1. Cadastrar Pessoa, Endereço e Deficiência")
        print("2. Consultar Dados da Pessoa")
        print("3. Consultar Endereço da Pessoa")
        print("4. Cadastrar Diretor")
        print("5. Consultar Diretor")
        print("6. Cadastrar Funcionário")
        print("7. Consultar Funcionário")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_pessoa_e_endereco(conn)
        elif opcao == "2":
            buscar_pessoa(conn)
        elif opcao == "3":
            buscar_endereco(conn)
        elif opcao == "4":
            cadastrar_diretor(conn)
        elif opcao == "5":
            buscar_diretor(conn)
        elif opcao == "6":
            cadastrar_funcionario(conn)
        elif opcao == "7":
            buscar_funcionario(conn)
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

if __name__ == "__main__":
    menu()
