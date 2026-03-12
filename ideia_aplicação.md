# Motor de Criação de Agentes Inteligentes

- [Motor de Criação de Agentes Inteligentes](#motor-de-criação-de-agentes-inteligentes)
  - [1. Visão do Produto](#1-visão-do-produto)
  - [2. Conceitos Gerais](#2-conceitos-gerais)
  - [3. Estrutura Geral de um Agente](#3-estrutura-geral-de-um-agente)
    - [Componentes principais](#componentes-principais)
  - [4. Motor de Criação de Agentes (Core do Sistema)](#4-motor-de-criação-de-agentes-core-do-sistema)
    - [Arquitetura do motor](#arquitetura-do-motor)
  - [5. Fluxo de Criação de um Agente](#5-fluxo-de-criação-de-um-agente)
    - [Etapa 1 - Ideia do Agente](#etapa-1---ideia-do-agente)
    - [Etapa 2 - Planejamento da Arquitetura](#etapa-2---planejamento-da-arquitetura)
    - [Etapa 3 - Configuração das Entradas](#etapa-3---configuração-das-entradas)
    - [Etapa 4 - Configuração de Conhecimento (RAG)](#etapa-4---configuração-de-conhecimento-rag)
    - [Etapa 5 - Ferramentas](#etapa-5---ferramentas)
    - [Etapa 6 - Guardrails](#etapa-6---guardrails)
    - [Etapa 7 - Testes (Evals)](#etapa-7---testes-evals)
    - [Etapa 8 — Deploy do Agente](#etapa-8--deploy-do-agente)
  - [6. Execução dos Agentes](#6-execução-dos-agentes)
  - [7. Playground de Agentes](#7-playground-de-agentes)
  - [8. Sistema de Testes (Evals)](#8-sistema-de-testes-evals)
  - [9. Arquitetura Técnica da Plataforma](#9-arquitetura-técnica-da-plataforma)

## 1. Visão do Produto

> A aplicação será uma plataforma de criação de agentes de IA personalizados, voltada para usuários com experiência em desenvolvimento.
O objetivo é permitir que usuários projetem, construam, testem e executem agentes inteligentes especializados sem precisar implementar toda a infraestrutura manualmente.

Em vez de oferecer apenas agentes pré-configurados, a plataforma funcionará como um motor de criação de agentes, onde o usuário descreve o comportamento desejado e o sistema projeta automaticamente a melhor arquitetura para aquele agente.

A plataforma funciona como um meta-sistema de engenharia de agentes, capaz de:

- Interpretar requisitos do usuário
- Projetar arquiteturas de agentes
- Configurar componentes automaticamente
- Gerar prompts e fluxos
- Testar e validar o comportamento do agente

## 2. Conceitos Gerais

> O sistema funciona como um Agent Creation Engine. Ou seja, O usuário não cria diretamente o agente.Ele fornece informações sobre o agente desejado, e o motor da plataforma projeta automaticamente a arquitetura ideal.

A plataforma usa agentes internos para auxiliar na criação do agente do usuário. Esses agentes internos podem:

- Interpretar a ideia do usuário
- Propor arquiteturas (Orchestrator, subagents...)
- Sugerir ferramentas
- Validar entradas e saídas
- Sugerir melhorias
- Gerar prompts
- Criar guardrails
- Configurar RAG

ele vai poder gerar algo como:

```
[ Input ]
    ↓ guardrails (input)
[ Orchestrator Agent ]
    ↓ planeja e delega
[ Subagent A ] [ Subagent B ] [ Subagent C ]
    ↓ usam ferramentas
[ Tools: RAG / APIs / Code / Browser ]
    ↓ resultados
[ Supervisor / Eval ]
    ↓ guardrails (output)
[ Output ]
```

Assim, nosso motor deve ter conhecimento, de acordo com o agent que o usuário quer criar sobre, se deve ser usado:

> **Stack relevante:** O diagrama acima já reflete os dois principais padrões de orquestração que o motor precisa dominar: **Orchestrator → Subagents** (o orquestrador decompõe e delega) e o **Supervisor Pattern** (avalia outputs antes de entregar). O próprio motor de criação também é um sistema multi-agente internamente — o Agent Architect, RAG Designer, Tool Planner etc. são subagentes colaborando via **Orchestrator → Subagents** para construir o blueprint final.

## 3. Estrutura Geral de um Agente

> Todo agente criado dentro da plataforma seguirá uma arquitetura padrão composta por módulos configuráveis.

### Componentes principais

**Ideia Central do Agente**

- propósito
- domínio
- tarefas principais
- comportamento esperado

> **Decisão do motor — Tipo de Agente:** Com base na ideia central, o **Agent Architect** decide se o agente gerado será:
> - **Single Agent** — um único modelo com acesso a ferramentas, memória e instruções. Adequado para tarefas bem definidas e lineares. Opera em **ReAct loop** (Reason → Act → Observe).
> - **Multi-Agent System** — múltiplos agentes colaborando, cada um com responsabilidade distinta. Adequado para tarefas complexas, com múltiplos domínios ou etapas paralelas.

> **Decisão do motor — Padrão de Orquestração:** Se multi-agente, o motor escolhe o padrão:
> - **Orchestrator → Subagents** — para tarefas decomponíveis em especializações (ex: agente jurídico + financeiro + risco)
> - **Handoff / Swarm** — para fluxos onde o contexto muda e o controle passa de um agente para outro dinamicamente
> - **Supervisor Pattern** — quando há necessidade de validação antes de entregar o output ao usuário
> - **Agent-to-Agent (A2A)** — quando os agentes gerados precisam se comunicar via protocolos como MCP ou Google A2A Protocol

> **Decisão do motor — Raciocínio:** O motor também configura como o agente vai raciocinar:
> - **ReAct** — padrão para agentes com ferramentas (raciocina e age em loop)
> - **Chain-of-Thought (CoT)** — quando o agente precisa de raciocínio passo a passo antes de responder
> - **Plan-and-Execute** — para tarefas complexas onde faz sentido criar um plano completo antes de agir
> - **Reflexion** — quando o agente deve criticar e autocorrigir seus próprios outputs
> - **Extended Thinking** — para modelos com scratchpad interno (ex: Claude com thinking ativado)

---

**Entradas do Agente**

Os agentes podem receber:

- texto
- imagens

O usuário define:

- quantos campos de entrada existem
- o propósito de cada campo

---

**Saídas do Agente**

Define:

- formato de resposta
- estrutura da resposta

---

**Memória do Agente**

O motor configura quais camadas de memória o agente terá:

- **In-context memory** — o que cabe na janela de contexto atual (sempre presente)
- **Episodic memory** — histórico de conversas e sessões passadas (ex: o agente lembra interações anteriores com o mesmo usuário)
- **Semantic memory** — fatos e conhecimento persistido sobre o domínio ou usuário (ex: preferências, perfil)
- **Procedural memory** — o próprio system prompt e instruções do agente (sempre presente, gerado pelo Prompt Engineer Agent)
- **External memory (RAG)** — vetores em banco externo (ver seção RAG abaixo)

> **Stack relevante:** As memórias episódica e semântica provavelmente exigem um banco de dados dedicado por agente. O motor precisa ser capaz de criar e configurar essas tabelas automaticamente no PostgreSQL quando o usuário solicitar esse tipo de memória.

---

**RAG (Retrieval Augmented Generation)** (opcional)

O agente pode ter acesso a uma base de conhecimento. Tipos possíveis:

- documentos
- PDFs
- banco vetorial
- websites
- banco de dados

> **Decisão do motor — Estratégia de RAG:** O **RAG Designer** decide qual abordagem usar com base na complexidade da base de conhecimento e das consultas esperadas:
> - **Naive RAG** — embed → busca por similaridade → injeta no contexto. Adequado para bases simples e consultas diretas.
> - **Advanced RAG** — adiciona reranking, query expansion e HyDE (Hypothetical Document Embeddings). Adequado quando a qualidade de retrieval precisa ser maior.
> - **Agentic RAG** — o agente decide quando e como buscar, podendo fazer múltiplas buscas iterativas. Adequado para tarefas de pesquisa ou análise profunda.
> - **GraphRAG** — usa grafos de conhecimento para capturar relações entre entidades. Adequado para domínios com entidades fortemente relacionadas (ex: documentos jurídicos, bases de conhecimento corporativas).

---

**Skills (Ferramentas)**

Ferramentas que o agente pode usar.

- busca web
- consulta banco de dados
- execução de código
- APIs externas
- geração de imagens
- cálculos

> **Stack relevante — Tipos de Tools que o motor configura:**
> - **Function calling** — chama funções definidas (buscar DB, chamar API, executar lógica customizada). É o tipo mais comum e o padrão para a maioria das integrações.
> - **Code interpreter** — executa código Python em sandbox. Usado quando o agente precisa de cálculos, análise de dados ou transformações programáticas.
> - **Web search / Browser** — navegação autônoma para busca de informações atualizadas. Inclui possibilidade de Web Scraping.
> - **MCP (Model Context Protocol)** — protocolo padrão da Anthropic para expor ferramentas a agentes. Permite integrar qualquer sistema externo de forma padronizada (ver Integrações abaixo).
> - **Computer Use** — controle de mouse, teclado e interfaces gráficas. Para casos avançados onde o agente precisa operar UIs.

---

**Guardrails**

Regras de comportamento e segurança do agente.

Exemplos:

- impedir respostas fora do domínio
- evitar alucinações
- validar formato de saída
- aplicar filtros de conteúdo

> **Stack relevante — Camadas de Guardrails que o motor configura:**
> - **Input guardrails** — filtram inputs maliciosos, prompt injection e PII antes de chegarem ao agente
> - **Output guardrails** — verificam outputs antes de entregar ao usuário (conteúdo, formato, alucinações)
> - **Human-in-the-loop** — aprovação humana em ações críticas ou irreversíveis (ex: o agente vai deletar dados ou enviar um e-mail)
>
> **Frameworks disponíveis:** Guardrails AI, NeMo Guardrails (NVIDIA), LlamaGuard (Meta). O **Guardrail Designer** escolhe e configura o framework mais adequado ao tipo de agente.

---

**Integrações (MCP / conectores)**

Permitem que o agente interaja com sistemas externos.

- Notion
- Google Drive
- Slack
- APIs externas
- bancos de dados
- webhooks

Essas integrações permitirão que o agente:

- leia dados externos
- escreva dados externos
- acione workflows

> **Stack relevante:** As integrações são implementadas como **MCP Servers** ou como **Function Calling tools**. O **Tool Planner** decide qual abordagem usar: MCP para integrações padronizadas e reutilizáveis, Function Calling para integrações customizadas específicas do agente.

---

## 4. Motor de Criação de Agentes (Core do Sistema)

> O principal diferencial da plataforma será o Agent Creation Engine.

Esse motor será responsável por:

- interpretar a ideia do usuário
- definir a arquitetura do agente
- sugerir componentes
- gerar prompts
- validar a configuração

> **Stack relevante — O motor em si é um Multi-Agent System:** Os agentes internos abaixo seguem o padrão **Orchestrator → Subagents**, onde um orquestrador principal recebe a ideia do usuário, coordena os subagentes especialistas e consolida o blueprint final. O padrão **Supervisor Pattern** é aplicado ao final para validar a coerência da arquitetura gerada antes de apresentar ao usuário.

### Arquitetura do motor

- **Agent Architect**
    - interpretar o objetivo do agente
    - definir a arquitetura ideal (Single Agent vs Multi-Agent, padrão de orquestração, padrão de raciocínio)
    - *Raciocínio interno:* usa **Plan-and-Execute** + **Chain-of-Thought** para mapear a ideia em componentes estruturados

- **RAG Designer**
    - se RAG é necessário
    - qual estratégia de retrieval usar (Naive / Advanced / Agentic / GraphRAG)
    - como estruturar o conhecimento
    - *Raciocínio interno:* usa **ReAct** para avaliar as características da base de conhecimento e decidir a melhor estratégia

- **Tool Planner**
    - quais ferramentas o agente precisa
    - como integrá-las (Function Calling, MCP, Code Interpreter, Browser)
    - *Raciocínio interno:* usa **ReAct** para mapear tarefas do agente em ferramentas disponíveis

- **Prompt Engineer Agent**
    - gerar prompts
    - estruturar instruções
    - definir comportamento do agente (procedural memory)
    - *Raciocínio interno:* usa **Reflexion** — gera o prompt, avalia, critica e refina iterativamente

- **Guardrail Designer**
    - políticas de comportamento
    - validações de saída (input/output guardrails)
    - configuração de human-in-the-loop quando necessário
    - *Raciocínio interno:* usa **Chain-of-Thought** para mapear riscos do domínio em regras de guardrail

- **Evaluation Agent**
    - testes
    - cenários de validação
    - *Raciocínio interno:* usa **LLM-as-judge** para avaliar os outputs do agente gerado e **trajectory evals** para validar o caminho de raciocínio

### Step Interviewers — Validação Conversacional por Etapa

Cada etapa do fluxo de criação possui um agente entrevistador especializado. Em vez de o usuário preencher um campo estático e avançar, o sistema analisa o que foi fornecido e, se não for suficiente, abre um ciclo de perguntas para coletar mais informações antes de prosseguir.

Esse é o mecanismo que garante que o `PromptEngineer` e o `Agent Architect` recebam informações ricas e precisas — não descrições vagas.

| Etapa | Step Interviewer | Critérios de suficiência | Exemplos de perguntas |
|---|---|---|---|
| Ideia | `IdeaInterviewer` | Propósito claro, domínio definido, público-alvo, exemplos de tarefas | "Que tipo de contrato? Quem vai usar?" |
| Entradas | `InputInterviewer` | Campos completos, tipos corretos, obrigatoriedade definida | "Esse campo é sempre obrigatório?" |
| RAG | `KnowledgeInterviewer` | Volume estimado, frequência de atualização, tipo de consulta | "Esses docs atualizam com frequência?" |
| Ferramentas | `ToolInterviewer` | Alinhamento tools ↔ tarefas reais do agente | "Ele só analisa código ou também executa?" |
| Guardrails | `GuardrailInterviewer` | Riscos do domínio mapeados, restrições de conteúdo | "Tem dados sensíveis que nunca devem vazar?" |

**Fluxo de cada entrevista:**

```
Usuário fornece input da etapa
        ↓
[StepInterviewer] avalia contra critérios de suficiência
        ↓
  suficiente? ──→ sim → consolida em StepSummary estruturado → avança
       │
       └──→ não → gera perguntas cirúrgicas → usuário responde → reavalia
```

**Estado persistido:** A criação de um agente passa a ser um processo multi-turn, com o estado de cada etapa salvo no banco como `creation_session`. O usuário pode pausar e retomar em qualquer ponto.

```json
{
  "session_id": "cs_xyz",
  "agent_id": "agt_abc",
  "current_step": "rag",
  "steps": {
    "idea":   { "status": "complete", "summary": { ... } },
    "inputs": { "status": "complete", "summary": { ... } },
    "rag":    { "status": "interviewing", "conversation": [ ... ] },
    "tools":  { "status": "pending" },
    "guardrails": { "status": "pending" }
  }
}
```

## 5. Fluxo de Criação de um Agente

### Etapa 1 - Ideia do Agente

Usuário descreve:

- o que o agente deve fazer
- quem vai usar
- exemplos de tarefas

> **`IdeaInterviewer` entra em ação:** analisa a descrição fornecida. Se estiver vaga (ex: "quero um agente de contratos"), abre um diálogo de clarificação: *"Que tipo de contrato? O agente vai redigir, revisar ou extrair dados? Quem vai usar — você mesmo ou clientes?"*. Só avança quando propósito, domínio, público-alvo e exemplos de tarefas estiverem claros. O resultado consolidado é um `IdeaSummary` estruturado que alimenta o **Agent Architect**.

### Etapa 2 - Planejamento da Arquitetura

O motor gera: **Agent Architecture Blueprint**

Esse blueprint inclui:

- tipo do agente (Single Agent ou Multi-Agent)
- padrão de orquestração (se multi-agente)
- padrão de raciocínio (ReAct, CoT, Plan-and-Execute, Reflexion...)
- componentes necessários
- ferramentas
- estratégia de RAG (se necessário)
- camadas de memória
- guardrails recomendados
- fluxo de execução

> O **Agent Architect** usa **Plan-and-Execute** para gerar o blueprint a partir do `IdeaSummary`. Ao final, o **Supervisor Pattern** valida a coerência do blueprint antes de apresentar ao usuário para confirmação ou ajuste. O usuário pode editar o blueprint antes de prosseguir.

### Etapa 3 - Configuração das Entradas

Usuário define:

- campos de entrada
- descrição de cada campo

> **`InputInterviewer` entra em ação:** verifica se os campos definidos são suficientes e bem descritos. Pergunta sobre obrigatoriedade, tipos de dado e se há campos que o blueprint sugere mas o usuário não configurou. Ex: *"O blueprint sugere um campo 'documento'. Ele sempre será enviado ou é opcional?"*

### Etapa 4 - Configuração de Conhecimento (RAG)

Usuário pode:

- subir documentos
- conectar bases de dados

> O **RAG Designer** já terá sugerido a estratégia (Naive / Advanced / Agentic / GraphRAG) no blueprint. **`KnowledgeInterviewer` entra em ação:** valida se as informações sobre a base de conhecimento são suficientes para configurar o RAG corretamente. Pergunta sobre volume estimado de documentos, frequência de atualização e tipo de consulta esperada. Ex: *"Esses documentos atualizam com frequência? Isso influencia se devemos usar ingestão incremental."* O motor então configura automaticamente o banco vetorial e o pipeline de ingestão.

### Etapa 5 - Ferramentas

Usuário escolhe as ferramentas sugeridas e/ou cria ferramentas customizadas.

> O **Tool Planner** terá sugerido Function Calling, MCP, Code Interpreter ou Browser conforme o tipo de agente. **`ToolInterviewer` entra em ação:** valida o alinhamento entre as ferramentas escolhidas e as tarefas reais do agente. Ex: *"Você quer que ele execute código Python ou apenas analise e sugira código? Isso muda se precisamos de Code Interpreter com sandbox."* Ferramentas customizadas são definidas via schema de Function Calling ou como MCP Servers.

### Etapa 6 - Guardrails

Sistema sugere regras de segurança.

> O **Guardrail Designer** propõe input/output guardrails com base no domínio. **`GuardrailInterviewer` entra em ação:** mapeia riscos específicos do contexto do agente que o Guardrail Designer pode não ter detectado automaticamente. Ex: *"O agente vai lidar com dados médicos? Isso exige filtros de PII mais rigorosos."* e *"Há ações que o agente propõe mas que exigem aprovação humana antes de executar?"* O usuário pode aceitar, ajustar ou adicionar regras.

### Etapa 7 - Testes (Evals)

O sistema gera:

- cenários de teste
- perguntas de validação
- métricas de qualidade

> O **Evaluation Agent** gera casos de teste com base no `IdeaSummary` e no blueprint completo. Usa **LLM-as-judge** (outro modelo avaliando as respostas) e **trajectory evals** (avaliando o caminho percorrido pelo agente, não só o resultado final). Ferramentas como LangSmith ou Braintrust podem ser usadas para instrumentar e registrar os traces.

### Etapa 8 — Deploy do Agente

O agente passa a rodar dentro da própria plataforma.

## 6. Execução dos Agentes

Os agentes criados rodam dentro da própria aplicação.

**Limitações iniciais:**

- Entradas suportadas:
- texto
- imagens

**Saídas suportadas:**

- texto
- JSON estruturado
- markdown
- fluxos
- imagem (posteriormente)

> **Stack relevante:** Cada agente em execução opera em seu próprio **ReAct loop** (ou no padrão configurado). O runtime da plataforma precisa gerenciar: contexto ativo (in-context memory), acesso ao banco vetorial (external memory via RAG), histórico de sessões (episodic memory) e chamadas a ferramentas (function calling / MCP). O grafo de execução (LangGraph ou similar) orquestra o fluxo de cada agente em tempo real.

## 7. Playground de Agentes

A plataforma terá um Playground avançado onde o usuário pode:

- testar o agente
- editar prompts
- ajustar ferramentas
- modificar guardrails
- testar cenários

Esse playground funciona como um ambiente de engenharia do agente.

> **Stack relevante:** O Playground deve expor os **traces de execução** (cada passo do ReAct loop, chamadas a ferramentas, outputs intermediários) para que o usuário entenda o raciocínio do agente. Ferramentas como **LangSmith** ou **Braintrust** são candidatas para instrumentar esse observability. O usuário também pode ativar **Extended Thinking** para modelos que suportam scratchpad interno e visualizar o raciocínio.

### Motor como Assistente no Playground

O motor não para na criação do agente — ele permanece disponível como assistente dentro do Playground. Para cada elemento editável, o usuário tem acesso a ações assistidas por IA:

**No editor de System Prompt:**

- **"Melhorar Prompt"** — motor reescreve o prompt mantendo a intenção original, mas tornando-o mais preciso, estruturado e eficiente
- **"Adicionar exemplos (few-shot)"** — motor gera exemplos de input/output específicos do domínio para adicionar ao prompt
- **"Detectar inconsistências"** — motor verifica se o prompt está alinhado com as ferramentas configuradas, os campos de entrada e os guardrails (ex: o prompt menciona fazer buscas web mas `web_search` não está habilitada)
- **"Explicar este prompt"** — motor descreve em linguagem simples o que cada bloco do prompt faz e por que

**Após uma conversa de teste:**

- **"Analisar esta conversa"** — motor revisa o trace completo e aponta o que funcionou bem e o que falhou
- **"Por que o agente fez isso?"** — usuário seleciona um step específico do trace e o motor explica a decisão tomada pelo agente naquele ponto
- **"Sugerir melhoria baseada nesta conversa"** — motor propõe mudanças concretas no prompt ou nos guardrails com base no que observou (ex: *"O agente demorou 4 steps para chegar à resposta. Adicione uma instrução de objetividade no prompt."*)
- **"Gerar mais casos parecidos"** — motor cria variações do input testado para cobrir edge cases do mesmo tipo

**No editor de Guardrails:**

- **Validar regra customizada** — ao escrever uma regra manualmente, o motor avalia se está bem formada e sem ambiguidade
- **"Sugerir guardrails adicionais"** — baseado nos resultados das conversas de teste, o motor propõe novas regras para cobrir falhas observadas
- **Detecção de conflito** — motor avisa quando duas regras de guardrail se contradizem

**No editor do Blueprint (após geração):**

- **Impacto de mudança** — ao alterar o tipo de agente ou padrão de orquestração, o motor explica as implicações: *"Mudar para Multi-Agent vai exigir que você defina como os subagentes se comunicam e aumentará a latência média."*
- **"Por que você escolheu isso?"** — o motor explica em linguagem simples cada decisão arquitetural do blueprint original

## 8. Sistema de Testes (Evals)

Cada agente terá um sistema de avaliação. O sistema pode gerar automaticamente:

- casos de teste
- inputs simulados
- métricas de qualidade

Exemplos de métricas:

- precisão
- aderência ao formato
- uso correto de ferramentas
- consistência das respostas

### Motor como Analista de Resultados

Após rodar os evals, o motor não só apresenta as métricas — ele interpreta os resultados e propõe ações:

- **Análise de padrões de falha** — motor agrupa os casos que falharam e identifica o padrão comum: *"67% das falhas ocorrem quando a query tem mais de uma pergunta. O agente não está decompondo perguntas compostas."*
- **Sugestões concretas de melhoria** — motor traduz cada padrão de falha em uma ação específica: mudança no prompt, novo guardrail, troca de ferramenta ou ajuste no RAG
- **Priorização** — motor rankeia quais problemas impactam mais a qualidade e sugere a ordem de correção
- **Regressão entre versões** — ao rodar evals em uma nova versão do agente, o motor detecta automaticamente se houve regressão em relação à versão anterior e explica o que mudou no comportamento

> **Stack relevante — Tipos de Evals que o motor suporta:**
> - **Offline evals** — benchmarks com datasets anotados, rodados antes do deploy para validar o comportamento base do agente
> - **LLM-as-judge** — outro modelo (ex: Claude Opus ou GPT-4) avalia os outputs gerados e pontua qualidade, correção e aderência às instruções
> - **Trajectory evals** — avalia o caminho percorrido pelo agente (quais ferramentas usou, quantos passos tomou, se o raciocínio foi coerente), não só o resultado final. Especialmente útil para agentes multi-step.
> - **RAGAS** — framework especializado para avaliar pipelines de RAG (faithfulness, relevance, context recall)
>
> **Ferramentas:** LangSmith, Braintrust, PromptFoo, Evals da OpenAI, RAGAS (para RAG).

## 9. Motor como Assistente Contínuo — Mapa Completo

> O motor não é apenas o componente que cria o agente. Ele é um assistente permanente em toda a plataforma. Abaixo está o mapa completo de onde e como ele atua além da criação inicial.

### 9.1 Durante a Criação (Step Interviewers)

Coberto na Seção 4 e 5. O motor valida e enriquece cada etapa da criação antes de avançar.

### 9.2 No Playground (Assistência à Edição)

Coberto na Seção 7. O motor atua como co-piloto no editor: melhora prompts, analisa traces, detecta inconsistências, explica decisões.

### 9.3 Nos Evals (Interpretação de Resultados)

Coberto na Seção 8. O motor analisa os resultados, identifica padrões de falha e propõe correções concretas com priorização.

### 9.4 No RAG — Após Ingestão de Documentos

Após o usuário subir os documentos ou conectar uma base:

- **Análise da base** — motor amostra os documentos ingeridos e avalia a qualidade dos chunks: detecta chunks muito curtos, sem contexto suficiente, ou com sobreposição excessiva
- **Revisão da estratégia** — motor verifica se a estratégia de RAG escolhida ainda faz sentido para o tipo de conteúdo ingerido. Ex: *"Seus documentos têm muitas tabelas e dados estruturados. Considere usar busca híbrida em vez de só semântica."*
- **Sugestão de chunking** — motor recomenda ajuste na estratégia de chunking com base no padrão do conteúdo (docs longos, FAQs curtos, contratos com cláusulas numeradas etc.)
- **Teste de retrieval** — motor executa queries simuladas e mostra quais chunks estão sendo recuperados, apontando se o retrieval está trazendo contexto relevante ou ruído

### 9.5 Na Configuração de Ferramentas Customizadas

Quando o usuário cria uma ferramenta customizada (via Function Calling schema):

- **Validação do schema** — motor valida se o schema está bem formado, os parâmetros bem descritos e os tipos corretos
- **Review de segurança** — motor detecta ferramentas com ações destrutivas ou irreversíveis (deletar dados, enviar e-mails, fazer chamadas a APIs externas) e sugere adicionar human-in-the-loop para essas ações específicas
- **Geração de casos de teste** — motor cria inputs de teste para a ferramenta e verifica se o agente a chama corretamente nos cenários esperados

### 9.6 Revisão Pré-Deploy (Deploy Reviewer)

Antes do agente ser colocado em produção, um agente revisor executa um **pre-flight check** completo:

```
[Deploy Reviewer]
    ├── Prompt cobre todos os campos de entrada definidos?
    ├── Todas as ferramentas têm descrições claras para o LLM usar corretamente?
    ├── Guardrails estão configurados para o domínio do agente?
    ├── RAG foi testado com queries reais?
    ├── Evals foram rodados e aprovados?
    └── Há ações irreversíveis sem human-in-the-loop configurado?
```

Se qualquer item falhar, o Deploy Reviewer bloqueia o deploy e apresenta o problema com uma sugestão de correção. O usuário pode ignorar avisos não-críticos, mas não pode ignorar bloqueios de segurança.

### 9.7 Monitoramento Pós-Deploy (Health Monitor)

Após o agente estar em produção, o motor monitora as execuções em andamento:

- **Alertas de degradação** — motor detecta quando a taxa de falhas de tool calls ou a qualidade das respostas caem abaixo de um threshold
- **Padrões emergentes** — motor identifica novos tipos de queries que o agente não estava preparado para responder e notifica o usuário
- **Sugestão de update** — motor propõe atualizações no prompt ou guardrails com base nos padrões observados em produção: *"Nas últimas 50 conversas, 30% dos usuários perguntaram sobre X, que está fora do escopo atual do agente. Deseja expandir o escopo?"*
- **Comparação de versões** — ao fazer um update, motor explica em linguagem natural as diferenças comportamentais entre a versão anterior e a nova antes de fazer o deploy

### 9.8 Adaptação e Clonagem de Agentes

- **"Adaptar para novo domínio"** — usuário tem um agente jurídico e quer um agente médico. Motor adapta o blueprint, reescreve o prompt para o novo domínio e sugere quais guardrails e ferramentas precisam mudar
- **"Criar variante"** — usuário quer uma versão mais restrita do mesmo agente (ex: versão para clientes finais com mais guardrails, vs versão para equipe interna com mais liberdade). Motor gera o blueprint derivado automaticamente

---

## 10. Arquitetura Técnica da Plataforma

**Backend**

- Python
- FastAPI

**Motor de agentes**

- LangGraph — grafos de execução para agentes multi-step e multi-agente
- OpenAI Agents SDK — alternativa para agentes com handoff e swarm
- Autogen (Microsoft) — alternativa para sistemas multi-agente conversacionais
- framework próprio — possível para lógica específica da plataforma

**Banco de dados**

- PostgreSQL — dados da plataforma, configurações dos agentes, memória episódica e semântica

**Vetores (RAG)**

- pgvector — integrado ao PostgreSQL, adequado para volume inicial
- Weaviate — para RAG avançado com suporte a GraphRAG e filtros híbridos
- Qdrant — alta performance para grandes volumes de vetores

**Guardrails**

- Guardrails AI — framework Python para validação de inputs e outputs
- NeMo Guardrails (NVIDIA) — para políticas de comportamento mais complexas
- LlamaGuard (Meta) — para classificação de conteúdo e segurança

**Observability e Evals**

- LangSmith — tracing de execução, visualização de traces e LLM-as-judge
- Braintrust — plataforma de evals com suporte a LLM-as-judge e datasets
- PromptFoo — testes e comparação de prompts
- RAGAS — avaliação específica de pipelines RAG

**Execução de agentes**

- pipelines
- grafos de execução (LangGraph)

**Interface**

- React
- Next.js

---

## 11. Arquitetura Técnica do Sistema

### 11.1 Visão Geral da Arquitetura

O sistema segue os princípios da **Clean Architecture** combinados com **Vertical Slice Architecture** organizada por features. Essa combinação resolve dois problemas simultaneamente: mantém o domínio da aplicação isolado de frameworks externos (FastAPI, LangGraph, SQLAlchemy), e organiza o código por capacidade de negócio em vez de por camada técnica — o que torna o sistema naturalmente extensível.

```
┌─────────────────────────────────────────────────────────────┐
│                         apps/                               │
│   ┌─────────────────┐         ┌─────────────────────────┐  │
│   │   api (FastAPI) │         │   worker (ARQ/Celery)   │  │
│   └────────┬────────┘         └────────────┬────────────┘  │
└────────────┼──────────────────────────────┼────────────────┘
             │                              │
┌────────────▼──────────────────────────────▼────────────────┐
│                       features/                             │
│  agent_creation │ agent_execution │ rag │ tools │ memory   │
│  guardrails     │ evals           │ playground              │
└────────────────────────────┬───────────────────────────────┘
                             │ usa interfaces de
┌────────────────────────────▼───────────────────────────────┐
│                         core/                               │
│           domain │ ports (interfaces) │ shared              │
└────────────────────────────┬───────────────────────────────┘
                             │ implementado por
┌────────────────────────────▼───────────────────────────────┐
│                     infrastructure/                         │
│  database │ vector_store │ llm │ messaging │ observability  │
└─────────────────────────────────────────────────────────────┘
```

**Princípios que guiam as decisões arquiteturais:**

- **Dependências apontam para dentro:** `infrastructure` depende de `core`, `features` depende de `core`. `core` não depende de nada externo.
- **Cada feature é uma ilha:** um módulo de feature não importa diretamente de outro módulo de feature. Comunicação entre features acontece via eventos ou via serviços do `core`.
- **Extensibilidade via interfaces:** trocar PostgreSQL por outro banco, ou LangGraph por outro framework de agentes, exige mudar apenas a camada `infrastructure` — o restante do sistema não sabe a diferença.
- **Features são ativáveis/desativáveis:** cada módulo registra suas próprias rotas e dependências, e pode ser habilitado ou não via `config/features.py`.

---

### 11.2 Estrutura de Diretórios do Projeto

```
agent-engine/
│
├── apps/
│   ├── api/                         # Entrypoint FastAPI
│   │   ├── main.py                  # Inicialização, registro de features
│   │   ├── dependencies.py          # Injeção de dependências global
│   │   ├── exception_handlers.py
│   │   └── middleware/
│   │       ├── auth.py
│   │       └── logging.py
│   │
│   └── worker/                      # Workers assíncronos (execução de agentes)
│       ├── main.py
│       └── tasks/
│           ├── agent_execution.py
│           └── rag_ingestion.py
│
├── core/                            # Domínio puro — zero dependências externas
│   ├── domain/
│   │   ├── agent/
│   │   │   ├── entities.py          # Agent, Blueprint, AgentConfig
│   │   │   ├── value_objects.py     # AgentType, RAGStrategy, MemoryLayer, ToolType
│   │   │   └── events.py            # AgentCreated, AgentDeployed, BlueprintGenerated
│   │   ├── execution/
│   │   │   ├── entities.py          # Execution, ExecutionStep, Message, Trace
│   │   │   └── events.py            # ExecutionStarted, ExecutionCompleted, ToolCalled
│   │   └── user/
│   │       └── entities.py          # User, Workspace
│   │
│   ├── ports/                       # Interfaces que a infra deve implementar
│   │   ├── repositories.py          # IAgentRepository, IExecutionRepository
│   │   ├── llm_provider.py          # ILLMProvider
│   │   ├── vector_store.py          # IVectorStore
│   │   ├── tool_executor.py         # IToolExecutor
│   │   ├── event_bus.py             # IEventBus
│   │   └── observability.py        # ITracer
│   │
│   └── shared/
│       ├── result.py                # Result[T, E] — tratamento funcional de erros
│       ├── pagination.py
│       └── exceptions.py           # Exceções de domínio
│
├── features/                        # Módulos de feature (vertical slices)
│   │
│   ├── agent_creation/              # Motor de criação — core differentiator
│   │   ├── __init__.py              # register(app, settings) — ponto de ativação
│   │   ├── router.py                # POST /agents/create, POST /sessions/{id}/message
│   │   ├── service.py               # CreationOrchestrator — coordena agentes internos
│   │   ├── internal_agents/         # Sistema multi-agente interno do motor
│   │   │   ├── orchestrator.py      # Recebe ideia, coordena os subagentes abaixo
│   │   │   ├── agent_architect.py   # Decide tipo, padrão de orquestração, raciocínio
│   │   │   ├── rag_designer.py      # Decide se/qual estratégia de RAG usar
│   │   │   ├── tool_planner.py      # Decide quais ferramentas e como integrá-las
│   │   │   ├── prompt_engineer.py   # Gera e refina o system prompt (Reflexion)
│   │   │   ├── guardrail_designer.py
│   │   │   └── evaluation_agent.py  # Gera casos de teste iniciais
│   │   ├── step_interviewers/       # Validação conversacional por etapa
│   │   │   ├── base.py              # IStepInterviewer — interface base
│   │   │   ├── idea.py              # IdeaInterviewer — valida descrição inicial
│   │   │   ├── inputs.py            # InputInterviewer — valida campos de entrada
│   │   │   ├── knowledge.py         # KnowledgeInterviewer — valida config de RAG
│   │   │   ├── tools.py             # ToolInterviewer — valida alinhamento de tools
│   │   │   └── guardrails.py        # GuardrailInterviewer — mapeia riscos do domínio
│   │   ├── session/
│   │   │   ├── manager.py           # CreationSessionManager — persiste estado multi-turn
│   │   │   └── schemas.py           # CreationSession, StepStatus, StepSummary
│   │   ├── blueprint/
│   │   │   ├── generator.py         # Produz o AgentArchitectureBlueprint
│   │   │   ├── validator.py         # Supervisor — valida coerência do blueprint
│   │   │   └── schemas.py           # BlueprintSchema, ArchitectureDecision
│   │   └── schemas.py               # CreateAgentRequest, CreateAgentResponse
│   │
│   ├── agent_execution/             # Runtime de execução dos agentes criados
│   │   ├── __init__.py
│   │   ├── router.py                # POST /agents/{id}/run, GET /executions/{id}
│   │   ├── service.py               # ExecutionService
│   │   ├── runtime/
│   │   │   ├── runner.py            # AgentRunner — executa o grafo do agente
│   │   │   ├── graph_builder.py     # Constrói grafo LangGraph a partir do blueprint
│   │   │   ├── context_manager.py   # Gerencia janela de contexto (in-context memory)
│   │   │   └── streaming.py         # SSE / WebSocket para output em tempo real
│   │   └── schemas.py
│   │
│   ├── rag/                         # Módulo RAG completo
│   │   ├── __init__.py
│   │   ├── router.py                # POST /rag/ingest, POST /rag/query
│   │   ├── service.py               # RAGService — facade para as estratégias
│   │   ├── strategies/              # Strategy Pattern
│   │   │   ├── base.py              # IRAGStrategy (protocolo/interface)
│   │   │   ├── naive.py             # embed → similaridade → injeta
│   │   │   ├── advanced.py          # + reranking, query expansion, HyDE
│   │   │   ├── agentic.py           # agente decide quando/como buscar
│   │   │   └── graph_rag.py         # Knowledge Graph + vetores
│   │   ├── ingestion/
│   │   │   ├── pipeline.py          # Orquestra ingestão de documentos
│   │   │   ├── chunkers.py          # Estratégias de chunking (fixed, semantic, etc.)
│   │   │   └── embedders.py         # Wrapper para modelos de embedding
│   │   └── schemas.py
│   │
│   ├── tools/                       # Registry de ferramentas
│   │   ├── __init__.py
│   │   ├── registry.py              # ToolRegistry — registro central de ferramentas
│   │   ├── executor.py              # ToolExecutor — executa tool calls do agente
│   │   ├── builtin/                 # Ferramentas nativas da plataforma
│   │   │   ├── web_search.py
│   │   │   ├── code_interpreter.py  # Sandbox Python (e2b ou similar)
│   │   │   ├── database_query.py
│   │   │   └── image_generation.py
│   │   └── schemas.py               # ToolDefinition, ToolCall, ToolResult
│   │
│   ├── guardrails/                  # Módulo de guardrails
│   │   ├── __init__.py
│   │   ├── service.py               # GuardrailService — aplica input/output guardrails
│   │   ├── adapters/                # Adapter Pattern para frameworks externos
│   │   │   ├── base.py              # IGuardrailAdapter
│   │   │   ├── guardrails_ai.py
│   │   │   ├── nemo.py
│   │   │   └── llama_guard.py
│   │   ├── validators/
│   │   │   ├── input_validator.py
│   │   │   └── output_validator.py
│   │   └── schemas.py               # GuardrailPolicy, ValidationResult
│   │
│   ├── memory/                      # Gerenciamento de memória dos agentes
│   │   ├── __init__.py
│   │   ├── service.py               # MemoryService — facade para as camadas
│   │   ├── layers/
│   │   │   ├── episodic.py          # Histórico de sessões (PostgreSQL)
│   │   │   ├── semantic.py          # Fatos persistidos sobre domínio/usuário
│   │   │   └── working.py           # Gerencia o que entra na janela de contexto
│   │   └── schemas.py
│   │
│   ├── evals/                       # Sistema de avaliação
│   │   ├── __init__.py
│   │   ├── router.py                # POST /evals/run, GET /evals/{agent_id}
│   │   ├── service.py               # EvalService
│   │   ├── judges/
│   │   │   ├── llm_judge.py         # LLM-as-judge (pontua qualidade das respostas)
│   │   │   └── trajectory_judge.py  # Avalia o caminho percorrido pelo agente
│   │   ├── generators/
│   │   │   └── test_case_generator.py  # Gera casos de teste automaticamente
│   │   ├── adapters/
│   │   │   ├── ragas_adapter.py     # Integração RAGAS para RAG evals
│   │   │   └── langsmith_adapter.py
│   │   └── schemas.py               # EvalCase, EvalResult, EvalMetrics
│   │
│   ├── playground/                  # Backend do Playground
│   │   ├── __init__.py
│   │   ├── router.py                # WebSocket /playground/{agent_id}
│   │   ├── service.py               # PlaygroundService
│   │   ├── assistants/              # Motor como assistente no Playground
│   │   │   ├── prompt_assistant.py  # Melhora, explica e detecta inconsistências no prompt
│   │   │   ├── trace_analyst.py     # Analisa conversas de teste e sugere melhorias
│   │   │   └── guardrail_assistant.py  # Valida e sugere guardrails
│   │   └── schemas.py
│   │
│   ├── deploy_review/               # Revisão pré-deploy
│   │   ├── __init__.py
│   │   ├── router.py                # POST /agents/{id}/review
│   │   ├── service.py               # DeployReviewService
│   │   ├── checklist.py             # Checks: prompt, tools, guardrails, evals, RAG, HITL
│   │   └── schemas.py               # ReviewReport, CheckResult, BlockingIssue
│   │
│   └── monitoring/                  # Monitoramento pós-deploy
│       ├── __init__.py
│       ├── router.py                # GET /agents/{id}/health
│       ├── service.py               # HealthMonitorService
│       ├── analyzers/
│       │   ├── failure_pattern.py   # Identifica padrões de falha nas execuções
│       │   ├── drift_detector.py    # Detecta degradação de qualidade ao longo do tempo
│       │   └── scope_analyzer.py    # Detecta queries fora do escopo do agente
│       └── schemas.py               # HealthReport, Alert, ImprovementSuggestion
│
├── infrastructure/                  # Implementações concretas dos ports
│   ├── database/
│   │   ├── connection.py            # SQLAlchemy engine + session factory
│   │   ├── migrations/              # Alembic migrations
│   │   └── repositories/            # Implementações concretas dos IRepository
│   │       ├── agent_repository.py
│   │       ├── execution_repository.py
│   │       └── creation_session_repository.py  # Persiste estado multi-turn da criação
│   │
│   ├── vector_store/
│   │   ├── pgvector_adapter.py      # IVectorStore → pgvector
│   │   ├── weaviate_adapter.py      # IVectorStore → Weaviate
│   │   └── qdrant_adapter.py        # IVectorStore → Qdrant
│   │
│   ├── llm/
│   │   ├── anthropic_adapter.py     # ILLMProvider → Anthropic (Claude)
│   │   ├── openai_adapter.py        # ILLMProvider → OpenAI
│   │   └── litellm_adapter.py       # ILLMProvider → LiteLLM (multi-provider)
│   │
│   ├── observability/
│   │   ├── langsmith_adapter.py     # ITracer → LangSmith
│   │   └── braintrust_adapter.py    # ITracer → Braintrust
│   │
│   ├── messaging/
│   │   └── redis_bus.py             # IEventBus → Redis Streams
│   │
│   └── cache/
│       └── redis_cache.py
│
├── config/
│   ├── settings.py                  # Pydantic Settings — variáveis de ambiente
│   ├── features.py                  # Feature flags — o que está ativo
│   └── logging.py
│
└── tests/
    ├── unit/                        # Testa core/domain e lógica de features isolada
    ├── integration/                 # Testa features com infra real (DB, Redis)
    └── e2e/                         # Testa fluxos completos via API
```

---

### 11.3 Módulos Principais do Sistema

| Módulo | Responsabilidade | Pode ser desativado? |
|---|---|---|
| `agent_creation` | Motor de criação — gera blueprints e conduz Step Interviewers | Não (core) |
| `agent_execution` | Runtime — executa os agentes criados | Não (core) |
| `rag` | Pipeline de RAG — ingestão, análise e retrieval | Sim |
| `tools` | Registry e execução de ferramentas | Parcial (registry sempre ativo, tools individuais ativáveis) |
| `guardrails` | Validação de inputs e outputs | Sim |
| `memory` | Camadas de memória (episódica, semântica) | Parcial (working memory sempre ativa) |
| `evals` | Avaliação, análise de falhas e sugestões de melhoria | Sim |
| `playground` | Ambiente de teste + assistentes de edição | Sim |
| `deploy_review` | Pre-flight check antes do deploy | Sim |
| `monitoring` | Health Monitor pós-deploy e alertas de degradação | Sim |

---

### 11.4 Explicação Detalhada dos Módulos

#### `core/` — O Coração do Sistema

**Responsabilidade:** Contém as entidades de domínio, regras de negócio e interfaces (ports). É o único módulo que não depende de nada externo — nem FastAPI, nem SQLAlchemy, nem LangGraph.

**Por que isso importa:** Se o LangGraph for substituído por outro framework de grafo, ou se o banco mudar de PostgreSQL para outro, o `core` não é tocado. Apenas a implementação em `infrastructure/` muda.

**Componentes principais:**

- `domain/agent/entities.py` — define as entidades centrais:
  - `Agent` — representa um agente criado pelo usuário (id, nome, blueprint, status)
  - `Blueprint` — a arquitetura projetada pelo motor (tipo, padrão de orquestração, raciocínio, componentes)
  - `AgentConfig` — configuração completa e persistida do agente

- `domain/agent/value_objects.py` — tipos imutáveis sem identidade:
  - `AgentType` — enum: `SINGLE_AGENT`, `MULTI_AGENT`
  - `OrchestrationPattern` — enum: `ORCHESTRATOR_SUBAGENTS`, `HANDOFF_SWARM`, `SUPERVISOR`, `A2A`
  - `ReasoningPattern` — enum: `REACT`, `COT`, `PLAN_AND_EXECUTE`, `REFLEXION`
  - `RAGStrategy` — enum: `NAIVE`, `ADVANCED`, `AGENTIC`, `GRAPH_RAG`
  - `MemoryLayer` — enum: `IN_CONTEXT`, `EPISODIC`, `SEMANTIC`, `EXTERNAL_RAG`

- `ports/` — interfaces que a infra implementa. O `core` nunca importa da `infrastructure`; ele define o contrato e espera que a injeção de dependências forneça a implementação correta em runtime.

---

#### `features/agent_creation/` — Motor de Criação (Core Differentiator)

**Responsabilidade:** Implementa o Agent Creation Engine. Quando o usuário descreve o agente que quer, este módulo orquestra os agentes internos para gerar o `Blueprint` completo.

**Fluxo interno:**

```
CreationOrchestrator (service.py)
    │
    ├── AgentArchitect      → decide: tipo, orquestração, raciocínio
    ├── RAGDesigner         → decide: estratégia RAG, estrutura do conhecimento
    ├── ToolPlanner         → decide: quais ferramentas, como integrá-las
    ├── PromptEngineer      → gera e refina o system prompt (loop Reflexion)
    ├── GuardrailDesigner   → propõe input/output guardrails
    └── EvaluationAgent     → gera casos de teste iniciais
         │
         ▼
    BlueprintGenerator  → consolida em um AgentArchitectureBlueprint
         │
         ▼
    BlueprintValidator  → Supervisor Pattern — valida coerência
```

**Tecnologias:** O `CreationOrchestrator` usa LangGraph internamente para coordenar os subagentes. Cada subagente é um nó no grafo com seu próprio system prompt e lógica de raciocínio (CoT, Plan-and-Execute, Reflexion conforme a Seção 4).

**Como se conecta:** Expõe rotas via `router.py`. Persiste o blueprint via `IAgentRepository` (port) → `infrastructure/database/repositories/agent_repository.py` (implementação).

**Step Interviewers — subcomponente crítico:**

Os `StepInterviewers` são agentes especializados que tornam a criação um processo **conversacional e iterativo**, não um formulário estático. Cada interviewer opera em um loop:

```
recebe input do usuário
    ↓
avalia contra critérios de suficiência (scoring interno por critério)
    ↓
  suficiente? → sim → gera StepSummary estruturado → sinaliza etapa completa
       ↓
      não → gera perguntas cirúrgicas → aguarda resposta → reavalia
```

A interface base que todos implementam:

```python
# step_interviewers/base.py
class IStepInterviewer(Protocol):
    async def evaluate(self, conversation: list[Message]) -> InterviewResult: ...
    # retorna: { "sufficient": bool, "questions": list[str], "summary": dict | None }
```

O estado de toda a sessão de criação é persistido pelo `CreationSessionManager` no PostgreSQL, permitindo que o usuário pause e retome em qualquer etapa sem perder o progresso:

```
creation_sessions (tabela)
  session_id, agent_id, user_id, current_step,
  steps: JSONB {
    idea:       { status, conversation, summary },
    inputs:     { status, conversation, summary },
    rag:        { status, conversation, summary },
    tools:      { status, conversation, summary },
    guardrails: { status, conversation, summary }
  },
  created_at, updated_at
```

A rota `POST /sessions/{id}/message` recebe a mensagem do usuário, repassa ao interviewer da etapa atual, e retorna ou a próxima pergunta ou a confirmação de avanço para a próxima etapa.

---

#### `features/agent_execution/` — Runtime de Execução

**Responsabilidade:** Pega um `Blueprint` salvo e o executa em runtime. É o módulo que o usuário final toca quando "conversa" com um agente.

**Componentes críticos:**

- `graph_builder.py` — converte o `Blueprint` em um grafo LangGraph executável. É aqui que o tipo de agente, padrão de orquestração e ferramentas são traduzidos em nós e arestas do grafo.
- `runner.py` — executa o grafo, gerencia o loop ReAct, chama ferramentas via `ToolExecutor` e aplica guardrails antes/depois.
- `context_manager.py` — decide o que entra na janela de contexto a cada step: histórico da conversa, resultados RAG, memória semântica relevante.
- `streaming.py` — transmite tokens via SSE (Server-Sent Events) para o frontend em tempo real.

**Como se conecta:** Usa `ToolRegistry` (features/tools), `GuardrailService` (features/guardrails), `MemoryService` (features/memory) e `RAGService` (features/rag) — todos injetados via interface, sem import direto entre features.

---

#### `features/rag/` — Pipeline de RAG

**Responsabilidade:** Gerencia toda a stack de RAG: ingestão de documentos, geração de embeddings, armazenamento vetorial e retrieval.

**Strategy Pattern — o centro do design:**

```python
# base.py
class IRAGStrategy(Protocol):
    async def retrieve(self, query: str, agent_id: str, k: int) -> list[Document]: ...

# naive.py
class NaiveRAG(IRAGStrategy):
    async def retrieve(self, query, agent_id, k):
        embedding = await self.embedder.embed(query)
        return await self.vector_store.similarity_search(embedding, agent_id, k)

# advanced.py
class AdvancedRAG(IRAGStrategy):
    async def retrieve(self, query, agent_id, k):
        expanded = await self.query_expander.expand(query)
        results = await self.vector_store.hybrid_search(expanded, agent_id, k * 2)
        return await self.reranker.rerank(query, results, k)
```

O `RAGService` recebe a estratégia via injeção — `graph_builder.py` do módulo de execução instancia a estratégia correta baseado no `Blueprint.rag_strategy`.

**Banco vetorial via adapter:** O `IVectorStore` é implementado por `pgvector_adapter`, `weaviate_adapter` ou `qdrant_adapter`. O ativo é definido em `config/settings.py` (`VECTOR_STORE=pgvector`).

---

#### `features/tools/` — Registry de Ferramentas

**Responsabilidade:** Mantém um catálogo central de ferramentas disponíveis e executa as chamadas quando um agente usa uma tool.

**Plugin/Registry Pattern:**

```python
# registry.py
class ToolRegistry:
    _tools: dict[str, ToolDefinition] = {}

    @classmethod
    def register(cls, tool: ToolDefinition) -> None:
        cls._tools[tool.name] = tool

    @classmethod
    def get(cls, name: str) -> ToolDefinition:
        return cls._tools[name]

    @classmethod
    def list_for_agent(cls, agent_config: AgentConfig) -> list[ToolDefinition]:
        return [cls._tools[t] for t in agent_config.enabled_tools]
```

Ferramentas built-in se registram na inicialização do módulo. Ferramentas customizadas do usuário são registradas dinamicamente via API. Esse design permite que novas ferramentas sejam adicionadas sem tocar no código de execução.

---

#### `features/guardrails/` — Validação de Comportamento

**Responsabilidade:** Aplica as políticas de segurança e comportamento antes do input chegar ao agente e antes do output chegar ao usuário.

**Adapter Pattern:** Cada framework externo (Guardrails AI, NeMo, LlamaGuard) é encapsulado em um adapter que implementa `IGuardrailAdapter`. O `GuardrailService` não sabe qual framework está usando — apenas chama `.validate_input()` e `.validate_output()`.

**Integração com o runtime:** O `runner.py` do módulo de execução chama o `GuardrailService` em dois pontos do loop: antes de passar o input para o agente, e antes de retornar o output para o usuário. Isso é configurado via `Blueprint.guardrail_policy`.

---

#### `features/memory/` — Camadas de Memória

**Responsabilidade:** Gerencia as diferentes camadas de memória que um agente pode ter, conforme configurado no blueprint.

**Camadas:**

- `working.py` — decide o que entra na janela de contexto. Não persiste nada; opera em memória de processo. Sempre ativo.
- `episodic.py` — persiste histórico de conversas por `(agent_id, user_id, session_id)` no PostgreSQL. Ativado se `MemoryLayer.EPISODIC` está no blueprint.
- `semantic.py` — persiste fatos sobre o usuário/domínio. Usa PostgreSQL com JSON estruturado. Ativado se `MemoryLayer.SEMANTIC` está no blueprint.

**Criação automática:** Quando o motor cria um agente com memória episódica ou semântica, o `MemoryService` provisiona automaticamente as tabelas necessárias no PostgreSQL via migrações Alembic programáticas.

---

#### `features/evals/` — Sistema de Avaliação

**Responsabilidade:** Gera casos de teste automaticamente e avalia a qualidade dos agentes usando LLM-as-judge e trajectory evals.

**Fluxo:**

```
EvalService.run_eval(agent_id)
    │
    ├── TestCaseGenerator   → gera inputs simulados com base no blueprint e domínio
    ├── AgentRunner         → executa o agente para cada input (via features/agent_execution)
    ├── LLMJudge            → avalia qualidade, correção e aderência ao formato
    ├── TrajectoryJudge     → avalia: usou as ferramentas certas? quantos steps? raciocínio coerente?
    └── EvalResult          → agrega métricas e persiste o relatório
```

Para agentes com RAG, o `RAGASAdapter` adiciona métricas específicas: faithfulness (resposta fiel aos documentos), context recall (documentos relevantes foram recuperados), answer relevance.

---

### 11.5 Estratégia de Modularidade e Ativação de Features

A ativação de features é controlada por `config/features.py`, que usa Pydantic Settings para carregar do ambiente:

```python
# config/features.py
from pydantic_settings import BaseSettings

class FeaturesConfig(BaseSettings):
    # Features principais — sempre ativas
    agent_creation_enabled: bool = True
    agent_execution_enabled: bool = True

    # Features opcionais
    rag_enabled: bool = True
    rag_strategy: str = "naive"          # naive | advanced | agentic | graph_rag

    evals_enabled: bool = True
    playground_enabled: bool = True

    guardrails_enabled: bool = True
    guardrails_framework: str = "guardrails_ai"  # guardrails_ai | nemo | llama_guard

    memory_episodic_enabled: bool = True
    memory_semantic_enabled: bool = False        # off por padrão, opt-in

    # Infraestrutura
    vector_store: str = "pgvector"       # pgvector | weaviate | qdrant
    llm_provider: str = "anthropic"      # anthropic | openai | litellm
    observability_provider: str = "langsmith"    # langsmith | braintrust | none
```

Cada feature module expõe uma função `register(app, settings)` no seu `__init__.py`:

```python
# features/rag/__init__.py
def register(app: FastAPI, settings: FeaturesConfig) -> None:
    if not settings.rag_enabled:
        return
    strategy = RAGStrategyFactory.create(settings.rag_strategy)
    service = RAGService(strategy=strategy)
    router = build_router(service)
    app.include_router(router, prefix="/rag", tags=["rag"])
```

O `apps/api/main.py` itera e registra apenas as features ativas:

```python
# apps/api/main.py
from config.features import FeaturesConfig
import features.agent_creation as agent_creation
import features.agent_execution as agent_execution
import features.rag as rag
# ...

settings = FeaturesConfig()
app = FastAPI()

for feature_module in [agent_creation, agent_execution, rag, tools, guardrails, memory, evals, playground]:
    feature_module.register(app, settings)
```

Isso permite, por exemplo, rodar uma instância da plataforma sem RAG, ou sem Evals, apenas ajustando variáveis de ambiente — sem nenhuma alteração no código.

**Ferramentas individuais seguem o mesmo padrão** no `ToolRegistry`: cada ferramenta built-in verifica se está habilitada antes de se registrar:

```python
# features/tools/builtin/code_interpreter.py
def register(registry: ToolRegistry, settings: FeaturesConfig) -> None:
    if settings.code_interpreter_enabled:
        registry.register(CodeInterpreterTool())
```

---

### 11.6 Considerações de Engenharia

**Injeção de dependência via FastAPI**

Usar `Depends()` do FastAPI para injetar repositórios, serviços e adapters. Isso torna tudo testável: nos testes unitários, injeta-se mocks das interfaces; nos testes de integração, injeta-se as implementações reais.

**Separação entre criação e execução de agentes**

A criação de agente (motor, blueprint) é síncrona e relativamente rápida. A execução de agentes é assíncrona e pode ser longa (multi-step, RAG, tool calls). Por isso, execuções rodam em `apps/worker/` (workers ARQ ou Celery) e o resultado é entregue via streaming ou polling, não via resposta síncrona da API.

**LangGraph como detalhe de implementação**

O `graph_builder.py` é o único arquivo que importa LangGraph. Se o framework for trocado no futuro, apenas esse arquivo muda. O restante do sistema trabalha com as abstrações do `core/`.

**Migrations de banco por agente**

Quando um agente com memória episódica ou semântica é criado, o sistema roda Alembic programaticamente para criar as tabelas necessárias (`agent_{id}_episodic_memory`, `agent_{id}_semantic_store`). Isso mantém o schema versionado e reversível.

**Observability por padrão**

O `ITracer` é injetado em todos os serviços críticos (execução, RAG, evals). Com `observability_provider=none`, o adapter é um no-op. Com `langsmith` ou `braintrust`, os traces são enviados automaticamente. Isso significa que observability é zero-cost quando desativado e não polui o código de negócio.

**Versionamento do Blueprint**

O `Blueprint` é persistido como JSON versionado no PostgreSQL. Quando o usuário ajusta o agente no Playground, uma nova versão do blueprint é criada (não sobrescreve). Isso permite rollback e comparação entre versões do agente.

**Testes**

- `tests/unit/` — testam `core/domain` e lógica de features usando mocks das interfaces. Sem banco, sem rede.
- `tests/integration/` — testam features com PostgreSQL real via Docker Compose. Validam que repositórios, migrações e queries funcionam.
- `tests/e2e/` — testam fluxos completos via HTTP: criar agente → executar → avaliar.
