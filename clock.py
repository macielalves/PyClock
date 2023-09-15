import time
from threading import Thread
try:
    from tkinter import Tk, Label
    GUI = True
except ImportError:
    GUI = False


CMD = '>>> '


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
        self.configurando = True  # ----
        print('Configuração',
              '[1] Definir HH:MM',
              '[2] Modo GUI' if GUI else '',
              sep="")

        op = input(CMD)
        if op == '1':
            print(
                "[h] h para definir a hora, [m] m para definir minutos, [t] Definir hora e minuto.")
            sub_op = input(CMD).strip().lower()
            self.op_span = 'H' if sub_op == 'h' else 'M' if sub_op == 'm' else 'H:M' if sub_op == 't' else None
            if sub_op and sub_op in 'hmt':
                tmp = input(f'[{self.op_span}]: ').strip()

        elif op == 'v':
            print(f'Horário [{self.string_tempo()}]')

    def run(self):  # lista de processos a serem iniciados em thread
        self.atualizar_hora()

    def stop(self):
        self.estado = False

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
        print(f'Relógio um   [{r1}]\nRelógio dois [{r2}]', end="\r\n\n")

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
