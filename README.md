#  Data Audit: Investimento em Defesa Civil e Infraestrutura (MG)

Este projeto realiza uma auditoria automatizada nos dados orçamentários do Estado de Minas Gerais, utilizando a API do Siconfi (Tesouro Nacional). O objetivo é confrontar narrativas sobre a alocação de recursos em prevenção de desastres e infraestrutura urbana.

##  Resumo da Investigação (Exercício 2023)
A análise técnica revelou uma dicotomia entre os valores empenhados (promessa/contrato) e os valores efetivamente pagos (entrega na ponta):

| Categoria | Empenhado (Contratado) | Pago (Liquidado) | Gap de Execução |
| :--- | :--- | :--- | :--- |
| **Defesa Civil** | R$ 903,3 Mi | R$ 804,1 Mi | ~11% |
| **Infraestrutura Urbana** | R$ 522,6 Mi | R$ 322,5 Mi | **~38%** |
| **Saneamento Rural** | R$ 23,0 Mi | R$ 7,7 Mi | **~66%** |

##  Stack Tecnológica
- **Python 3.x**: Motor de extração e transformação.
- **Pandas**: Pivotagem de dados e normalização de schemas.
- **API REST Siconfi**: Fonte primária de dados do Tesouro Nacional.

##  Insights Investigativos (Fact-Checking)
1. **Diferença entre Discurso e Entrega:** Enquanto a rubrica de **Defesa Civil** apresenta alta execução (89%), a área de **Infraestrutura Urbana** possui um gargalo de R$ 200 milhões não pagos, o que sustenta as críticas sobre a demora na entrega de obras preventivas.
2. **Cancelamentos e Restos a Pagar:** Identificou-se que o "investimento" anunciado pelo governo frequentemente refere-se ao empenho, enquanto a percepção social e da imprensa é pautada pelo pagamento final.
3. **Saneamento:** A baixa execução em saneamento rural (apenas 33%) aponta uma fragilidade crítica em áreas vulneráveis a desastres climáticos.

##  Como Executar
1. Instale as dependências: `pip install pandas requests`
2. Rode o script: `python main.py`
