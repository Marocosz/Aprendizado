# Claude Code — Guia Avançado de Produtividade

> **Cobertura:** claude.ai, VS Code (extensão/API) e Claude Code CLI — skills, tokens, prompts, organização e workflows reais.

---

## Sumário

- [Parte 0 — VS Code vs CLI: Prós, Contras e Quando Usar Cada Um](#parte-0)
- [Parte I — Claude Code no VS Code](#parte-i)
  - [1. Fundamentos: o que são skills no VS Code](#1-fundamentos-vscode)
  - [2. Consumo de Tokens](#2-tokens-vscode)
  - [3. Prompt Engineering](#3-prompts-vscode)
  - [4. Organização de Contexto](#4-contexto-vscode)
  - [5. Workflow Diário](#5-workflow-vscode)
  - [6. Escalando para Projetos Grandes](#6-escala-vscode)
  - [7. Anti-Patterns](#7-antipatterns-vscode)
  - [8. Checklist de Produtividade](#8-checklist-vscode)
  - [9. Configuração Recomendada da Extensão](#9-config-vscode)
  - [10. Referência Rápida](#10-referencia-vscode)
- [Parte II — Claude Code CLI](#parte-ii)
  - [11. Fundamentos: skills, commands e escopos](#11-fundamentos-cli)
  - [12. Skills 2.0 — Recursos que mudam o jogo](#12-skills20-cli)
  - [13. Consumo de Tokens no CLI](#13-tokens-cli)
  - [14. Prompt Engineering no CLI](#14-prompts-cli)
  - [15. Organização de Contexto no CLI](#15-contexto-cli)
  - [16. Workflow Diário com o CLI](#16-workflow-cli)
  - [17. Anti-Patterns do CLI](#17-antipatterns-cli)
  - [18. Checklist CLI](#18-checklist-cli)
  - [19. Comparativo por Cenário](#19-comparativo-cli)
  - [20. Referência Rápida CLI](#20-referencia-cli)

---

<a name="parte-0"></a>
# Parte 0 — VS Code vs CLI: Prós, Contras e Quando Usar Cada Um

Antes de entrar nos detalhes de cada ambiente, esta seção responde a pergunta central: **qual usar e quando?**

---

## Quadro comparativo direto

| Dimensão | VS Code (extensão/API) | Claude Code CLI |
|---|---|---|
| **Modelo de interação** | Assistente de chat com contexto de arquivo | Agente autônomo com acesso ao filesystem |
| **Controle do contexto** | Você — manual e preciso | Parcialmente o agente — guiado por CLAUDE.md e rules |
| **Progressive disclosure** | ❌ Não existe | ✅ Nativo — skills carregam sob demanda |
| **Skills 2.0** | ❌ Não disponível | ✅ Completo (evals, A/B, injeção dinâmica, fork) |
| **Execução de comandos** | ❌ Não executa nativamente | ✅ Bash, leitura e escrita de arquivos autônomos |
| **Custo de tokens** | Alto — system prompt cobrado em toda requisição | Eficiente — progressive disclosure reduz custo base |
| **Feedback loop** | Rápido — resposta imediata | Mais lento — agente executa múltiplos passos |
| **Curva de aprendizado** | Baixa — interface familiar | Média/alta — requer entender workflows agentivos |
| **Previsibilidade** | Alta — você sabe o que é enviado | Média — agente pode tomar caminhos inesperados |
| **Integração com IDE** | ✅ Nativa — arquivo aberto, seleção, erros inline | ❌ Terminal separado, sem integração visual |
| **Pair programming** | ✅ Conversa natural e contextual | ❌ Não é o uso ideal |
| **Tarefas multi-arquivo** | ❌ Você referencia tudo manualmente | ✅ Agente navega o projeto sozinho |
| **Workflows repetitivos** | ❌ Você reproduz o prompt toda vez | ✅ Skills automatizam completamente |
| **Debugging com execução** | ❌ Você copia output e cola no chat | ✅ Agente roda, vê o erro e itera |
| **Memória entre sessões** | ❌ Você repassa contexto toda vez | ✅ CLAUDE.md + rules são persistentes |
| **Rastreabilidade** | Alta — você vê cada mensagem | Média — agente pode fazer várias mudanças antes do checkpoint |

---

## Prós e Contras detalhados

### VS Code — Prós

**Controle granular e previsível.**
Você decide exatamente o que o modelo vê. Selecionar uma função de 30 linhas em vez de um arquivo de 500 é trivial. O contexto é cirúrgico quando você quer que seja.

**Feedback loop imediato.**
Escreve o prompt, recebe a resposta, avalia, itera. Sem passos intermediários, sem aguardar execução de comandos. Para exploração e pair programming, isso é decisivo.

**Integração visual com o IDE.**
Erros sublinhados, arquivo aberto, seleção ativa — tudo acessível diretamente no chat. O fluxo "vejo um erro → peço ajuda" é zero-fricção.

**Menor risco de mudanças indesejadas.**
O modelo responde, você decide o que aplicar. Não há risco de um agente modificar arquivos que você não queria tocados.

**Zero configuração.**
Não precisa criar CLAUDE.md, skills, settings.json. Você abre e usa. Ideal para projetos pontuais ou quando não quer overhead de setup.

**Ideal para exploração.**
Quando você não sabe exatamente o que quer — explorando uma API nova, entendendo um codebase alheio, prototipando — o chat conversacional é superior ao workflow agentivo.

---

### VS Code — Contras

**Sem progressive disclosure — custo fixo alto.**
Tudo que está no system prompt é cobrado em toda requisição. Você não consegue ter muitas "skills" sem pagar por elas constantemente, o que obriga a um system prompt enxuto.

**Gerenciamento de contexto manual e propenso a erro.**
Esquecer de incluir um arquivo relevante, incluir um arquivo grande desnecessariamente, não limpar o histórico — são erros frequentes que custam tokens e qualidade.

**Sem automação de workflows.**
Cada tarefa repetitiva você reproduz manualmente. Code review? Cola o diff, escreve o prompt. Todo dia. Não existe `/review-pr` que faz tudo sozinho.

**Sem execução de comandos.**
Você é o intermediário obrigatório: roda o teste, copia o erro, cola no chat, repete.

**Sem memória de projeto entre sessões.**
Cada sessão começa do zero. Em projetos longos com muitas convenções, isso escala muito mal.

**Output descartado sem custo de aprovação prévia.**
O modelo pode gerar uma implementação inteira que você vai rejeitar. No CLI com checkpoint de planejamento, você aprovaria a direção antes de qualquer código ser escrito.

---

### CLI — Prós

**Progressive disclosure nativa.**
Você pode ter 20 skills configuradas e pagar apenas ~2k tokens de metadata de startup. O corpo das skills só carrega quando ativado. Isso muda o modelo de custo completamente.

**Agente real com acesso ao filesystem.**
Lê arquivos, escreve código, executa testes, itera sobre falhas — sem você precisar intermediar. Para tarefas com 5+ passos sequenciais, a diferença de produtividade é enorme.

**Skills 2.0 — automação com qualidade garantida.**
Evals garantem que o workflow funciona. A/B testing permite otimizar versões. Injeção dinâmica elimina copiar/colar de dados externos. Uma skill bem construída roda igual toda vez, por qualquer pessoa do time.

**Memória permanente do projeto.**
CLAUDE.md + rules criam memória hierárquica e persistente. Você não repassa contexto toda sessão — ele está sempre lá, sempre consistente.

**Tarefas multi-arquivo sem fricção.**
"Refatore o módulo de auth para usar o novo padrão de error handling" — o agente lê todos os arquivos relevantes, faz as mudanças em todos eles, roda os testes. Você revisa o resultado.

**Modo não-interativo para CI e automações.**
`claude -p "verifique vulnerabilidades" --output-format json` — o CLI pode ser parte de pipelines e scripts de time.

**Contexto de execução real.**
O agente vê o output real dos comandos que executa. Não precisa que você descreva o erro — ele roda, lê o stderr, corrige e tenta de novo.

---

### CLI — Contras

**Curva de aprendizado real.**
Você precisa entender CLAUDE.md, skills, rules, settings.json, permissões, injeção dinâmica e `context: fork`. O setup inicial de um projeto bem configurado leva algumas horas. Sem esse investimento, você não aproveita o diferencial.

**Menor controle granular do contexto.**
O agente decide o que ler. Ele pode incluir arquivos desnecessários (aumentando custo) ou ignorar arquivos relevantes (reduzindo qualidade).

**Risco de mudanças além do escopo esperado.**
Um agente com permissões amplas e objetivo mal delimitado pode modificar mais arquivos do que você pretendia. Sem checkpoints explícitos, você pode encontrar 20 arquivos alterados quando esperava 3.

**Feedback loop mais lento para tarefas simples.**
Para uma edição pontual, o overhead do agente não compensa. Você escreve o prompt, o agente executa vários passos, você aguarda — quando no VS Code já teria a resposta em segundos.

**Sem integração visual com o IDE.**
Você está no terminal. Não vê o arquivo aberto, não tem acesso à seleção atual, sem sublinhado de erros inline.

**Tarefas exploratórias são menos naturais.**
A natureza agentiva pressupõe objetivo claro. Sem isso, o agente pode ir em direções não intencionais.

**Debugging de skills tem fricção própria.**
Quando uma skill não funciona como esperado, diagnosticar o porquê (description que não aciona, injeção dinâmica que falha silenciosamente, `allowed-tools` muito restrito) requer ciclos de teste e ajuste.

---

## Quando usar cada um — árvore de decisão

```
Você tem um objetivo claro e verificável?
├── Sim → envolve múltiplos arquivos ou execução de comandos?
│   ├── Sim  → CLI
│   └── Não  → VS Code ou CLI (indiferente)
└── Não (exploração, pair programming, dúvida) → VS Code

É um workflow que você repete regularmente (3x+/semana)?
├── Sim → CLI (crie uma skill)
└── Não → VS Code (não compensa o setup)

A tarefa tem mais de 5 passos sequenciais?
├── Sim → CLI
└── Não → VS Code

Você quer controle total sobre o que é enviado ao modelo?
├── Sim → VS Code
└── Tanto faz → CLI (mais eficiente em tokens a longo prazo)

Você está no meio de uma sessão de coding ativa no editor?
├── Sim → VS Code (zero fricção de troca de contexto)
└── Não → CLI
```

---

## claude.ai — uma terceira opção

O claude.ai (site/app) tem seu próprio sistema de skills via interface — diferente do CLI e das extensões VS Code.

**Como funciona:** vá em **Settings > Customize > Skills**. Você pode ativar as skills prontas da Anthropic (pdf, docx, xlsx, pptx) ou fazer upload de um arquivo ZIP com uma skill customizada. Um toggle individual liga/desliga cada skill.

**Estrutura do ZIP:**
```
minha-skill.zip
└── skill/
    ├── SKILL.md        ← frontmatter + instruções
    └── assets/         ← (opcional) arquivos de suporte
```

**Vantagem sobre VS Code:** o claude.ai tem progressive disclosure nativa — apenas ~100 tokens de metadata por skill no startup; o conteúdo completo só carrega quando a skill é ativada.

**Quando usar:** tarefas rápidas que não precisam do CLI, trabalho em documento Office/PDF com as skills prontas da Anthropic, contextos sem acesso ao terminal.

**Pré-requisito:** Code execution habilitado em Settings > Capabilities. Disponível para planos Free, Pro, Max, Team e Enterprise.

### Disponibilidade por superfície

| Superfície | Skills 2.0 | Como acessar |
|---|---|---|
| **claude.ai** | ✅ | Settings > Skills + toggle |
| **Claude Code (CLI)** | ✅ | `.claude/skills/` ou `~/.claude/skills/` |
| **Claude API** | ✅ | Campo `agent_skills` na requisição |
| **VSCode (extensões)** | ❌ | Apenas via system prompt manual |

> Skills não sincronizam entre superfícies. Uma skill criada no CLI não aparece automaticamente no claude.ai.

---

## A combinação ideal na prática

Os dois ambientes não são excludentes — são complementares.

**Use o CLI para:** features novas end-to-end, refactoring de módulos inteiros, code review automatizado via skill, manutenção de dependências, migrations, qualquer workflow que se repete regularmente.

**Use o VS Code para:** pair programming e exploração, edições pontuais, dúvidas sobre APIs, refinamento do código que o CLI gerou, qualquer tarefa onde você quer controle exato do contexto.

O padrão mais comum na prática: **CLI gera a implementação base → VS Code refina os detalhes e casos de borda.**

---

<a name="parte-i"></a>
# Parte I — Claude Code no VS Code

> Via extensão no VS Code você está operando direto na API. Não existe progressive disclosure, não existem Skills 2.0. Tudo que vai no system prompt é cobrado em cada requisição.

---

<a name="1-fundamentos-vscode"></a>
## 1. Fundamentos: o que são skills no VS Code

### O que cada conceito do CLI vira no VS Code

| Conceito CLI/claude.ai | Equivalente no VS Code |
|---|---|
| Skill global (`~/.claude/skills/`) | Custom Instructions da extensão (system prompt fixo) |
| Skill de projeto (`.claude/skills/`) | Arquivo `.md` referenciado manualmente com `@arquivo` |
| Progressive disclosure | Não existe — você gerencia manualmente |
| `/comando` | Snippets de prompt ou atalhos da extensão |
| `CLAUDE.md` | Arquivo referenciado via `@CLAUDE.md` no início da sessão |

### Escopo local vs global

**Global (Custom Instructions da extensão):** preferências pessoais universais, convenções que valem em todo projeto, regras de comportamento geral. Custo: cobrado em toda requisição — mantenha abaixo de 300 tokens.

**Local (arquivo `.md` por projeto):** stack específica do projeto, padrões de arquitetura, convenções de nomenclatura. Custo: você controla quando incluir via `@arquivo`.

**Regra de ouro:** se vai precisar em mais de 70% das sessões do projeto, coloque no arquivo local de contexto. Senão, referencie pontualmente com `@`.

---

<a name="2-tokens-vscode"></a>
## 2. Consumo de Tokens

### O que consome tokens (em ordem de impacto)

**1. Context window acumulado na conversa.**
O maior vilão. Cada mensagem inclui todo o histórico anterior. Uma conversa de 20 turnos com código longo pode consumir 60k+ tokens só de histórico.

**2. Arquivos abertos e seleções grandes.**
Algumas extensões incluem automaticamente o arquivo ativo inteiro no contexto. Verifique as configurações — procure por "include active file" ou "context files".

**3. System prompt fixo inflado.**
Instruções redundantes, exemplos desnecessários, formatação verbosa. Cada byte do system prompt é cobrado em toda requisição.

**4. Respostas longas desnecessárias.**
Output tokens custam mais que input em alguns modelos. Pedir "explique em detalhes" quando você quer só o código é custo à toa.

**5. Retrabalho por prompt mal estruturado.**
Um prompt ambíguo que gera 3 idas e vindas custa 3x mais que um prompt preciso.

### Erros comuns e como evitar

**❌ Conversa longa sem reset**
```
[20 mensagens acumuladas com código, erros, tentativas...]
"Agora refatore essa função"
```
**✅** Inicie nova conversa para tarefas independentes. Use `@` para repassar só o contexto relevante.

---

**❌ System prompt com exemplos de código inline**
```
"Sempre use TypeScript. Por exemplo:
interface User { id: string; name: string; }
type Result<T> = { data: T; error?: string }..."
```
**✅** Descreva o padrão, não demonstre com exemplos longos no system prompt. Exemplos ficam em `@docs/patterns.md`.

---

**❌ Pedir tudo de uma vez**
```
"Implemente o serviço, explique como funciona, escreva os testes,
adicione JSDoc e crie um README para o módulo"
```
**✅** Uma tarefa por vez. Implemente → valide → teste. Cada passo usa só o contexto necessário.

---

**❌ Repassar código inteiro para perguntas pontuais**
```
[Cola 500 linhas de código]
"Por que essa função retorna undefined às vezes?"
```
**✅** Selecione apenas a função relevante + o contexto mínimo de tipos necessários.

---

**❌ Ordem inconsistente de inclusão de arquivos**
Repetir os mesmos arquivos em ordens diferentes entre sessões impede o cache de funcionar. Mantenha uma ordem consistente de inclusão.

### Estratégias de redução de custo

**Sessões curtas e focadas.** Uma conversa = uma tarefa coesa. Quando terminar ou mudar de assunto, inicie nova sessão.

**Prompt de bootstrap padronizado.**
```
@.claude/CLAUDE.md
Contexto desta sessão: [2-3 linhas específicas]
Tarefa: [uma coisa]
```

**Níveis de detalhe explícitos.** Diga ao modelo quanto de output você quer:
- `"Só o código, sem explicação"`
- `"Código + comentários só nas partes não-óbvias"`
- `"Pseudocódigo primeiro, implemente só se eu aprovar"`

**Perguntas binárias antes de implementar.**
```
"Você usaria abordagem A (event-driven) ou B (polling) para esse caso?
Responda em 1-2 linhas."
```
Evita implementações completas que você vai rejeitar.

**Chunking de arquivos grandes.** Em vez de colar um arquivo de 800 linhas, cole só a interface relevante + a função problemática.

---

<a name="3-prompts-vscode"></a>
## 3. Prompt Engineering

### Estrutura de prompt eficiente

```
[CONTEXTO]    — o que é relevante agora
[RESTRIÇÕES]  — o que NÃO fazer (evita retrabalho)
[TAREFA]      — o que você quer, específico
[FORMATO]     — como quer o output
```

**Exemplo concreto:**
```
CONTEXTO: API Fastify, PostgreSQL via Prisma, TypeScript strict.
Handler de auth em src/routes/auth.ts já existe.

RESTRIÇÕES: Não modifique a interface UserPayload. Não use any.
Não instale novas dependências.

TAREFA: Adicione rate limiting no endpoint POST /login.
Limite: 5 tentativas por IP em 15 minutos.
Use Redis (já configurado em src/lib/redis.ts).

FORMATO: Só o código modificado. Não repita o arquivo inteiro.
```

### Templates reutilizáveis

**Code Review focado**
```
Revise o código selecionado com foco em: [segurança | performance | manutenibilidade].
Para cada issue: severidade (alta/média/baixa), linha, problema, sugestão de fix.
Ignore style issues triviais.
```

**Debug dirigido**
```
Comportamento esperado: [X]
Comportamento atual: [Y]
Já tentei: [Z]
Analise o código e aponte a causa raiz. Não implemente o fix ainda.
```

**Refactoring seguro**
```
Refatore [função/módulo] para [objetivo].
Restrições:
- Mantenha a assinatura pública idêntica
- Não adicione dependências externas
Mostre o diff, não o arquivo completo.
```

**Geração de testes**
```
Escreva testes unitários para [função].
Framework: [Jest/Vitest].
Cubra: happy path, edge cases (null, empty, boundary), erros esperados.
Mock: [lista o que mockar].
Não teste implementação interna, teste comportamento observável.
```

**Arquitetura / design**
```
Problema: [2-3 linhas]
Constraints: [escala, latência, equipe, prazo]
Proponha 2 abordagens com trade-offs. Não implemente ainda.
Formato: Abordagem → Pros → Contras → Quando usar.
```

### Como evitar respostas genéricas

**Dê o que você já sabe.**
```
# Ruim
"Como implementar cache em Node.js?"

# Bom
"Usando Redis com ioredis, preciso cachear o resultado de uma query Prisma
que agrega 3 tabelas (~200ms). TTL de 5 minutos. Mostre só o wrapper de cache."
```

**Referencie decisões arquiteturais existentes.**
```
"Seguindo o padrão Repository em src/repositories/userRepository.ts,
implemente o mesmo para a entidade Order."
```

**Force estrutura na resposta.**
```
"Responda nessa estrutura:
1. Causa raiz (1 parágrafo)
2. Fix mínimo (código)
3. Fix correto a longo prazo (código ou descrição)"
```

**Explicite o nível de senioridade esperado.**
```
"Assuma que sou sênior. Pule explicações básicas.
Se houver trade-off não-óbvio, mencione. Caso contrário, só o código."
```

**Peça contra-argumentos.**
```
"Implemente X. Depois aponte os problemas dessa implementação em produção."
```
Força o modelo a sair do modo geração automática e pensar criticamente.

---

<a name="4-contexto-vscode"></a>
## 4. Organização de Contexto

### Estrutura recomendada de arquivos

```
projeto/
└── .claude/
    ├── CLAUDE.md              ← contexto principal (inclua no início de cada sessão)
    ├── arch.md                ← decisões arquiteturais
    ├── api-contracts.md       ← interfaces e contratos públicos
    └── patterns/
        ├── error-handling.md
        ├── testing.md
        └── data-access.md
```

### O que colocar no CLAUDE.md — mantenha abaixo de 500 tokens

```markdown
# [Nome do Projeto]

## Stack
- Node.js 20, TypeScript 5.4 strict
- Fastify 4 + Prisma 5 (PostgreSQL 15)
- Testes: Vitest + Supertest

## Convenções críticas
- Erros: throw new AppError(code, message) — nunca throw new Error()
- Validação: Zod em todas as rotas
- Async: sempre async/await, nunca .then()
- Imports: path aliases (@/lib, @/routes, @/repositories)

## Estrutura
src/routes/       → handlers Fastify
src/services/     → lógica de negócio
src/repositories/ → acesso a dados (Prisma)
src/lib/          → utilitários compartilhados

## NÃO fazer
- Não use any
- Não coloque lógica de negócio em routes/
- Não acesse Prisma fora de repositories/
```

### O que NÃO colocar no CLAUDE.md

- Exemplos de código (ficam em `patterns/`)
- Documentação de APIs externas (referencie quando precisar)
- Histórico de decisões (ficam em `arch.md`)
- Qualquer coisa que não é relevante em mais de 70% das sessões

---

<a name="5-workflow-vscode"></a>
## 5. Workflow Diário

### Início de sessão

```
@.claude/CLAUDE.md

Sessão de hoje:
- Feature/bug: [descrição em 1 linha]
- Arquivos envolvidos: [lista]
- Objetivo desta sessão: [resultado esperado]
```

### Regras de sessão

**Uma sessão, uma tarefa coesa.** Feature complexa? Quebre em sessões: definir interface → implementar service → escrever testes → atualizar docs.

**Reset proativo.** Se a conversa chegou em 10+ turnos ou o modelo começou a "se perder", inicie nova sessão. Repassar o contexto relevante é mais barato que carregar um histórico longo.

**Valide antes de implementar.** Para mudanças com impacto ≥ 30 linhas, peça primeiro um plano em pseudocódigo. Valide. Depois implemente.

**Diff, não arquivo completo.** Sempre que possível, peça só o que mudou. "Mostre só o que mudou" pode reduzir o output em 80%.

**Feche o loop de erro corretamente.** Se o modelo errou, não corrija na mesma thread com "não, era assim...". Explique o erro, o porquê e o que você esperava.

### Workflow para features novas

```
Sessão 1 — Design
"Dado o contexto em @.claude/CLAUDE.md, preciso implementar [feature].
Proponha a assinatura das interfaces e o contrato de entrada/saída.
Não implemente ainda."

→ Valide e ajuste as interfaces

Sessão 2 — Implementação
"@.claude/CLAUDE.md @.claude/patterns/data-access.md
Implemente [serviço X] seguindo as interfaces que definimos:
[cole as interfaces]
Use o padrão de repository em @src/repositories/userRepository.ts como referência."

Sessão 3 — Testes
"@.claude/patterns/testing.md
Escreva testes para [serviço X]:
[cole a implementação]
Foque em: [lista de cenários específicos]"
```

### Workflow para debugging

```
1. Isole o problema antes de abrir o Claude
   - Reproduza com o mínimo de código possível
   - Identifique: entrada → processamento → saída errada

2. Prompt de debug
"Comportamento esperado: [X]
Comportamento atual: [Y]
Stack trace: [só as linhas relevantes]
Código: [só a função/trecho]
Aponte a causa raiz. Não implemente o fix ainda."

3. Valide o diagnóstico antes de pedir o fix
```

---

<a name="6-escala-vscode"></a>
## 6. Escalando para Projetos Grandes

### Camadas de contexto

```
Camada 1 — Sempre presente (CLAUDE.md):
Stack, convenções críticas, estrutura. < 500 tokens.

Camada 2 — Por domínio (quando relevante):
@.claude/arch.md           → decisões de arquitetura
@.claude/api-contracts.md  → interfaces públicas

Camada 3 — Por padrão (quando a tarefa pede):
@.claude/patterns/error-handling.md
@.claude/patterns/testing.md

Camada 4 — Contexto imediato:
Arquivo específico, função específica (seleção no editor)
```

### Outras estratégias de escala

**ADRs como contexto.**
```
@docs/adr/001-escolha-do-orm.md
Baseado nessa decisão, como devo estruturar [nova feature]?
```

**Interface-first.** Antes de implementar, defina as interfaces TypeScript. São pequenas, eliminam ambiguidade e servem como âncora em todos os prompts relacionados.

**Glossário de domínio.** Um arquivo `@.claude/glossary.md` com termos do negócio elimina confusão:
```markdown
- Pedido (Order): transação confirmada. Não confundir com Cart.
- Usuário (User): sempre pessoa física. Empresas são Account.
```

**Múltiplos serviços (monorepo):**
```
monorepo/
├── .claude/CLAUDE.md                    ← convenções globais do monorepo
├── services/auth/.claude/CLAUDE.md      ← contexto do serviço auth
└── services/payments/.claude/CLAUDE.md
```
Carregue ambos quando trabalhar em um serviço:
```
@.claude/CLAUDE.md @services/auth/.claude/CLAUDE.md
```

---

<a name="7-antipatterns-vscode"></a>
## 7. Anti-Patterns

### Anti-patterns de prompt

| Anti-pattern | Por que é ruim | Alternativa |
|---|---|---|
| "Melhore esse código" | Ambíguo → resposta genérica | "Refatore para reduzir complexidade ciclomática, mantendo a assinatura pública" |
| "Está certo?" | Provoca confirmação, não análise | "Quais problemas você vê nessa implementação em produção?" |
| Colar o projeto inteiro | Dilui o foco, explode tokens | Selecione só o relevante |
| Perguntas encadeadas | O modelo perde o fio | Uma pergunta por vez |
| "Como faz X?" sem contexto | Resposta genérica/tutorial | "Usando asyncio + aiohttp, como [caso específico]?" |

### Anti-patterns de organização

| Anti-pattern | Por que é ruim | Alternativa |
|---|---|---|
| CLAUDE.md com 2000+ tokens | Tudo no contexto, sempre | Separe em camadas, use `@` pontual |
| Copiar contexto manualmente sem template | Inconsistência, esquecimento | Template de início de sessão |
| Continuar conversa claramente quebrada | Modelo perde consistência | Reset + recontextualização limpa |
| System prompt com exemplos de código | Custo alto em toda requisição | Exemplos em arquivo separado |

### Anti-patterns de custo

| Anti-pattern | Custo extra estimado | Fix |
|---|---|---|
| Arquivo inteiro quando precisa de uma função | 3–10x | Selecione a função |
| Conversa de 30 turnos sem reset | 5–15x | Reset após 8–10 turnos |
| Explicação detalhada quando quer só o código | 2–3x | "Só o código com comentários inline" |
| Output completo quando precisava de diff | 2–5x | "Mostre só o que mudou" |
| Múltiplas tarefas em um prompt | 1.5–3x (mais retrabalho) | Uma tarefa por prompt |

---

<a name="8-checklist-vscode"></a>
## 8. Checklist de Produtividade

### Antes de abrir uma sessão
- [ ] Sei exatamente o que quero resolver nessa sessão?
- [ ] Tenho o contexto mínimo necessário identificado?
- [ ] A tarefa pode ser quebrada em algo menor?

### Ao escrever um prompt
- [ ] Inclui contexto específico (não genérico)?
- [ ] Tem restrições explícitas (o que NÃO fazer)?
- [ ] Define o formato de saída esperado?
- [ ] É uma tarefa só, não várias encadeadas?

### Ao revisar a resposta
- [ ] O modelo entendeu o problema real?
- [ ] A resposta respeita as restrições que dei?
- [ ] Tem código que não foi pedido?
- [ ] Preciso de follow-up ou posso abrir nova sessão?

### Ao final da semana
- [ ] Quais prompts funcionaram bem? → Adicionar em `.claude/prompts.md`
- [ ] O CLAUDE.md ainda reflete o estado atual do projeto?
- [ ] Há padrões repetidos que poderiam virar templates?

---

<a name="9-config-vscode"></a>
## 9. Configuração Recomendada da Extensão

### Custom Instructions — enxuto e técnico (~120 tokens)

```
Você é um assistente de desenvolvimento para um desenvolvedor sênior.

Comportamento padrão:
- Responda na linguagem da pergunta (PT-BR ou EN)
- Skip explicações básicas a menos que eu peça
- Prefira código funcional a pseudocódigo
- Quando houver trade-off não óbvio, mencione brevemente
- Não repita o código que eu passei a menos que seja necessário

Formatação:
- Use blocos de código com linguagem especificada
- Para diffs, use formato unified diff quando possível
- Sem markdown excessivo em respostas conversacionais

Quando não souber algo: diga claramente. Não invente APIs ou comportamentos.
```

### Configurando "skills" nas extensões VS Code

Cada extensão tem seu próprio mecanismo. O equivalente ao system prompt da extensão é onde você injeta instruções persistentes:

| Extensão | Onde configurar |
|---|---|
| **Cline / Roo Code** | Campo **Custom Instructions** nas configurações da extensão |
| **Continue** | Campo `systemMessage` no `config.json` |
| **Cursor** | Arquivo `.cursorrules` na raiz do projeto (local) ou **Rules for AI** nas configurações globais |
| **Todas** | Algumas extensões leem `CLAUDE.md` ou `AGENTS.md` na raiz do projeto automaticamente |

**Limitação crítica:** não existe progressive disclosure na API. Todo o conteúdo que você coloca no system prompt é cobrado em **todas as requisições**, sem exceção. Por isso, na prática, inclua apenas as 2–3 instruções mais importantes — não tente replicar 20 skills do CLI.

**Alternativa avançada:** extensões como Cline permitem criar hooks que injetam contexto dinamicamente com base no tipo de arquivo ou comando. Isso imita o comportamento de progressive disclosure do Claude Code, mas exige configuração manual.

---

<a name="10-referencia-vscode"></a>
## 10. Referência Rápida — VS Code

### Ações essenciais

| Ação | Como fazer |
|---|---|
| Incluir arquivo específico | `@caminho/do/arquivo.ts` no chat |
| Incluir seleção atual | Selecione o código → "Add to Chat" |
| Nova sessão limpa | Feche e abra o painel ou botão de nova conversa |
| Template de início | Snippet de VS Code configurado |

### Fórmula de prompt para 80% dos casos

```
[Stack/contexto em 1-2 linhas]
[Restrições: o que não fazer]
[Tarefa específica]
[Formato de output]
```

### Sinais de que você deve resetar a sessão

- Omodelo começou a "esquecer" instruções anteriores
- A resposta veio com código inconsistente com o padrão do projeto
- O histórico tem mais de 10–12 turnos
- Você está em uma subtarefa completamente diferente da original
- O modelo começou a repetir código que você já passou

---

<a name="parte-ii"></a>
# Parte II — Claude Code CLI

> O CLI é um agente autônomo com acesso ao filesystem — não um assistente de chat. Ele lê arquivos, escreve código, executa comandos e itera sobre resultados. Isso muda a semântica dos prompts, o modelo de custo e o que é possível fazer.

---

<a name="11-fundamentos-cli"></a>
## 11. Fundamentos: Skills, Commands e Escopos

### Estrutura de arquivos — o mapa completo

```
~/.claude/                              ← escopo global (todos os projetos)
├── CLAUDE.md                           ← preferências pessoais universais
├── settings.json                       ← configurações globais
└── skills/                             ← skills disponíveis em qualquer projeto
    ├── pr-review/
    │   └── SKILL.md
    └── explain-code/
        └── SKILL.md

projeto/                                ← escopo do projeto
├── CLAUDE.md                           ← contexto do projeto (auto-carregado)
└── .claude/
    ├── settings.json                   ← overrides locais
    ├── rules/                          ← instruções por caminho
    │   ├── api-routes.md               ← aplicada em src/routes/**
    │   └── tests.md                    ← aplicada em **/*.test.ts
    └── skills/                         ← skills do projeto (prioridade sobre globais)
        ├── deploy-check/
        │   ├── SKILL.md
        │   └── scripts/pre-deploy.sh
        └── onboarding-review/
            ├── SKILL.md
            └── examples/
                ├── good-review.md
                └── bad-review.md
```

**Regra de prioridade:** skill de projeto sobrescreve skill global de mesmo nome.

### Skills vs Rules vs CLAUDE.md — a decisão certa

| | CLAUDE.md | `.claude/rules/` | Skills |
|---|---|---|---|
| **Quando carrega** | Sempre, desde o início | Quando o arquivo ativo bate o padrão de caminho | Sob demanda (~100 tokens de metadata sempre) |
| **Para o quê** | Padrões universais do projeto | Regras específicas por tipo de arquivo | Workflows reutilizáveis com lógica própria |
| **Custo** | Sempre no contexto | Presente só quando relevante | Metadata sempre + corpo só quando ativada |
| **Exemplo real** | "Use TypeScript strict, errors via AppError" | "Em arquivos de rota, sempre use Zod" | `/review-pr`, `/explain-code`, `/gen-changelog` |

**Teste de decisão:**
- Preciso disso em mais de 80% das tarefas? → `CLAUDE.md`
- É específico para um tipo de arquivo? → `rules/`
- É um workflow que roda às vezes, com lógica própria? → `skills/`
- Precisa de dados ao vivo (git diff, PR status)? → `skills/` com injeção dinâmica

### Skills globais vs locais

**Skills globais (`~/.claude/skills/`)** — workflows que você repete em qualquer projeto:
- `explain-code` — explicar qualquer código com diagrama
- `gen-commit-msg` — gerar mensagem de commit a partir do diff
- `review-pr` — revisar PRs com padrão consistente

**Skills de projeto (`.claude/skills/`)** — workflows que dependem do repositório:
- `deploy-check` — verifica pré-requisitos do seu pipeline específico
- `onboarding-review` — review com contexto das convenções deste projeto
- `seed-db` — popula o banco com dados deste domínio

**Regra prática:** se você copiaria a skill para outro projeto e ela funcionaria igual, é global. Se ela referencia arquivos ou padrões específicos do repositório, é local.

---

<a name="12-skills20-cli"></a>
## 12. Skills 2.0 — Recursos que Mudam o Jogo

### Skills 1.0 vs 2.0 — o que mudou

| Aspecto | Skills 1.0 | Skills 2.0 |
|---|---|---|
| Arquitetura | Template estático de instruções | Feedback loop com auto-otimização |
| Comandos vs Skills | Separados | Unificados (`.claude/commands/` e `.claude/skills/` produzem o mesmo `/comando`) |
| Contexto | Único por sessão | Subagentes isolados com contextos próprios (`context: fork`) |
| Dados externos | Estáticos (você escreve no SKILL.md) | Shell commands injetam dados ao vivo antes do processamento |
| Avaliação | Nenhuma estrutura formal | Sistema de evals com score (ex: 7/9 prompts passaram) |
| A/B Testing | Não disponível | Comparação paralela de versões integrada |
| Otimização | Manual | Otimização automática de descriptions |
| Controle de ferramentas | Limitado | `allowed-tools` restringe quais ferramentas a skill pode usar |
| Override de modelo | Não disponível | Cada skill pode declarar qual modelo usar |
| Hooks | Nenhum | Hooks de ciclo de vida (pré/pós execução) |

### O frontmatter completo

```yaml
---
name: pr-review
description: |
  Reviews the current open PR focusing on correctness and security.
  Use when: user says "review the PR", "check my PR".
  Do NOT use for: reviewing local uncommitted changes (use diff-review instead).

allowed-tools: Bash(gh *), Bash(git log *), Read
context: fork
model: claude-opus-4-6
disable-model-invocation: false
user-invocable: true

evals:
  - prompt: "Review this PR: adds null check to user.email before sending"
    expected: Identifies the null check, comments on test coverage
  - prompt: "Review PR #42"
    expected: Fetches PR data via gh cli, provides structured feedback
---
```

### Campos do frontmatter — guia de uso

| Campo | O que faz | Quando usar |
|---|---|---|
| `allowed-tools` | Lista branca de ferramentas da skill | Sempre — restrinja ao mínimo necessário |
| `context: fork` | Executa em subagente com contexto isolado | Skills com Bash extenso ou que não devem poluir o contexto principal |
| `model` | Override do modelo para esta skill | Skills que exigem mais capacidade (Opus) ou menor custo (Haiku) |
| `disable-model-invocation` | Impede ativação automática | Skills que só fazem sentido invocadas explicitamente |
| `user-invocable: false` | Só Claude invoca, não aparece como `/comando` | Skills de "background knowledge" |
| `evals` | Casos de teste estruturados | Sempre — estabelece baseline e detecta regressões |

### Injeção dinâmica — o recurso mais subutilizado

A sintaxe `!` executa um shell command antes do Claude processar. Claude recebe o resultado, não o comando. Elimina completamente o ciclo de copiar/colar dados externos.

**Exemplo — PR review com contexto ao vivo:**

```yaml
---
name: pr-review
description: Reviews the current open PR with live data from GitHub.
context: fork
allowed-tools: Bash(gh *)
---

## Contexto atual do PR

Diff: !`gh pr diff | head -200`
Descrição: !`gh pr view --json title,body --jq '.title + "\n\n" + .body'`
Checks: !`gh pr checks`
Arquivos alterados: !`gh pr diff --name-only`

## Tarefa

Revise o PR com foco em:
1. Correctness — a lógica faz o que a descrição diz?
2. Security — inputs não validados, dados expostos?
3. Cobertura — as mudanças têm testes?

Formato: Resumo em 2-3 linhas → Issues: [severidade] [arquivo:linha] descrição → sugestão → Aprovação ou mudanças necessárias.
```

**Outros exemplos úteis:**

```yaml
# Changelog desde o último release
Commits: !`git log $(git describe --tags --abbrev=0)..HEAD --oneline`

# Estado do ambiente
Node: !`node --version`
Desatualizadas: !`npm outdated --json`

# Estado do banco
Schema: !`cat prisma/schema.prisma`
Migrations pendentes: !`npx prisma migrate status`
```

**Sempre filtre antes de injetar:**
```yaml
# ❌ Pode explodir o context window
Diff: !`gh pr diff`

# ✅ Controlado
Diff: !`gh pr diff | head -200`
Arquivos: !`gh pr diff --name-only`
```

### Evals — testes unitários para skills

```yaml
---
name: summarize-pr
evals:
  - prompt: "Summarize: adds input validation to login endpoint using Zod"
    expected: Mentions validation and Zod, under 3 sentences
  - prompt: "Summarize: fixes typo in README"
    expected: One sentence max
---
```

```bash
claude skill eval summarize-pr
# Output: 2/2 passed
```

**Use evals para:** estabelecer baseline ao criar a skill, verificar acionamento automático após mudar a description, confirmar comportamento após atualização do modelo.

### A/B Testing

```bash
claude skill compare summarize-pr summarize-pr-v2
# v1: 3/5 | v2: 5/5 — v2 recomendada
```

### Skill Creator Tool

O Skill Creator é uma ferramenta integrada que opera em linguagem natural — você descreve o que quer e ela gera, testa e otimiza a skill sem necessidade de código. Funciona em 4 modos:

```bash
/skill-creator criar    # descreve o objetivo, gera o SKILL.md
/skill-creator testar   # define exemplos de entrada e saída esperada
/skill-creator otimizar # reescreve a description para melhorar acionamento automático
/skill-creator comparar # roda A/B testing entre versões
```

Use para criar o rascunho inicial de uma skill a partir de uma descrição em português, depois ajuste o SKILL.md gerado conforme necessário.

### Pre-built Agent Skills da Anthropic

A Anthropic disponibiliza skills prontas para formatos de documento que podem ser usadas diretamente:

| Skill | O que faz |
|---|---|
| `pdf` | Extrai texto, tabelas e estrutura de PDFs |
| `docx` (Word) | Lê e gera documentos Word mantendo formatação |
| `xlsx` (Excel) | Lê planilhas, faz cálculos, gera novas planilhas |
| `pptx` (PowerPoint) | Lê e cria apresentações |

No CLI, essas skills vêm incluídas (bundled). Para ativá-las em uma skill própria ou verificar disponibilidade: `claude /skills`.

### `context: fork` — quando usar

**Use quando:** a skill executa Bash com output longo, a skill não deve influenciar a conversa subsequente, você quer contexto sempre limpo.

**Não use quando:** a skill precisa do histórico da conversa atual, é uma skill simples — o overhead de subagente não compensa.

### Dois tipos fundamentais de skills

**Capability Uplift** — elevam a qualidade em áreas onde o modelo é mais fraco:
```yaml
---
name: pixel-perfect-ui
description: Use when designing UI components requiring precise visual specs.
---
## Diretrizes para UI pixel-perfect
[centenas de linhas de referência que carregam só quando necessário]
```

**Workflow / Preference** — documentam onde encontrar informações e em que ordem:
```yaml
---
name: onboarding-review
description: Use when reviewing code from new engineers or a first PR.
---
Padrões: !`cat docs/engineering-standards.md`
PRs anteriores: !`gh pr list --author $AUTHOR --limit 5`

## Abordagem
1. Priorize feedback educativo sobre nitpicks
2. Explique o porquê de cada sugestão
```

---

<a name="13-tokens-cli"></a>
## 13. Consumo de Tokens no CLI

### O que muda em relação ao VS Code

| | VS Code (API) | Claude Code CLI |
|---|---|---|
| Metadata de skills | Você decide o que incluir | ~100 tokens por skill no startup, sempre |
| Corpo da skill | Você inclui explicitamente | Carrega só quando a skill é ativada |
| Arquivos extras da skill | Você cola manualmente | Lidos via Bash quando necessário, zero custo antes |
| CLAUDE.md do projeto | Você referencia com `@` | Lido automaticamente ao entrar no diretório |
| Rules | Não existe | Carregam só quando o arquivo ativo bate o padrão |

### O que ainda consome tokens desnecessariamente no CLI

**CLAUDE.md global inflado.** O global carrega em todo projeto, toda sessão. Mantenha abaixo de 400 tokens.

**Skills com instruções duplicadas do CLAUDE.md.** Se a skill repete as mesmas regras do CLAUDE.md, você paga duas vezes. Skills devem complementar, não repetir.

**`context: fork` desnecessário.** Para skills simples, o overhead de subagente custa mais do que economiza.

**Injeção dinâmica sem filtro.** Sempre use `head`, `grep` ou `jq` antes de injetar dados externos.

### Estratégias de custo específicas do CLI

**Segmente skills por frequência.** Skills usadas toda hora devem ser enxutas (< 1k tokens). Skills ocasionais podem ser mais ricas — o custo só acontece quando ativadas.

**Use rules em vez de skills para regras simples.** "Quando em `src/routes/`, sempre use Zod" é uma rule, não uma skill. Rules são mais baratas.

```markdown
<!-- .claude/rules/api-routes.md — aplicada em src/routes/** -->
Sempre que modificar um handler de rota:
1. Valide o corpo com Zod antes de qualquer lógica
2. Use o schema em src/schemas/[recurso].schema.ts
3. Retorne erros via throw new AppError(400, 'mensagem')
```

---

<a name="14-prompts-cli"></a>
## 14. Prompt Engineering no CLI

### Estrutura de prompt para tarefas agentivas

```
[OBJETIVO FINAL]   — o que deve estar funcionando ao final
[CONTEXTO]         — caminhos dos arquivos relevantes (não o conteúdo)
[RESTRIÇÕES]       — o que não tocar, o que não instalar
[CRITÉRIO DE DONE] — como saber que terminou
[PERMISSÕES]       — o que pode executar sem pedir confirmação
```

**Exemplo real:**

```
OBJETIVO: Adicionar soft delete em todas as entidades do projeto.

CONTEXTO:
- Modelos Prisma em prisma/schema.prisma
- Repositories em src/repositories/
- Convenções em CLAUDE.md

RESTRIÇÕES:
- Não modifique a interface pública dos repositories
- Não adicione campos além de deletedAt e updatedAt
- Não altere migrations existentes, crie novas

CRITÉRIO DE DONE:
- Schema atualizado com deletedAt em todas as entidades
- Migration criada e aplicada (npx prisma migrate dev)
- Todos os find* filtram deletedAt is null automaticamente
- Testes existentes passando

PERMISSÕES:
- Pode ler qualquer arquivo do projeto
- Pode escrever em src/repositories/ e prisma/
- Pode executar npx prisma migrate dev e vitest
- Pergunte antes de modificar qualquer outro diretório
```

### Como evitar que o agente saia do trilho

**Permissões explícitas.** Liste o que pode e o que precisa de confirmação.

**Checkpoints intermediários.**
```
Fase 1: Analise o schema e me mostre o plano de mudanças.
Não implemente ainda — aguarde minha aprovação.
```

**Critério de done claro.** Sem ele, o agente pode continuar "melhorando" coisas que você não pediu.

**`allowed-tools` em skills.** Se a skill só precisa ler arquivos e rodar `gh`:
```yaml
allowed-tools: Read, Bash(gh *), Bash(git log *)
```

### Skills como automação de workflows repetitivos

```yaml
---
name: security-review
description: |
  Security-focused code review.
  Use when: user asks to "check security", "review for vulnerabilities".
allowed-tools: Read, Bash(git diff *)
---

## Código a revisar
!`git diff HEAD~1`

## Checklist

Para cada issue: [SEVERIDADE] arquivo:linha — vulnerabilidade — como explorar — fix

- Inputs não validados ou sanitizados
- SQL/NoSQL injection
- Secrets hardcoded ou em logs
- Autenticação/autorização inadequada
- Rate limiting ausente em endpoints sensíveis
- Dados sensíveis em respostas de erro

Não comente sobre style, performance ou arquitetura — apenas segurança.
```

---

<a name="15-contexto-cli"></a>
## 15. Organização de Contexto no CLI

### Hierarquia de carregamento

```
1. ~/.claude/CLAUDE.md           → carrega em todo projeto, sempre
2. projeto/CLAUDE.md             → carrega ao entrar no diretório
3. .claude/rules/*.md            → carregam quando arquivo ativo bate o padrão
4. Skill metadata (~100 tokens)  → carregam no startup para todas as skills
5. Corpo da skill                → carrega quando a skill é ativada
6. Arquivos extras da skill      → carregam via Bash quando a skill precisa
```

### O que colocar em cada nível

**`~/.claude/CLAUDE.md` (global) — máximo 400 tokens:**
```markdown
# Preferências globais

## Comportamento
- Responda em PT-BR por padrão, EN se a pergunta for em EN
- Skip explicações básicas — sou sênior
- Nunca reescreva função inteira quando só um trecho muda
- Mencione trade-offs não-óbvios brevemente

## Ao executar comandos
- Rode testes após mudanças que possam quebrar comportamento
- Prefira --dry-run quando disponível antes de executar destrutivo

## Commits: conventional commits (feat/fix/refactor/chore), EN
```

**`projeto/CLAUDE.md` (projeto) — máximo 500 tokens:**
```markdown
# [Nome do Projeto]

## Stack
- Node.js 20, TypeScript 5.4 strict
- Fastify 4 + Prisma 5 (PostgreSQL 15)
- Testes: Vitest + Supertest

## Estrutura
src/routes/       → handlers (routing e validação Zod)
src/services/     → lógica de negócio
src/repositories/ → acesso a dados
src/lib/          → utilitários compartilhados

## Convenções críticas
- Erros: throw new AppError(code, message)
- Nunca acesse Prisma fora de repositories/
- Validação de entrada: Zod obrigatório em todas as rotas

## Comandos
- npm run dev      → inicia com hot reload
- npm test         → vitest
- npm run db:reset → reseta e popula banco de dev
```

**`.claude/rules/api-routes.md`:**
```markdown
---
globs: src/routes/**/*.ts
---
1. Valide o body com Zod antes de qualquer lógica
2. Use o schema em src/schemas/
3. Chame services, nunca repositories diretamente
4. Retorne erros via throw new AppError(statusCode, message)
```

### Estrutura de projeto madura com CLI

```
projeto/
├── CLAUDE.md
└── .claude/
    ├── settings.json
    ├── rules/
    │   ├── api-routes.md        ← globs: src/routes/**
    │   ├── repositories.md      ← globs: src/repositories/**
    │   └── tests.md             ← globs: **/*.test.ts
    └── skills/
        ├── deploy-check/
        │   ├── SKILL.md
        │   └── scripts/validate-env.sh
        ├── gen-changelog/
        │   └── SKILL.md
        └── onboarding-review/
            ├── SKILL.md
            └── examples/
                ├── ideal-feedback.md
                └── avoid-this.md
```

---

<a name="16-workflow-cli"></a>
## 16. Workflow Diário com o CLI

### Iniciando uma sessão

```bash
cd meu-projeto   # CLAUDE.md carrega automaticamente
claude

# Vá direto ao ponto:
"Preciso implementar paginação cursor-based no endpoint GET /orders.
O endpoint atual está em src/routes/orders.ts.
Siga as convenções do projeto."
```

### Workflow para features — faseado

**Fase 1 — Planejamento**
```
Preciso implementar [feature].
Leia os arquivos relevantes e me proponha:
1. As interfaces TypeScript que vão existir
2. Os arquivos que serão criados ou modificados
3. A sequência de implementação

Não implemente ainda.
```

**Fase 2 — Implementação incremental**
```
Aprovado o plano. Implemente a Fase 1: [somente o repository].
Após implementar, rode os testes unitários do módulo.
```

**Fase 3 — Validação**
```
Implemente os testes de integração para o que foi feito.
Use o padrão em [arquivo de referência].
```

**Por que faseado?** Detectar problemas no planejamento custa zero código descartado. Detectar na fase 3 pode significar refazer tudo.

### Workflow para debugging

```
Bug no endpoint POST /payments.
Esperado: criar registro na tabela payments e retornar o ID.
Atual: retorna 200 mas nenhum registro é criado.

Leia:
- src/routes/payments.ts
- src/services/paymentService.ts
- src/repositories/paymentRepository.ts

Execute os testes existentes do módulo e analise os logs.
Aponte a causa raiz antes de propor qualquer fix.
```

O CLI tem vantagem clara aqui: roda o código, vê o erro, itera — tudo sem você copiar nada.

### Workflow de manutenção

```bash
/deploy-check

# Se passar:
"Atualize as dependências com vulnerabilidades conhecidas.
1. Rode npm audit e liste os problemas
2. Atualize as dependências afetadas
3. Rode os testes
4. Se passarem, gere um commit convencional com o sumário"
```

---

<a name="17-antipatterns-cli"></a>
## 17. Anti-Patterns do CLI

### Anti-patterns de skills

| Anti-pattern | Por que é ruim | Alternativa |
|---|---|---|
| Description vaga | Skill nunca ativa automaticamente | Inclua frases de trigger: "Use when user says 'review PR'" |
| Description específica demais | Skill ativa raramente | Teste com `claude skill eval` e ajuste |
| Skill sem `allowed-tools` | Acesso irrestrito a ferramentas | Especifique o mínimo necessário |
| Injeção dinâmica sem filtro | Output gigante no contexto | Use `head`, `grep`, `jq` antes de injetar |
| Corpo da skill com 5k+ tokens | Carregamento pesado em toda ativação | Divida em skill principal + arquivos extras via Bash |
| Skill global com lógica de projeto | Conflitos em outros projetos | Skills de projeto ficam em `.claude/skills/` |

### Anti-patterns de workflow agentivo

| Anti-pattern | Consequência | Alternativa |
|---|---|---|
| Tarefa aberta demais | Mudanças em locais inesperados | Especifique escopo, arquivos e critério de done |
| Sem checkpoints em tarefas longas | 30 min na direção errada | Peça plano antes de implementar, aprove cada fase |
| Ignorar permissões no settings.json | Agente executa comandos destrutivos sem confirmação | Configure `permissions` explicitamente |
| Continuar após erro sem investigar | Agente empilha correções em cima do problema | "Pare e me explique o erro antes de tentar corrigir" |
| Tarefa sem critério de done | Agente não sabe quando parar | Sempre inclua "Termine quando: [condição verificável]" |

### Anti-patterns de custo no CLI

| Anti-pattern | Custo extra | Fix |
|---|---|---|
| CLAUDE.md global com 3k+ tokens | Pago em todo projeto, toda sessão | Máximo 400 tokens |
| Skill com instruções duplicadas do CLAUDE.md | 2x o custo quando ativada | Skills complementam, não repetem |
| Injeção dinâmica retornando diff de 2000 linhas | Explode o context window | `gh pr diff \| head -300` |
| `context: fork` em skill simples | Overhead de subagente desnecessário | Reserve `fork` para skills com Bash extenso |

---

<a name="18-checklist-cli"></a>
## 18. Checklist CLI

### Configuração inicial de um projeto novo
- [ ] Criar `CLAUDE.md` na raiz com stack, estrutura e convenções (< 500 tokens)
- [ ] Configurar `.claude/settings.json` com permissões explícitas
- [ ] Criar rules para os principais padrões de caminho do projeto
- [ ] Mapear quais workflows se repetem → candidatos a skill local
- [ ] Verificar quais skills globais já existem e se há conflito de nome

### Antes de criar uma skill
- [ ] O workflow se repete pelo menos 3–4x por semana?
- [ ] Tem lógica suficiente para justificar uma skill (vs. só um prompt)?
- [ ] Precisa de dados ao vivo? → adicionar injeção dinâmica
- [ ] Precisa de isolamento? → adicionar `context: fork`
- [ ] Definir pelo menos 2–3 casos de teste (evals)
- [ ] É global ou local?

### Antes de executar uma tarefa agentiva longa
- [ ] O objetivo está claro e verificável?
- [ ] As restrições estão explícitas (o que NÃO tocar)?
- [ ] O critério de done está definido?
- [ ] As permissões estão claras?
- [ ] Dividi em fases com checkpoints de aprovação?

### Ao criar ou modificar uma skill
- [ ] A description cobre os casos de uso principais?
- [ ] Inclui frases de trigger do usuário?
- [ ] Exclui casos onde NÃO deve ativar?
- [ ] O `allowed-tools` está restrito ao mínimo?
- [ ] Os evals cobrem happy path e edge cases?
- [ ] Rodei `claude skill eval [nome]` e passou?

---

<a name="19-comparativo-cli"></a>
## 19. Comparativo por Cenário

| Cenário | Melhor ambiente | Por quê |
|---|---|---|
| Feature nova end-to-end | **CLI** | Agente lê, implementa, testa sem intervenção |
| Editar uma função específica | **VS Code** | Feedback loop rápido, contexto controlado |
| Code review automatizado | **CLI** | Skill com `gh` integrado, sem copiar diff |
| Debug de bug pontual | Empate | VS Code para bugs simples, CLI para bugs que requerem execução |
| Refactoring de módulo inteiro | **CLI** | Agente faz mudanças em múltiplos arquivos consistentemente |
| Pair programming / exploração | **VS Code** | Interação conversacional mais natural |
| Manutenção de dependências | **CLI** | Executa audit, atualiza, testa, commita |
| Geração de testes em massa | **CLI** | Lê todos os arquivos do módulo, gera cobertura completa |
| Dúvida rápida sobre API | **VS Code** | Resposta imediata sem overhead de agente |
| Deploy check / CI local | **CLI** | Skill com injeção dinâmica de status real |

**Regra geral:** CLI quando a tarefa tem mais de 3 passos que o agente pode executar em sequência. VS Code quando você quer controle preciso do contexto e resposta rápida.

---

<a name="20-referencia-cli"></a>
## 20. Referência Rápida — CLI

### Comandos essenciais

```bash
claude                                         # iniciar no projeto
/nome-da-skill                                 # invocar skill
/review-pr 42                                  # skill com argumento
/skills                                        # listar skills disponíveis
claude skill eval nome-da-skill                # rodar evals
claude skill compare skill-v1 skill-v2        # A/B testing
claude -p "prompt" --output-format json        # modo não-interativo (CI)
```

### settings.json — configuração de permissões

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "allow": [
      "Read(**)",
      "Write(src/**)",
      "Write(tests/**)",
      "Bash(npm test)",
      "Bash(npm run *)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(gh pr *)"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(rm -rf *)",
      "Write(.env*)"
    ]
  }
}
```

### Fórmula de prompt agentivo para 80% dos casos

```
[OBJETIVO verificável]
[CONTEXTO: caminhos dos arquivos relevantes]
[RESTRIÇÕES: o que não tocar]
[CRITÉRIO DE DONE: condição testável]
[PERMISSÕES: o que pode executar sem confirmação]
```

### Sinais de que você deve interromper o agente

- Está modificando arquivos fora do escopo definido
- Está tomando mais de 15 passos sem nenhum checkpoint
- Começou a instalar dependências que você não pediu
- O output dos testes está piorando a cada tentativa de fix
- Está reescrevendo código sem relação com a tarefa
