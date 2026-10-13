"""Artigos de exemplo. Entram no banco só na primeira vez (ou quando SEED_VERSION sobe e o slug ainda não existe).
Troque, edite ou apague à vontade pela API: apagar um deles não o traz de volta."""

SEED_VERSION = 2

SEED_POSTS = [
    # ---------- Nintendo ----------
    {
        "slug": "o-que-a-fase-1-1-de-super-mario-bros-ensina-sobre-design",
        "title": "O que a fase 1-1 de Super Mario Bros. ensina sobre design de jogos",
        "excerpt": "A primeira fase do Mario ensina a jogar sem uma linha de texto. Veja como ela faz isso e o que dá para aprender com ela.",
        "tag": "Nintendo",
        "published_at": "2026-10-13",
        "featured": 1,
        "content": """Abra Super Mario Bros. e você não lê nenhum tutorial. Mesmo assim, em poucos segundos você já sabe andar, pular e desviar de inimigos. A fase 1-1 é considerada por muita gente uma aula de design de jogos, e vale entender por quê.

## Ensinar sem explicar

Logo no começo, o caminho é livre e você só pode ir para a direita. Não há perigo, então você experimenta os controles à vontade. Pouco depois aparece o primeiro inimigo, um Goomba, que vem em sua direção. Você tem duas opções: pular nele ou levar o dano. Em poucas tentativas você aprende que pular em cima derrota o inimigo.

## Mostrar antes de exigir

Os blocos com ponto de interrogação ficam no alto, chamando a atenção. Ao bater neles de baixo, sai um item. O cogumelo que aparece é difícil de evitar por causa da posição dos blocos ao redor, então você acaba pegando e descobre que ele deixa o Mario maior.

## Risco crescente

Depois do básico, entram buracos e canos. Cada elemento novo aparece primeiro em uma situação segura e só depois em uma situação perigosa. Esse ritmo, apresentar, praticar e combinar, é usado até hoje.

## O que levar para os seus projetos

- Mostre a regra no jogo em vez de despejar texto.
- Crie um espaço seguro para o jogador errar sem medo.
- Introduza um elemento novo por vez.

Se você quer fazer seu primeiro jogo, a melhor dica é copiar essa ideia: comece com uma mecânica simples e deixe o jogador descobrir o resto.""",
    },
    {
        "slug": "game-boy-por-que-uma-tecnologia-simples-venceu",
        "title": "Game Boy: por que uma tecnologia simples venceu",
        "excerpt": "O Game Boy não tinha a tela mais bonita nem o chip mais forte. Mesmo assim, virou um clássico. A explicação está em uma ideia de design.",
        "tag": "Nintendo",
        "published_at": "2026-10-10",
        "featured": 0,
        "content": """Quando o Game Boy chegou, outros portáteis tinham tela colorida e processadores mais potentes. Ainda assim, o aparelho da Nintendo foi o que marcou época. A razão tem a ver com escolhas simples e bem pensadas.

## A ideia por trás

O engenheiro Gunpei Yokoi defendia o que ficou conhecido como pensamento lateral com tecnologia madura: usar componentes baratos, conhecidos e confiáveis, e criar algo divertido com eles. Em vez de perseguir o hardware mais novo, o foco era a experiência de jogar.

## O que isso significou na prática

- **Bateria que durava.** A tela monocromática gastava pouca energia, então dava para jogar por muito tempo longe da tomada.
- **Preço acessível.** Peças simples ajudaram a manter o aparelho barato.
- **Resistência.** O console aguentava o dia a dia de quem leva tudo na mochila.
- **Bons jogos.** Títulos como Tetris mostraram que diversão não depende de gráficos.

## A lição para quem programa

Escolher a ferramenta mais moderna não garante um bom produto. Muitas vezes o melhor caminho é usar algo simples que você domina e dedicar o tempo ao que importa: a experiência de quem vai usar.""",
    },
    # ---------- Games ----------
    {
        "slug": "o-que-e-uma-engine-de-jogos-unity-unreal-e-godot",
        "title": "O que é uma engine de jogos? Unity, Unreal e Godot explicadas",
        "excerpt": "Engine é o motor que faz um jogo funcionar. Entenda o que ela faz e como escolher entre Unity, Unreal e Godot para começar.",
        "tag": "Games",
        "published_at": "2026-10-12",
        "featured": 1,
        "content": """Uma engine de jogos é um conjunto de ferramentas que cuida das partes repetitivas de criar um jogo, para que você foque no que o deixa único. Sem ela, você teria que escrever do zero como desenhar na tela, detectar colisões e tocar sons.

## O que uma engine faz

- **Gráficos:** desenha personagens, cenários e efeitos na tela.
- **Física:** calcula quedas, colisões e movimento.
- **Áudio:** toca músicas e efeitos.
- **Entrada:** lê teclado, mouse e controle.
- **Editor:** permite montar fases arrastando elementos, sem escrever tudo em código.

## Três opções populares

### Unity
Usa a linguagem C#. É muito usada em jogos móveis e independentes e tem uma comunidade enorme, com muitos tutoriais.

### Unreal Engine
Conhecida pelos gráficos realistas. Usa C++ e um sistema visual chamado Blueprints, que permite criar lógica ligando blocos.

### Godot
É gratuita e de código aberto. Tem a linguagem GDScript, parecida com Python, e é leve, o que a torna ótima para aprender.

## Qual escolher para começar?

Se você é iniciante, Godot costuma ser a porta de entrada mais simples. Se o seu objetivo é trabalhar na indústria, vale conhecer Unity e Unreal também. O mais importante é escolher uma e terminar um projeto pequeno.""",
    },
    {
        "slug": "o-loop-de-jogo-o-coracao-de-todo-game",
        "title": "O loop de jogo: o coração de todo game",
        "excerpt": "Por trás de qualquer jogo existe um laço que se repete dezenas de vezes por segundo. Entenda como ele funciona com um exemplo em código.",
        "tag": "Games",
        "published_at": "2026-10-08",
        "featured": 0,
        "content": """Todo jogo, do mais simples ao mais complexo, roda sobre a mesma ideia: um laço que se repete sem parar enquanto o jogo está aberto. Esse laço é chamado de **loop de jogo**.

## Os três passos

A cada volta, o jogo faz três coisas em ordem:

- **Ler a entrada:** o que o jogador apertou?
- **Atualizar o estado:** mover personagens, aplicar regras, checar colisões.
- **Desenhar:** mostrar o resultado na tela.

## Um exemplo em JavaScript

```js
let x = 0;

function loop() {
  // 1. entrada: nada por enquanto
  // 2. atualizar
  x += 2;
  // 3. desenhar
  console.log("posição:", x);
  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
```

A função `requestAnimationFrame` pede ao navegador para chamar o `loop` de novo antes da próxima atualização da tela. Assim o jogo continua rodando.

## Por que o tempo importa

Se o jogo andasse um passo fixo por volta, ele seria mais rápido em computadores potentes. Por isso muitos jogos medem o tempo entre uma volta e outra e multiplicam o movimento por esse valor.

## Próximo passo

Tente fazer um quadrado se mover na tela usando o teclado. Quando isso funcionar, você já entendeu a base de qualquer jogo.""",
    },
    {
        "slug": "jogos-que-ensinam-logica-de-programacao",
        "title": "Jogos que parecem aula de programação",
        "excerpt": "Alguns jogos ensinam lógica sem você perceber. Uma lista de títulos para treinar o raciocínio de quem programa ou quer começar.",
        "tag": "Games",
        "published_at": "2026-09-30",
        "featured": 0,
        "content": """Programar é, em grande parte, resolver problemas com regras. Por isso vários jogos de quebra-cabeça funcionam como treino para quem quer aprender. Aqui vão alguns que valem a pena.

## Baba Is You

As regras do jogo ficam escritas na própria fase, em blocos de palavras que você pode mover. Mudar uma regra muda tudo, e isso lembra muito alterar uma linha de código para mudar o comportamento de um programa.

## Human Resource Machine

Você dá instruções a um funcionário de escritório para resolver tarefas, usando comandos parecidos com os de uma linguagem simples. É uma boa introdução a ideias como repetição, condições e variáveis.

## Jogos da Zachtronics

Estúdio conhecido por quebra-cabeças que lembram programação de verdade. Alguns, como Shenzhen I/O, usam um código parecido com o de microcontroladores. São mais difíceis e indicados para quem já tem alguma base.

## O que treinar com eles

- **Decompor problemas** em partes menores.
- **Testar hipóteses** e aprender com os erros.
- **Pensar em padrões** que se repetem.

Se o seu objetivo é aprender a programar, jogar é um bom complemento. Mas lembre-se de também escrever código: a prática continua sendo a parte principal.""",
    },
    # ---------- IA ----------
    {
        "slug": "o-que-e-um-modelo-de-linguagem-sem-misterio",
        "title": "O que é um modelo de linguagem, sem mistério",
        "excerpt": "Você já conversou com uma IA. Mas como ela funciona por dentro? Uma explicação simples, sem fórmulas, e com os limites que você precisa conhecer.",
        "tag": "IA",
        "published_at": "2026-10-11",
        "featured": 1,
        "content": """Um modelo de linguagem é um programa treinado para trabalhar com texto. Quando você escreve uma pergunta, ele gera uma resposta palavra por palavra, escolhendo a continuação mais adequada com base no que aprendeu.

## Como ele aprende

Durante o treinamento, o modelo lê uma quantidade enorme de textos e ajusta milhões de parâmetros internos para prever melhor qual trecho vem a seguir. Ele não guarda os textos como um arquivo. Ele aprende padrões de como a linguagem funciona.

## Como ele responde

Ao receber a sua mensagem, o modelo calcula as continuações mais prováveis e escolhe uma. Depois repete o processo com a nova palavra incluída, e assim vai montando a resposta.

## Limites importantes

- **Pode errar com confiança.** Uma resposta bem escrita não é garantia de que esteja correta. Confira informações importantes.
- **Não sabe o que aconteceu depois do treinamento,** a menos que tenha acesso a ferramentas de busca.
- **Pode refletir vieses** dos textos com que aprendeu.

## Como usar bem

Trate a IA como um assistente que dá um primeiro rascunho. Peça explicações, exemplos e revisões, mas valide o resultado, principalmente em temas de saúde, dinheiro ou leis.

Entender esses limites é o primeiro passo para tirar proveito da ferramenta sem cair em armadilhas.""",
    },
    {
        "slug": "como-pedir-melhor-para-uma-ia-cinco-dicas",
        "title": "Como pedir melhor para uma IA: 5 dicas simples",
        "excerpt": "A qualidade da resposta depende muito da forma como você pergunta. Cinco hábitos fáceis para melhorar os seus pedidos.",
        "tag": "IA",
        "published_at": "2026-10-05",
        "featured": 0,
        "content": """Quando a resposta de uma IA decepciona, muitas vezes o problema está no pedido. Pequenos ajustes fazem uma grande diferença.

## 1. Diga o objetivo

Em vez de \"explique SQL\", escreva \"explique SQL para quem já sabe Excel e quer analisar vendas\". Quanto mais claro o objetivo, mais útil a resposta.

## 2. Dê o contexto

Informe o que você já tentou, o que tem em mãos e quais limites existem. Se for código, cole o trecho e a mensagem de erro.

## 3. Peça um formato

Diga como quer receber: uma lista, uma tabela, um passo a passo, um texto curto. Isso evita respostas longas e confusas.

## 4. Peça exemplos

Exemplos concretos ajudam a entender. Você pode pedir \"dê dois exemplos simples e um mais difícil\".

## 5. Itere

Raramente a primeira resposta é a final. Peça ajustes: \"deixe mais curto\", \"explique como se eu tivesse 12 anos\", \"mostre outra abordagem\".

## Um exemplo completo

```
Sou iniciante em Python. Explique o que é uma lista,
em até 5 linhas, e mostre 2 exemplos com frutas.
Depois me dê um exercício para praticar.
```

Esse pedido tem objetivo, contexto, formato e exemplos. Teste e compare com uma pergunta solta: a diferença costuma ser grande.""",
    },
    # ---------- Mundo de Dados ----------
    {
        "slug": "sql-em-cinco-consultas",
        "title": "SQL em cinco consultas: do básico ao JOIN",
        "excerpt": "Com cinco comandos você já consegue extrair respostas de um banco de dados. Veja cada um com um exemplo simples de vendas.",
        "tag": "Mundo de Dados",
        "published_at": "2026-10-09",
        "featured": 1,
        "content": """SQL é a linguagem usada para conversar com bancos de dados. Para começar, imagine uma tabela de vendas com as colunas `produto`, `categoria`, `valor` e `cliente_id`.

## 1. SELECT: escolher colunas

```sql
SELECT produto, valor
FROM vendas;
```

Mostra só as colunas que você pediu.

## 2. WHERE: filtrar linhas

```sql
SELECT produto, valor
FROM vendas
WHERE valor > 100;
```

Traz apenas as vendas acima de 100.

## 3. ORDER BY: ordenar

```sql
SELECT produto, valor
FROM vendas
ORDER BY valor DESC;
```

Do maior para o menor valor. Use `ASC` para o contrário.

## 4. GROUP BY: resumir

```sql
SELECT categoria, SUM(valor) AS total
FROM vendas
GROUP BY categoria;
```

Soma o valor de cada categoria. É a base de muitos relatórios.

## 5. JOIN: juntar tabelas

```sql
SELECT c.nome, v.produto, v.valor
FROM vendas v
JOIN clientes c ON c.id = v.cliente_id;
```

Combina a tabela de vendas com a de clientes, ligando os dois pelo identificador.

## Como praticar

Crie um banco de teste e invente dados parecidos com os de um negócio que você conhece. Responder perguntas reais, como qual categoria vende mais, é a melhor forma de fixar.""",
    },
    {
        "slug": "o-que-faz-uma-pessoa-analista-de-dados",
        "title": "O que faz uma pessoa analista de dados no dia a dia",
        "excerpt": "Planilhas, SQL e muita conversa. Uma visão realista da rotina de quem trabalha com dados e das habilidades para começar.",
        "tag": "Mundo de Dados",
        "published_at": "2026-10-03",
        "featured": 0,
        "content": """A profissão de analista de dados costuma parecer misteriosa de fora. Na prática, o trabalho gira em torno de uma pergunta: o que os números estão dizendo sobre o negócio?

## Uma rotina típica

- **Entender a pergunta.** Antes de abrir qualquer ferramenta, conversar com quem precisa da resposta.
- **Buscar e limpar dados.** Muitas vezes é a parte mais demorada, porque os dados vêm com erros e lacunas.
- **Analisar.** Usar SQL, planilhas ou linguagens como Python para calcular e comparar.
- **Mostrar o resultado.** Criar gráficos e painéis, e explicar com clareza o que foi encontrado.

## Ferramentas comuns

SQL para consultar bancos, planilhas para análises rápidas, Python ou R para análises maiores, e ferramentas de painéis para apresentar os resultados.

## Habilidades que ajudam

- Curiosidade para fazer boas perguntas.
- Cuidado com os detalhes, porque um filtro errado muda a conclusão.
- Comunicação: de nada adianta uma boa análise que ninguém entende.

## Como começar

Escolha um assunto que você gosta, como futebol, jogos ou finanças pessoais, encontre dados públicos sobre ele e tente responder uma pergunta. Compartilhe o resultado. Esse tipo de projeto vale mais do que uma lista de cursos.""",
    },
    # ---------- Programação ----------
    {
        "slug": "o-que-e-uma-api-explicado-com-um-restaurante",
        "title": "O que é uma API, explicado com um restaurante",
        "excerpt": "Todo dev fala de API o tempo todo. Em poucos minutos você entende o conceito com uma cena que todo mundo já viveu: pedir comida.",
        "tag": "Programação",
        "published_at": "2026-10-07",
        "featured": 0,
        "content": """Você chega a um restaurante, senta e abre o cardápio. Não entra na cozinha para pegar o ingrediente nem ensina o cozinheiro a fazer o prato. Você faz o pedido ao garçom e o prato chega na mesa.

Esse garçom é a **API**.

## Os três papéis da cena

- **Você** é o aplicativo que precisa de algo, como o clima de hoje ou a lista de filmes em cartaz.
- **A cozinha** é o servidor, onde os dados e as regras de verdade vivem.
- **O garçom** é a API: recebe o pedido num formato combinado, leva até a cozinha e traz a resposta.

O cardápio também faz parte. Ele diz o que você pode pedir e como pedir. Numa API, esse cardápio é a **documentação**.

## Como isso aparece no código

Quando um app pede dados, ele faz uma requisição HTTP. O servidor responde, quase sempre em JSON:

```js
const resposta = await fetch("https://api.exemplo.com/filmes");
const filmes = await resposta.json();
console.log(filmes[0].titulo);
```

Se você pedir algo que não existe, o garçom avisa. Em HTTP isso é um código de status, como `404` para "não encontrei".

## Por que isso importa

Graças às APIs, quem faz o app de previsão do tempo não precisa montar uma estação meteorológica. Basta pedir o dado a quem já tem. Entender esse fluxo de pedido e resposta é um dos primeiros passos para criar qualquer coisa útil na web.""",
    },
    {
        "slug": "hello-world-em-quatro-linguagens",
        "title": "Hello, World em quatro linguagens",
        "excerpt": "O primeiro programa de quase todo dev é imprimir uma saudação. Veja como ele muda de uma linguagem para outra.",
        "tag": "Programação",
        "published_at": "2026-10-06",
        "featured": 0,
        "content": """O famoso \"Hello, World\" é o primeiro programa de quase todo mundo. Ele serve para provar que o ambiente funciona e para mostrar o jeito de cada linguagem.

## Python

```python
print("Hello, World!")
```

Uma linha, sem cerimônia. Por isso muita gente começa por aqui.

## JavaScript

```js
console.log("Hello, World!");
```

Roda no navegador e também no servidor com Node.js.

## C

```c
#include <stdio.h>

int main(void) {
    printf("Hello, World!\\n");
    return 0;
}
```

Mais passos, porque em C você diz ao computador cada detalhe: qual biblioteca usar e onde o programa começa.

## F#

```fsharp
[<EntryPoint>]
let main argv =
    printfn "Hello, World!"
    0
```

Esse é o trecho que aparece no visual da Nerd Dev. A função `main` é o ponto de entrada e o `0` no final é o código de saída, que significa "terminou sem erro".

## O que observar

Todas fazem a mesma coisa, mas mostram escolhas diferentes: algumas priorizam a simplicidade, outras o controle. Conhecer mais de uma linguagem ajuda a entender o que é essencial em programação e o que é só sintaxe.""",
    },
    # ---------- Ferramentas ----------
    {
        "slug": "git-em-cinco-comandos",
        "title": "Git em cinco comandos",
        "excerpt": "Você não precisa decorar o Git inteiro para começar. Cinco comandos já cobrem o dia a dia de um projeto pequeno.",
        "tag": "Ferramentas",
        "published_at": "2026-10-04",
        "featured": 0,
        "content": """Git é um sistema que guarda o histórico do seu projeto. Se algo quebra, você volta no tempo. Se duas pessoas mexem no mesmo código, o Git ajuda a juntar tudo.

Para começar, cinco comandos bastam.

## 1. Criar o repositório

```bash
git init
```

Transforma a pasta atual em um repositório Git.

## 2. Ver o que mudou

```bash
git status
```

Mostra quais arquivos foram alterados e o que já está pronto para ser salvo.

## 3. Escolher o que entra no próximo registro

```bash
git add .
```

O ponto significa "tudo o que mudou". Para ser mais cuidadoso, passe o nome de um arquivo no lugar.

## 4. Salvar um registro

```bash
git commit -m "Adiciona a página inicial"
```

Um commit é uma foto do projeto naquele momento. Escreva a mensagem dizendo o que mudou, no presente.

## 5. Conferir o histórico

```bash
git log --oneline
```

Lista os commits, do mais novo para o mais antigo.

## E depois?

Com esses cinco você já registra seu trabalho. O próximo passo natural é aprender sobre **branches** e sobre enviar o código para o GitHub com `git push`.""",
    },
    # ---------- Carreira ----------
    {
        "slug": "como-comecar-em-tecnologia-sem-se-perder",
        "title": "Como começar em tecnologia sem se perder",
        "excerpt": "Tem muita área, muita linguagem e muito curso. Um caminho simples para dar os primeiros passos sem pular de tutorial em tutorial.",
        "tag": "Carreira",
        "published_at": "2026-10-02",
        "featured": 0,
        "content": """O maior obstáculo de quem está começando raramente é a dificuldade. É a quantidade de opções. Web, dados, jogos, mobile, segurança: por onde ir?

## Escolha uma direção por agora

Você não precisa decidir sua carreira inteira. Escolha uma área para explorar por alguns meses. Se não gostar, você troca e leva junto tudo o que aprendeu, porque a base é a mesma: lógica, variáveis, condições, repetições e funções.

## Aprenda fazendo

Assistir aula dá a sensação de progresso, mas o aprendizado acontece quando você escreve código e algo quebra. Depois de cada conceito, crie uma coisa pequena:

- uma calculadora de gorjeta
- uma lista de tarefas
- um quiz sobre seu filme ou jogo favorito

## Mantenha um registro

Guarde o que você construiu em um repositório no GitHub. Com o tempo, isso vira um portfólio que mostra sua evolução melhor do que qualquer lista de cursos.

## Pergunte e compartilhe

Comunidades existem para isso. Pergunte quando travar e, quando entender, explique para outra pessoa. Ensinar é uma das melhores formas de fixar.""",
    },
    # ---------- Cultura Pop ----------
    {
        "slug": "por-que-filmes-de-hacker-erram-o-teclado",
        "title": "Por que filmes de hacker erram o teclado",
        "excerpt": "Telas verdes, digitação em velocidade absurda e senhas descobertas em segundos. Uma conversa leve sobre o que o cinema inventa e o que acontece na vida real.",
        "tag": "Cultura Pop",
        "published_at": "2026-09-28",
        "featured": 1,
        "content": """Todo mundo já viu a cena: alguém senta, digita furiosamente, e em poucos segundos aparece escrito \"acesso liberado\" em letras grandes.

Na vida real, o trabalho é bem diferente, e é isso que torna a conversa divertida.

## O que o cinema costuma inventar

- **Interfaces chamativas.** Programas reais costumam ser texto simples e discreto, não animações piscando.
- **Velocidade.** Quebrar proteção de verdade pode levar tempo, tentativa e muito estudo.
- **Gente sozinha com tudo pronto.** No mundo real, boa parte do trabalho é ler documentação e testar hipóteses.

## O que é parecido

O terminal existe e é muito usado. Programar passa por escrever comandos, ler mensagens de erro e corrigir. A diferença é que a cena de cinema corta a parte em que o dev passa uma hora procurando um ponto e vírgula esquecido.

## Para quem quer ver o lado real

Se a cena te deixou curioso, o melhor é aprender o básico de redes e de programação. Entender como as coisas funcionam torna os filmes mais divertidos, porque você começa a notar os exageros.""",
    },
]
