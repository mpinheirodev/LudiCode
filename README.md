<div align="center">

# LudiCode

# Compilador para Robótica Educacional

</div>

<div align="start">

O **LudiCode** é um compilador desenvolvido em Python (utilizando a biblioteca :contentReference[oaicite:0]{index=0}) para uma linguagem de programação educacional focada no ensino de lógica e controle de hardware. Com uma sintaxe amigável e inteiramente em português brasileiro, o projeto busca quebrar a barreira do idioma e reduzir a curva de aprendizado para estudantes no mundo do pensamento computacional.

Diferente de linguagens de propósito geral, a LudiCode foi pensada para interagir com o mundo físico. A linguagem possui comandos nativos e simplificados para controle de atuadores e leitura de dados. Isso permite que conceitos abstratos de programação se transformem rapidamente em ações reais — seja para acionar um motor DC, interpretar um sensor de distância ou construir a rotina autônoma de varredura e ataque de um robô sumô.

## Principais Características

- **Sintaxe em Português Natural:** Estruturas de controle que soam como frases do dia a dia (`se`, `senão`, `enquanto`, `repita`), facilitando a assimilação da lógica.
- **Foco em Hardware:** Comandos integrados nativamente (como `ligarMotor`, `pararMotor` e `lerSensor`) para acelerar o desenvolvimento de projetos de robótica.
- **Tipagem Dinâmica e Simples:** Sem ponteiros ou gerenciamento complexo de memória. As variáveis (`var`) adaptam-se aos dados numéricos, lógicos ou de texto, permitindo que o foco fique 100% no algoritmo.
- **Fundamento Acadêmico:** Desenvolvido como projeto universitário, contemplando todas as fases clássicas de construção de um compilador — desde a análise léxica (Scanner) e sintática (Parser/AST), até a avaliação semântica e documentação tipográfica em LaTeX.

---

## Como executar o Projeto

```git clone https://github.com/seu-usuario/LudiCode.git````
```cd LudiCode```
```pip install -r requirements.txt```
```python main.py```

ou executar um arquivo .ludi:
```python main.py ./tests/teste_enquanto.ludi```

## Exemplo de código
```var idade = 18

se idade >= 18 então
    mostrar("Maior de idade")
senão
    mostrar("Menor de idade")
fim```

### Saída Esperada
```Maior de idade```