# ⏳ Séries Temporais

## 📌 Definição

Uma **série temporal** é uma sequência de observações registradas em momentos específicos no tempo.  
Exemplos: vendas diárias de um produto, temperaturas mensais ou valores de ações ao longo de semanas.

---

## 🧩 Estrutura

- **Observações (y_t):** Valores medidos em momentos *t*.  
- **Tempo (t):** Pode ser diário, semanal, mensal, anual ou em intervalos irregulares.

---

## 🎯 Utilidade e Quando Usar Séries Temporais

Séries temporais são úteis em cenários onde os dados variam ao longo do tempo e existe a necessidade de:

- **Previsão:** Estimar valores futuros (estoques, vendas, energia, preços).  
- **Análise de padrões:** Detectar tendências, sazonalidades e ciclos.  
- **Monitoramento:** Identificar anomalias em tempo real (fraudes, falhas, tráfego).  
- **Decisão estratégica:** Apoiar campanhas, precificação e planejamento urbano.  
- **Otimização:** Automatizar processos (produção, energia, transporte).  

---

## 🔎 Componentes de Séries Temporais

1. **📈 Tendência (Trend):** Movimento de longo prazo.  
   Ex: Crescimento de vendas anuais.  

2. **📊 Sazonalidade (Seasonality):** Padrões que se repetem em intervalos fixos.  
   Ex: Aumento de vendas no Natal.  

3. **🔄 Ciclo (Cycle):** Flutuações ligadas a fatores econômicos, não fixas.  
   Ex: Crises financeiras.  

4. **🎲 Resíduo (Noise):** Variações aleatórias.  
   Ex: Oscilações inesperadas em vendas diárias.  

---

## 🧮 Tipos de Séries Temporais

- **Univariada:** Apenas 1 variável observada no tempo.  
  Ex: Preço diário de uma ação.  

- **Multivariada:** Múltiplas variáveis inter-relacionadas.  
  Ex: Preço de ação + taxa de juros + volume de negociação.  

---

## ⚖️ Estacionaridade

Uma série é **estacionária** quando suas propriedades estatísticas não mudam ao longo do tempo:  

- Média constante  
- Variância constante  
- Autocovariância constante  

### Testes de Estacionaridade

- **ADF (Dickey-Fuller Aumentado):**  
  - H0: série não estacionária  
  - H1: série estacionária  

- **KPSS:**  
  - H0: série estacionária  
  - H1: série não estacionária  

- **Phillips-Perron (PP):** Mais robusto à heterocedasticidade.  

### Tornando uma série estacionária

- **Diferenciação:**
$$
\Delta y_t = y_t - y_{t-1}
$$

- **Transformação logarítmica:**
$$
y_t' = \log(y_t)
$$

- **Diferenciação sazonal:**
$$
\Delta_s y_t = y_t - y_{t-S}
$$

---

## 📊 Modelos e Técnicas

### 1. Média Móvel (MA)
$$
\hat{y}_t = \frac{1}{k} \sum_{i=1}^{k} y_{t-i}
$$

### 2. ARIMA (AutoRegressive Integrated Moving Average)

Representado como:  
**ARIMA(p, d, q)**

- **AR (p):** Parte autorregressiva.  
- **I (d):** Diferenciações para estacionaridade.  
- **MA (q):** Média móvel dos erros.  

Exemplo de previsão:
$$
y_t = c + \phi_1 y_{t-1} + \dots + \phi_p y_{t-p} + \theta_1 \varepsilon_{t-1} + \dots + \theta_q \varepsilon_{t-q} + \varepsilon_t
$$

### 3. SARIMA (Seasonal ARIMA)

Inclui sazonalidade:  
**SARIMA(p, d, q) × (P, D, Q, S)**

---

## 🔬 Etapas Práticas de Análise

### 1. 📥 Importar e Visualizar Dados  
- Gráfico de linha  
- Histogramas / Boxplots  
- ACF / PACF  
- Decomposição da série  

### 2. 📉 Verificar Estacionaridade  
- Visualização gráfica  
- Rolling mean/variance  
- Testes estatísticos  

### 3. 🔎 Decomposição  

- **Aditiva:**
$$
y_t = T_t + S_t + e_t
$$
- **Multiplicativa:**
$$
y_t = T_t \times S_t \times e_t
$$

### 4. ⚙️ Modelagem  
- ARIMA, SARIMA, LSTM, Prophet...  

### 5. 📏 Avaliação  
- Divisão sequencial (treino/teste)  
- Métricas:  

**RMSE:**  
$$
RMSE = \sqrt{\frac{1}{n} \sum_{t=1}^n (y_t - \hat{y}_t)^2}
$$
**MAE:**  
$$
MAE = \frac{1}{n} \sum_{t=1}^n |y_t - \hat{y}_t|
$$
**MAPE:**  
$$
MAPE = \frac{100}{n} \sum_{t=1}^n \left| \frac{y_t - \hat{y}_t}{y_t} \right|
$$

---

## ⚠️ Desafios em Séries Temporais

- **Não-estacionaridade →** Diferenciação / log  
- **Dados ausentes →** Interpolação / preenchimento  
- **Séries curtas →** Variáveis externas / modelos robustos  
- **Sazonalidade complexa →** Modelos híbridos  

---

# 📊 Regressão Logística

A regressão logística é um modelo para **classificação binária**.  
Exemplo: "compra ou não compra", "fraude ou não fraude".

---

## 🧮 Fórmula Matemática

A probabilidade é modelada pela **função sigmoide**:
$$
p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \dots + \beta_n x_n)}}
$$

Classificação final:
$$
Classe =
\begin{cases}
1 & \text{se } p \geq 0.5 \\
0 & \text{se } p < 0.5
\end{cases}
$$

---

## 📌 Assunções do Modelo

- Relação linear entre variáveis independentes e logit  
- Observações independentes  
- Ausência de multicolinearidade  

---

## 📏 Métricas de Avaliação

- **Acurácia**  
- **Precisão, Recall, F1-score**  
- **ROC e AUC**  
- **Matriz de Confusão**  

---

## 🌍 Aplicações Práticas

- **Medicina:** Diagnóstico de doenças  
- **Marketing:** Previsão de churn  
- **Financeiro:** Inadimplência em empréstimos  
- **RH:** Aprovação de candidatos  

---

## 🧑‍💼 Exemplo Prático

**Problema:**  
Prever se um cliente comprará um seguro de vida com base em **idade** e **renda anual**.

- **Variáveis independentes:** idade, renda  
- **Dependente:** compra (1 ou 0)  

**Modelo:**  
$$
z = \beta_0 + \beta_1 \cdot idade + \beta_2 \cdot renda
$$

$$
p = \frac{1}{1 + e^{-z}}
$$

- Cliente A (25 anos, $20k) → p = 0.20 → Não comprador  
- Cliente B (45 anos, $50k) → p = 0.85 → Comprador  

**Interpretação dos coeficientes:**  
- $\beta_1 = 0.03$: cada ano aumenta 3% na chance de compra  
- $\beta_2 = 0.1$: cada $1000$ a mais de renda aumenta 10.5% na chance de compra
