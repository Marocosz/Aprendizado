A fórmula da Distância Euclidiana entre um ponto $P$ e um centroide $\mu$ é:
$$d(P, \mu) = \sqrt{(P_x - \mu_x)^2 + (P_y - \mu_y)^2}$$

Vamos organizar os dados iniciais:
* **Centroides Iniciais:** $\mu_1 = (1.0, 1.0)$ e $\mu_2 = (5.0, 7.0)$
* **Pontos (Subject):** $P_1(1.0, 1.0)$, $P_2(1.5, 2.0)$, $P_3(3.0, 4.0)$, $P_4(5.0, 7.0)$, $P_5(3.5, 5.0)$, $P_6(4.5, 5.0)$, $P_7(3.5, 4.5)$

---

### Iteração 1: Atribuição Inicial

Vamos calcular a distância de cada ponto para $\mu_1$ e $\mu_2$ e alocá-los no grupo do centroide mais próximo.

* **P1 (1.0, 1.0):**
    * Para $\mu_1$: $d = 0$ (é o próprio ponto)
    * Para $\mu_2$: $d = \sqrt{(1-5)^2 + (1-7)^2} = \sqrt{16 + 36} \approx 7.21$
    * **Atribuição:** Grupo 1
* **P2 (1.5, 2.0):**
    * Para $\mu_1$: $d = \sqrt{(1.5-1)^2 + (2-1)^2} = \sqrt{0.25 + 1} \approx 1.12$
    * Para $\mu_2$: $d = \sqrt{(1.5-5)^2 + (2-7)^2} = \sqrt{12.25 + 25} \approx 6.10$
    * **Atribuição:** Grupo 1
* **P3 (3.0, 4.0):**
    * Para $\mu_1$: $d = \sqrt{(3-1)^2 + (4-1)^2} = \sqrt{4 + 9} \approx 3.61$
    * Para $\mu_2$: $d = \sqrt{(3-5)^2 + (4-7)^2} = \sqrt{4 + 9} \approx 3.61$
    * *Nota: Houve um empate exato. A convenção padrão do algoritmo é alocar no primeiro grupo em caso de empate.*
    * **Atribuição:** Grupo 1
* **P4 (5.0, 7.0):**
    * Para $\mu_1$: $d \approx 7.21$
    * Para $\mu_2$: $d = 0$ (é o próprio ponto)
    * **Atribuição:** Grupo 2
* **P5 (3.5, 5.0):**
    * Para $\mu_1$: $d = \sqrt{(3.5-1)^2 + (5-1)^2} = \sqrt{6.25 + 16} \approx 4.72$
    * Para $\mu_2$: $d = \sqrt{(3.5-5)^2 + (5-7)^2} = \sqrt{2.25 + 4} = 2.50$
    * **Atribuição:** Grupo 2
* **P6 (4.5, 5.0):**
    * Para $\mu_1$: $d = \sqrt{(4.5-1)^2 + (5-1)^2} = \sqrt{12.25 + 16} \approx 5.32$
    * Para $\mu_2$: $d = \sqrt{(4.5-5)^2 + (5-7)^2} = \sqrt{0.25 + 4} \approx 2.06$
    * **Atribuição:** Grupo 2
* **P7 (3.5, 4.5):**
    * Para $\mu_1$: $d = \sqrt{(3.5-1)^2 + (4.5-1)^2} = \sqrt{6.25 + 12.25} \approx 4.30$
    * Para $\mu_2$: $d = \sqrt{(3.5-5)^2 + (4.5-7)^2} = \sqrt{2.25 + 6.25} \approx 2.92$
    * **Atribuição:** Grupo 2

**Resultado ao fim da Iteração 1:**
* **Grupo 1:** $\{P_1, P_2, P_3\}$
* **Grupo 2:** $\{P_4, P_5, P_6, P_7\}$

---

### Iteração 2: Atualização dos Centroides

Agora recalculamos os centroides tirando a média das coordenadas $(A, B)$ dos pontos em cada grupo.

* **Novo $\mu_1$** (Média de $P_1, P_2, P_3$):
    * $A = (1.0 + 1.5 + 3.0) / 3 = 5.5 / 3 \approx 1.83$
    * $B = (1.0 + 2.0 + 4.0) / 3 = 7.0 / 3 \approx 2.33$
    * **$\mu_1$ atualizado:** $(1.83, 2.33)$
