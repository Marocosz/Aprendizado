# n8n

> O n8n é uma ferramenta de automação de fluxo de trabalho (workflow) baseada em código aberto (open-source) e "low-code". Ele permite conectar aplicativos, bancos de dados e APIs para automatizar tarefas repetitivas visualmente, sem necessidade de programação complexa. Pode ser hospedado no próprio servidor (self-hosted) ou usado na nuvem.

## Fundamentos

### Nós (Nodes)

> **A Analogia:** Imagine que o n8n é uma grande fábrica. Um **Nó** é um operário ou uma máquina específica nessa linha de montagem. Um operário só sabe apertar parafusos; outro só sabe pintar; outro só sabe colocar na caixa.

**Na Prática:** É aquele "quadradinho" que você arrasta para a tela. Cada nó tem apenas **uma especialidade**. Você tem um nó especializado em ler planilhas, outro especializado em mandar mensagens no WhatsApp, outro especializado em fazer contas matemáticas. O fluxo inteiro é construído ligando o trabalho de vários nós.

### Conexões

> **A Analogia:** É a esteira rolante que liga uma máquina à outra.

**Na Prática:** Quando o Nó 1 termina o trabalho dele, ele coloca o resultado (os dados/informações) nessa "esteira" e envia para o Nó 2. A informação sempre viaja **da esquerda para a direita** através dessas linhas. Se não há linha ligando dois nós, eles não se conversam.

### Fluxo (Workflow)

> **A Analogia:** É a linha de montagem completa, do começo ao fim.

**Na Prática:** É a tela inteira do n8n com todos os nós e conexões que você construiu. O arquivo `JSON` (como o que você exporta ou importa) é a "planta baixa" ou o projeto arquitetônico do seu workflow.

### Gatilho (Trigger Node)

> **A Analogia:** É o botão de "Ligar" da fábrica, ou o relógio de ponto que desperta os operários. Sem ele, a fábrica fica parada no escuro, não faz nada.

**Na Prática:** Todo fluxo **precisa** começar com um nó de Gatilho (ele sempre fica na extrema esquerda e não tem nenhuma entrada de informação vindo antes dele). Ele é o evento que inicia tudo. Existem vários tipos:
* **Schedule Trigger:** O "despertador". *Ex: Todo dia às 08:00, inicie o fluxo.*
* **App Trigger:** Fica "olhando" um app. *Ex: A cada 5 minutos, olhe o Gmail; se tiver email novo, inicie o fluxo.*
* **Webhook:** O mais instantâneo e versátil de todos.

### Webhook

> **A Analogia:** O Webhook é como a **campainha da sua casa**, com uma caixa de correio acoplada. A sua casa (seu fluxo) está lá, quietinha. De repente, alguém na rua aperta a campainha e enfia uma carta na caixa. No instante em que a campainha toca, as luzes se acendem, você pega a carta e começa a trabalhar.

**Na Prática:** Um Webhook é um endereço de internet (uma URL, como `https://seu-n8n.com/webhook/receber`) que o n8n cria e deixa "aberto" escutando. Você configura um sistema externo (Bitrix, Hyper, WhatsApp) para enviar dados para esse link sempre que houver novidades. Como é **em tempo real**, o n8n não precisa ficar "perguntando" de tempos em tempos se há mensagens novas; ele apenas reage instantaneamente quando é chamado.

### Ramificação (Branching / Lógica)

> **A Analogia:** Imagine que a esteira da fábrica chega em um **cruzamento com um guarda de trânsito**. O guarda olha a caixa que chegou e diz: *"Hmm, essa caixa é VIP, vai para a esteira da direita. Essa caixa é Normal, vai para a esquerda"*.

**Na Prática:** São os nós de lógica, principalmente o **Nó If** (Se) ou **Switch** (Interruptor). Eles *não modificam* a informação, apenas fazem uma validação com base em regras (ex: "A mensagem tem um arquivo anexo?").
* Se **Verdadeiro** (`true`), os dados seguem pelo caminho superior.
* Se **Falso** (`false`), os dados seguem pelo caminho inferior.

### Merge (Juntar)

> **A Analogia:** O oposto da ramificação. São duas esteiras da fábrica que se encontram e despejam os produtos em uma esteira só.

