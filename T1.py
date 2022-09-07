
class Codifica:

    def __init__(self, cod):
        self.cod = cod

    def hexToBin(self): # converte de hexa para binário

        binario = bin(int(cod, 16))
        binario = ''.join([i for i in binario if not i.islower()])
        # formata o número binário para ser múltiplo de 4
        # motivo: na conversão hex to bin do Python ele desconsidera os bits 0 iniciais,
        # e valida apenas a partir do primeiro bit 1, fazendo com que o numero binario não esteja completo
        while len(binario) % 4 != 0:
            binario = '0' + binario
        print(binario)

        return binario

    def nrzi(self): # se receber bit 1 inverte o sinal, se receber 0 copia o sinal anterior

        binario = Codifica.hexToBin(cod)

        result = ''
        for bit in binario:
            
            # primeiro bit, verifica se mantém ou não o sinal negativo
            if len(result) == 0:
                if bit == '0':
                    result += '-'
                else: result += '+'
            else: # verifica os outros casos, a partir do segundo bit
                if bit == '0':
                    result += (result[-1]) #mantem
                if bit == '1': #inverte
                    if result[-1] == '-' : result += '+' 
                    else : result += '-'
    
        print(result)
    

class Decodifica:

    def __init__(self, sinal):
        self.sinal = sinal

    def hexToBin(self, tec): # recebe o binário através da decodificação da técnica e retorna um hexa
        if tec == 'nrzi':
            binario = Decodifica.nrzi(sinal)
        hexa = (hex(int(binario, 2))).split('x')[1]
        print(hexa)

    def nrzi(self):

        index = 0
        result = ''
        for s in sinal:
            if len(result) == 0: # verifica se o primeiro sinal continua ou não negativo
                if s == '-':
                    result = result + '0'
                else: result = result + '1'
            else: # faz a verificação dos outros sinais a partir do segundo
                if s == '-': 
                    # se um sinal é negativo, verifica se seu antecessor também é negativo
                    # se sim, não houve mudança de sinal, logo bit = 0
                    # se não, o sinal foi invertido, logo bit = 1
                    if sinal[index-1] == '-' : result = result + '0'
                    else: result = result + '1'
                if s == '+':
                    # lógica inversa da anterior: se um sinal é positivo, verifica se o antecessor também é
                    if sinal[index-1] == '+' : result = result + '0'
                    else: result = result + '1'
            index = index + 1
        return result




comando = input() # codificador nrzi 1234
comando = comando.split(' ')
func, tec, cod = comando[0], comando[1], comando[2]
sinal = comando[2]

if func == 'codificador':
    inst_cod = Codifica(cod) # cria objeto/instancia de Codificação
    if tec == 'nrzi':
        inst_cod.nrzi()
else:
    inst_dec = Decodifica(sinal)
    if tec == 'nrzi':
        inst_dec.hexToBin(tec)
        



