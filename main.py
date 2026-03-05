import pandas as pd
import requests
import logging

# Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_budget_data(city_code="3136702"): # Código IBGE para Juiz de Fora
    logging.info(f"Iniciando coleta de dados para o município: {city_code}")
    
    # API
    try:
        # Dataset
        data = {
            'ano': [2022, 2023, 2024, 2024],
            'rubrica': ['Defesa Civil', 'Obras de Contenção', 'Drenagem Urbana', 'Gestão de Riscos'],
            'valor_empenhado': [1500000.00, 2800000.50, 4200000.00, 950000.00],
            'valor_liquidado': [1200000.00, 2500000.00, 1800000.00, 900000.00]
        }
        return pd.DataFrame(data)
    except Exception as e:
        logging.error(f"Erro ao coletar dados: {e}")
        return None

def transform_data(df):
    if df is None: return None
    logging.info("Iniciando transformações e cálculos de KPIs.")
    
    # Cálculo de aproveitamento orçamentário
    df['percentual_executado'] = (df['valor_liquidado'] / df['valor_empenhado']) * 100
    
    # Normalização
    df['rubrica'] = df['rubrica'].str.upper()
    
    return df

def save_output(df, filename="orcamento_jf_processado.csv"):
    if df is not None:
        df.to_csv(filename, index=False)
        logging.info(f"Arquivo salvo com sucesso: {filename}")

if __name__ == "__main__":
    # Execução
    df_raw = fetch_budget_data()
    df_clean = transform_data(df_raw)
    save_output(df_clean)
