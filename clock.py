import time
from threading import Thread
try:
    from tkinter import Tk, Label
    GUI = True
except ImportError:
    GUI = False


CMD = '>>> '
"""A constante é o indicador de prompt"""
_R = '\x1b[31m'
_G = '\x1b[32m'
_B = '\x1b[34m'
_0 = '\x1b[0m'

V_ERROR = 'Valor inválido'
I_ERROR = 'Falta de valores'
NONE_UPDATE = 'Nenhuma alteração foi feita'


class Relogio(Thread):
    H = 0
    M = 0
    S = 0
    marca_do_relogio = None
    estado = False
    configurando = False
    op_span = None

    def __init__(self,
                 marca=None,
                 formato=24,
                 horas=0,
                 minutos=0,
                 estado=False) -> None:
        super().__init__(name="PyClock")
        self.marca_do_relogio = marca
        self.formato_hora = formato
        self.H = horas
        self.M = minutos
        self.estado = estado
        pass

    def string_tempo(self):
        return f'{self.H:02}:{self.M:02}:{self.S:02}'

    def atualizar_hora(self):
        # executa quando estiver com self.estado = True
        while self.estado:
            if self.H == self.formato_hora:
                self.H = 0
            if self.M == 59:
                self.H += 1
                self.M = 0
            if self.S == 59:
                self.M += 1
                self.S = 0
            self.S += 1
            time.sleep(1)

    def definir_hora(self, hora):
        self.H = hora

    def definir_minuto(self, minuto):
        self.M = minuto

    def definir_segundo(self, segundo):
        self.S = segundo

    def configurar(self):
        self.configurando = True

    def estado_true(self, f=None):
        if not self.estado:
            self.estado = True

    def run(self):  # lista de processos a serem iniciados em thread
        self.estado_true()
        self.atualizar_hora()

    def stop(self):
        self.estado = False

    def resume(self):
        """Liga o contador interno se estiver desligado
        """
        self.estado_true()
        self.atualizar_hora()

    def __str__(self) -> str:
        return self.string_tempo()


r1 = Relogio()
r2 = Relogio()

r1.estado = True
r1.start()
r2.estado = True
r2.start()

try:
    while True:
        print(
            f'R[1] {_G}[{r1}]\n{_0}R[2] {_B}[{r2}]', end=f"\r\n\n{_0}")

        print(
            'Digite:',
            '[1] para configurar o relogio 1, [2] para configurar o relogio 2 ou [q] para sair.', sep="\n"
        )

        op = input(CMD).strip()
        if op and op[0].lower() == 'q':
            break

        if op and op[0] == '1':
            conf = r1
        elif op and op[0] == '2':
            conf = r2
        else:
            conf = None

        if conf is not None:
            print(conf)
            print("[h] mudar a hora ")
            print("[m] mudar os minutos")
            print("[t] definir hora e minuto")
            sub_op = input(CMD).strip().lower()
            if sub_op:
                if sub_op[0] == 'h':
                    print("Digite a hora [HH]")
                    try:
                        h = int(input(CMD))
                        conf.definir_hora(h)
                    except ValueError:
                        print(V_ERROR)
                elif sub_op[0] == 'm':
                    try:
                        print("Digite o minuto [MM]")
                        m = int(input(CMD))
                    except ValueError:
                        print(V_ERROR)

                elif sub_op[0] == 't':
                    print("Digite o horário [HH:MM]")
                    t = input(CMD).strip()
                    require = ''
                    if ':' in t:
                        t.split(':')
                    else:
                        require = 'Requer o separador ":" entre HH e MM, HH:MM'
                    try:
                        h, m = int(t[0]), int(t[1])
                    except ValueError:
                        print(require)
                        print(V_ERROR)
                    except IndexError:
                        print(require)
                        print('', I_ERROR, sep=_R, end=_0+"\n")
                    else:
                        conf.definir_hora(h)
                        conf.definir_minuto(m)


except Exception as err:
    r1.stop()
    r2.stop()
    print(err)

finally:
    r1.stop()
    r2.stop()
