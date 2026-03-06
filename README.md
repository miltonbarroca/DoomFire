# DoomFire

Uma recriacao do efeito de fogo do DOOM no terminal usando Python e `curses`.

O projeto suporta tres modos de renderizacao:

- `ASCII mode`
- `Color mode`
- `Block mode`

Tambem inclui um menu de opcoes para ajustar propriedades da simulacao, como intensidade da fonte, `decay` maximo e velocidade de atualizacao.

## Requisitos

- Python 3
- Terminal com suporte a `curses`

## Como executar

No diretorio do projeto:

```bash
python3 main.py
```

## Controles

### Menu principal

- `Setas para cima/baixo`: navegar entre itens
- `Enter`: iniciar no modo selecionado, abrir `Options` ou sair

### Menu de opcoes

- `Setas para cima/baixo`: navegar entre propriedades
- `Setas para esquerda/direita`: diminuir ou aumentar o valor
- `R`: restaurar valores padrao
- `Enter` ou `Esc`: voltar ao menu principal

## Opcoes disponiveis

- `Source intensity`: intensidade da linha que alimenta o fogo
- `Max decay`: quanto a intensidade pode cair em cada propagacao
- `Frame delay`: intervalo entre frames da animacao

## Estrutura

- [main.py](/home/morgoth/Projetos/DoomFire/main.py): menu, loop principal e integracao geral
- [fire.py](/home/morgoth/Projetos/DoomFire/fire.py): simulacao e configuracao do fogo
- [render.py](/home/morgoth/Projetos/DoomFire/render.py): renderizacao em `ascii`, cor e blocos

## Observacoes

- O `Block mode` usa fundo colorido para evitar flicker em alguns terminais.
- A simulacao usa uma linha extra oculta como fonte de combustivel, o que deixa a base visivel mais estavel.

## Ideias futuras

- suporte a vento lateral
- troca de paleta de cores
- empacotamento como aplicativo instalavel
