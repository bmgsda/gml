import ConnectionManager as CM
conn = CM.Connection()
for i in range(20):
    fila = (i%4) + 1
    qry = f"INSERT INTO automation_items VALUES (default, 'PENDENTE', {fila}, null)"
    conn.execute_query(qry)
    
conn.connection.close()