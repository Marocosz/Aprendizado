**Séries Temporais**

**Definição**

Uma série temporal é uma sequência de observações registradas em momentos específicos no tempo.  
Exemplo: vendas diárias de um produto, temperaturas mensais ou valores de ações ao longo de semanas.

**Estrutura**

**Observações (yt​​)**: Valores medidos em momentos t.

**Tempo (t)**: Pode ser diário, semanal, mensal, anual ou em intervalos irregulares.

**Utilidade e Quando Usar Séries Temporais**

Séries temporais são úteis em cenários onde os dados variam ao longo do tempo e existe a necessidade de entender padrões, realizar análises ou prever eventos futuros. Elas são empregadas em diversas áreas devido à sua capacidade de capturar tendências, sazonalidades e dependências temporais.

A análise de séries temporais é essencial para previsão, identificação de padrões, monitoramento, tomada de decisão estratégica e otimização de processos.

A previsão permite estimar valores futuros com base em dados históricos, sendo útil para demandas de estoque, vendas, produção de energia e preços de mercado. Já a análise de padrões identifica tendências, sazonalidades e ciclos, auxiliando no entendimento de variações de vendas, padrões climáticos e comportamento do consumidor.

O monitoramento detecta anomalias em tempo real, como falhas em máquinas, fraudes financeiras e variações no tráfego de redes. Na tomada de decisão estratégica, essas informações ajudam no planejamento de campanhas, precificação dinâmica e infraestrutura urbana.

Por fim, a otimização permite ajustar processos automaticamente, como controlar a produção industrial, gerenciar o consumo de energia e otimizar transportes públicos.

**Componentes de Séries Temporais**

As séries temporais podem ser decompostas em quatro componentes principais:

**1\. Tendência (Trend)**

Representa o movimento de longo prazo na série. Exemplo: Crescimento consistente no número de vendas ao longo dos anos.

**2\. Sazonalidade (Seasonality)**

Padrões que se repetem em intervalos regulares de tempo. Exemplo: Aumento de vendas no Natal.

**3\. Ciclo (Cycle)**

Flutuações que ocorrem devido a fatores econômicos ou outros ciclos (não tem a ver com o tempo). Exemplo: Alta e baixa de um mercado financeiro em períodos não fixos.

**4\. Resíduo (Noise)**

Variação aleatória ou irrelevante na série. Exemplo: Pequenas flutuações inesperadas em vendas diárias.

**Tipos de Séries Temporais**

1. **Univariada**

Contém apenas uma variável observada ao longo do tempo. O foco é entender e prever essa única variável com base em seus próprios valores passados. Exemplo: Preço diário de uma ação, temperatura média mensal, vendas de um produto ao longo do ano.

1. **Multivariada**

Envolve múltiplas variáveis inter-relacionadas, analisadas simultaneamente. Essas variáveis podem influenciar umas às outras, tornando a modelagem mais complexa. Exemplo: Preço de uma ação considerando também taxas de juros e volume de negociação, previsão de demanda levando em conta fatores climáticos e promoções.

**Estacionaridade**

Um conjunto de dados estacionário é aquele cujas propriedades estatísticas não mudam ao longo do tempo. Isso significa que a média, a variância e a auto covariância do processo são constantes. Em outras palavras, uma série temporal estacionária não apresenta tendências ou sazonalidades de longo prazo, tornando-a mais previsível e mais fácil de modelar.

**Modelos e Técnicas de Análise**

**Modelos Estatísticos**

1. **Média Móvel (Moving Average)**

A Média Móvel suaviza flutuações em uma série temporal, facilitando a identificação de tendências. Ela calcula a média de um número fixo de valores anteriores, eliminando variações aleatórias.

1. **ARIMA (AutoRegressive Integrated Moving Average)**

O modelo ARIMA combina três componentes principais para modelar séries temporais:

**AR (AutoRegressive)**: Usa valores passados da própria série para prever futuros.

**I (Integrated)**: Aplica diferenciação para tornar a série estacionária.

**MA (Moving Average)**: Modela os erros da previsão baseando-se em valores passados.