**Na Prática:** O **Nó Merge** pega informações que vieram de dois caminhos diferentes e as cruza em um único lugar. É muito útil quando você pesquisa os dados do cliente por um caminho, busca a fatura dele por outro, e depois precisa juntar o "Nome" com o "Valor" no mesmo pacote `JSON` para seguir em frente.

---

## Conceitos Primordiais

### Arquitetura de Itens

> No n8n, os dados **nunca** transitam como um texto solto ou um `JSON` único. Eles **sempre transitam como uma lista (um Array) de objetos**.

Mesmo que você receba apenas um nome, o n8n enxerga assim:
`[ { "json": { "nome": "Leandro" } } ]`

> [!IMPORTANT]
> **Por que isso importa?** Porque o n8n tem um **Loop Implícito**. Se o Nó A enviar 10 itens para o Nó B, o Nó B vai rodar sua ação 10 vezes (uma para cada item) automaticamente. Você não precisa criar um "For" ou um "While" na maioria das vezes. O próprio n8n gerencia essa iteração.

### JSON vs. Binário

Quando um nó processa uma informação, ele divide o pacote em dois compartimentos distintos na memória:

* **JSON:** É a parte de texto, números, booleanos (`true`/`false`). É a estrutura leve, fácil de ler, e a que você mais vai manipular usando expressões.
* **Binário (Binary):** São os arquivos pesados (PDFs, Áudios, Imagens). Eles não ficam misturados no JSON por motivos de performance. Eles ficam em uma aba separada chamada "Binary" e são referenciados apenas por uma chave de identificação interna.

### O Grafo Direcionado Acíclico (DAG)



> **"Direcionado"** significa que os dados só andam para a frente (da esquerda para a direita). **"Acíclico"** significa que não existem loops infinitos naturais (ciclos) desenhados na interface.

**O que acontece por trás:** O n8n constrói uma árvore de execução. Se você cria uma bifurcação (um nó `If`), o n8n pausa a execução de um lado, resolve o outro, e depois volta para finalizar as ramificações pendentes. Ele segue o caminho até que não haja mais nós conectados àquela ramificação.

### O Motor de Expressões (Sintaxe Mustache)

Quando você usa as chaves duplas `{{ }}` em um campo de configuração, você está dizendo ao motor do n8n: *"Pare de ler isso como texto puro e execute o JavaScript que está aqui dentro"*.

* **O escopo:** Dentro do `{{ }}`, você tem acesso ao objeto `$json` (os dados daquele item atual no loop) e a métodos nativos do JavaScript (como `.replace()`, `.split()`, contas matemáticas, etc.).

### O Paradigma de Referência Cruzada (Data Pairing)

> Como acessar um dado que ficou 5 nós para trás no fluxo? O n8n usa a sintaxe `$('Nome do Nó')`. Porém, existe uma armadilha mecânica de como ele funciona por trás:

* **Alinhamento de Itens (Matching):** Se o seu nó atual tem 3 itens sendo processados, e você pede um dado de um nó lá de trás usando `$('Nó Antigo').item.json.nome`, o n8n vai tentar fazer um pareamento exato (1:1). Ele vai cruzar o item 1 do nó atual com o item 1 do nó antigo; o item 2 com o item 2, etc.
* **E se o nó antigo só tiver 1 item?** Você usa `$('Nó Antigo').first().json.nome`. Isso instrui o n8n: *"Não importa em qual item do loop eu estou agora, pegue sempre a primeira resposta daquele nó lá de trás"*.

### Estados de Execução: Manual vs. Produção

O n8n gerencia o processamento e a memória de maneira diferente dependendo de como você o aciona:

* **Execução Manual (Test Workflow/Step):** O n8n guarda **todos** os dados de **todos** os nós na memória RAM do seu navegador para que você possa inspecionar o Input/Output de cada um. É um processo mais "pesado", mas indispensável para debugar e construir a automação.
* **Execução de Produção (Active):** O n8n opera de forma otimizada. Ele descarta os dados da memória assim que o nó termina sua função (a menos que outra parte do fluxo precise deles mais à frente). Isso poupa CPU e RAM do servidor, garantindo que fluxos gigantes operem com fluidez sem derrubar a infraestrutura.

---

## Famílias de Nós

