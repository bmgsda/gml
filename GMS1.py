import ConnectionManager as CM
import pandas as pd
import time

conn_des = CM.Connection('TB5_DESENV')
conn_prod = CM.Connection('TB5_PROD')

def show_menu():
    print("""Escolher opção:
1 - Mostrar produtos
2 - Mostrar macroprocessos
3 - Mostrar microprocessos
4 - Mostrar apps
5 - Mostrar robôs
6 - Mostrar domínios dos robôs
7 - Cadastrar produto
8 - Cadastrar macroprocesso
9 - Cadastrar microprocesso
10 - Cadastrar app
11 - Cadastrar robô
12 - Cadastrar domínio de robô
13 - Remover produto
14 - Remover macroprocesso
15 - Remover microprocesso
16 - Remover robô
17 - Remover domínio de robô
0 - Sair
""")

def show_table(table):
    if table == 'TBTB5_GMS_ROBODOMINIO':
        query = """SELECT D.idDominio, R.idRobo, R.nomeRobo, P.nomeProduto, MA.nomeMacroprocesso, MI.nomeMicroprocesso
                   FROM TBTB5_GMS_ROBO AS R INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.FK_idRobo
                   INNER JOIN TBTB5_GMS_PRODUTO AS P ON D.Fk_idProduto = P.idProduto
                   INNER JOIN TBTB5_GMS_MACROPROCESSO AS MA ON D.Fk_idMacroprocesso = MA.idMacroprocesso
                   INNER JOIN TBTB5_GMS_MICROPROCESSO AS MI ON D.Fk_idMicroprocesso = MI.idMicroprocesso"""
    else:
        query = f'SELECT * FROM {table}'
    result_prod = conn_prod.execute_query(query)
    print(result_prod)

def get_greater_pk(table, pk):
    query = f'SELECT TOP 1 {pk} FROM {table} ORDER BY {pk} DESC'
    result = conn_prod.execute_query(query)
    greater_pk = result.iloc[0]['id_item']
    return greater_pk

def confirm_execution(query):
    print("A executar: " + query)
    confirm = input('Confirma? (Y/N): ')
    if confirm == 'Y' or confirm == 'y':
        return True
    elif confirm == 'N' or confirm == 'n':
        return False
    else:
        return confirm_execution(query)

