# Séries Temporais: Resumo Completo

## 1. Definição

Uma série temporal é uma sequência de dados ou observações registradas em momentos consecutivos no tempo, geralmente em intervalos regulares, que refletem a evolução de uma variável ao longo do tempo. Ela permite analisar padrões, tendências, ciclos e sazonalidades para entender o comportamento passado e fazer previsões futuras.

### Exemplos:

- Vendas diárias de uma loja.
- Temperatura média mensal de uma cidade.
- Cotação diária de ações na bolsa.

## 2. Estrutura

- **Observações (yt)**: Valores medidos em momentos t.
- **Tempo (t)**: Pode ser diário, semanal, mensal, anual ou em intervalos irregulares.

## 3. Utilidade e Quando Usar Séries Temporais

Séries temporais são úteis em cenários onde os dados variam ao longo do tempo e existe a necessidade de entender padrões, realizar análises ou prever eventos futuros. Elas são empregadas em diversas áreas devido à sua capacidade de capturar tendências, sazonalidades e dependências temporais.

A análise de séries temporais é essencial para:

- **Previsão:** Permite estimar valores futuros com base em dados históricos, sendo útil para demandas de estoque, vendas, produção de energia e preços de mercado.
- **Identificação de padrões:** Identifica tendências, sazonalidades e ciclos, auxiliando no entendimento de variações de vendas, padrões climáticos e comportamento do consumidor.
- **Monitoramento:** Detecta anomalias em tempo real, como falhas em máquinas, fraudes financeiras e variações no tráfego de redes.
- **Tomada de decisão estratégica:** Informações ajudam no planejamento de campanhas, precificação dinâmica e infraestrutura urbana.
- **Otimização:** Permite ajustar processos automaticamente, como controlar a produção industrial, gerenciar o consumo de energia e otimizar transportes públicos.

## 4. Componentes de Séries Temporais

As séries temporais podem ser decompostas em quatro componentes principais:

1. **Tendência (Trend):** Representa o movimento de longo prazo na série. Exemplo: Crescimento consistente no número de vendas ao longo dos anos.
2. **Sazonalidade (Seasonality):** Padrões que se repetem em intervalos regulares de tempo. Exemplo: Aumento de vendas no Natal.
3. **Ciclo (Cycle):** Flutuações que ocorrem devido a fatores econômicos ou outros ciclos (não tem a ver com o tempo). Exemplo: Alta e baixa de um mercado financeiro em períodos não fixos.
4. **Resíduo (Noise):** Variação aleatória ou irrelevante na série. Exemplo: Pequenas flutuações inesperadas em vendas diárias.

## 5. Tipos de Séries Temporais

1. **Univariada:** Contém apenas uma variável observada ao longo do tempo. O foco é entender e prever essa única variável com base em seus próprios valores passados. Exemplo: Preço diário de uma ação, temperatura média mensal, vendas de um produto ao longo do ano.
2. **Multivariada:** Envolve múltiplas variáveis inter-relacionadas, analisadas simultaneamente. Essas variáveis podem influenciar umas às outras, tornando a modelagem mais complexa. Exemplo: Preço de uma ação considerando também taxas de juros e volume de negociação, previsão de demanda levando em conta fatores climáticos e promoções.

## 6. Estacionaridade

Um conjunto de dados estacionário é aquele cujas propriedades estatísticas não mudam ao longo do tempo. Isso significa que a média, a variância e a autocovariância do processo são constantes. Em outras palavras, uma série temporal estacionária não apresenta tendências ou sazonalidades de longo prazo, tornando-a mais previsível e mais fácil de modelar.

## 7. Modelos e Técnicas de Análise

### Modelos Estatísticos

1. **Média Móvel (Moving Average):** A Média Móvel suaviza flutuações em uma série temporal, facilitando a identificação de tendências. Ela calcula a média de um número fixo de valores anteriores, eliminando variações aleatórias.

2. **ARIMA (AutoRegressive Integrated Moving Average):**
   O modelo ARIMA combina três componentes principais para modelar séries temporais:

- **AR (AutoRegressive):** Usa valores passados da própria série para prever futuros.
- **I (Integrated):** Aplica diferenciação para tornar a série estacionária.
- **MA (Moving Average):** Modela os erros da previsão baseando-se em valores passados.

O ARIMA é indicado para séries temporais estacionárias ou que podem ser transformadas em estacionárias. Ele é representado como **ARIMA(p, d, q)**, onde:

- **p** = Número de defasagens na parte autoregressiva.
- **d** = Número de diferenciações para tornar a série estacionária.
- **q** = Número de termos de média móvel.
  _Exemplo de Aplicação:_ Previsão de demanda por produtos ou previsão de inflação.

3. **SARIMA (Seasonal ARIMA):**
   O **SARIMA** é uma extensão do ARIMA que incorpora sazonalidade, ou seja, padrões que se repetem periodicamente. Ele adiciona quatro novos parâmetros para capturar variações sazonais:

