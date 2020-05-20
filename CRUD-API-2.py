from flask import Flask, request
import ConnectionManager as CM
import pandas as pd

app = Flask(__name__)

@app.route('/solicitarItem', methods = ['POST'])
def solicitarItem():
    try:
        data = request.get_json()
        instancia = int(data['instancia'])
        conn = CM.Connection()
        result = conn.execute_query(f"SELECT id_item FROM automation_items WHERE status = 'PENDENTE' AND fila = {instancia} LIMIT 1")
        if result.empty:
            return 'Fila vazia'
        item = result.iloc[0]['id_item']
        conn.execute_query(f"UPDATE automation_items SET status = 'ENVIADO' WHERE id_item = {item}")
        conn.connection.close()
        return str(item)
    except Exception as e:
        return str(e)

@app.route('/atualizarItem', methods = ['POST'])
def atualizarItem():
    try:
        data = request.get_json()
        item = int(data['item'])
        resultado = data['resultado']
        conn = CM.Connection()
        conn.execute_query(f"UPDATE automation_items SET status = 'PROCESSADO', resultado = '{resultado}' WHERE id_item = {item}")
        conn.connection.close()
        return "Atualização efetivada!"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)