Existem mais de 1.000 integrações no n8n, mas **absolutamente todos os nós se dividem em 5 famílias principais**:

### 1. Família dos Gatilhos (Triggers)
Ficam na extrema esquerda do fluxo. Eles **geram** os primeiros dados que dão partida no motor.
* **Webhook:** Cria uma URL pública que fica escutando dados em tempo real.
* **Schedule Trigger:** O despertador (ex: "rodar toda segunda-feira às 09h").
* **App Triggers:** Monitoram um app ativamente (ex: *Gmail Trigger* - "quando chegar email", *Telegram Trigger*).
* **Error Trigger:** Ativado automaticamente apenas se **outro** fluxo der erro (ótimo para alertas de falha).

### 2. Família de Controle e Lógica (Flow)
São os "guardas de trânsito". Não transformam os dados, apenas dizem para onde a informação deve ir.
* **If / Switch:** Fazem perguntas (condicionais). O *If* divide em 2 caminhos, o *Switch* divide em vários.
* **Merge:** Junta duas ou mais esteiras em uma só.
* **Wait:** Pausa a execução (espera um tempo fixo ou até um Webhook ser chamado).
* **Split In Batches (Loop):** Pega uma lista de 100 itens e processa de 10 em 10 (evita sobrecarregar APIs).
* **Stop and Error:** Força a parada do fluxo e acusa um erro customizado.

### 3. Família de Transformação de Dados (Data Manipulation)
Os operários que abrem o pacote, trocam etiquetas, fazem contas e montam um novo pacote.
* **Set (Edit Fields):** Cria novas variáveis, renomeia chaves ou fixa valores estáticos.
* **Code:** Permite escrever JavaScript ou Python puro para manipular dados complexos.
* **Item Lists:** Manipula as listas (Arrays) do n8n (ordenar, limitar, remover duplicados).
* **Date & Time:** Formata e converte datas e fusos horários.
* **Crypto:** Criptografa dados, gera hashes (MD5, SHA256) ou assinaturas de segurança.

### 4. Família de Ação e Integração (Apps & Core Nodes)
As máquinas que falam com o mundo exterior (APIs e Bancos de Dados).
* **HTTP Request:** O "Canivete Suíço". Usado para comunicar com qualquer API que não tenha um nó pronto.
* **Bancos de Dados:** *MongoDB, PostgreSQL, MySQL, Redis.* Servem para ler, criar, atualizar ou deletar dados.
* **Nós de Apps:** *Slack, Trello, Jira, Pipedrive, etc.* Trazem a interface pronta para preencher parâmetros.

### 5. Família de Inteligência Artificial (Advanced AI / LangChain)
A família mais recente, baseada no framework LangChain, que constrói agentes autônomos.
* **AI Agent / Chain:** O cérebro que gerencia o prompt e as decisões.
* **Language Models (LLMs):** Os motores de raciocínio (*OpenAI, Gemini, Claude*).
* **Memory:** Diz ao Agente como lembrar do contexto passado (*Window Buffer, Thread ID*).
* **Tools (Ferramentas):** Dá habilidades ao Agente (ex: permitir que a IA acione outro fluxo do n8n para consultar um banco de dados sozinha).
* **Output Parsers:** Força a IA a responder em um formato estruturado (ex: `JSON` ou `Booleano`).

---

## Anatomia e Configurações dos Nós

Ao abrir qualquer nó, a interface possui opções estruturais padrão, divididas em abas:

### 1. Parâmetros (Parameters)
Onde você define *o que* a máquina deve fazer.
* **Fixed Value (Valor Fixo):** Texto puro que não muda (ex: Assunto = "Sua fatura chegou").
* **Expression (Expressões / `Fx`):** Torna o campo dinâmico usando a sintaxe `{{ }}` para puxar dados da esteira (ex: Assunto = `{{ $json.nome_cliente }}, sua fatura chegou`).

### 2. Credenciais (Credentials)
* **Segurança em primeiro lugar:** Você **não** digita sua senha dentro do nó. O n8n salva a senha no "Cofre" (menu lateral) e o nó apenas faz uma referência a ela. Isso permite exportar fluxos sem vazar dados sensíveis.

