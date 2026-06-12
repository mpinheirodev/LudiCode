import sys
from lexer import LudiCodeLexer
from parse import LudiCodeParser
from interpreter import LudiCodeInterpreter
from sly.lex import LexError

def executar_bloco(codigo_fonte, lexer, parser, interpretador):
    if not codigo_fonte.strip():
        return

    try:
        tokens = lexer.tokenize(codigo_fonte)
        ast = parser.parse(tokens)

        if ast is None:
            return

        interpretador.run(ast)
        
    except LexError as le:
        print(f"Erro Lexico: Caractere invalido ou nao suportado na instrucao.")
    except Exception as e:
        print(f"Erro durante a execucao: {e}")

def modo_interativo():
    lexer = LudiCodeLexer()
    parser = LudiCodeParser()
    interpretador = LudiCodeInterpreter()

    print("====================================================")
    print("                 LudiCode              ")
    print(" Digite seu codigo estruturado normalmente.         ")
    print(" Pressione ENTER em uma linha vazia para executar.  ")
    print(" Para sair, digite 'sair' ou pressione Ctrl+C.        ")
    print("====================================================")

    while True:
        try:
            linha_inicial = input(">>> ")
            
            if linha_inicial.strip().lower() == 'sair':
                print("Encerrando LudiCode. Até logo!")
                break
                
            linhas_codigo = [linha_inicial]
            
            if linha_inicial.strip():
                while True:
                    linha_adicional = input("... ")
                    if not linha_adicional.strip():
                        break
                    linhas_codigo.append(linha_adicional)
            
            codigo_completo = "\n".join(linhas_codigo)
            
            executar_bloco(codigo_completo, lexer, parser, interpretador)
            
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando LudiCode. Até logo!")
            break

def compilar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            codigo_fonte = arquivo.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' nao foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    lexer = LudiCodeLexer()
    parser = LudiCodeParser()
    ast = parser.parse(lexer.tokenize(codigo_fonte))

    if ast is None:
        print("Execucao interrompida devido a erros sintaticos.")
        return

    try:
        interpretador = LudiCodeInterpreter()
        resultado = interpretador.run(ast)

        print("\nSaida do programa:")
        for item in resultado.get("saida", []):
            print(item)

        print("\nEstado final:")
        print("Variaveis:", resultado.get("variaveis", {}))
        print("Sensores:", resultado.get("sensores", {}))
        print("Motores:", resultado.get("motores", {}))
        print("Eventos:", resultado.get("eventos", []))

    except Exception as e:
        print(f"Erro durante a execucao: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        compilar_arquivo(sys.argv[1])
    else:
        modo_interativo()