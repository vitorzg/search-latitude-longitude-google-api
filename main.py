import os
import pandas as pd
import requests

def get_lat_long(api_key, query):

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        'query': query,
        'key': api_key
    }

    # Fazer a solicitação à API
    response = requests.get(url, params=params)
    data = response.json()

    # Verificar se houve sucesso na busca
    if data['status'] == 'OK':
        # Obter o primeiro resultado da lista
        result = data['results'][0]
        # Extrair latitude e longitude
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        return lat, lng
    else:
        print("Erro na busca:", data['status'])
        return None

def main():
    # Substitua pela sua chave de API do Google Maps
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    
    # Ler o arquivo .xlsx
    file_path = 'planilha.xlsx'  # Substitua pelo nome do seu arquivo
    df = pd.read_excel(file_path)

    # Verificar se as colunas existem
    if 'NOME' not in df.columns or 'MUNICIPIO' not in df.columns:
        print("As colunas 'NOME' e 'MUNICIPIO' não foram encontradas.")
        return

    results = []

    # Iterar pelas linhas do DataFrame
    for _, row in df.iterrows():
        query = f"{row['NOME']} - {row['MUNICIPIO']}"
        coordinates = get_lat_long(api_key, query)
        if coordinates:
            result_line = f"{query}: Latitude: {coordinates[0]}, Longitude: {coordinates[1]}"
            results.append(result_line)

    # Salvar os resultados em um arquivo .txt
    with open('resultados.txt', 'w') as file:
        for line in results:
            file.write(line + '\n')

    print("Resultados salvos em 'resultados.txt'.")

if __name__ == "__main__":
    main()