### 3. Configurações do Motor (Settings / Engrenagem)
Controla o comportamento do n8n frente a problemas ou cargas de trabalho:
* **On Error (O que fazer em caso de erro?):**
    * *Stop Workflow:* Para a fábrica inteira (padrão).
    * *Continue (Continue Regular Output):* Aceita o erro, insere o aviso no `JSON` e continua a esteira.
* **Retry On Fail (Tentar novamente):** Em vez de falhar, tenta de novo. Permite configurar o *Max Tries* (tentativas) e o *Wait Between Tries* (tempo de espera entre elas).
* **Execute Once:** Força o nó a rodar apenas 1 vez (pegando apenas o primeiro item), ignorando o loop oculto natural do n8n.
* **Always Output Data:** Se uma busca (ex: banco de dados) não encontrar nada, a esteira ficaria vazia e o fluxo pararia silenciosamente. Essa opção força o nó a soltar um `JSON` vazio (`[{}]`), mantendo a esteira rodando para verificações futuras.
* **Timeout:** Define um tempo limite de execução. Se o nó travar aguardando um servidor externo, o n8n força a parada para não consumir toda a memória do sistema.

### 4. Propriedades Avançadas de Integração
Opções cruciais encontradas em nós de Apps e no **HTTP Request**:

* **Pagination (Paginação / Return All):** Usado para não derrubar APIs. Se a API tem 10.000 clientes, o n8n (com *Return All* ativado) busca a página 1, depois a 2, depois a 3 automaticamente, juntando tudo no final.
* **Add Field / Additional Options:** Oculta parâmetros não-obrigatórios. Sempre clique aqui para ver filtros, ordenações e superpoderes ocultos da integração.
* **Simplify Response:** Muitas APIs enviam "lixo" junto com o dado (status HTTP, headers). Essa opção limpa a resposta, entregando apenas a lista útil que você quer processar.
* **Batching / Send as Array:** Envio em lote. Em vez de fazer 500 requisições separadas para salvar 500 clientes no banco, o n8n agrupa todos em um pacote só e faz 1 única requisição rápida.
* **Allow Unauthorized Certificates:** Ignora erros de certificado SSL. Vital para conectar o n8n a servidores internos (intranet) ou ambientes de desenvolvimento (dev/homologação).
* **Ignore Response Code:** Se uma API retorna erro `404` (Não encontrado), o n8n costuma falhar o nó. Ativando isso, o n8n aceita o `404` como uma resposta normal, permitindo que o fluxo continue para um nó `If` e trate a ausência do dado de forma inteligente.

## Conceitos Avançados

Aqui entramos no território de um **Arquiteto de Automação (Tech Lead)**. Compreender estes conceitos com profundidade não apenas permite que você crie fluxos, mas garante que eles sejam escaláveis, seguros, fáceis de dar manutenção e que não quebrem o servidor da sua empresa.

---

### Fluxos Secundários (Sub-workflows)



> **A Analogia:** Imagine que na sua linha de montagem principal (Fluxo Pai), existe uma etapa muito complexa: *Montar o motor do carro*. Em vez de colocar as 50 máquinas de montar motor no meio da sua esteira principal (o que deixaria a fábrica caótica), você terceiriza isso. Você abre uma porta, envia as peças para um "Galpão Anexo" (Fluxo Filho). A esteira principal pausa, espera o Galpão Anexo montar o motor e devolver ele pronto. Assim que o motor volta, a esteira principal continua andando.

**Na Prática:** É a capacidade de um fluxo do n8n acionar outro fluxo do n8n usando o nó genérico **Execute Workflow**. 

**Por que isso é tão importante? (Vantagens de Arquitetura)**
* **Organização e Modularidade:** Mantém o seu fluxo principal limpo, legível e focado apenas na regra de negócio macro (a "orquestração").
* **Reutilização (A maior vantagem):** Se você tem um processo de "Buscar dados do cliente no ERP" ou "Gerar um link Pix", você não deve recriar esses nós em 10 fluxos diferentes. Você cria um fluxo "Filho" (módulo) só para isso e o "chama" quando precisar. Se a API do ERP mudar ou o banco trocar de token, você só arruma em **um único lugar**!
* **Isolamento de Erros e Debug:** Se o fluxo Filho der erro, a falha fica restrita àquele escopo. No painel de Execuções (Executions) do n8n, você pode abrir o log do fluxo Pai e clicar para "entrar" no log do fluxo Filho, facilitando rastrear onde o dado corrompeu.