O ARIMA é indicado para séries temporais estacionárias ou que podem ser transformadas em estacionárias. Ele é representado como **ARIMA(p, d, q)**, onde:

**p** = Número de defasagens na parte autoregressiva.

**d** = Número de diferenciações para tornar a série estacionária.

**q** = Número de termos de média móvel.

**Exemplo de Aplicação**: Previsão de demanda por produtos ou previsão de inflação.

1. **SARIMA (Seasonal ARIMA)**

O **SARIMA** é uma extensão do ARIMA que incorpora sazonalidade, ou seja, padrões que se repetem periodicamente. Ele adiciona quatro novos parâmetros para capturar variações sazonais:

**P** = Ordem da parte autoregressiva sazonal.

**D** = Diferenciação sazonal necessária.

**Q** = Ordem da média móvel sazonal.

**S** = Período da sazonalidade (exemplo: 12 para dados mensais).

O modelo é representado como **SARIMA(p, d, q) × (P, D, Q, S)**.

**Exemplo de Aplicação**: Previsão de vendas sazonais, como consumo de energia elétrica ao longo do ano.

**Etapas Práticas para Análise de Séries Temporais**

**1\. Importar e Visualizar os Dados**

A visualização de dados é uma etapa essencial na análise de séries temporais, pois permite identificar padrões, tendências, sazonalidade e anomalias antes da modelagem. Algumas das principais técnicas incluem:

**Gráfico de Linha:** A forma mais comum de visualização, exibindo a evolução dos dados ao longo do tempo. Ajuda a detectar tendências e padrões sazonais.

**Histogramas e Boxplots:** Úteis para analisar a distribuição dos dados e identificar outliers.

**Autocorrelação (ACF) e Parcial (PACF):** Mostram como os valores passados influenciam os valores futuros, auxiliando na escolha de modelos ARIMA/SARIMA.

**Decomposição de Série Temporal:** Separa os componentes da série em tendência, sazonalidade e resíduo, facilitando a interpretação.

**Heatmaps e Gráficos de Dispersão:** Podem ser usados para visualizar padrões sazonais ou relações entre múltiplas variáveis em séries temporais multivariadas.

**2\. Analisar a Estacionaridade**

**Visualização Gráfica**

**Gráfico de Linha:** Se houver uma tendência crescente/decrescente ou padrões sazonais evidentes, a série pode não ser estacionária.

**Rolling Statistics:** Calcular e plotar a média e a variância em janelas móveis para ver se se mantêm constantes.

**Testes Estatísticos**

**Teste de Dickey-Fuller Aumentado (ADF)**

Hipótese nula (H0): A série tem raiz unitária (não estacionária).

Hipótese alternativa (H1​): A série é estacionária.

Se o p-valor for menor que 0,05, rejeitamos H0 e concluímos que a série é estacionária.

**Teste KPSS (Kwiatkowski-Phillips-Schmidt-Shin)**

Hipótese nula (H0​): A série é estacionária.

Hipótese alternativa (H1​): A série não é estacionária.

Se o p-valor for menor que 0,05, rejeitamos H0, indicando que a série não é estacionária.

**Teste de Phillips-Perron (PP)**

Similar ao ADF, mas mais robusto a heterocedasticidade.

**Função de Autocorrelação (ACF) e Autocorrelação Parcial (PACF)**

Se a ACF decai lentamente em vez de cair rapidamente para zero, a série pode ser não estacionária.

**Como Tornar uma Série Estacionária?**

Se a série não for estacionária, pode-se aplicar transformações para estabilizar suas propriedades:

**Diferenciação:** Subtrair o valor anterior do atual () para remover tendências.

**Transformação Logarítmica** **():** para estabilizar a variância.

**Diferenciação Sazonal:** Para séries com sazonalidade, subtrair valores do mesmo período anterior (​).

**Remover Tendência com Modelos de Regressão:** Ajustar e remover uma tendência linear ou polinomial.

**Yt​** representa o valor da série temporal no instante t. Ou seja, é o valor observado no tempo t.

**S** representa a sazonalidade da série, ou seja, o número de períodos após os quais os padrões se repetem.

**3\. Decomposição**

