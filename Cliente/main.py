from clientemodbus import ClienteMODBUS
from interfacemodbus import ClienteInterface
from classes_widget import BasicApp
from kivy.config import Config



#c = ClienteMODBUS('localhost',502)

if __name__ == '__main__':
    Config.set('graphics','resizable',True)
    BasicApp().run()


#ci = ClienteInterface(c)
#ci.atendimento()

