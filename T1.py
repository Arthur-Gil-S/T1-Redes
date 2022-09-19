
import csv

class Codifica:

    def __init__(self, cod):
        self.cod = cod

    def hexToBin(self): # converte de hexa para binário

        #binario = bin(int(cod, 16))[2:]
        binario = bin(int('1'+cod, 16))[3:]

        # formata o número binário para ser múltiplo de 4
        # motivo: na conversão hex to bin do Python ele desconsidera os bits 0 iniciais,
        # e valida apenas a partir do primeiro bit 1, fazendo com que o numero binario não esteja completo
        while len(binario) % 4 != 0:
            binario = '0' + binario
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

    def mdif(self):
        binario = Codifica.hexToBin(cod)
        result = ''
        for bit in binario:
            if len(result) == 0:
                if bit == '0':
                    result += '+-'
                else: result += '-+'
            else:
                if bit == '0':
                    size = len(result)
                    result += result[size-2] + result[size-1]
                else:
                    size = len(result)
                    if result[size-1] == '-':
                        result += '-+'
                    else: result += '+-'
        print(result)

    def eightBsixT(self):
        binario = Codifica.hexToBin(cod)
        space_bin = ''

        # adiciona marcação para separar de 8 em 8 o número binario
        cont = 0
        for b in binario:
            cont = cont + 1
            if cont % 8 == 0:
                space_bin += b + ' '
            else:
                space_bin += b
        binario = space_bin.split() # lista contendo 8 bits em cada posição

        # converte o arquivo csv para um dicionario
        tabel = {}
        with open('8b6t.csv') as file:
            csv_tabel = csv.reader(file, delimiter=',')
            for row in csv_tabel:
                tabel.update({row[0]:row[1]})
        
        # seleciona o código ternario equivalente ao binário da tabela
        list_result = []
        for i in binario:
            list_result.append(tabel.get(i))

        result = []
        balance = 0
        for signal in list_result:
            weight = 0
            plus = 0
            minus = 0
            for c in signal:
                if c == '+' : plus += 1
                if c == '-' : minus += 1
            weight = plus - minus
            
            if weight == 0: # se difernça entre + e - for 0
                result.append(signal)
            if weight == 1:
                if balance == 0:
                    balance = balance + 1
                    result.append(signal)
                    continue

                if balance == 1:
                    balance = balance - 1
                    inverse_signal = ''
                    for c in signal: #realiza a troca de sinais, anexando os valore a uma nova string de sinais inversos
                        if c == '+' : inverse_signal += '-' 
                        if c == '-' : inverse_signal += '+'
                        if c == '0' : inverse_signal += '0'
                    result.append(inverse_signal)

        new_result = ''.join(result)
        print(new_result)


class Decodifica:

    def __init__(self, sinal):
        self.sinal = sinal

    def hexToBin(self, tec): # recebe o binário através da decodificação da técnica e retorna um hexa
        if tec == 'nrzi':
            binario = Decodifica.nrzi(sinal)
        if tec == 'mdif':
            binario = Decodifica.mdif(sinal)
        if tec == '8b6t':
            binario = Decodifica.eightBsixT(sinal)
        if binario.startswith('0000'):
            hexa = '0' + str((hex(int(binario, 2))).split('x')[1])
        else:
            hexa = (hex(int(binario, 2))).split('x')[1]
        print(hexa)

    def nrzi(self):
        global sinal
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

    def mdif(self):
        global sinal
        if len(sinal) % 2 == 1:
            print('ERRO')
        result = ''
        size = len(sinal)
        i = 0
        for i in range(size):
            if i == 0:
                if sinal[i] == '+':
                    result += '0'
                else:
                    result += '1'
            elif i % 2 == 0:
                last = sinal[i-2] + sinal[i-1]
                current = sinal[i] + sinal[i+1]
                if last == current:
                    result += '0'
                else: result += '1'
        return result
    
    def eightBsixT(self):
        global sinal
        signals = []
        cont = 0
        space = ''
        for s in sinal:
            cont = cont + 1
            if cont % 6 == 0:
                space += s + ' '
            else:
                space += s
        signals = space.split()

        # realiza a contagem do peso
        list_signals = []
        for sinal in signals:
            weight = 0
            plus = 0
            minus = 0
            for c in sinal:
                if c == '+' : plus += 1
                if c == '-' : minus += 1
            weight = plus - minus

            if weight == -1: # se o peso do sinal for -1 inverte para voltar ao normal
                origin_signal = ''
                for c in sinal:
                    if c == '+' : origin_signal += '-' 
                    if c == '-' : origin_signal += '+'
                    if c == '0' : origin_signal += '0'
                list_signals.append(origin_signal)
                continue
            list_signals.append(sinal)

        tabel = {}
        with open('8b6t.csv') as file:
            csv_table = csv.reader(file, delimiter=',')
            for row in csv_table:
                tabel.update({row[1]:row[0]})
        
        list_binarios = []
        for signal in list_signals:
            list_binarios.append(tabel.get(signal))
        
        binario_result = ''
        binario_result = binario_result.join(list_binarios)

        return binario_result

comando = input() # codificador nrzi 1234
comando = comando.split(' ')
func, tec, cod = comando[0], comando[1], comando[2]
sinal = comando[2]

if func == 'codificador':
    inst_cod = Codifica(cod) # cria objeto/instancia de Codificação
    if tec == 'nrzi':
        inst_cod.nrzi()
    if tec == 'mdif':
        inst_cod.mdif()
    if tec == '8b6t':
        inst_cod.eightBsixT()
else:
    inst_dec = Decodifica(sinal)
    inst_dec.hexToBin(tec)