* **Novo $\mu_2$** (Média de $P_4, P_5, P_6, P_7$):
    * $A = (5.0 + 3.5 + 4.5 + 3.5) / 4 = 16.5 / 4 = 4.125$
    * $B = (7.0 + 5.0 + 5.0 + 4.5) / 4 = 21.5 / 4 = 5.375$
    * **$\mu_2$ atualizado:** $(4.125, 5.375)$

Com os novos centroides, calculamos as distâncias novamente para ver se algum ponto muda de grupo.

* **P1:** Mais próximo de $\mu_1$ ($1.57$ vs $5.37$) $\rightarrow$ Mantém no Grupo 1
* **P2:** Mais próximo de $\mu_1$ ($0.46$ vs $4.27$) $\rightarrow$ Mantém no Grupo 1
* **P3 (3.0, 4.0):**
    * Para o novo $\mu_1$: $d = \sqrt{(3-1.83)^2 + (4-2.33)^2} \approx 2.03$
    * Para o novo $\mu_2$: $d = \sqrt{(3-4.125)^2 + (4-5.375)^2} \approx 1.77$
    * *Atenção:* O ponto $P_3$ agora está mais perto do Grupo 2. $\rightarrow$ **Muda para o Grupo 2**
* **P4 a P7:** Todos continuam matematicamente muito mais próximos do novo $\mu_2$.

**Resultado ao fim da Iteração 2:**
* **Grupo 1:** $\{P_1, P_2\}$
* **Grupo 2:** $\{P_3, P_4, P_5, P_6, P_7\}$

---

### Iteração 3: Convergência

Como um ponto mudou de grupo, precisamos recalcular os centroides mais uma vez.

* **Novo $\mu_1$** (Média de $P_1, P_2$):
    * $A = (1.0 + 1.5) / 2 = 1.25$
    * $B = (1.0 + 2.0) / 2 = 1.5$
    * **$\mu_1$ final:** $(1.25, 1.5)$
* **Novo $\mu_2$** (Média de $P_3, P_4, P_5, P_6, P_7$):
    * $A = (3.0 + 5.0 + 3.5 + 4.5 + 3.5) / 5 = 19.5 / 5 = 3.9$
    * $B = (4.0 + 7.0 + 5.0 + 5.0 + 4.5) / 5 = 25.5 / 5 = 5.1$
    * **$\mu_2$ final:** $(3.9, 5.1)$

Se você calcular as distâncias com esses centroides finais, verá que **nenhum ponto muda de grupo**. O P3, por exemplo, está a $3.05$ de distância do $\mu_1$ e apenas $1.42$ do $\mu_2$. 

Como os grupos se estabilizaram (não houve mais trocas), o algoritmo atingiu a **convergência**.

---

### Resposta Final

Os grupos finais encontrados pela clusterização são:

1.  **Grupo 1:** P1, P2
2.  **Grupo 2:** P3, P4, P5, P6, P7
3.  

# Atividade 2

Usaremos a **Distância Euclidiana** para medir a proximidade entre os pontos.

### Passo 1: Organizar os Dados
Os nossos sujeitos (pontos) são:
* $P_1(1.0, 1.0)$
* $P_2(1.5, 2.0)$
* $P_3(3.0, 4.0)$
* $P_4(5.0, 7.0)$
* $P_5(3.5, 5.0)$
* $P_6(4.5, 5.0)$
* $P_7(3.5, 4.5)$

No início, cada ponto é um cluster individual.

---

### Passo 2: Calcular a Matriz de Distâncias Iniciais
Vamos focar em calcular as menores distâncias entre os pontos para encontrar o primeiro par a ser agrupado. 
A fórmula da distância euclidiana é: $d(A, B) = \sqrt{(A_x - B_x)^2 + (A_y - B_y)^2}$

Calculando algumas das menores distâncias visíveis:
* $d(1, 2) = \sqrt{(1.5-1)^2 + (2-1)^2} = \sqrt{0.25 + 1} = \sqrt{1.25} \approx 1.12$
* $d(5, 6) = \sqrt{(4.5-3.5)^2 + (5-5)^2} = \sqrt{1.0} = 1.0$
* $d(3, 7) = \sqrt{(3.5-3)^2 + (4.5-4)^2} = \sqrt{0.25 + 0.25} = \sqrt{0.50} \approx 0.71$
* $d(5, 7) = \sqrt{(3.5-3.5)^2 + (4.5-5)^2} = \sqrt{0 + 0.25} = \sqrt{0.25} = 0.50$

**Análise Iteração 1:**
A menor distância geral é entre $P_5$ e $P_7$ ($d = 0.50$). 
* **Ação:** Agrupar $P_5$ e $P_7$. 
* **Cluster criado:** $(5, 7)$ na altura $0.50$ do dendrograma.

