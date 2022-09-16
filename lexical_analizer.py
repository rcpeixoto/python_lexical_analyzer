from symbol_table import symbolTable
from tokens import tokens
import string

class lexicalAnalyzer:

    def __init__(self, filePath):
        self.file = filePath
        self.symbolTable = symbolTable()
        self.token = tokens()
        self.states = ['initial_state', 'identifier', 'digit', 'float_digit',
                       'ponctuation_symbol', 'negative_num', 'artih_-', 'artith_+',
                       'logical_operator&', 'logical_operator|', 'relational_1', 'relational_2',
                        'digit_space', 'start_comment', 'line_comment', 'block_comment', 'end_comment',
                        'different', 'equal', 'greater', 'smaller','string']
        self.currentState = self.states[0]
        self.letters = list(string.ascii_letters)
        self.digits = list(string.digits)
        self.ponctuation = list(string.punctuation)
        self.arithmetic = list("+-/*")
        self.logical = list("|&!")
        self.delimiters = list(";,()[]{}.")
        self.relational = list("<>=!")

    def parse(self):
        f = open(self.file)
        lines = f.readlines()
        j = 0
        for line in lines:
            if self.currentState is self.states[14]:
                self.currentState = self.states[0]
            j = j + 1
            # Creates Symbol List for the line to be read
            symbol = ''
            line = line + ' '
            for i in range(0, len(line) - 1):
                
                if line[i] is '"' or  self.currentState is self.states[21]:
                    print(line [i])
                    if (self.currentState is self.states[0] and line[i] is '"') or (self.currentState is self.states[21] and (line[i] in self.letters or line[i] in self.digits or (line[i] in self.ponctuation and not line[i] is '"'))):                        
                        print(line[i] in self.ponctuation and not line[i] is '"')
                        symbol = symbol + line[i]
                    elif self.currentState is self.states[21] and line[i] is '"':
                        print("entrou na criacao")
                        symbol = symbol + line[i]
                        self.token.createtoken(
                        'CAC', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                    self.currentState = self.states[21]

                if line[i] in self.letters:
                    if self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]:
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''
                    if self.currentState is self.states[17]:
                        self.token.createtoken('LOG',j, self.symbolTable.insertSymbol(symbol))
                        self.currentState = self.states[0]
                        symbol = ''


                    # Starts reading a identifier, begining with a letter
                    if self.currentState is self.states[0] or self.currentState is self.states[1]:
                        self.currentState = self.states[1]
                        symbol = symbol + line[i]

                    # Reading digit then finds a letter
                    # Finish reading and saves token
                    elif self.currentState is self.states[2] or self.currentState is self.states[3]:
                        # ERROR
                        a = 1
                    elif self.currentState is self.states[6] or self.currentState is self.states[7]:
                        self.token.createtoken(
                            'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                        symbol = ''
                        self.currentState = self.states[1]
                        symbol = symbol + line[i]

                # Reads a digit
                elif line[i] in self.digits:
                    if self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]:
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                    if self.currentState is self.states[17]:
                        self.token.createtoken('LOG',j, self.symbolTable.insertSymbol(symbol))
                        self.currentState = self.states[0]
                        symbol = ''
                    # if the digit read is in initial_state, then it must be a number
                    elif self.currentState is self.states[0] or self.currentState is self.states[5] or self.currentState is self.states[6] or self.currentState is self.states[3]:
                        self.currentState = self.states[2]
                        symbol = symbol + line[i]
                    # if not, it can be anything TEMPORALY
                    else:
                        symbol = symbol + line[i]

                elif line[i].isspace() or line[i] is '\t':
                    if self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]:
                        self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                        self.currentState = self.states[0]
                        symbol = ''
                    elif self.currentState is self.states[17]:
                        self.token.createtoken('LOG',j, self.symbolTable.insertSymbol(symbol))
                        self.currentState = self.states[0]
                        symbol = ''
                    elif self.currentState is self.states[2] or self.currentState is self.states[3]:
                        if symbol[0] is '-' and self.token.lasttoken()[0] is 'NRO' and self.token.lasttoken()[2] == j:
                            symbol_1 = symbol[0]
                            symbol_2 = symbol[1:]
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol_1))
                            self.token.createtoken(
                                'NRO', j, self.symbolTable.insertSymbol(symbol_2))
                        else:
                            self.token.createtoken(
                                'NRO', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                    elif self.currentState is self.states[1]:
                        if self.symbolTable.verifyReservedWord(symbol):
                            self.token.createtoken(
                                'PRE', j, self.symbolTable.insertSymbol(symbol))
                        else:
                            self.token.createtoken(
                                'IDE', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                        # Reads a symbol after identifier
                    elif self.currentState is self.states[7]:
                        self.token.createtoken(
                            'ART', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                    elif self.currentState is self.states[6]:
                        self.token.createtoken(
                            'ART', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                    elif self.currentState is self.states[8]:
                        self.token.createtoken('LOG', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
                    elif self.currentState is self.states[13]:
                        self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                        symbol = ''
                        self.currentState = self.states[0]
          
                # Reads a ponctuation symbol
                elif line[i] in self.ponctuation:

                    if (self.currentState is self.states[2] or self.currentState is self.states[3]) and line[i] is not '.':
                        if symbol[0] is '-' and self.token.lasttoken()[0] is 'NRO' and self.token.lasttoken()[2] is j:
                            symbol_1 = symbol[0]
                            symbol_2 = symbol[1:]
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol_1))
                            self.token.createtoken(
                                'NRO', j, self.symbolTable.insertSymbol(symbol_2))
                        else:
                            self.token.createtoken(
                                'NRO', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]

                    # Reading a Identifier, then finds a ponctuation symbol which is not "_"
                    # Finish reading and save token
                    if self.currentState is self.states[1] and line[i] is not '_':
                        # Verifies whether the token represents a Reserved word
                        if self.symbolTable.verifyReservedWord(symbol):
                            self.token.createtoken(
                                'PRE', j, self.symbolTable.insertSymbol(symbol))
                        else:
                            self.token.createtoken(
                                'IDE', j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        # Reads a symbol after identifier
                        self.currentState = self.states[0]

                    # Starts reading of a '.'
                    if line[i] is '.':
                        # if the reading is current in a digit, the '.' is seen as a float point divisor
                        if self.currentState is self.states[2]:
                            self.currentState = self.states[3]
                            symbol = symbol + line[i]

                    # starts reading of a '_'
                    elif line[i] is '_':
                        # If the reading is current in a identifier, the '_' is seen as part of the identifier
                        if self.currentState is self.states[1]:
                            symbol = symbol + line[i]

                    elif line[i] in self.arithmetic:
                        if self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]:
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        if self.currentState is self.states[8] or self.currentState is self.states[9]:
                            self.token.createtoken('LOG',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''


                        if self.currentState is self.states[0] and line[i] is '+':
                            self.currentState = self.states[7]
                            symbol = symbol + line[i]
                        elif self.currentState is self.states[0] and line[i] is '-':
                            self.currentState = self.states[6]
                            symbol = symbol + line[i]
                        elif (self.currentState is self.states[6] and line[i] is '+') or (self.currentState is self.states[7] and line[i] is '-'):
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                            symbol = line[i]
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                            symbol = ''
                            self.currentState = self.states[0]

                        elif (self.currentState is self.states[6] and line[i] is '-') or (self.currentState is self.states[7] and line[i] is '+'):
                            symbol = symbol + line[i]
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                            symbol = ''
                            self.currentState = self.states[0]

                        elif self.currentState is self.states[0] and line[i] is '/':
                            self.currentState = self.states[13]
                            symbol = symbol + line[i]             
                        elif self.currentState is self.states[13] and line[i] is '/':     
                            self.currentState = self.states[14]
                            symbol = ''       
                        elif self.currentState is self.states[13] and line[i] is '*':
                            self.currentState = self.states[15]
                        elif self.currentState is self.states[15] and line[i] is '*':
                            self.currentState = self.states[16]
                        elif self.currentState is self.states[16] and line[i] is '/':
                            self.currentState = self.states[0]
                        elif self.currentState is self.states[16] and line[i] is not '/':
                            if line[i] is '*':
                                self.currentState = self.states[16]
                            else:
                                self.currentState = self.states[15]
                            symbol = ''
                        elif self.currentState is not self.states[14] and self.currentState is not self.states[15]:
                            print(self.currentState)
                            if symbol.strip() is '-':
                                self.token.createtoken(
                                    'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                            symbol = line[i]
                            self.token.createtoken(
                                'ART', j, self.symbolTable.insertSymbol(symbol.strip()))
                            symbol = ''
                            self.currentState = self.states[0]

                    elif line[i] in self.relational:

                        if self.currentState is self.states[6] or self.currentState is self.states[7] or self.currentState is self.states[13]:
                            self.token.createtoken('ART',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        if self.currentState is self.states[8] or self.currentState is self.states[9]:
                            self.token.createtoken('LOG',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        if self.currentState is self.states[0] and line[i] is '!':
                            self.currentState = self.states[17]
                            symbol = symbol + line[i]
                        elif self.currentState is self.states[0] and line[i] is '=':
                            self.currentState = self.states[18]
                            symbol = symbol + line[i]
                        elif self.currentState is self.states[0] and line[i] is '>':
                            self.currentState = self.states[19]
                            symbol = symbol + line[i]
                        elif self.currentState is self.states[0] and line[i] is '<':
                            self.currentState = self.states[20]
                            symbol = symbol + line[i]

                        elif (self.currentState is self.states[17] or self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]) and line[i] is '=':
                            symbol = symbol + line[i]
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''
                        else:
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            symbol = line[i]
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        

                    elif line[i] in self.logical:
                        if self.currentState is self.states[18] or self.currentState is self.states[19] or self.currentState is self.states[20]:
                            self.token.createtoken('REL',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        if self.currentState is self.states[6] or self.currentState is self.states[7] or self.currentState is self.states[13]:
                            self.token.createtoken('ART',j, self.symbolTable.insertSymbol(symbol))
                            self.currentState = self.states[0]
                            symbol = ''

                        if self.currentState is self.states[0] and line[i] is '&':
                            self.currentState = self.states[8]
                            symbol = symbol + line[i]
                        elif self.currentState is self.states[0] and line[i] is '|':
                            self.currentState = self.states[9]
                            symbol = symbol + line[i]
                        elif (self.currentState is self.states[8] and line[i] is '&') or (self.currentState is self.states[9] and line[i] is '|'):
                            symbol = symbol + line[i]
                            self.token.createtoken('LOG', j, self.symbolTable.insertSymbol(symbol))
                            symbol = ''
                            self.currentState = self.states[0]
                        elif (self.currentState is self.states[9] and line[i] is '&') or (self.currentState is self.states[8] and line[i] is '|'):
                            self.token.createtoken('LOG', j, self.symbolTable.insertSymbol(symbol))
                            symbol = line[i]
                            self.token.createtoken('LOG', j, self.symbolTable.insertSymbol(symbol))
                            symbol = ''
                            self.currentState = self.states[0]

                    elif line[i] in self.delimiters:
                        if self.currentState is self.states[6] or self.currentState is self.states[7] or self.currentState is self.states[13]:
                            self.token.createtoken('ART',j, self.symbolTable.insertSymbol(symbol))
                        symbol = line[i]
                        self.token.createtoken(
                        'DEL',j, self.symbolTable.insertSymbol(symbol))
                        symbol = ''
                        self.currentState = self.states[0]
            
        f.close()

    def printar(self):
        print(self.ponctuation)

    def printtokens(self):
        f = open(self.file + '-saida.txt', 'w')
        token = self.token.getAlltoken()
        for token in token:
            f.write(str(token[2]) + ' ' + token[0] + ' ' +
                    self.symbolTable.getSymbol(token[1], token[0]) + '\n')
        f.close()


if __name__ == '__main__':
    lexicalAnalyzer = lexicalAnalyzer("./files/entrada.txt")
    lexicalAnalyzer.printar()
