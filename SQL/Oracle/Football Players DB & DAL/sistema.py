import cx_Oracle

def conectar_banco():
    try:
        conn = cx_Oracle.connect(
            user="usuario",
            password="senha",
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

def error_handler(error_arg):
    error_obj = error_arg[0]
    match error_obj.code:
        ## Violação de pk/unique
        case 1: 
            if 'UQ_SECRETARIA' in error_obj.message:
                print("Erro: Diretor/Responsável já designado")
            elif 'UQ_MODALIDADE' in error_obj.message:
                print("Erro: Modalidade já existente")
            else:
                print("Erro: Cadastro já existente")

        ## Precisão ou numeros grandes demais
        case 1438: 
            print("Erro: Você está utilizando valores grandes demais, garanta que seus dados não excedam os limites explicitados e tente novamente")

        ## Strings grandes demais    
        case 12899: 
            print("Erro: Você está utilizando caracteres demais, garanta que seus dados não excedam os limites explicitados e tente novamente")

        ## Violação de checagem (cpf ou tipo)
        case 2290:
            if 'CK_TIPO' in error_obj.message:
                print("Erro: Tipo de funcionário inválido")
            else:
                print("Erro: Formato de CPF inválido")

        ## Violação de fk
        case 2291:
            if 'FK_MAIOR_PESSOA' in error_obj.message:
                print("Erro: O responsável do menor precisa estar cadastrado previamente no sistema")
            elif '_UNIDADE' in error_obj.message:
                print("Erro: A Secretaria de Esporte referente associada ao Municipio precisa estar cadastrada previamente no sistema")
            elif 'FK_SECRETARIA_DIRETOR' in error_obj.message:
                print("Erro: Diretor precisa estar cadastrado previamente no sistema")
            elif 'FK_MODALIDADE_RESPONSAVEL' in error_obj.message:
                print("Erro: Responsável precisa estar cadastrado previamente no sistema")
            else:
                print(error_obj.code)
                print(error_obj.message)
        case _:
            print("Erro desconhecido:")
            print(error_obj.code)
            print(error_obj.message)

        

def cadastrar_pessoa_e_endereco(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Pessoa ===")
        cpf = input("CPF (limite: 14 caracteres) (formato 000.000.000-00): ")
        data_nasc = input("Data de nascimento (formato DD-MM-AAAA): ")
        idade = int(input("Idade: (limite: 3 digitos)"))
        nome = input("Nome: ")
        peso = float(input("Peso (kg) (limite:3 digitos e 2 casas decimais): "))
        altura = int(input("Altura (cm) (limite:3 digitos): "))
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
        cep = input("CEP: (limite:10 caracteres)")
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
        error_handler(erro)
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
        error_handler(e.args)
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
        error_handler(e.args)
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
        error_handler(e.args)
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
        error_handler(e.args)
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

        ## Apenas para Responsável pois Personal depende de ter modalidade previamente cadastrada
        if tipo == 'RESPONSAVEL':
            print("=== Cadastro de Responsável ===")
            certificacao = input("Certifição do responsável :")
            anos_exp = input("Anos de Experiência (limite 2 dígitos) :")

            sql_insert_responsavel = """
            INSERT INTO RESPONSAVEL (CPF, CERTIFICACAO, ANOSEXP)
            VALUES (:cpf, :certificacao, :anosexp)
            """
            cursor.execute(sql_insert_responsavel, {
            "cpf": cpf,
            "certificacao": certificacao,
            "anosexp": anos_exp
            })
                     
        conn.commit()
        print("Cadastro de funcionário realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
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
        error_handler(e.args)
    finally:
        if cursor:
            cursor.close()

def cadastrar_secretaria(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Secretaria ===")
        municipio = input("Municipio: ")
        nome = input("Nome da Secretaria: ")
        diretor = input("CPF do diretor (limite 14 caracteres) (formato 000.000.000-00): ")

        sql_insert_secretaria = """
            INSERT INTO SECRETARIA_ESPORTE (MUNICIPIO, NOME, DIRETOR)
            VALUES (:municipio, :nome, :diretor)
            """
        cursor.execute(sql_insert_secretaria, {
                "municipio": municipio,
                "nome": nome,
                "diretor": diretor,
        })

        conn.commit()
        print("Cadastro de secretaria realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_secretaria(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Secretaria ===")
        municipio = input("Digite o Municipio da secretaria :").strip()

        sql_consulta_secretaria = """
            SELECT MUNICIPIO, NOME, DIRETOR
            FROM SECRETARIA_ESPORTE
            WHERE MUNICIPIO = :municipio
            """
        cursor.execute(sql_consulta_secretaria, {"municipio": municipio})
        resultado = cursor.fetchone()

        if resultado:
            print("\n=== Dados da Secretaria ===")
            print(f"Municipio: {resultado[0]}")
            print(f"Nome: {resultado[1]}")
            print(f"CPF do Diretor: {resultado[2]}")
        else:
            print("Secretaria não encontrada no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
    finally:
        if cursor:
            cursor.close()



def cadastrar_modalidade(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Modalidade ===")
        nome = input("Nome da Modalidade :")
        unidade = input("Unidade(Municipio) :")
        local = input("Local onde vai ser ministrada :")
        responsavel = input("CPF do funcionário responsável (limite 14 caracteres) (formato 000.000.000-00): ")
        menor = input("Aceita menores de idade? 0(N)/1(S): ")

        sql_insert_modalidade = """
            INSERT INTO MODALIDADE (NOME, UNIDADE, LOCAL, RESPONSAVEL, MENOR)
            VALUES (:nome, :unidade, :local, :responsavel, :menor)
            """
        cursor.execute(sql_insert_modalidade, {
                "nome": nome,
                "unidade": unidade,
                "local": local,
                "responsavel": responsavel,
                "menor": menor,
        })

        conn.commit()
        print("Cadastro de modalidade realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_modalidades(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Modalidades ===")
        municipio = input("Digite a Unidade(Municipio) :").strip()

        sql_consulta_modalidades = """
            SELECT NOME, LOCAL, RESPONSAVEL
            FROM MODALIDADE
            WHERE UNIDADE = :municipio
            """
        cursor.execute(sql_consulta_modalidades, {"municipio": municipio})
        resultados = cursor.fetchall()

        if resultados:
            for resultado in resultados:
                nome,local,responsavel = resultado
                print(f"Nome da modalidade: {nome}, Local: {local}, CPF do Responsável: {responsavel}")
        else:
            print("Nenhuma modalidade encontrada no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
    finally:
        if cursor:
            cursor.close()

def cadastrar_matricula(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Cadastro de Matricula ===")
        pessoa = input("CPF do cadastrado (limite 14 caracteres) (formato 000.000.000-00) :")
        modalidade = input("Modalidade :")
        unidade = input("Unidade(Municipio) :")
        data_hora = input("Data e hora (formato YYYY-MM-DD HH24:MI:SS) :")

        cursor.execute("SELECT IDADE FROM PESSOA WHERE CPF = :pessoa", pessoa=pessoa)
        p1 = cursor.fetchone()
        idade = p1[0]
        
        cursor.execute("SELECT MENOR FROM MODALIDADE WHERE NOME = :modalidade", modalidade=modalidade)
        m1 = cursor.fetchone()
        menor = m1[0]

        if (idade < 18) and (m1 != 1):
            print("Menor não pode ser cadastrado nessa modalidade")
        else:
            sql_insert_matricula = """
                INSERT INTO MATRICULA (PESSOA, MODALIDADE, UNIDADE, DATA_HORA)
                VALUES (:pessoa, :modalidade, :unidade, TO_TIMESTAMP(:data_hora , 'YYYY-MM-DD HH24:MI:SS'))
                """
            cursor.execute(sql_insert_matricula, {
                    "pessoa": pessoa,
                    "modalidade": modalidade,
                    "unidade": unidade,
                    "data_hora": data_hora,
            })

            conn.commit()
            print("Cadastro de matrícula realizado com sucesso!")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_matriculas_porpessoa(conn):
    try:
        if not verificar_conexao(conn):
            conn = conectar_banco()

        cursor = conn.cursor()

        print("=== Consulta de Matrículas ===")
        pessoa = input("CPF do matriculado (limite 14 caracteres) (formato 000.000.000-00) :").strip()

        sql_consulta_matriculas = """
        SELECT MODALIDADE,UNIDADE,DATA_HORA
        FROM MATRICULA
        WHERE PESSOA = :pessoa
        """
        cursor.execute(sql_consulta_matriculas, {"pessoa": pessoa})
        resultados = cursor.fetchall()

        if resultados:
            for resultado in resultados:
                modalidade,unidade,data_hora = resultado
                print(f"Nome da modalidade : {modalidade}, Unidade(Municipio) : {unidade}, Dia e horário : {data_hora}")
        else:
            print("Nenhuma matrícula encontrada para esta pessoa no banco de dados.")

    except cx_Oracle.DatabaseError as e:
        erro, = e.args
        error_handler(e.args)
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
        print("8. Cadastrar Secretaria")
        print("9. Buscar Secretaria")
        print("10. Cadastrar modalidade")
        print("11. Consultar modalidades disponíveis em uma unidade")
        print("12. Cadastrar matrícula")
        print("13. Consultar matrículas por pessoa")
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
        elif opcao == "8":
            cadastrar_secretaria(conn)
        elif opcao == "9":
            buscar_secretaria(conn)
        elif opcao == "10":
            cadastrar_modalidade(conn)
        elif opcao == "11":
            buscar_modalidades(conn)
        elif opcao == "12":
            cadastrar_matricula(conn)
        elif opcao == "13":
            buscar_matriculas_porpessoa(conn)
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()
    print("Conexão fechada")

if __name__ == "__main__":
    menu()