A decomposição de séries temporais é uma técnica que separa a série em diferentes componentes para facilitar a análise e a modelagem. Isso permite entender melhor as tendências, identificar padrões sazonais e remover ruídos. Podendo ser dividida em Tendencia, Sazonalidade e Resíduo.

**1\. Decomposição Aditiva**

Quando os componentes são somados:

Usada quando a **amplitude da sazonalidade é constante** ao longo do tempo.

**Exemplo:** Temperatura média diária ao longo do ano.

**2\. Decomposição Multiplicativa**

Quando os componentes são multiplicados:

Aplicada quando a **sazonalidade varia em intensidade** conforme a tendência cresce ou diminui.

**Exemplo:** Receita de uma empresa, onde picos sazonais aumentam à medida que a empresa cresce.

**4\. Modelagem**

Escolher e ajustar o modelo apropriado (ARIMA, SARIMA, LSTM, Prophet, etc.).

**5\. Avaliação**

Ao trabalhar com séries temporais, a separação dos dados deve ser feita de forma **sequencial**, mantendo a ordem cronológica. Diferente de problemas comuns de aprendizado de máquina, onde a divisão pode ser aleatória, em séries temporais isso comprometeria a capacidade preditiva do modelo.

**Como Dividir os Dados?**

A abordagem mais utilizada é:

**Conjunto de Treino**: Parte inicial dos dados, usada para ajustar o modelo.

**Conjunto de Teste**: Últimos períodos da série, utilizados para avaliar a performance.

**Métricas de Avaliação para Séries Temporais**

Depois de treinar o modelo, ele precisa ser avaliado com métricas que quantificam o erro das previsões em relação aos valores reais. As mais utilizadas são:

**1\. RMSE (Erro Quadrático Médio - Root Mean Squared Error)**

Mede a diferença média entre valores reais e previstos, penalizando mais os erros grandes:

![RMSE (Raiz Do Erro Quadrático Médio) Em Machine Learning | Mario Filho |  Machine Learning](data:image/png;base64,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)

Valores menores indicam previsões mais precisas.

Penaliza fortemente erros grandes devido à elevação ao quadrado.

**2\. MAE (Erro Absoluto Médio - Mean Absolute Error)**

Mede a média dos erros absolutos, sem dar peso maior para erros grandes:

