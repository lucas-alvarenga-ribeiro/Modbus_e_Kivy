from pymodbus.client import ModbusTcpClient
from time import sleep


class ClienteMODBUS():
    """
    Classe Cliente MODBUS usando pymodbus
    """
    def __init__(self, server_ip, porta, scan_time=1):
        """
        Construtor
        """
        # Cria o cliente TCP
        self._cliente = ModbusTcpClient(host=server_ip, port=porta)
        self._scan_time = scan_time
        self._cliente.connect()

    def connect(self):
        return self._cliente.connect()
         
    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        Retorna o valor lido ou None em caso de falha.
        """
        # Holding Register (função 03)
        if tipo == 1:
            resp = self._cliente.read_holding_registers(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.registers[0]
            return None

        # Coil (função 01)
        if tipo == 2:
            resp = self._cliente.read_coils(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.bits[0]
            return None

        # Input Register (função 04)
        if tipo == 3:
            resp = self._cliente.read_input_registers(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.registers[0]
            return None

        # Discrete Input (função 02)
        if tipo == 4:
            resp = self._cliente.read_discrete_inputs(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.bits[0]
            return None

        # Tipo inválido
        return None

    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na Tabela MODBUS
        Retorna True em caso de sucesso, False em caso de falha.
        """
        # Holding Register (função 06 - single)
        if tipo == 1:
            resp = self._cliente.write_register(address=addr, value=valor, device_id=1)
            return bool(resp and not resp.isError())

        # Coil (função 05 - single)
        if tipo == 2:
            # Em coils, valor esperado é 0/1 (False/True)
            resp = self._cliente.write_coil(address=addr, value=bool(valor), device_id=1)
            return bool(resp and not resp.isError())

        # Tipo inválido
        return False
    
    def lerFloat(self, addr):
        resp = self._cliente.read_holding_registers(address=addr,count=2,device_id=1)
        if resp and not resp.isError():
            valor_float = self._cliente.convert_from_registers(resp.registers, ModbusTcpClient.DATATYPE.FLOAT32)
            return valor_float
        
        return None
    
    def escreveFloat(self, addr, valor):
        valor_ints = self._cliente.convert_to_registers(valor, ModbusTcpClient.DATATYPE.FLOAT32, word_order="big")
        resp = self._cliente.write_registers(address=addr, values=valor_ints, device_id=1)
        return bool(resp and not resp.isError())

    def lerBitsHolding(self, addr):

        valor = self.lerDado(1,addr)

        binario = format(valor,'016b')

        bits = [int(bit) for bit in binario]

        return bits
    

    def escreveBits(self, addr, bit, posicao):

        valor = self.lerDado(1, addr)

        binario = format(valor, '016b')

        bits = [int(b) for b in binario]

        bits[posicao] = bit

        novo_binario = ''.join(str(b) for b in bits)

        novo_valor = int(novo_binario, 2)

        return self.escreveDado(1, addr, novo_valor)
    
    def close(self):
        self._cliente.close()
    

class ClienteInterface():
    def __init__(self, cliente, scan_time=1):
        self._cliente = cliente
        self._scan_time = scan_time  

    
    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        # Abre a conexão com o servidor MODBUS 
        try:
            atendimento = True
            while atendimento:
                sel = input("Deseja realizar uma leitura, escrita ou configuração? (1- Leitura | 2- Escrita | 3- Configuração | 4- Sair): ")
                
                "Adicionando float como opção de leitura"
                if sel == '1':
                    tipo = input("""Qual tipo de dado deseja ler? (1- Holding Register | 2- Coil | 3- Input Register | 4- Discrete Input | 5- Float | 6- Ler Bit): """)
                    if(tipo == '1' or tipo == '2' or tipo == '3' or tipo == '4'):
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        nvezes = input("Digite o número de vezes que deseja ler: ")
                        for i in range(0, int(nvezes)):
                            print(f"Leitura {i+1}: {self._cliente.lerDado(int(tipo), int(addr))}")
                            sleep(self._scan_time)
                    elif tipo == '5':
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        nvezes = input("Digite o número de vezes que deseja ler: ")
                        for i in range(0, int(nvezes)):
                            print(f"Leitura {i+1}: {self._cliente.lerFloat(int(addr))}")
                            sleep(self._scan_time)
                    elif tipo == '6':
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        print(f"Leitura {1}: {self._cliente.lerBitsHolding(int(addr))}")
                elif sel == '2':
                    tipo = input("""Qual tipo de dado deseja escrever? (1- Holding Register | 2- Coil | 3- Float | 4- Bit): """)
                    if(tipo == '1' or tipo == '2'):
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        valor = input("Digite o valor que deseja escrever: ")
                        ok = self._cliente.escreveDado(int(tipo), int(addr), int(valor))
                        print("Escrita realizada." if ok else "Falha na escrita.")
                    elif tipo == '3':
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        valor = input("Digite o valor float que deseja escrever: ")
                        self._cliente.escreveFloat(int(addr), float(valor))
                        print("Escrita realizada.")
                    elif tipo == '4':
                        addr = input("Digite o endereço da tabela MODBUS: ")
                        posicao = input("Digite qual bit quer acessar: ")
                        bit = input("Digite o valor do bit que deseja escrever: ")
                        self._cliente.escreveBits(int(addr), int(bit), int(posicao))
                        print("Escrita realizada.")

                elif sel == '3':
                    scant = input("Digite o tempo de varredura desejado [s]: ")
                    self._scan_time = float(scant)

                elif sel == '4':
                    atendimento = False
                else:
                    print("Seleção inválida")
        except Exception as e:
            print('Erro no atendimento: ', e.args)
        finally:
            # Fecha a conexão ao sair
            self._cliente.close()