**A Mecânica: Como eles conversam?**
1. **No Fluxo Pai (Quem chama):** Você usa o nó **Execute Workflow**. Você escolhe qual fluxo quer chamar (recomenda-se chamar pelo **ID do fluxo** e não pelo nome, pois se alguém renomear o fluxo filho, a conexão não quebra). O n8n empurra o pacote `JSON` que está na esteira naquele momento para o fluxo Filho.
    * *Dica Sênior:* No nó *Execute Workflow*, você pode escolher o modo de execução: **"Run Once with All Items"** (manda a lista inteira de uma vez pro fluxo filho) ou **"Run Once for Each Item"** (chama o fluxo filho separadamente para cada item da lista). Para integração com APIs, mandar tudo de uma vez costuma ser mais performático.
2. **No Fluxo Filho (Quem é chamado):** O fluxo Filho **obrigatoriamente** precisa começar com um gatilho específico chamado **Execute Workflow Trigger**. Ele atua como a "porta do galpão" que recebe as caixas do fluxo Pai. Sem esse gatilho, o fluxo não pode ser invocado internamente.
3. **O Retorno e a Saída:** O fluxo Filho devolve os dados do seu **último nó executado**. Quando ele termina o trabalho, o n8n pega o `JSON` final dessa tarefa, "teletransporta" de volta para o nó `Execute Workflow` do fluxo Pai, e a esteira do Pai volta a andar a partir dali com os novos dados processados.

---

### A Estrutura Obrigatória do Nó "Code" (JavaScript)



> **A Analogia:** Se o nó de Código for um operário altamente qualificado que montou um produto totalmente customizado, ele não pode simplesmente jogar o produto solto e desprotegido na esteira. Ele precisa colocar o produto dentro de uma **caixa padronizada**, colar uma **etiqueta específica ("json")** e só então soltar na esteira para que as próximas máquinas reconheçam o pacote.

O nó **Code** permite escrever JavaScript ou Python puro, sendo a principal ferramenta para formatar textos (Regex), cruzar arrays, ou fazer cálculos complexos. Porém, existe uma "casca de banana" onde 99% dos desenvolvedores escorregam: o n8n tem uma **regra estrita de embalagem** para o retorno dos dados. Como a "Arquitetura de Itens" exige que tudo seja uma Lista (Array) de Objetos, você precisa respeitar esse formato na hora de dar o comando `return`.

**A Regra de Ouro da Devolução:**

❌ **ERRADO (Vai quebrar o fluxo):**
O n8n não vai entender esse formato direto, pois ele espera metadados.
```javascript
return { nome: "Leandro", status: "ativo" };
```

✅ **CERTO (Padrão Ouro do n8n):**
Você envelopa os dados dentro de uma propriedade obrigatória chamada `json` e coloca isso dentro de uma lista `[ ]`.
```javascript
return [
  {
    json: {
      nome: "Leandro",
      status: "ativo"
    }
  }
];
```
*(Nota de versão: Versões mais recentes do n8n aceitam o retorno de apenas `{ json: { ... } }`, montando a lista automaticamente por trás para facilitar sua vida, mas o uso da propriedade `json:` continua sendo absolutamente obrigatório).*

**O "Dicionário" do Nó Code (Como ler e manipular os dados):**
Dentro do código, você não usa variáveis soltas. Você utiliza comandos nativos da API interna do n8n para "puxar" os dados das esteiras:

* `$input.first().json`: Pega apenas a **primeira "caixa"** que chegou na esteira naquele momento. É o comando mais seguro e usado quando você tem a certeza de que está processando um único item/cliente por vez.
* `$input.all()`: Devolve **todas as caixas** que chegaram de uma vez num formato de Array.
    * *Exemplo Avançado (Multiplicando itens):* Se você recebeu um array com 3 faturas dentro de 1 único item e quer transformar isso em 3 itens separados para a esteira (para que o próximo nó rode 3 vezes), você faz:
      ```javascript
      const faturas = $input.first().json.listaFaturas;
      // Transforma a matriz simples no padrão do n8n
      return faturas.map(fatura => {
          return { json: fatura }; 
      });
      ```