---

### Passo 3: Atualizar Distâncias (Método MIN)
Agora temos os grupos: $\{1\}, \{2\}, \{3\}, \{4\}, \{6\}, \{5, 7\}$.
Como usamos o método MIN, a distância de um ponto para o grupo $(5, 7)$ é a *menor* distância entre ele e os integrantes do grupo.

Vamos checar a distância de $P_3$ e $P_6$ em relação ao novo grupo:
* $d(3, (5,7)) = \min[d(3,5), d(3,7)]$
  * $d(3,5) = \sqrt{(3.5-3)^2 + (5-4)^2} = \sqrt{1.25} \approx 1.12$
  * $d(3,7) \approx 0.71$ (calculado antes)
  * Portanto, $d(3, (5,7)) = 0.71$.

**Análise Iteração 2:**
A menor distância no momento é $0.71$, entre $P_3$ e o grupo $(5, 7)$.
* **Ação:** Agrupar $P_3$ com o cluster $(5, 7)$.
* **Cluster criado:** $(3, 5, 7)$ na altura $0.71$.

---

### Passo 4: Próximas Iterações

**Iteração 3:**
Grupos atuais: $\{1\}, \{2\}, \{4\}, \{6\}, \{3, 5, 7\}$.
Vamos verificar as distâncias em torno do grupo recém-formado e dos pontos restantes:
* $d(6, (3,5,7)) = \min[d(6,3), d(6,5), d(6,7)]$
  * Sabemos que $d(6,5) = 1.0$. Esta é a menor distância de $P_6$ para o grupo.
* Outra distância pequena que ainda existe: $d(1, 2) = 1.12$.
A menor distância atual é $1.0$ (entre $P_6$ e o grupo $\{3, 5, 7\}$ através de $P_5$).
* **Ação:** Agrupar $P_6$ com o cluster $(3, 5, 7)$.
* **Cluster criado:** $(3, 5, 6, 7)$ na altura $1.0$.

**Iteração 4:**
Grupos atuais: $\{1\}, \{2\}, \{4\}, \{3, 5, 6, 7\}$.
Distâncias notáveis:
* $d(1, 2) = 1.12$
* A menor distância de $P_4(5,7)$ para o grupão é até $P_6(4.5, 5.0)$: $d = \sqrt{0.5^2 + 2^2} \approx 2.06$.
A menor distância global agora é $1.12$.
* **Ação:** Agrupar $P_1$ e $P_2$.
* **Cluster criado:** $(1, 2)$ na altura $1.12$.

**Iteração 5:**
Grupos atuais: $\{1, 2\}, \{4\}, \{3, 5, 6, 7\}$.
A menor distância de $P_4$ para o grupo maior é $2.06$.
A menor distância entre o grupo $(1,2)$ e o grupo maior é de $P_2(1.5, 2.0)$ para $P_3(3.0, 4.0)$: $d = \sqrt{1.5^2 + 2.0^2} = \sqrt{2.25 + 4} = 2.50$.
A menor das duas opções é $2.06$.
* **Ação:** Agrupar $P_4$ com o cluster $(3, 5, 6, 7)$.
* **Cluster criado:** $(3, 4, 5, 6, 7)$ na altura $2.06$.

**Iteração 6 (Final):**
Restam apenas os grupos $(1, 2)$ e $(3, 4, 5, 6, 7)$.
Como vimos, a menor distância entre qualquer elemento desses dois grupos é de $P_2$ para $P_3$ ($d = 2.50$).
* **Ação:** Agrupar tudo.
* **Cluster único final criado** na altura $2.50$.

---

### Estrutura do Dendrograma Final
Para desenhar o dendrograma, você deve criar um gráfico de eixos onde o Eixo X representa os Sujeitos (1 a 7) e o Eixo Y representa a Distância (Altura de junção). O formato visual seria:

1.  Uma junção unindo **5 e 7** na altura $0.50$.
2.  Uma linha subindo dessa junção, unindo-se com o **3** na altura $0.71$.
3.  Uma linha subindo, unindo-se com o **6** na altura $1.0$.
4.  No outro lado do gráfico, uma junção unindo **1 e 2** na altura $1.12$.
5.  Voltando ao grupo grande, uma linha subindo para se unir com o **4** na altura $2.06$.
6.  Finalmente, um "arco" principal unindo o braço do grupo **(1,2)** com o braço do grupão **(3,4,5,6,7)** na altura $2.50$.