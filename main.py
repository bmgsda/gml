import requests
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = 'https://localhost:8088/services/collector/event'
AUTH_HEADER = {'Authorization': 'Splunk d7ea56c0-afa2-403a-927c-fe3e0c8860eb'}

# keys = lista dos campos, values = lista dos valores de cada campo
# constroi json campos x valores
def build_json_data(keys, values):
   data = {}
   for i in range (0,len(keys)-1):
      data[keys[i]] = values[i]
   return data

# data = json campos x valores
# envia request post para o servidor do splunk, se sucesso, inseriu no splunk
def send_request_splunk(data):
   response = requests.post(URL, headers = AUTH_HEADER, json = {'event': data}, verify = False)
   if response.ok:
      print("Enviado log de " + data['nomeRobo'])
      return True
   else:
      print("Problema ao enviar log de " + data['nomeRobo'] + " - " + response.text)
      return False

# df = dataframe gerado pela leitura de uma planilha
# para cada linha da planilha, monta o json e enviar o log
def send_logs(df):
   keys = list(df)
   keys.pop(0)
   values_list = df.values.tolist()
   line_index = 0
   for values in values_list:
      values.pop(0)
      data = build_json_data(keys, values)
      response = send_request_splunk(data)
      if (response):
         df.ix[line_index, 'Status'] = 'OK'
      line_index =+ 1

# MAIN
# carrega as planilhas e transforma em dataframe
df_malha_batch = pd.read_excel('MalhaBatch.xlsx')
df_eventos = pd.read_excel('Eventos.xlsx')

# faz os envios
send_logs(df_malha_batch)
send_logs(df_eventos)

# atualiza o excel
df_malha_batch.to_excel('MalhaBatch.xlsx', index=False)
df_eventos.to_excel('Eventos', index=False)
