import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.clock import Clock

from clientemodbus import ClienteMODBUS


class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.tipo = None

    def changelb(self):
        """
        Método simples para incremento do valor mostrado no label
        """
        self.ids['lb'].text = str(int(self.ids.lb.text) + 1) 

    def connectar(self):
        ip = self.ids.ip.text
        porta = int(self.ids.porta.text)
        print(f"Conectando ao servidor MODBUS em {ip}:{porta}...")
        self.cliente = ClienteMODBUS(ip, porta)
        print("Conexão estabelecida." if self.cliente.connect() else "Falha na conexão.")
    
    def ler(self):
        if (self.ids.lcon.active):
            Clock.schedule_interval(self.executa_leitura,1)
        else:
            self.executa_leitura()

    def escrever(self):
        if(self.tipo == '1' or self.tipo == '2'):
            reg = int(self.ids.reg.text)
            valor_escrita = int(self.ids.escrever.text)
            tipo = int(self.tipo)
            valor_escrita = self.cliente.escreveDado(tipo, reg, valor_escrita)
            #self.ids.ler.text = "Escrita realizada." if valor_escrita else "Falha na escrita."
        elif self.tipo == '5':
            reg = int(self.ids.reg.text)
            valor_escrita = float(self.ids.escrever.text)
            self.cliente.escreveFloat(reg, valor_escrita)
            #self.ids.ler.text = "Escrita realizada."
        elif self.tipo == '6':
            reg = int(self.ids.reg.text)
            valor_escrita = int(self.ids.escrever.text)
            self.cliente.escreveBitsHolding(reg, valor_escrita)
            #self.ids.ler.text = "Escrita realizada."

    def executa_leitura(self, dt=None):
        if(self.tipo == '1' or self.tipo == '2' or self.tipo == '3' or self.tipo == '4'):
            reg = int(self.ids.reg.text)
            tipo = int(self.tipo)
            valor_leitura = self.cliente.lerDado(tipo, reg)
            self.ids.ler.text = str(valor_leitura)

        elif self.tipo == '5':
            reg = int(self.ids.reg.text)
            valor_leitura = self.cliente.lerFloat(reg)
            self.ids.ler.text = str(valor_leitura)
        
        elif self.tipo == '6':
            reg = int(self.ids.reg.text)
            valor_leitura = self.cliente.lerBitsHolding(reg)
            self.ids.ler.text = str(valor_leitura)
        




class BasicApp(App):
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        return MyWidget()