# 📚 Repositório de Estudos

Este repositório é o meu espaço de aprendizado.
Aqui organizo **anotações, resumos e materiais** que utilizo para estudar e aprofundar conhecimentos em diferentes áreas — principalmente IA, automação, dados e desenvolvimento de software.

A ideia é manter um registro centralizado e acessível, que me ajude a revisar conteúdos e ter sempre à mão referências importantes.

---

## 📜 Sumário

- [✏️ Conteúdos](#️-conteúdos)
  - [Agents Stack](#agents-stack)
  - [Skills do Claude](#skills-do-claude)
  - [n8n](#n8n)
  - [Supabase](#supabase)
  - [Mineração e Classificação de Dados](#mineração-e-classificação-de-dados)
  - [Séries Temporais](#séries-temporais)
- [🔧 Ferramentas](#-ferramentas)
- [📖 Livros](#-livros)

---

## ✏️ Conteúdos

> Os documentos são escritos em **Markdown** (`.md`) — formato principal, legível direto no GitHub.
> Cada um tem também uma versão **PDF** gerada automaticamente para leitura/impressão.

---

### Agents Stack

Referência completa sobre os principais conceitos, padrões e ferramentas para construção de sistemas baseados em agentes de IA: tipos de agentes, orquestração multi-agent, memória, RAG, tools, planejamento, guardrails, protocolos (MCP, A2A) e principais frameworks.

📄 [Ler em Markdown](documentos/md/agents_stack.md) · [Versão PDF](documentos/pdf/agents_stack.pdf)

---

### Skills do Claude

Guia completo sobre o sistema de Skills nos três ambientes do Claude: Claude.ai, Claude Code e a API da Anthropic. Criação, configuração e uso de skills personalizadas.

📄 [Ler em Markdown](documentos/md/skills_claude.md) · [Versão PDF](documentos/pdf/skills_claude.pdf)

---

### n8n

Estudo sobre o n8n, ferramenta open-source de automação de workflows low-code. Fundamentos, nodes, integrações com APIs e bancos de dados, execuções e boas práticas.

📄 [Ler em Markdown](documentos/md/n8n_estudo.md) · [Versão PDF](documentos/pdf/n8n_estudo.pdf)

---

### Supabase

Estudo sobre o Supabase como backend open-source: banco de dados PostgreSQL, autenticação, storage e funções edge.

📄 [Ler em Markdown](documentos/md/supabase_estudo.md) · [Versão PDF](documentos/pdf/supabase_estudo.pdf) *(em construção)*

---

### Mineração e Classificação de Dados

Guia completo sobre mineração de dados e aprendizado de máquina supervisionado: fundamentos, pré-processamento, algoritmos de classificação (Árvores de Decisão, SVM, KNN, Redes Neurais), avaliação de modelos e métricas.

📄 [Ler em Markdown](documentos/md/mineracao_classificacao.md) · [Versão PDF](documentos/pdf/mineracao_classificacao.pdf)

---

### Séries Temporais

Resumo completo sobre séries temporais: definição, componentes (tendência, sazonalidade, ciclo, resíduo), estacionaridade, modelos estatísticos (ARIMA, SARIMA, Holt-Winters) e modelos de deep learning (LSTM, Transformer).

📄 [Ler em Markdown](documentos/md/series_temporais.md) · [Versão PDF](documentos/pdf/series_temporais.pdf)

---

## 🔧 Ferramentas

### Conversor de Documentos

O script [`scripts/converter.py`](scripts/converter.py) converte arquivos entre **PDF, Word (DOCX) e Markdown** automaticamente, com renderização idêntica ao GitHub para a saída em PDF.

```bash
# Exemplos (executar da raiz do projeto)
python scripts/converter.py documentos/md/arquivo.md documentos/pdf/arquivo.pdf
python scripts/converter.py arquivo.pdf arquivo.md
python scripts/converter.py arquivo.docx arquivo.md
```

---

## 📖 Livros

<p style="color:gray;font-size:90%;">Clique nos títulos para acessar os links de download dos livros no meu Drive.</p>

- [**Artificial Intelligence: A Modern Approach**](https://drive.google.com/file/d/1h5dNLsWW71hqEZa5UwJIxxO2QpBlZx-M/view?usp=drive_link)
  > **Autores: Stuart Russell e Peter Norvig**
  > Um dos textos mais completos e usados em cursos de IA. Aborda agentes, busca, raciocínio, aprendizado de máquina, visão computacional, planejamento e robótica. Base sólida para entender IA de forma ampla.

- [**Deep Learning – Ian Goodfellow**](https://drive.google.com/file/d/12F3SP2l9dY3CnvAyQuLk3eL3qkco_VW2/view?usp=drive_link)
  > **Autores: Ian Goodfellow, Yoshua Bengio e Aaron Courville**
  > Guia abrangente sobre aprendizado profundo: fundamentos matemáticos, redes feedforward, convolucionais, recorrentes, regularização e técnicas modernas. Referência para quem quer entender os detalhes do deep learning.

- [**Inteligência Artificial: Uma Abordagem de Aprendizado de Máquina**](https://drive.google.com/file/d/1pK9f_T2YVE8ppfe2EQ9InlAAHjDfDoyq/view?usp=drive_link)
  > **Autores: Katti Faceli et al.**
  > Livro-texto para graduação/pós em IA e ML. Cobre preparação de dados, modelos preditivos e descritivos, avaliação, redes neurais profundas e aplicações práticas em Python.

- [**Clean Code – A Handbook of Agile Software Craftsmanship**](https://drive.google.com/file/d/1DUgKBZIEp1JmnvBhxrL0OkLumwSzPLp_/view?usp=drive_link)
  > **Autor: Robert C. Martin**
  > Boas práticas para escrever código limpo, legível e fácil de manter: nomes significativos, funções pequenas, testes unitários e refatoração.

- [**300 Ideias Para Programar**](https://drive.google.com/file/d/1iiRruywUUVOg3iSjfIjODvTZqZlb_uGZ/view?usp=drive_link)
  > **Autor: Roger Meiners**
  > Coletânea de sugestões de programas para praticar lógica e estruturas comuns, progressivos em dificuldade. Útil para aprender fazendo, sem depender de linguagem específica.

- [**Design de Interação – Jennifer Preece**](https://drive.google.com/file/d/1wK2VQZQneKpuyveaRaK6FJdlUkJvlHHY/view?usp=drive_link)
  > **Autores: Jennifer Preece, Yvonne Rogers e Helen Sharp**
  > Obra fundamental de IHC. Design centrado no usuário, usabilidade, prototipagem, testes de interface e como projetar melhores experiências interativas.

- [**Designing Interactive Systems**](https://drive.google.com/file/d/1gb2xkalGk4Z4DILmy5uM99SBxqlcHrNh/view?usp=drive_link)
  > **Autores: David Benyon, Phil Turner e Susan Turner**
  > Manual abrangente de design de interação: teorias, métodos e práticas de HCI com exemplos e estudos de caso.

- [**Atenção Plena - Mindfulness**](https://drive.google.com/file/d/1GBjCe5CBAyFbg7ZLmhI_o4OppsjiwFGa/view?usp=drive_link)
  > **Autores: Mark Williams e Danny Penman**
  > Programa de oito semanas baseado em MBCT para reduzir estresse e ansiedade, integrando meditação e mindfulness ao cotidiano.

- [**Hiperfoco - Chris Bailey**](https://drive.google.com/file/d/1XjKGU25s3dk2JYCoWsHn2x4bKI2JbzMl/view?usp=drive_link)
  > **Autor: Chris Bailey**
  > Como manter foco intenso em tarefas importantes e usar momentos de atenção dispersa para criatividade. Estratégias práticas para produtividade sustentada.
