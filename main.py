import pandas as pd
import requests
import logging

# Configurações de exibição e log
pd.options.display.float_format = 'R$ {:,.2f}'.format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_siconfi(ano, id_ente, nome_ente):
    """Extrai dados brutos do Siconfi (DCA) para um ente específico."""
    logging.info(f"Extraindo dados de {nome_ente} ({id_ente}) para o ano {ano}...")
    url = f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio={ano}&id_ente={id_ente}"
    
    try:
        response = requests.get(url, timeout=40)
        response.raise_for_status()
        items = response.json().get('items', [])
        if not items:
            return None
        df = pd.DataFrame(items)
        df.columns = [col.lower() for col in df.columns]
        return df
    except Exception as e:
        logging.error(f"Erro ao conectar com {nome_ente}: {e}")
        return None

def process_audit(df):
    """Transforma os dados brutos em uma tabela de auditoria comparativa."""
    if df is None: return None
    
    col_valor = 'vlr_conta' if 'vlr_conta' in df.columns else 'valor'
    
    # Pivotagem
    df_pivot = df.pivot_table(
        index='conta', 
        columns='coluna', 
        values=col_valor, 
        aggfunc='sum'
    ).reset_index()
    
    # Filtro focado em Defesa Civil e Infraestrutura
    termos = ['Defesa Civil', 'Urbanismo', 'Saneamento', 'Gestão Ambiental', 'Transporte Rodoviário']
    mask = df_pivot['conta'].str.contains('|'.join(termos), case=False, na=False)
    
    return df_pivot[mask].copy()

if __name__ == "__main__":
    ano_analise = 2023
    
    # 1. Auditoria Nível Estadual (Minas Gerais - ID 31)
    df_mg_raw = fetch_siconfi(ano_analise, "31", "Estado de Minas Gerais")
    df_mg_audit = process_audit(df_mg_raw)
    
    if df_mg_audit is not None:
        df_mg_audit.to_csv("auditoria_estado_mg.csv", index=False)
        logging.info("Arquivo auditoria_estado_mg.csv gerado.")

    # 2. Auditoria Nível Municipal (Juiz de Fora - ID 3136702)
    df_jf_raw = fetch_siconfi(ano_analise, "3136702", "Juiz de Fora")
    df_jf_audit = process_audit(df_jf_raw)
    
    if df_jf_audit is not None:
        df_jf_audit.to_csv("auditoria_municipio_jf.csv", index=False)
        logging.info("Arquivo auditoria_municipio_jf.csv gerado.")

    print("\n Processamento concluído! Verifique os arquivos CSV para a análise comparativa.")