* `$('Nome do Nó').first().json`: A "máquina do tempo". Pega o resultado final de um nó que **já ficou muito para trás** no fluxo, sem precisar que esses dados passem por todas as conexões intermediárias. 
    * *Cuidado com o Item Matching:* Se você usar `$('Nó Antigo').item.json`, o n8n tenta achar o item de índice idêntico (ex: item 3 do nó atual buscando a resposta do item 3 do nó antigo). Se as listas tiverem tamanhos diferentes, dará erro. Por isso usamos o `.first().json` quando queremos um valor global e estático (como um token ou ID de usuário).

---

### O Cérebro da IA: A Engenharia por trás de "Agentes" e "Tools"



> **A Analogia:** Imagine que o Agente de IA é um Diretor Executivo brilhante e carismático, mas que fica trancado em uma sala sem internet. Ele é ótimo em conversar e deduzir coisas, mas não sabe qual é o saldo atual do cliente. As "Tools" (Ferramentas) são seus funcionários especialistas (o contador, o pesquisador, o analista de banco de dados). O Diretor não chuta a resposta; ele interfona para o contador, preenche um formulário de solicitação padrão, lê o relatório devolvido e só então responde ao cliente com propriedade e empatia.

**Na Prática (O Framework ReAct):**
No n8n (usando a integração com o ecossistema LangChain), o nó do **AI Agent** não é apenas um "gerador de texto cego" como a interface web do ChatGPT. Ele funciona usando um ciclo lógico e autônomo chamado **ReAct (Reason + Act / Raciocínio + Ação)**. 

**A Anatomia do Loop Interno do Agente:**
Quando o cliente manda: *"Quero pagar meu boleto vencido, meu CNPJ é 12.345.678/0001-90"*, o fluxo não gera a resposta na hora. O Agente entra em um loop cognitivo que você não vê na tela:
1. **System Prompt (A Personalidade):** Antes de tudo, o Agente lê suas diretrizes globais ("Você é a Esperanza, assistente de cobrança, seja educada, não prometa o que não pode cumprir...").
2. **Thought (O Raciocínio):** O Agente "pensa": *"O cliente quer pagar um boleto. Eu não tenho boletos na minha memória. Eu tenho uma ferramenta chamada `gerar_pagamento` que exige um CNPJ. Eu encontrei o CNPJ na mensagem do cliente."*
3. **The Schema (O Formulário de Requisição):** É aqui que a integração técnica ocorre. No nó da Tool (a ferramenta), existe uma aba de **Schema** (Esquema de Dados). Ali você define as regras estritas: "Esta ferramenta exige a variável `cnpj` e ela deve ser uma *String*". O modelo de linguagem gera internamente um JSON estruturado para acionar a ferramenta.
4. **Action (A Execução):** O Agente pausa o seu processamento semântico, envia o JSON para o fluxo secundário da Tool (o Sub-workflow que você construiu) e aguarda.
5. **Observation (O Retorno):** O Sub-workflow roda, acessa o ERP da empresa, gera o código Pix e devolve um texto cru ou um JSON (ex: `{"status": "sucesso", "codigoPix": "0002012658..."}`). O Agente lê essa observação técnica.
6. **Final Answer (A Resposta Final):** Só após obter todos os dados necessários (ou após perceber que a ferramenta falhou), o Agente formula a resposta humanizada: *"Perfeito! Aqui está o seu código Pix gerado para o CNPJ informado..."*.

> [!IMPORTANT]
> **Técnicas Avançadas para Tools:**
> * **Engenharia de Prompt nas Descrições:** O Agente só escolhe a Tool certa se a *descrição (Description)* que você digitou na ferramenta for impecável. Uma descrição curta como "*gera pagamento*" faz a IA alucinar e usar na hora errada. Uma descrição de nível Sênior seria: "*USE ESTA TOOL SEMPRE que o cliente solicitar expressamente um boleto, código pix ou código de barras. Requer extrair o CNPJ do cliente. Não use para dúvidas gerais.*".
> * **Memória (Memory Nodes):** O Agente não tem memória longa natural. Você precisa anexar um nó de Memória (ex: *Window Buffer Memory*) que puxa as últimas 'X' mensagens da Thread do banco de dados, caso contrário, a IA esquecerá o que o cliente disse na mensagem anterior.
> * **Max Iterations (Proteção contra Loops Infinitos):** Se uma Tool der erro (ex: a API do banco cair), um Agente mal configurado vai tentar rodar a Tool de novo, e de novo, torrando todo o seu saldo na OpenAI. Na aba "Settings" do AI Agent, sempre configure o `Max Iterations` (limite de iterações, ex: 3 a 5) para que ele desista e emita uma resposta de segurança: "Estou com instabilidade no sistema, tente novamente mais tarde".

