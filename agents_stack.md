### 1. Tipos de Agentes

**Single Agent** — Um único modelo com acesso a ferramentas, memória e instruções. Resolve tarefas de forma autônoma em loop (ReAct loop: Reason → Act → Observe).

**Multi-Agent Systems** — Múltiplos agentes colaborando, cada um com responsabilidades distintas. É o coração das arquiteturas modernas.

---

### 2. Padrões de Orquestração Multi-Agent

**Orchestrator → Subagents**
- Um agente "maestro" decompõe a tarefa e delega para agentes especialistas. Exemplo: um orquestrador recebe "analise este contrato" e delega para agente jurídico, agente financeiro e agente de risco.

**Agent-to-Agent (A2A)**
- Agentes se comunicam diretamente via protocolos como o Google A2A Protocol ou MCP (Model Context Protocol) da Anthropic. Cada agente expõe uma interface e pode ser chamado por outros.

**Handoff / Swarm**
- O agente atual "passa o bastão" para outro agente mais adequado conforme o contexto muda — padrão popularizado pelo OpenAI Swarm.

**Supervisor Pattern**
- Um agente supervisor avalia os outputs dos subagentes e decide se estão corretos antes de prosseguir.

---

### 3. Memória (analisar melhor esse, pois talvez um BD (com tabelas que o motor também consiga criar) seja necessário)

- **In-context memory:** O que cabe na janela de contexto atual
- **External memory (RAG):** Vetores em banco como Pinecone, Weaviate, pgvector
- **Episodic memory:** Histórico de conversas/sessões passadas
- **Semantic memory:** Fatos e conhecimento persistido sobre o usuário/domínio
- **Procedural memory:** O próprio system prompt e instruções do agente

---

### 4. RAG 

- **Naive RAG:** embed → busca por similaridade → injeta no contexto
  
- **Advanced RAG:** reranking, query expansion, HyDE (Hypothetical Document Embeddings)
  
- **Agentic RAG:** o agente decide quando e como buscar, podendo fazer múltiplas buscas iterativas

- **GraphRAG:** usa grafos de conhecimento (Knowledge Graphs) para relações entre entidades

---

### 5. Tools / Skills / Actions

O agente executa ações no mundo real via ferramentas:

- **Function calling** — chama funções definidas (buscar DB, chamar API, executar código)

- **Code interpreter** — executa código Python em sandbox

- **Web search / Browser** — navegação autônoma

- **MCP (Model Context Protocol)** — protocolo padrão para expor ferramentas a agentes

- **Computer Use** — controle de mouse, teclado e interfaces gráficas

---

### 6. Planejamento e Raciocínio

**ReAct:** Reason + Act em loop, intercalando pensamento e ação

**Chain-of-Thought (CoT):** Raciocínio passo a passo antes de responder

**Tree of Thoughts (ToT):** Explora múltiplos caminhos de raciocínio em paralelo

**Plan-and-Execute:** Cria plano completo primeiro, depois executa cada etapa

**Reflexion:** O agente critica seus próprios outputs e se autocorrige

**Extended Thinking:** Modelos com "scratchpad" interno (ex: Claude com thinking)

---

### 7. Guardrails

- **Input guardrails:** filtra inputs maliciosos, prompt injection, PII

- **Output guardrails:** verifica outputs antes de entregar (conteúdo, formato, alucinações)

- **Frameworks:** Guardrails AI, NeMo Guardrails (NVIDIA), LlamaGuard (Meta)

- **Human-in-the-loop:** aprovação humana em ações críticas ou irreversíveis

---

### 8. Evals (Avaliação)

- **Offline evals:** benchmarks com datasets anotados (ex: MMLU, HumanEval)
- **LLM-as-judge:** outro modelo avalia os outputs (ex: GPT-4 avaliando respostas)
- **Trajectory evals:** avalia o caminho percorrido pelo agente, não só o resultado final
- **Ferramentas:** LangSmith, Braintrust, PromptFoo, Evals da OpenAI, RAGAS (para RAG)