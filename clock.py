import time


class Relogio:
    H = 0
    M = 0
    S = 0
    marca_do_relogio = None
    estado = False
    configurando = False

    def __init__(self,
                 marca=None,
                 formato=24,
                 horas=0,
                 minutos=0,
                 segundos=0,
                 estado=False) -> None:
        """Todos são parâmetros opcionais"""
        self.marca_do_relogio = marca
        self.formato_hora = formato
        self.H = horas
        self.M = minutos
        self.estado = estado
        pass

    def ligar(self):
        self.estado = True
        return

    def mostrar_tempo(self):
        print(f'{self.H:0>2}:{self.M:0>2}:{self.S:0>2}')

    def atualizar_hora(self):
        if self.H == self.formato_hora:
            self.H = 0
        if self.M == 59:
            self.H += 1
            self.M = 0
        if self.S == 59:
            self.M += 1
            self.S = 0
        self.S += 1

    def configurar(self):
        self.configurando = True

    def definir_hora(self, hora: int) -> None:
        if self.configurando:
            self.H = hora

    def definir_minuto(self, minuto: int) -> None:
        if self.configurando:
            self.M = minuto

    def definir_segundo(self, segundo: int) -> None:
        if self.configurando:
            self.S = segundo

    def voltar(self):
        if self.configurando:
            self.configurando = False
        pass


r1 = Relogio(formato=12)
r1.ligar()
while r1.estado:
    r1.atualizar_hora()
    r1.mostrar_tempo()
    r1.configurar()
    r1.definir_hora(3)
    r1.definir_minuto(6)
    r1.definir_segundo(50)
    time.sleep(1)
