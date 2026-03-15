# Agents Stack — Referência Completa

Guia de referência sobre os principais conceitos, padrões e ferramentas para construção de sistemas baseados em agentes de IA.

---

### 1. Tipos de Agentes

**Single Agent** — Um único modelo com acesso a ferramentas, memória e instruções. Resolve tarefas de forma autônoma em loop (ReAct loop: Reason → Act → Observe).

**Multi-Agent Systems** — Múltiplos agentes colaborando, cada um com responsabilidades distintas. É o coração das arquiteturas modernas.

**Reactive Agent** — Age diretamente em resposta ao ambiente, sem estado interno persistente. Rápido, mas limitado para tarefas complexas.

**Deliberative Agent** — Mantém um modelo interno do mundo e planeja antes de agir. Mais lento, porém capaz de raciocínio de longo prazo.

**Autonomous Agent** — Executa tarefas longas com mínima intervenção humana. Exemplos: Devin, SWE-agent, OpenHands.

**Cognitive Architecture** — Agentes inspirados em psicologia cognitiva com módulos separados de percepção, memória, raciocínio e ação. Exemplo: SOAR, ACT-R adaptados para LLMs.

---

### 2. Padrões de Orquestração Multi-Agent

**Orchestrator → Subagents**
- Um agente "maestro" decompõe a tarefa e delega para agentes especialistas.
- Exemplo: um orquestrador recebe "analise este contrato" e delega para agente jurídico, agente financeiro e agente de risco.

**Agent-to-Agent (A2A)**
- Agentes se comunicam diretamente via protocolos padronizados (ver seção 10).
- Cada agente expõe uma interface e pode ser chamado por outros sem um orquestrador central.

**Handoff / Swarm**
- O agente atual "passa o bastão" para outro agente mais adequado conforme o contexto muda.
- Padrão popularizado pelo OpenAI Swarm e adotado no SDK de Agentes da Anthropic.

**Supervisor Pattern**
- Um agente supervisor avalia os outputs dos subagentes e decide se estão corretos antes de prosseguir.
- Garante qualidade sem precisar de revisão humana em cada etapa.

**Pipeline (Sequential)**
- Agentes executam em sequência, o output de um é o input do próximo.
- Simples e previsível; ideal quando as etapas têm dependência estrita.

**Map-Reduce**
- Um agente "mapeia" uma tarefa em N subtarefas paralelas, executa subagentes em paralelo, e um agente "reduce" consolida os resultados.
- Ideal para processamento de grandes volumes (ex: analisar 100 contratos ao mesmo tempo).

**DAG (Directed Acyclic Graph)**
- Grafo de dependências entre tarefas. Permite paralelismo onde possível e sequência onde necessário.
- Implementado nativamente no LangGraph e similares.

---

### 3. Memória

> (analisar melhor esse, pois talvez um BD com tabelas que o motor também consiga criar seja necessário)

| Tipo | Onde fica | Duração | Exemplo de uso |
|---|---|---|---|
| **In-context** | Janela de contexto do modelo | Só durante a sessão | Histórico da conversa atual |
| **External (RAG)** | Banco vetorial (pgvector, Pinecone, Weaviate) | Persistente | Base de conhecimento corporativa |
| **Episodic** | Banco de dados (SQL, NoSQL) | Persistente | Histórico de sessões passadas |
| **Semantic** | Embedding store + metadados | Persistente | Fatos sobre o usuário, preferências |
| **Procedural** | System prompt / CLAUDE.md | Persistente | Instruções e regras do agente |
| **Cache (KV)** | Cache do provedor (ex: prompt caching Anthropic) | Temporário | Reduzir custo de contextos repetidos |

**Estratégias de gestão de contexto:**
- **Summarization:** comprime histórico antigo em resumos para liberar tokens
- **Sliding window:** mantém apenas as N últimas mensagens no contexto
- **Memory consolidation:** periodicamente transfere memórias in-context para armazenamento externo

---

### 4. RAG (Retrieval-Augmented Generation)

**Naive RAG:** embed documento → busca por similaridade coseno → injeta chunks no contexto → gera resposta.

**Advanced RAG:**
- *Reranking:* usa um modelo cross-encoder para reordenar os chunks recuperados (ex: Cohere Rerank)
- *Query Expansion:* reformula a query em múltiplas variações para aumentar recall
- *HyDE (Hypothetical Document Embeddings):* gera um documento hipotético e usa seu embedding para buscar
- *Hybrid Search:* combina busca densa (vetores) com busca esparsa (BM25/TF-IDF)

**Agentic RAG:** o agente decide quando e como buscar, podendo fazer múltiplas buscas iterativas e refinadas conforme o raciocínio evolui.

**Self-RAG:** o modelo decide dinamicamente se precisa recuperar informação, avalia a relevância do que recuperou e critica sua própria resposta antes de entregar.

**GraphRAG:** usa grafos de conhecimento (Knowledge Graphs) para representar relações entre entidades. Melhor para perguntas que requerem raciocínio relacional. Implementação de referência: Microsoft GraphRAG.

**Modular RAG:** pipeline configurável onde cada etapa (indexing, retrieval, reranking, generation) pode ser trocada independentemente.