---

### Tratamento Global de Erros (Error Trigger & Observabilidade)



> **A Analogia:** Nós já vimos que o botão "Continue On Fail" (na engrenagem de um nó específico) é como um operário sabendo lidar com um erro local (ex: "se o e-mail não foi, deixe em branco e continue"). Mas e se a fábrica inteira pegar fogo de madrugada? E se o banco de dados principal cair? Você precisa de um "Guarda Noturno" e um "Sistema de Alarme Central". O Guarda fica em um galpão blindado e só acorda para acionar os engenheiros quando a linha de produção colapsa por inteiro.

**Na Prática (Observabilidade e Recuperação):**
Nenhum fluxo de produção está imune a instabilidades. Apagar incêndios perguntando "o que aconteceu?" é amador. O **Error Trigger** (Gatilho de Erro) é a garantia de que sua empresa será notificada no mesmo segundo que algo crítico falhar.

**Como estruturar essa técnica de resiliência:**
1. **O Fluxo Guarda Noturno:** Você cria um fluxo **completamente novo e isolado**. O nó inicial (gatilho) é unicamente o `Error Trigger`. Depois dele, você coloca um nó de notificação (ex: enviar uma mensagem para um canal do Slack/Teams da equipe de TI, ou criar um card urgente no Trello).
2. **Conectando o Alarme:** Você volta no seu fluxo principal (o da Esperanza), vai em **Workflow Settings** (Configurações do Fluxo) e, no campo "Error Workflow", seleciona o fluxo "Guarda Noturno" que acabou de criar. Se qualquer nó do fluxo principal falhar fatalmente (Stop Workflow), a execução é abortada e o alerta é disparado automaticamente.

**A Estrutura de Dados do Erro (O que o n8n te entrega no Error Trigger):**
O fluxo de erro recebe um pacote JSON riquíssimo com o "diagnóstico" da falha:
* `$json.execution.id`: O número da "OS" (ID) daquela execução específica.
* `$json.execution.workflowId` e `workflowName`: O nome exato de onde o erro aconteceu.
* `$json.execution.error.message`: O motivo do erro (ex: *"404 Not Found"*, *"Connection Timeout"*, *"Invalid JSON"*).
* `$json.execution.lastNodeExecuted`: O nome exato do "operário" (nó) que quebrou.

**Técnicas de Arquitetura Sênior:**
* **URL Dinâmica de Debug:** O maior diferencial é mandar o alerta no Slack já com o link clicável direto para a tela gráfica do erro. Você monta isso usando expressões: 
   `https://[SEU-DOMINIO-N8N]/workflow/{{$json.execution.workflowId}}/executions/{{$json.execution.id}}`
   Assim, ao receber a notificação no celular, você clica e cai exatamente no nó vermelho com problema.
* **Saída de Erro Local (Error Output):** Em versões recentes do n8n, os nós de integração possuem uma saída extra (um ponto vermelho além do ponto cinza/verde padrão). Se ativada, quando aquele nó falha, em vez de parar todo o fluxo (e chamar o Guarda Noturno), ele desvia os dados para um caminho secundário. Isso permite "Tratamento de Exceções Direcionado" (Ex: Se a API 1 falhar, siga pelo fio vermelho e tente a API 2 de backup).

---

### Variáveis de Ambiente, de Fluxo e de Sistema ($env, $vars, $execution)

> **A Analogia:** Se o endereço do porto de entregas mudou e você escreveu isso com caneta permanente na mesa de 50 operários diferentes, você terá que parar a fábrica, ir de mesa em mesa, apagar e reescrever 50 vezes. O ideal é ter um **Quadro de Avisos Global**. O operário não decora o endereço; ele simplesmente lê o quadro na parede no momento de despachar. Se o gerente atualizar o quadro uma única vez, a fábrica inteira passa a usar a nova rota instantaneamente.