![MAE (Erro Médio Absoluto) Em Machine Learning | Mario Filho | Machine  Learning](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAesAAAEmCAMAAAB1W0j5AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURf////f394CAgIyMjP7+/v39/fv7+9/f32lpaRISEltbW/z8/NbW1qqqqpOTk0ZGRhkZGQQEBAAAAPr6+vHx8WhoaAkJCSoqKnFxcdLS0gcHB+7u7gYGBvb29rq6uq2trc3Nzfn5+fDw8MTExLGxscHBwevr65ycnIqKivT09HBwcFJSUkJCQiEhIYuLi7KysmZmZldXV09PTyUlJVVVVczMzMjIyKSkpOXl5ZiYmOnp6QUFBRgYGNTU1ENDQ+Li4tjY2DAwMAsLC7m5uY6Ojjc3N6Ojo93d3fPz83t7ezQ0NOzs7FhYWCAgIODg4Kurq0hISGNjYwEBAXZ2drS0tLOzs6ampqenp52dnVBQUC0tLQgICAICAqKiouHh4URERCQkJDs7O87OzsXFxRUVFcDAwDk5ORwcHMnJyQMDA42NjWBgYHNzc+3t7fX19ePj421tbRcXF0lJSefn56ioqDMzMwoKChQUFMfHx4iIiBYWFvj4+BAQEI+Pj729vVpaWr6+visrKx8fHyIiInp6eq6urtDQ0Hx8fLy8vJSUlMbGxjg4OImJiX19fWJiYjIyMtfX19ra2jU1NWFhYXd3d9PT0y4uLktLS0xMTFZWVllZWVFRUT4+PpqamhoaGsvLy11dXe/v7x0dHbe3t3V1dYeHh15eXtHR0To6OiMjIw8PDw4ODpmZmQ0NDW9vb7CwsNXV1SkpKYKCgqWlpX5+figoKHR0dPLy8iwsLKysrObm5s/Pz2VlZWRkZH9/f05OTt7e3urq6hMTE+jo6BERETY2NuTk5Li4uCYmJr+/v3Jycj09PVNTU8PDwzw8PLW1tUBAQJ6ennh4eNvb22pqaoODg5WVlYGBgaGhobu7u6CgoFRUVNzc3G5ubnl5eZubm7a2tqmpqcrKyoaGhmdnZ0dHRzExMU1NTV9fXxsbGycnJ5GRkS8vLwwMDFxcXEpKSpaWloSEhEFBQdnZ2WxsbIWFha+vr2tra5+fnx4eHpeXlz8/P0VFRcLCwpKSkpCQkNpexxMAAAAJcEhZcwAAIdUAACHVAQSctJ0AABUVSURBVHhe7dx3fBTV3gbwE50NZSEkT5CSAmyUQIQgoGAg1AASxQAuSEmWjuZGIZRIScJVqUpv0gUEpBNEWmiiFAFfEJQgoqCCXkRQFOWiYuP9zM7MltnZzZpEAe/z/YfJmbPL7Pzm9LMrBBERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERH9cwTccac+if55JJMpsFjxEiUD9Sfon8ZcqnRQmeAQlAzVn6F/mrJ3lStfoWIYY/0/QDKHhprDIxjr/xVFGuvISpWrWIQQUXffU7lqtP4s3WS+Yl2tul8qx6j5I++tUTO2Vri4r3bJOnXvf6CeSfd+fpLqP3hr9RbjGjTUJ92WfMU6Hn5p1FjJLgU1adqseUKLlq0eap2Y+HDEI230b+gf6dGktvq0m+qhsHb6pIKSGrd/sIBFoPB8xfoxK4AOHXUe79Spc5eW93ZNTrHJ5wF0U4phYHJVqXsP9OzVW/6rT9+UJ/Rv6B/pydR/6dNuquppTzmOzRq3HCpJO+k1nOFPo1+kPtHxMg+SPmuh+Ip1w+YAavbXJ0uSZA5Nj4oe0HHgIHu0B2fY058Zki4al8dQJVBPDAvrrHuhn6RWqcP1aTdVZlot7TA6K0QxONs9j8zUYoRyMv7fXoItPQs8p7+h0vMjR41Kio2NTUpKih0tk4+SkmKT7q9UpI2Zr1hL9coBGBOgT9eYzNljH4kAMM7+/BV/IVB6EQhS3m58QrkJ+hf4R5qYWl+fdlNNSnNMLSZOvnfKxIh4YOo09zyy6RPDgIQZM1/qMEt/StVmNjBH3/hL9efMfbIRgLDZZebNly2Y+/LUnkMBLPQWmgLxFWuRvbAckNbRy0MqM8VMirVistz5FtEWKbs6Fi1WzryCEkt0mf10K8dalpHaxIqly1yT7CInT00FXtUnuwh9CsCQ7vpkWcswoFdZl4Riy2OBewybioLyGWsRvgLAMG9PqWLlKqyOUo+j56CO8tiG90IZrxWCb7d6rCutaReCtd1ck5T0OesAW1N9souVOQCSpuuTZR3SEL/ePem1VEwr0gbbd6zFhtcBW3vfHepxU0MqqYeth2Gj8ih2HoZNBWxsbvVYb97SNB626q5JsshWT2wF7s/Vp7toP3obkLNB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9gy8ONAIsUZLxAd6YHK2NOuSYxPj7R7rgQuEuGcvflAC0yWir+u8nVPk7rDkDMOIaMJPDkOsfR9elFmYx2Kov79+5Eeso2oAQ5VlgVPx8c4bfnDN5SV7nupasK8QOZzKwSNGg4bwXQjKrviAY2vSbR/rD14U5kxEqEP2KbZUw0GV9Mze+32O6rMrPW0DPtRatjZ1MdfwjQz4EevEB1J6vmRvQCplWSs4d3MEDtw75ek6vvqT/qiThm8NL+DzGb0GzrnDfS7ldpZt32P/ntr/bI5VhkOYKodKlPbeL5Pizj2dKu9dmqDdsnFhUL6J7Qc/Yi1291XWuJ7JCtvtumIY0K76wkI11tkTPvtgPzDxyscTDCaJNlypftDlY9/usZYDcwjVlV7XhGDbp0Yh2tE84hejWk6IxGkTHuw3p/kwe9+6hzZbadps3fK5kOQavenG4j8Z2PXOnxpzxZ0/3Dmu2Nh5Cb3GGoSkEJo2iQASYI1IeS7/bxje/rGWDtqgbBaQPomIyDO47bkXYF3U08jo68FZaxw/YblO+4aheRAetUjmUXGSOHg9zJBzu4P3WLv8lt2+G+evD5r6yrJ9hjkLztL9at6ZYmfO5F2NM6zQ3Lj8lt1tKrQlriubCROHWCeaRGi0vugc9+8HSUtow1xTJev+LkIq3TNdEgH7dhjyZ8z1m3pdsuw2cQca5vNts7/a+JBq+qTbzJIjWKDUX6X3RmwS4mxXt+0Scudly+t+6DlQmwQOfNU6JEPE9OrsV2i8x7rfYc9vo99MZ1cXflvEzZWxCJn2xtN0F/qGi+zj9/qeMsmfeRNWRXavsEKf7imxbFTbT4E73sotG2kYbypKpgkop/w0gHk+akSK358s/Np/6PykXfNWePxsgKcKj351WF4jPDyz5DWXH02gv0bAboxUZ41q2ZosWdZ1fBH8EEtU55ad/YldtVpBJ9dVq7bu5B8tzxntvqQiFfrQ5Q/USrtN5sgvu1YuglATEREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREdE/xf8DLQh5KI833+EAAAAASUVORK5CYII=)

Fácil de interpretar, pois está na mesma unidade dos dados.

Não amplifica tanto os erros maiores, diferente do RMSE.

**3\. MAPE (Erro Percentual Médio Absoluto - Mean Absolute Percentage Error)**

Expressa o erro médio em termos percentuais, o que facilita a interpretação:

​​​ ![MAPE (Erro Absoluto Percentual Médio) em Machine Learning | Mario Filho |  Machine Learning](data:image/png;base64,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)

Útil para comparar previsões em diferentes escalas de valores.

Problemático quando Yi​ se aproxima de zero, pois pode gerar distorções.

**Desafios em Séries Temporais**

1. **Não-estacionaridade**

Séries temporais que possuem média ou variância variando ao longo do tempo.

Solução: Transformações (diferenciação, logaritmos).

1. **Dados Perdidos (Missing Data)**

Dados ausentes podem prejudicar a análise.

Solução: Interpolação ou preenchimento com valores estimados.

1. **Séries Curta**

Poucos dados dificultam a identificação de padrões.

Solução: Adicionar variáveis externas ou usar modelos que lidem bem com pequenos conjuntos de dados.

1. **Sazonalidades Complexas**

Séries com múltiplos padrões sazonais podem ser difíceis de modelar.

**Regressão Logística**

A regressão logística é um modelo estatístico usado para classificação, especialmente em problemas binários (onde o resultado pode ser 0 ou 1, como "sim" ou "não", "spam" ou "não spam"). Diferente da regressão linear, que prevê valores contínuos, a regressão logística prevê probabilidades e as transforma em classes usando a função sigmoide.

**Fórmula Matemática**

A regressão logística modela a probabilidade como uma função logística (sigmoide) baseada em uma combinação linear das variáveis independentes.

Onde:

- p: Probabilidade estimada de uma observação pertencer à classe positiva.
- β0​: Intercepto.
- β1, β2, ..., βn ​: Coeficientes das variáveis independentes.
- x1, x2, ..., ​: Variáveis independentes.

Essa equação utiliza a função sigmoide, que transforma qualquer valor real em um número entre 0 e 1, permitindo interpretar a saída como uma probabilidade.

A decisão final é feita com base em um limiar (threshold), geralmente 0.5

Classe= {1 se p≥0.5 0 se p<0.5​}

**Assunções do Modelo**

- **Dependência linear**: A relação entre variáveis independentes e o logit (log das odds) é linear.
- **Independência das observações**: As amostras devem ser independentes umas das outras.
- **Ausência de multicolinearidade**: As variáveis independentes não devem ser altamente correlacionadas.
- **Homogeneidade da variância (não essencial)**.

**Métricas de Avaliação**

- **Acurácia**: Porcentagem de classificações corretas.
- **Precisão, Recall e F1-score**: Medem a performance em cada classe.
- **ROC e AUC**: Avaliam o desempenho do modelo em diferentes limiares.
- **Matriz de Confusão**: Analisa verdadeiros positivos, verdadeiros negativos, falsos positivos e falsos negativos.

**Limitações**

- Assume relação linear entre as variáveis independentes e o logit.
- Não é eficiente com dados altamente correlacionados (multicolinearidade).
- Pode subestimar ou superestimar quando o conjunto de dados não é balanceado.
- Pode ser inadequada para problemas não lineares.

**Aplicações Práticas**

- **Medicina**: Diagnóstico de doenças (ex.: probabilidade de ter câncer).
- **Marketing**: Previsão de churn (clientes que deixam o serviço).
- **Financeiro**: Probabilidade de inadimplência em empréstimos.
- **Recursos Humanos**: Probabilidade de um candidato ser aprovado.

**Exemplo**

**Problema:**  
Uma empresa deseja prever se um cliente comprará um seguro de vida baseado em dois fatores: **idade** e **renda anual**. A variável dependente é categórica (comprou ou não o seguro: 1 ou 0).

**1\. Entendendo o Contexto**

**Variáveis:**

- **Independentes (Preditoras):**
  - **Idade:** A idade do cliente em anos.
  - **Renda anual:** A renda do cliente em milhares de dólares.
- **Dependente (Resposta):**
  - **Compra:** Se o cliente comprou o seguro (1) ou não (0).

**Objetivo:**

- Estimar a **probabilidade de compra** com base na idade e na renda anual.
- Classificar cada cliente como **comprador (1)** ou **não comprador (0)**.

**2\. Como o Modelo Funciona**

1. **Modelo Conceitual:**
    - A regressão logística transforma as variáveis preditoras (x1=idade, x2=renda) em uma **combinação linear**.
    - A combinação linear (z) é mapeada para uma **probabilidade (p)** usando a função sigmoide (f(z)):  
        <br/>
2. **Tomada de Decisão:**
    - Se p≥0, o cliente será classificado como **comprador (1)**.
    - Se p<0.5, o cliente será classificado como **não comprador (0)**.

**3\. Suposições do Modelo**

- A probabilidade de compra varia **logisticamente** com a idade e a renda.
- Os efeitos de idade e renda são **aditivos** e contribuem linearmente para z.
- As observações (clientes) são **independentes**.

**4\. Exemplos de Situações**

- **Cliente A:** 25 anos, renda anual de $20.000.
  - O modelo pode prever uma probabilidade de 0.20 (ou 20%), classificando-o como **não comprador (0)**.
- **Cliente B:** 45 anos, renda anual de $50.000.
  - O modelo pode prever uma probabilidade de 0.85 (ou 85%), classificando-o como **comprador (1)**.

**5\. Como Interpretar os Coeficientes**

Se o modelo estimar os seguintes coeficientes:

- β0=−2.5: A probabilidade inicial sem levar em conta idade e renda.
- β1=0.03: Cada ano de idade aumenta a probabilidade de compra em e<sup>0.03</sup>\=1.03, ou seja, **3% a mais na chance de compra**.
- β2=0.1: Cada $1.000 extras na renda anual aumenta a probabilidade em e<sup>0.1</sup>\=1.105, ou seja, **10.5% a mais na chance de compra**.

**6\. Limitações do Modelo**

- **Não-linearidade real:** Se a relação entre idade/renda e probabilidade não for linear, o modelo pode ser inadequado.
- **Classes desbalanceadas:** Se poucos clientes compram o seguro, o modelo pode ter dificuldade em prever corretamente os compradores.

**7\. Benefícios Conceituais**

- A regressão logística não apenas classifica, mas também fornece uma **probabilidade estimada**.
- Permite entender **quais fatores influenciam mais** na compra.

Simplicidade e facilidade de explicação para tomadores de decisão.