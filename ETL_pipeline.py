import pandas as pd
import requests
import json
import csv

ibge_paises_api_url = "http://servicodados.ibge.gov.br/api/v1/paises"


## Extract
df = pd.read_csv('data.csv')
sigla_paises = df["pais"].tolist()

def get_mercosul(sigla):
    response = requests.get(f"{ibge_paises_api_url}/{sigla}")
    return response.json() if response.status_code == 200 else None

paises = [pais for sigla in sigla_paises if (pais := get_mercosul(sigla)) is not None]


## Transform
def transform_data(pais):
    nome_abreviado = pais["nome"]["abreviado"]
    moeda = pais["unidades-monetarias"][0]["nome"]
    area_total = pais["area"]["total"]
    unidade_area = pais["area"]["unidade"]["nome"]
    linguas = ", ".join([lang["nome"] for lang in pais["linguas"]])
    regiao = pais["localizacao"]["regiao"]["nome"]
    sub_regiao = pais["localizacao"]["sub-regiao"]["nome"]
    
    transformed_dict = {
        'nome_abreviado': nome_abreviado,
        'moeda': moeda,
        'area_total': area_total,
        'unidade_area': unidade_area,
        'linguas': linguas,
        'regiao': regiao,
        'sub_regiao': sub_regiao,
    }
    return transformed_dict

transformed_paises = [transform_data(pais[0]) for pais in paises]


## Load
def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['pais', 'moeda', 'area', 'linguas', 'regiao', 'sub_regiao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow({
                'pais': row['nome_abreviado'],
                'moeda': row['moeda'],
                'area': row['area_total'],
                'linguas': row['linguas'],
                'regiao': row['regiao'],
                'sub_regiao': row['sub_regiao'],
            })

csv_file_path = "paises_mercosul.csv"
save_to_csv(transformed_paises, csv_file_path)