**Na Prática (Gestão de Estado e Configurações):**
Colocar valores fixos ou sensíveis diretamente dentro dos campos dos nós — prática conhecida como *Hardcoding* (como escrever URLs de APIs de produção, números de telefone padrão para testes ou emails de gestores) — é uma má prática de programação. O n8n gerencia isso de forma robusta e dinâmica através de três categorias de variáveis globais injetadas na memória.

#### 1. Variáveis de Sistema (O Contexto da Execução)
O n8n injeta dados sobre "o momento presente" e sobre "ele mesmo" que você pode acessar de qualquer lugar usando expressões:
* `{{ $execution.id }}`: Retorna o ID único da execução atual. Excelente para rastreabilidade (ex: enviar esse ID no cabeçalho HTTP para a sua API, assim, se o desenvolvedor backend ver um erro no banco, ele sabe exatamente qual execução no n8n causou aquilo).
* `{{ $now }}`: Baseado na biblioteca Luxon (muito melhor que o *Date* padrão do JS). Substitui a necessidade de criar nós de "Date & Time". Traz a data/hora exatas. 
    * *Uso Prático:* No seu fluxo, vi o uso de `{{ $now.toISO() }}`, que gera a string (ex: `2024-03-02T14:30:00.000Z`). É a forma mais profissional e à prova de falhas de fuso horário para salvar carimbos de tempo (timestamps) em bancos como o MongoDB.

#### 2. Variáveis de Fluxo (`$vars` ou Variables)
* **O que são:** O "Quadro de Avisos" restrito a um único fluxo (escopo local).
* **Onde ficam:** Clicando no fundo da tela do fluxo > **Workflow Settings** > **Variables**.
* **Como usar:** `{{ $vars.DIAS_TOLERANCIA }}` ou `{{ $vars.EMAIL_ADMIN }}`.
* **Quando usar:** Para regras de negócio (Business Rules) daquele fluxo específico. Permite que um analista ou gerente altere a tolerância de um boleto de 3 para 5 dias na tela de configurações, sem nunca precisar abrir, ler ou entender a complexidade dos nós internos do fluxo.

#### 3. Variáveis de Ambiente (`$env`)
* **O que são:** O nível mais alto, profundo e global de configuração. São visíveis para **todos os fluxos** de toda a instância do n8n.
* **Onde ficam:** Elas não são criadas na interface visual. Elas residem a nível de infraestrutura, cadastradas no arquivo `.env` do servidor (seja Docker, Linux ou Railway/AWS onde seu n8n roda). Ex: `WEBHOOK_BITRIX_URL=https://blips.bitrix24...`
* **Como usar:** `{{ $env.WEBHOOK_BITRIX_URL }}`
* **A Técnica Sênior de Dev/Prod (CI/CD):** Imagine que você possui um servidor n8n de "Homologação" (testes) e outro n8n de "Produção" (onde os clientes reais estão). Se você fixar a URL da sua API de cobranças direto no nó, ao migrar o fluxo de Testes para Produção, você vai acabar fazendo cobranças irreais em clientes reais se esquecer de trocar o campo.
Ao usar `{{ $env.API_COBRANCA }}`, você pode exportar o arquivo JSON do seu fluxo do ambiente de testes e importar na Produção sem alterar uma única vírgula. A mágica acontece porque o n8n de testes lerá a URL de *mock/sandbox* do arquivo `.env` dele, enquanto o n8n de produção lerá a URL real e oficial do `.env` dele automaticamente.

> [!WARNING]
> **Segurança (O que NUNCA fazer):** > Nunca use Variáveis de Fluxo (`$vars`) ou de Ambiente (`$env`) para armazenar **Senhas, Tokens de API ou Chaves Privadas** (ex: seu `Bearer Token` da OpenAI). 
> **Motivo:** Variáveis de fluxo e ambiente ficam expostas no código JSON quando você exporta o fluxo e podem aparecer em formato legível nos logs do servidor. 
> **A Solução Correta:** **Sempre** utilize a funcionalidade nativa de **Credentials** do n8n para senhas. O "Cofre" de credenciais salva sua senha criptografada no banco de dados e só injeta o dado real de forma oculta na exata fração de segundo em que a requisição sai do servidor, garantindo total isolamento de dados sensíveis.