import operator


class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self.values = {}

    def declare(self, name, value=None):
        if name in self.values:
            raise SemanticError(f"Variavel '{name}' ja foi declarada.")
        self.values[name] = value
        return value

    def assign(self, name, value):
        if name not in self.values:
            raise SemanticError(f"Variavel '{name}' nao foi declarada.")
        self.values[name] = value
        return value

    def get(self, name):
        if name not in self.values:
            raise SemanticError(f"Variavel '{name}' nao foi declarada.")
        return self.values[name]


class SimulationRuntime:
    def __init__(self, sensors=None):
        self.sensors = sensors or {}
        self.motors = {}
        self.events = []

    def ligar_motor(self, nome, velocidade=100):
        self.motors[nome] = {"ligado": True, "velocidade": velocidade}
        self.events.append(
            {"acao": "ligarMotor", "motor": nome, "velocidade": velocidade}
        )

    def desligar_motor(self, nome):
        self.motors[nome] = {"ligado": False, "velocidade": 0}
        self.events.append({"acao": "desligarMotor", "motor": nome})

    def ler_sensor(self, nome):
        if nome not in self.sensors:
            raise SemanticError(f"Sensor '{nome}' nao foi configurado.")
        valor = self.sensors[nome]
        self.events.append({"acao": "lerSensor", "sensor": nome, "valor": valor})
        return valor

    def configurar_sensor(self, nome, valor):
        self.sensors[nome] = valor


