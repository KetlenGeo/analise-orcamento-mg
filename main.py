import pandas as pd
import requests

pd.options.display.float_format = 'R$ {:,.2f}'.format

def auditoria_zema_vs_realidade(ano=2023):
    # ID de Minas Gerais no Siconfi para o Ente Estadual é '31'
    url = f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio={ano}&id_ente=31"
    
    try:
        response = requests.get(url, timeout=30)
        data = response.json().get('items', [])
        df = pd.DataFrame(data)
        df.columns = [col.lower() for col in df.columns]
        
        # Pivotando
        col_valor = 'vlr_conta' if 'vlr_conta' in df.columns else 'valor'
        df_pivot = df.pivot_table(index='conta', columns='coluna', values=col_valor, aggfunc='sum').reset_index()
        
        # Onde o investimento pode estar "escondido"?
        categorias_investigadas = [
            'Defesa Civil', 
            'Urbanismo', 
            'Transporte Rodoviário', # Reconstrução de estradas pós-chuva
            'Infraestrutura Urbana',
            'Saneamento',
            'Gestão Ambiental'
        ]
        
        mask = df_pivot['conta'].str.contains('|'.join(categorias_investigadas), case=False, na=False)
        df_analise = df_pivot[mask].copy()
        
        # Foco na "Despesa Paga" para ver o que saiu do caixa do Estado
        return df_analise[['conta', 'Despesas Empenhadas', 'Despesas Pagas']]
        
    except Exception as e:
        return f"Erro na análise: {e}"

df_mg = auditoria_zema_vs_realidade(2023)
print(df_mg)
