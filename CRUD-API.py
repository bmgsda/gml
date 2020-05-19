from flask import Flask, request
import ConnectionManager as CM

app = Flask(__name__)

@app.route('/execute', methods = ['POST'])
def execute():
    data = request.get_json()
    qry = data['qry']
    conn = CM.Connection()
    result = conn.execute_query(qry)
    conn.connection.close()
    if (result == True):
        return 'Comando efetivado!'
    else:
        return str(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)