class LudiCodeInterpreter:
    def __init__(self, sensors=None, loop_limit=1000):
        self.symbols = SymbolTable()
        self.runtime = SimulationRuntime(sensors)
        self.output = []

        self.loop_limit = loop_limit

        self.builtins = {
            "ligarmotor": self._call_ligar_motor,
            "desligarmotor": self._call_desligar_motor,
            "lersensor": self._call_ler_sensor,
            "configurarsensor": self._call_configurar_sensor,
            "mostrar": self._call_mostrar,
        }

        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            ">": operator.gt,
            "<=": operator.le,
            ">=": operator.ge,
            "e": self._operator_e,
            "ou": self._operator_ou,
        }

        self.executors = {
            "programa": self._exec_container,
            "bloco": self._exec_container,
            "declaracao_var": self._exec_declaracao,
            "atribuicao": self._exec_atribuicao,
            "mostrar": self._exec_mostrar,
            "se": self._exec_se,
            "enquanto": self._exec_enquanto,
            "repita": self._exec_repita,
            "chamada": self.execute_call,
        }

    def run(self, ast):
        self.execute(self.normalize(ast))
        return {
            "saida": self.output,
            "variaveis": self.symbols.values,
            "sensores": self.runtime.sensors,
            "motores": self.runtime.motors,
            "eventos": self.runtime.events,
        }

    def normalize(self, node):
        if node is None or isinstance(node, (int, float, str, bool)):
            return node

        if isinstance(node, list):
            return [self.normalize(item) for item in node]

        if isinstance(node, tuple):
            return (node[0], *(self.normalize(item) for item in node[1:]))

        if not isinstance(node, dict):
            raise SemanticError("No de AST invalido.")

        tipo = node["tipo"]

        if tipo in {"programa", "bloco"}:
            return (tipo, self.normalize(node["comandos"]))

        if tipo == "declaracao_variavel":
            return ("declaracao_var", node["nome"], self.normalize(node.get("valor")))

        if tipo == "atribuicao":
            return ("atribuicao", node["nome"], self.normalize(node["valor"]))

        if tipo == "mostrar":
            return ("mostrar", self.normalize(node["valor"]))

        if tipo == "se":
            if isinstance(node, tuple):
                if len(node) > 3:
                    return ("se", self.normalize(node[1]), self.normalize(node[2]), self.normalize(node[3]))
                return ("se", self.normalize(node[1]), self.normalize(node[2]))
            
            if "senao" in node:
                return (
                    "se",
                    self.normalize(node["condicao"]),
                    self.normalize(node["entao"]),
                    self.normalize(node["senao"]),
                )
            return (
                "se",
                self.normalize(node["condicao"]),
                self.normalize(node["entao"]),
            )

        if tipo == "enquanto":
            return ("enquanto", self.normalize(node["condicao"]), self.normalize(node["corpo"]))

        if tipo == "repita":
            return ("repita", self.normalize(node["corpo"]), self.normalize(node["condicao"]))

        if tipo in {"numero", "texto", "booleano"}:
            return (tipo, node["valor"])

        if tipo == "identificador":
            return ("variavel", node["nome"])

        if tipo == "binaria":
            return (
                "operacao",
                node["operador"],
                self.normalize(node["esquerda"]),
                self.normalize(node["direita"]),
            )

        if tipo == "chamada":
            argumentos = [self.normalize(arg) for arg in node.get("argumentos", [])]
            return ("chamada", node["nome"], *argumentos)

        raise SemanticError(f"No de AST desconhecido: {tipo}")

    def execute(self, node):
        if node is None:
            return None

        if isinstance(node, list):
            for comando in node:
                self.execute(comando)
            return None

        if not isinstance(node, tuple):
            return self.evaluate(node)

        executor = self.executors.get(node[0])
        return executor(node) if executor else self.evaluate(node)

    def evaluate(self, node):
        if node is None or isinstance(node, (int, float, str, bool)):
            return node

        if not isinstance(node, tuple):
            raise SemanticError("Expressao invalida.")

        tipo = node[0]

        if tipo in {"numero", "texto", "booleano"}:
            return node[1]

        if tipo in {"variavel", "identificador"}:
            return self.symbols.get(node[1])

        if tipo == "operacao":
            operador = self.operators.get(node[1])
            if operador is None:
                raise SemanticError(f"Operador '{node[1]}' nao suportado.")
            esquerda = self.evaluate(node[2])
            direita = self.evaluate(node[3])
            try:
                return operador(esquerda, direita)
            except ZeroDivisionError as error:
                raise SemanticError("Divisao por zero.") from error
            except TypeError as error:
                raise SemanticError(
                    f"Tipos incompativeis para o operador '{node[1]}': "
                    f"{type(esquerda).__name__} e {type(direita).__name__}."
                ) from error

        if tipo == "chamada":
            return self.execute_call(node)

        raise SemanticError(f"No de AST desconhecido: {tipo}")

    def _exec_container(self, node):
        return self.execute(node[1])

    def _exec_declaracao(self, node):
        return self.symbols.declare(node[1], self.evaluate(node[2]))

    def _exec_atribuicao(self, node):
        return self.symbols.assign(node[1], self.evaluate(node[2]))

    def _exec_mostrar(self, node):
        return self._call_mostrar(self.evaluate(node[1]))

    def _exec_se(self, node):
        condicao = self.evaluate(node[1])
        if condicao:
            return self.execute(node[2])
        elif len(node) > 3:
            return self.execute(node[3])
        return None

    def _exec_enquanto(self, node):
        repeticoes = 0
        while self.evaluate(node[1]):
            repeticoes += 1
            if repeticoes > self.loop_limit:
                raise SemanticError("Limite do laco 'enquanto' excedido.")
            self.execute(node[2])

    def _exec_repita(self, node):
        limite_iteraçoes = int(self.evaluate(node[1]))
        for _ in range(limite_iteraçoes):
            self.execute(node[2])

    def execute_call(self, node):
        nome = node[1].lower()
        argumentos = [self.evaluate(arg) for arg in node[2:]]
        builtin = self.builtins.get(nome)

        if builtin is None:
            raise SemanticError(f"Funcao '{node[1]}' nao suportada.")

        return builtin(*argumentos)

    def _call_ligar_motor(self, motor, velocidade=100):
        self.runtime.ligar_motor(motor, velocidade)

    def _call_desligar_motor(self, motor):
        self.runtime.desligar_motor(motor)

    def _call_ler_sensor(self, sensor):
        return self.runtime.ler_sensor(sensor)

    def _call_configurar_sensor(self, sensor, valor):
        self.runtime.configurar_sensor(sensor, valor)

    def _call_mostrar(self, valor=None):
        self.output.append(valor)
        print(valor)
        return valor

    def _operator_e(self, esquerda, direita):
        return bool(esquerda) and bool(direita)

    def _operator_ou(self, esquerda, direita):
        return bool(esquerda) or bool(direita)