def register_PRODUTO():
    id_pk = get_greater_pk('TBTB5_GMS_PRODUTO', 'idProduto') + 1
    nomeProduto = input("Digite o nome do novo produto: ")
    query = f"INSERT INTO TBTB5_GMS_PRODUTO VALUES ({id_pk},'{nomeProduto}')"
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('PRODUTO INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('PRODUTO INSERIDO EM PROD')

def register_MACROPROCESSO():
    id_pk = get_greater_pk('TBTB5_GMS_MACROPROCESSO', 'idMacroprocesso') + 1
    nomeMacroprocesso = input("Digite o nome do novo macroprocesso: ")
    query = f"INSERT INTO TBTB5_GMS_MACROPROCESSO VALUES ({id_pk},'{nomeMacroprocesso}')"
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('MACROPROCESSO INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('MACROPROCESSO INSERIDO EM PROD')

def register_MICROPROCESSO():
    id_pk = get_greater_pk('TBTB5_GMS_MICROPROCESSO', 'idMicroprocesso') + 1
    nomeMicroprocesso = input("Digite o nome do novo microprocesso: ")
    query = f"INSERT INTO TBTB5_GMS_MICROPROCESSO VALUES ({id_pk},'{nomeMicroprocesso}')"
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('MICROPROCESSO INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('MICROPROCESSO INSERIDO EM PROD')

def register_APP():
    id_pk = get_greater_pk('TBTB5_GMS_APP', 'idApp') + 1
    nomeApp = input("Digite o nome do novo app: ")
    query = f"INSERT INTO TBTB5_GMS_APP VALUES ({id_pk},'{nomeApp}')"
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('APP INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('APP INSERIDO EM PROD')

def register_ROBO():
    idRobo = int(input("Digite o ID do robô: "))
    result = conn_prod.execute_query(f"SELECT idRobo FROM TBTB5_GMS_ROBO WHERE status = {idRobo}")
    if not result.empty:
        print('Robô já existente')
        return
    nomeRobo = input("Digite o nome do robô: ")
    id_batch = int(input("Digite o tipo de execução (1 - BATCH, 2 - ONLINE): "))
    query = f"INSERT INTO TBTB5_GMS_ROBO VALUES ({idRobo},'{nomeRobo}', 23, 'DOC', 'SUP OPER CIV', 'GER OPER CONTROLE CIV', {id_batch})"
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('ROBO INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('ROBO INSERIDO EM PROD')

def register_ROBODOMINIO():
    idRobo = int(input("Digite o ID do robô: "))
    result = conn_prod.execute_query(f"SELECT idRobo FROM TBTB5_GMS_ROBO WHERE status = {idRobo}")
    if result.empty:
        print('Robô não existente')
        return
    result = conn_prod.execute_query(f"SELECT TOP 1 idDominio FROM TBTB5_GMS_ROBODOMINIO WHERE FK_idRobo = {idRobo} ORDER BY idDominio DESC")
    if result.empty:
        idDominio = 1
    else:
        idDominio = result.iloc[0]['idDominio'] + 1
    print(f'Registrando Domínio {idDominio} para o robô {idRobo}\n')
    show_table('TBTB5_GMS_PRODUTO')
    idProduto = int(input("Digite o id do PRODUTO: "))
    show_table('TBTB5_GMS_MACROPROCESSO')
    idMacroprocesso = int(input("Digite o id do MACROPROCESSO: "))
    show_table('TBTB5_GMS_MICROPROCESSO')
    idMicroprocesso = int(input("Digite o id do MICROPROCESSO: "))
    query = f"INSERT INTO TBTB5_GMS_ROBODOMINIO VALUES ({idDominio},{idRobo},{idProduto},{idMacroprocesso},{idMicroprocesso})"
    if(confirm_insert(query)):
        conn_des.execute_query(query)
        print('DOMINIO INSERIDO EM DESENV')
        conn_prod.execute_query(query)
        print('DOMINIO INSERIDO EM PROD')

def remove_PRODUTO():
    show_table('TBTB5_GMS_PRODUTO')
    idProduto = int(input('Digite o id do Produto: '))
    result = conn_prod.execute_query(f"""SELECT R.nomeRobo FROM TBTB5_GMS_ROBO AS R
                                         INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.Fk_IdRobo
                                         INNER JOIN TBTB5_GMS_PRODUTO AS P ON P.idProduto = D.Fk_IdProduto
                                         WHERE P.idProduto = {idProduto}""")
    if not result.empty:
        print('O produto está amarrado com os seguintes robôs:')
        print(result)
        return
    query = f'DELETE FROM TBTB5_GMS_PRODUTO WHERE idProduto = {idProduto}'
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('PRODUTO REMOVIDO EM DESENV')
        conn_prod.execute_query(query)
        print('PRODUTO REMOVIDO EM PROD')

def remove_MACROPROCESSO():
    show_table('TBTB5_GMS_MACROPROCESSO')
    idMacroprocesso = int(input('Digite o id do Macroprocesso: '))
    result = conn_prod.execute_query(f"""SELECT R.nomeRobo FROM TBTB5_GMS_ROBO AS R
                                         INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.Fk_IdRobo
                                         INNER JOIN TBTB5_GMS_MACROPROCESSO AS MA ON MA.idMacroprocesso = D.Fk_idMacroprocesso
                                         WHERE MA.idMacroprocesso = {idMacroprocesso}""")
    if not result.empty:
        print('O macroprocesso está amarrado com os seguintes robôs:')
        print(result)
        return
    query = f'DELETE FROM TBTB5_GMS_MACROPROCESSO WHERE idMacroprocesso = {idMacroprocesso}'
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('MACROPROCESSO REMOVIDO EM DESENV')
        conn_prod.execute_query(query)
        print('MACROPROCESSO REMOVIDO EM PROD')

def remove_MICROPROCESSO():
    show_table('TBTB5_GMS_MICROPROCESSO')
    idMicroprocesso = int(input('Digite o id do Microprocesso: '))
    result = conn_prod.execute_query(f"""SELECT R.nomeRobo FROM TBTB5_GMS_ROBO AS R
                                         INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.Fk_IdRobo
                                         INNER JOIN TBTB5_GMS_MICROPROCESSO AS MI ON MI.idMicroprocesso = D.Fk_idMicroprocesso
                                         WHERE MI.idMicroprocesso = {idMicroprocesso}""")
    if not result.empty:
        print('O microprocesso está amarrado com os seguintes robôs:')
        print(result)
        return
    query = f'DELETE FROM TBTB5_GMS_MICROPROCESSO WHERE idMicroprocesso = {idMicroprocesso}'
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('MICROPROCESSO REMOVIDO EM DESENV')
        conn_prod.execute_query(query)
        print('MICROPROCESSO REMOVIDO EM PROD')

def remove_ROBO():
    show_table('TBTB5_GMS_ROBO')
    idRobo = int(input('Digite o id do Robo: '))
    result = conn_prod.execute_query(f"""SELECT D.idDominio, P.nomeProduto, MA.nomeMacroprocesso, MI.nomeMicroprocesso FROM TBTB5_GMS_ROBO AS R
                                         INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.Fk_IdRobo
                                         INNER JOIN TBTB5_GMS_PRODUTO AS P ON D.Fk_idProduto = P.idProduto
                                         INNER JOIN TBTB5_GMS_MACROPROCESSO AS MA ON D.Fk_idMacroprocesso = MA.idMacroprocesso
                                         INNER JOIN TBTB5_GMS_MICROPROCESSO AS MI ON D.Fk_idMicroprocesso = MI.idMicroprocesso
                                         WHERE R.idRobo = {idRobo}""")
    if not result.empty:
        print('O robô está amarrado com os seguintes domínios:')
        print(result)
    query = f'DELETE FROM TBTB5_GMS_RODODOMINIO WHERE fk_idRobo = {idRobo}; DELETE FROM TBTB5_GMS_ROBO WHERE idRobo = {idRobo}'
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('ROBÔ REMOVIDO EM DESENV')
        conn_prod.execute_query(query)
        print('ROBÔ REMOVIDO EM PROD')
    
def remove_ROBODOMINIO():
    show_table('TBTB5_GMS_ROBO')
    idRobo = int(input('Digite o id do Robo: '))
    result = conn_prod.execute_query(f"""SELECT D.idDominio, P.nomeProduto, MA.nomeMacroprocesso, MI.nomeMicroprocesso FROM TBTB5_GMS_ROBO AS R
                                         INNER JOIN TBTB5_GMS_ROBODOMINIO AS D ON R.idRobo = D.Fk_IdRobo
                                         INNER JOIN TBTB5_GMS_PRODUTO AS P ON D.Fk_idProduto = P.idProduto
                                         INNER JOIN TBTB5_GMS_MACROPROCESSO AS MA ON D.Fk_idMacroprocesso = MA.idMacroprocesso
                                         INNER JOIN TBTB5_GMS_MICROPROCESSO AS MI ON D.Fk_idMicroprocesso = MI.idMicroprocesso
                                         WHERE R.idRobo = {idRobo}""")
    if result.empty:
        print('O robô não possui domínios!')
        return
    else:
        print(result)
    idDominio = int(input('Digite o id do Domínio: '))
    query = f'DELETE FROM TBTB5_GMS_RODODOMINIO WHERE fk_idRobo = {idRobo} AND idDominio = {idDominio}'
    if(confirm_execution(query)):
        conn_des.execute_query(query)
        print('DOMÍNIO REMOVIDO EM DESENV')
        conn_prod.execute_query(query)
        print('DOMÍNIO REMOVIDO EM PROD')

while(True):
    show_menu()
    try:
        choice = int(input('Selecionar a opção:'))
        if(choice > 17 or choice < 0):
            raise Exception('')
    except:
        print('Opção inválida')
        continue
    try:
        if choice == 0:
            conn_des.close()
            conn_prod.close()
            break
        elif choice == 1:
            show_table('TBTB5_GMS_PRODUTO')
        elif choice == 2:
            show_table('TBTB5_GMS_MACROPROCESSO')
        elif choice == 3:
            show_table('TBTB5_GMS_MICROPROCESSO')
        elif choice == 4:
            show_table('TBTB5_GMS_APP')
        elif choice == 5:
            show_table('TBTB5_GMS_ROBO')
        elif choice == 6:
            show_table('TBTB5_GMS_ROBODOMINIO')
        elif choice == 7:
            register_PRODUTO()
        elif choice == 8:
            register_MACROPROCESSO()
        elif choice == 9:
            register_MICROPROCESSO()
        elif choice == 10:
            register_APP()
        elif choice == 11:
            register_ROBO()
        elif choice == 12:
            register_ROBODOMINIO()
        elif choice == 13:
            remove_PRODUTO()
        elif choice == 14:
            remove_MACROPROCESSO()
        elif choice == 15:
            remove_MICROPROCESSO()
        elif choice == 16:
            remove_ROBO()
        elif choice == 17:
            remove_ROBODOMINIO()
        time.sleep(2)
    except Exception as e:
        print(e)
        continue