- **P** = Ordem da parte autoregressiva sazonal.
- **D** = Diferenciação sazonal necessária.
- **Q** = Ordem da média móvel sazonal.
- **S** = Período da sazonalidade (exemplo: 12 para dados mensais).

O modelo é representado como **SARIMA(p, d, q) × (P, D, Q, S)**.
_Exemplo de Aplicação:_ Previsão de vendas sazonais, como consumo de energia elétrica ao longo do ano.

## 8. Etapas Práticas para Análise de Séries Temporais

### Etapa 1: Importar e Visualizar os Dados

A visualização de dados é uma etapa essencial, pois permite identificar padrões, tendências, sazonalidade e anomalias antes da modelagem.

- **Gráfico de Linha:** A forma mais comum de visualização. Ajuda a detectar tendências e padrões sazonais.
- **Histogramas e Boxplots:** Úteis para analisar a distribuição dos dados e identificar outliers.
- **Autocorrelação (ACF) e Parcial (PACF):** Mostram como os valores passados influenciam os futuros, auxiliando na escolha de modelos.
- **Decomposição:** Separa os componentes da série em tendência, sazonalidade e resíduo.
- **Heatmaps e Gráficos de Dispersão:** Para visualizar padrões sazonais ou relações entre variáveis multivariadas.

### Etapa 2: Analisar a Estacionaridade

**Visualização Gráfica:**

- Gráfico de Linha (busca de padrões óbvios).
- Rolling Statistics (média e variância em janelas móveis).

**Testes Estatísticos:**

- **Teste de Dickey-Fuller Aumentado (ADF):** H0 (não estacionária). H1 (estacionária). Se p-valor < 0,05, a série é estacionária.
- **Teste KPSS:** H0 (estacionária). H1 (não estacionária). Se p-valor < 0,05, a série não é estacionária.
- **Teste de Phillips-Perron (PP):** Similar ao ADF, mas mais robusto a heterocedasticidade.
- **ACF e PACF:** Se decai lentamente, pode ser não estacionária.

**Como Tornar uma Série Estacionária?**

- **Diferenciação:** Subtrair o valor anterior do atual ($Y_t - Y_{t-1}$).
- **Transformação Logarítmica:** ($\log Y_t$) para estabilizar a variância.
- **Diferenciação Sazonal:** Subtrair valores do mesmo período anterior ($Y_t - Y_{t-S}$).
- **Remover Tendência via Regressão:** Ajustar e remover uma tendência linear ou polinomial.

> **Nota:** $Y_t$ representa o valor observado no tempo $t$. $S$ representa o número de períodos da sazonalidade.

### Etapa 3: Decomposição

1. **Decomposição Aditiva:**
   $$ Y_t = Trend_t + Seasonal_t + Residual_t $$
   Usada quando a **amplitude da sazonalidade é constante**. Ex: Temperatura média diária.

2. **Decomposição Multiplicativa:**
   $$ Y_t = Trend_t \times Seasonal_t \times Residual_t $$
   Aplicada quando a **sazonalidade varia em intensidade**. Ex: Receita de uma empresa em forte crescimento.

### Etapa 4: Modelagem

Escolher e ajustar o modelo apropriado (ARIMA, SARIMA, LSTM, Prophet, etc.).

### Etapa 5: Avaliação (Divisão de Dados e Métricas)

A separação dos dados deve ser feita de forma **sequencial** (ordem cronológica), diferente do ML tradicional.

- **Conjunto de Treino:** Parte inicial dos dados.
- **Conjunto de Teste:** Últimos períodos da série.

**Métricas mais utilizadas:**

1. **RMSE (Root Mean Squared Error):** Mede a diferença média entre valores reais e previstos, penalizando mais os erros grandes. Valores menores indicam precisão maior.
2. **MAE (Mean Absolute Error):** Mede a média dos erros absolutos. Fácil de interpretar por estar na mesma unidade dos dados. Não amplifica erros grandes.
3. **MAPE (Mean Absolute Percentage Error):** Expressa o erro médio em termos percentuais. Útil para comparar previsões em diferentes escalas, mas problemático quando o valor real se aproxima de zero.

## 9. Desafios em Séries Temporais

1. **Não-estacionaridade:** Séries com média ou variância variando ao longo do tempo. (Solução: Diferenciação, logaritmos).
2. **Dados Perdidos (Missing Data):** Podem prejudicar a análise. (Solução: Interpolação ou preenchimento com estimativas).
3. **Séries Curtas:** Poucos dados dificultam identificar padrões. (Solução: Adicionar variáveis externas ou usar modelos mais simples).
4. **Sazonalidades Complexas:** Séries com múltiplos padrões sazonais (ex: diário e semanal) podem ser difíceis de modelar.