**Long-context vs RAG:** modelos com janelas grandes (ex: Gemini 1M tokens, Claude 200k) permitem colocar documentos inteiros no contexto — às vezes mais simples e eficaz que RAG para corpora menores.

---

### 5. Tools / Skills / Actions

O agente executa ações no mundo real via ferramentas:

- **Function calling** — chama funções definidas (buscar DB, chamar API, executar código). Base de quase todos os agentes modernos.

- **Code interpreter** — executa código Python em sandbox isolada. Usado intensamente por agentes de análise de dados.

- **Web search / Browser** — navegação autônoma, scraping, preenchimento de formulários.

- **MCP (Model Context Protocol)** — protocolo padrão da Anthropic para expor ferramentas a agentes (ver seção 10).

- **Computer Use** — controle de mouse, teclado e interfaces gráficas. O agente age como um usuário humano na tela.

- **Tool composition** — ferramentas que chamam outras ferramentas, criando pipelines de ação complexos.

- **Parallel tool calls** — o modelo emite múltiplas chamadas de ferramenta em uma única resposta para execução simultânea, reduzindo latência.

---

### 6. Planejamento e Raciocínio

**ReAct** — Reason + Act em loop, intercalando pensamento e ação. Padrão base da maioria dos agentes.

**Chain-of-Thought (CoT)** — Raciocínio passo a passo antes de responder. Melhora acurácia em tarefas complexas.

**Tree of Thoughts (ToT)** — Explora múltiplos caminhos de raciocínio em paralelo, avalia cada ramo e faz backtrack se necessário.

**Plan-and-Execute** — Cria plano completo primeiro, depois executa cada etapa. Reduz erros de curto prazo por falta de visão global.

**Reflexion** — O agente critica seus próprios outputs e se autocorrige iterativamente, sem feedback humano.

**Extended Thinking** — Modelos com "scratchpad" interno antes da resposta final (ex: Claude com thinking, o1/o3 da OpenAI). O raciocínio acontece antes do output visível.

**MCTS (Monte Carlo Tree Search)** — Busca por soluções explorando aleatoriamente um espaço de estados, usado em agentes de jogos e planejamento de longo prazo.

**Subgoal Decomposition** — Decompõe objetivos complexos em subobjetivos menores e verificáveis, reduzindo a probabilidade de desvio em tarefas longas.

---

### 7. Context Engineering

O "context engineering" é a disciplina de projetar e gerenciar o que entra na janela de contexto do modelo para maximizar qualidade e minimizar custo.

**Componentes do contexto:**
- System prompt (instruções, persona, restrições)
- Memória recuperada (RAG, episodic)
- Histórico da conversa (comprimido ou completo)
- Outputs de ferramentas
- Documentos de referência

**Boas práticas:**
- Coloque as informações mais relevantes no início e no fim do contexto (os modelos dão mais atenção a essas posições — *lost in the middle*)
- Separe claramente dados de instruções para evitar prompt injection
- Use *prompt caching* (Anthropic, OpenAI) para partes estáticas do contexto, reduzindo custo em até 90%
- Mantenha o system prompt enxuto: instruções longas diluem a atenção do modelo

**Token budget:** planeje quanto de contexto cada componente vai consumir. Ferramentas com outputs grandes (ex: busca web, leitura de arquivos) podem esgotar o contexto rapidamente.

---

### 8. Guardrails

- **Input guardrails:** filtra inputs maliciosos, prompt injection, PII, conteúdo fora de escopo

- **Output guardrails:** verifica outputs antes de entregar — conteúdo proibido, formato incorreto, alucinações detectáveis

- **Jailbreak detection:** identifica tentativas de contornar as restrições do agente

- **Frameworks:** Guardrails AI, NeMo Guardrails (NVIDIA), LlamaGuard (Meta)

- **Human-in-the-loop:** aprovação humana em ações críticas ou irreversíveis (ex: enviar e-mail, executar query destrutiva, fazer pagamento)

- **Sandboxing:** execução de código em ambientes isolados (Docker, E2B, Modal) para evitar que o agente danifique o sistema host

---

### 9. Segurança

**Prompt Injection** — O conteúdo processado pelo agente (e-mail, página web, documento) tenta sequestrar as instruções do agente. É o principal vetor de ataque em agentes com acesso à internet.

**Indirect Prompt Injection** — A injeção vem de dados externos (não diretamente do usuário). Ex: uma página web com instruções escondidas que o agente lê.

**Mitigações:**
- Separar claramente dados de instruções no prompt
- Usar modelos com instrução-following forte e resistência a injection
- Validar outputs antes de executar ações irreversíveis
- Aplicar o princípio do menor privilégio nas ferramentas disponíveis

**Exfiltração de dados** — Um agente com acesso a dados sensíveis pode ser induzido a vazar informações. Guardrails de output são essenciais.

**Privilege escalation** — O agente usa ferramentas para obter mais permissões do que deveria ter. Controle granular de escopos é fundamental.

---

### 10. Protocolos de Comunicação

