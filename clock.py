import time
from threading import Thread
try:
    from tkinter import Tk, Label
    GUI = True
except ImportError:
    GUI = False


CMD = '>>> '
_R = '\x1b[31m'
_G = '\x1b[32m'
_B = '\x1b[34m'
_0 = '\x1b[0m'


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
        super().__init__()
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

    def definir_hora(self, hora: int) -> None:
        self.H = hora

    def definir_minuto(self, minuto: int) -> None:
        self.M = minuto

    def definir_segundo(self, segundo: int) -> None:
        self.S = segundo

    def configurar(self):
        self.configurando = True

    def run(self):  # lista de processos a serem iniciados em thread
        self.atualizar_hora()

    def stop(self):
        self.estado = False

    def resume(self):
        """Liga o contador interno se estiver desligado
        """
        if not self.estado:
            self.atualizar_hora()
            self.estado = True

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
            f'{_R}R[1] [{r1}]\nR[2] [{r2}]', end=f"\r\n\n{_0}")

        print(
            'Digite:'
            '[1] para configurar o relogio 1, [2] para configurar o relogio 2 ou [q] para sair.'
        )

        op = input(CMD).strip()
        if op and op[0].lower() == 'q':
            break

        if op and op[0] == '1':
            r1.configurar()
        elif op and op[0] == '2':
            r2.configurar()


except Exception as err:
    r1.stop()
    r2.stop()
    print(err)

r1.stop()
r2.stop()
