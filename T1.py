
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

    def hexToBin6B8B(self): # converte de hexa para binário

        #binario = bin(int(cod, 16))[2:]
        binario = bin(int('1'+cod, 16))[3:]

        # formata o número binário para ser múltiplo de 4
        # motivo: na conversão hex to bin do Python ele desconsidera os bits 0 iniciais,
        # e valida apenas a partir do primeiro bit 1, fazendo com que o numero binario não esteja completo
        while len(binario) % 6 != 0:
            binario = '0' + binario
        i = 0
        list = []
        num = ''
        for i in range(len(binario)):
            num += binario[i]
            if len(num) == 6:
                list.append(num)
                num = ''
        return list
    
    def countDisparity(binario):
        disparity = 0
        for b in binario:
            if b == '0':
                disparity -= 1
            else: disparity += 1
        return disparity

    def findCode(binario):
        file = open("6b8b.txt","r")

        for line in file:
            code = line.split()
            if code[0] == binario:
                return code[1]
        file.close()

    def encode6b8b(self):
  
        listNum = Codifica.hexToBin6B8B(cod)
        result = ''
        for num in listNum:
            disparity = Codifica.countDisparity(num)
            if disparity == 0:
                result += '10' + num
            elif disparity == 2 and num != '001111':
                result += '00' + num
            elif disparity == -2 and num != '110000':
                result += '11' + num
            elif disparity == -6:
                result += '01011001'
            elif disparity == 6:
                result += '01100110'
            elif num == '001111':
                result += '01001011'
            elif num == '110000':
                result += '01110100'
            elif disparity == 4 or disparity == -4:
                result += Codifica.findCode(num)
        return result

    def nrzi(self, tec): # se receber bit 1 inverte o sinal, se receber 0 copia o sinal anterior
        if tec == 'nrzi':
            binario = Codifica.hexToBin(cod)
        else:
            binario = Codifica.encode6b8b(cod)

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

    def countViolation(binario):
        lastBit = '-'
        count = 0
        i = 0
        result = ''
        for i in range(len(binario)):
            if binario[i] == '0':
                count+=1
                if count == 4:
                    if lastBit == '-':
                        result += '+'
                    else: result += '-'
                else: result += '0'
            else: 
                result += '1'
                count = 0
        return result

    def hdb3(self):
        binario = Codifica.hexToBin(cod)
        violation = Codifica.countViolation(binario)

        lastSignal = '-'
        i = 0
        result = ''
        for i in range(len(violation)):
            if i == 0 and violation[0] == '1':
                result += '+'
                lastSignal = '+'
            elif violation[i] == '1':
                if lastSignal == '+':
                    result += '-'
                    lastSignal = '-'
                else: 
                    result += '+'
                    lastSignal = '+'
            elif violation[i] == '0':
                if i < len(violation)-3:
                    if violation[i+3] == '+' and lastSignal == '-':
                        result += '+'
                        lastSignal = '+'
                    elif violation[i+3] == '-' and lastSignal == '+':
                        result += '-'
                        lastSignal = '-'
                    else:
                        result += '0'
                else:
                    result += '0'
            elif violation[i] == '+':
                result += '+'
                lastSignal = '+'
            elif violation[i] == '-':
                result += '-'
                lastSignal = '-'   
        print(result)


class Decodifica:

    def __init__(self, sinal):
        self.sinal = sinal

    def hexToBin(self, tec): # recebe o binário através da decodificação da técnica e retorna um hexa
        if tec == 'nrzi':
            binario = Decodifica.nrzi(sinal)
        if tec == 'mdif':
            binario = Decodifica.mdif(sinal)
            if binario == 'ERRO':
                print('ERRO')
                return
        if tec == '8b6t':
            binario = Decodifica.eightBsixT(sinal)
            if binario == 'ERRO':
                print('ERRO')
                return
        if tec == 'hdb3':
            binario = Decodifica.hdb3(sinal)
        if tec == '6b8b':
            binario = Decodifica.sixBeightB(sinal)
            if binario == 'ERRO':
                print('ERRO')
                return
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
            return 'ERRO'
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

        if len(sinal) % 6 != 0:
            return 'ERRO'

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

    def hdb3(self):
        result = ''
        i = 0
        for i in range(len(sinal)):
            if sinal[i] == '0':
                result += '0'
            else:
                if i < len(sinal)-4 and sinal[i+4] == sinal[i+1] and sinal[i+2] == '0' and sinal[i+3] == '0' and sinal[i] != sinal[i+4] and sinal[i] != '0':
                    result += '1'
                elif i < len(sinal)-4 and sinal[i+4] == sinal[i] and sinal[i+1] == '0' and sinal[i+2] == '0' and sinal[i+3] == '0':
                    result += '1'
                elif i < len(sinal)-3 and sinal[i+3] == sinal[i] and sinal[i+1] == '0' and sinal[i+2] == '0':
                    result += '0'
                elif len(result) > 3 and sinal[i-4] == sinal[i] and sinal[i-1] == '0' and sinal[i-2] == '0' and sinal[i-3] == '0':
                    result += '0'
                elif len(result) > 2 and sinal[i-3] == sinal[i] and sinal[i-1] == '0' and sinal[i-2] == '0':
                    result += '0'
                elif len(result) > 3 and sinal[i-3] == sinal[i] and sinal[i-1] == '0' and sinal[i-2] == '0' and sinal[i] != sinal[i-4] and sinal[i-4] != '0':
                    result += '0'
                else:
                    result += '1'
                
        #print(result)
        return result

    def sixBeightB(self):
        global sinal
        
        if len(sinal) % 8 != 0:
            return 'ERRO'

        binario = Decodifica.nrzi(sinal)

        binaries = []
        cont = 0
        space = ''
        for b in binario:
            cont = cont + 1
            if cont % 8 == 0:
                space += b + ' '
            else:
                space += b
        binaries = space.split()

        tabel = {}
        with open('6b8b.csv') as file:
            csv_table = csv.reader(file, delimiter=',')
            for row in csv_table:
                tabel.update({row[0]:row[1]})

        results = []
        for bin in binaries:
            prefix = bin[0] + bin[1]
            if prefix == '01':
                results.append(tabel.get(bin))
            else:
                results.append(bin[2:])
            
        result = ''.join(results)
        return result

comando = input() # codificador nrzi 1234
comando = comando.split(' ')
func, tec, cod = comando[0], comando[1], comando[2]
sinal = comando[2]

if func == 'codificador':
    inst_cod = Codifica(cod) # cria objeto/instancia de Codificação
    if tec == 'nrzi':
        inst_cod.nrzi('nrzi')
    if tec == 'mdif':
        inst_cod.mdif()
    if tec == '8b6t':
        inst_cod.eightBsixT()
    if tec == 'hdb3':
        inst_cod.hdb3()
    if tec == '6b8b':
        inst_cod.nrzi('6b8b')
else:
    inst_dec = Decodifica(sinal)
    inst_dec.hexToBin(tec)