**MCP (Model Context Protocol)** — Protocolo aberto da Anthropic (open-source) para conectar modelos a fontes de dados e ferramentas de forma padronizada.
- Usa arquitetura cliente-servidor: o host (Claude, IDE) conecta a servidores MCP
- Cada servidor expõe *tools*, *resources* (dados) e *prompts* (templates)
- Elimina integrações customizadas: um servidor MCP de Slack funciona com qualquer modelo que suporte MCP
- Amplamente adotado: suportado por Claude, Cursor, Windsurf, Zed, e muitos outros

**A2A Protocol (Google)** — Protocolo para comunicação direta entre agentes, independente de qual modelo ou framework cada um usa.
- Cada agente expõe um "Agent Card" (metadados, capacidades, autenticação)
- Comunicação via HTTP com payloads JSON padronizados
- Permite sistemas multi-vendor onde agentes da Anthropic, Google e OpenAI colaboram

**OpenAI Swarm / Handoffs** — Padrão leve para transferência de controle entre agentes dentro do mesmo framework. Focado em simplicidade e legibilidade.

---

### 11. Frameworks de Agentes

| Framework | Empresa | Ponto forte | Melhor para |
|---|---|---|---|
| **LangChain** | LangChain Inc. | Ecossistema enorme, integrações | Protótipos e POCs |
| **LangGraph** | LangChain Inc. | Grafos de estado, ciclos, persistência | Agentes complexos e stateful |
| **CrewAI** | CrewAI | Multi-agent simples, roles | Times de agentes colaborativos |
| **AutoGen** | Microsoft | Conversação multi-agent, code execution | Automação de tarefas com código |
| **Semantic Kernel** | Microsoft | Integração enterprise, .NET/Python | Sistemas corporativos |
| **Haystack** | deepset | Pipelines de NLP e RAG | Aplicações de busca e Q&A |
| **Claude Agent SDK** | Anthropic | Native Claude, subagents, tools | Apps com Claude como base |
| **Agno** | Agno | Leve, alta performance | Agentes de produção rápidos |
| **PydanticAI** | Pydantic | Type-safety, validação de outputs | Agentes com outputs estruturados |

> **Tendência:** frameworks mais leves e com menos "magia" estão ganhando espaço sobre LangChain, que é criticado pela complexidade excessiva e abstrações que dificultam debug.

---

### 12. Observabilidade

Agentes são difíceis de debugar pela natureza não-determinística e multi-step. Observabilidade é essencial em produção.

**O que monitorar:**
- Traces completos de cada execução (cada LLM call, tool call, resultado)
- Latência por etapa
- Custo de tokens por sessão
- Taxa de erros e tipos de falha
- Qualidade dos outputs (com evals automáticos)

**Ferramentas:**

| Ferramenta | Foco |
|---|---|
| **LangSmith** | Traces para LangChain/LangGraph |
| **Langfuse** | Open-source, agnóstico de framework |
| **Helicone** | Proxy para qualquer LLM com logging automático |
| **Braintrust** | Evals + logging integrados |
| **Arize Phoenix** | Open-source, forte em RAG tracing |
| **Weights & Biases** | MLOps com suporte a LLM tracing |

**Structured logging:** logar inputs, outputs e metadados de cada step em formato estruturado (JSON) facilita análises retroativas e alertas.

---

### 13. Evals (Avaliação)

- **Offline evals:** benchmarks com datasets anotados (ex: MMLU, HumanEval, SWE-Bench para código)

- **LLM-as-judge:** outro modelo avalia os outputs (ex: Claude avaliando respostas de outro agente). Escalável, mas com vieses próprios.

- **Trajectory evals:** avalia o caminho percorrido pelo agente (decisões, ferramentas usadas), não só o resultado final. Crucial para agentes autônomos.

- **Human eval:** anotadores humanos avaliam amostras. Caro, mas é o ground truth.

- **A/B Testing de prompts:** compara versões do system prompt em produção com métricas reais.

- **Ferramentas:** LangSmith, Braintrust, PromptFoo, Evals da OpenAI, RAGAS (especializado em RAG), Inspect (UK AI Safety Institute)

> **Dica:** comece sempre com um eval simples (mesmo que manual) antes de ir para produção. Um agente sem evals é um agente sem controle.

---

### 14. Deployment

**Serverless Functions** — AWS Lambda, Google Cloud Functions, Vercel. Boa para agentes com picos de uso e execuções curtas (< 15 min). Custo por invocação.

**Containers (Docker/Kubernetes)** — Maior controle, ideal para agentes com execuções longas ou que precisam de ferramentas instaladas (ex: interpretador de código).

**Plataformas gerenciadas:**
- **Modal** — Executa código Python em containers efêmeros, muito usado para agentes com code execution
- **E2B** — Sandboxes para execução segura de código gerado por agentes
- **Render / Railway** — Deploy de agentes como serviços web simples

**Considerações:**
- Agentes longos precisam de *checkpoint/resume* para sobreviver a falhas
- Estado do agente deve ser persistido externamente (banco de dados), não em memória
- Defina timeouts e limites de iteração para evitar loops infinitos e custos explosivos
- Use filas (SQS, Redis Queue) para agentes que processam tarefas assíncronas em volume
