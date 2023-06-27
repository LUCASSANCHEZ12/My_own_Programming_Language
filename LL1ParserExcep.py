from collections import deque
import Lexer as Lexer

class Parser:
    
    def __init__(self):
        
        self.input = ""
        self.index = -1
        self.stack = deque()
        self.non_terminals = ["Stmt","Stmt'","else_case","args","args'","arg","type","B","B'","B1","B1'","B2", "Relop", "E","E'","T","T'","F","num"]
        self.terminals = ["$","def","id","(",")","do","end", "if","then", "while", "int","=",";","float","bool","string","else",",","or","and","not","True","False","STRING","==","!=",">","<",">=","<=","+","-","*","/","INT","FLOAT"]
        self.table = [
            #   "$"     "def"       "id"        "("     ")"        "do"        "end"        "if"       "then"      "While"     "int"       "="     ";"     "float"     "bool"      "string"        ","     "or"        "and"       "not"       "True"      "False"     "STRING"        "=="        "!="        ">"     "<"     ">="        "<="        "+"        "-"        "*"        "/"        "INT"      "FLOAT"]                         
            [    None, ["def","id","(", "args",")","do","Stmt","end" ,"Stmt'"], ["id","=","E",";","Stmt'"], None, None ,None, None, ["if", "(","B",")","then","Stmt", "else_case"], None, ["while", "(", "B", ")", "do", "Stmt", "end", "Stmt'"], ["int" ,"id", "=", "E", ";", "Stmt'"],None, None, ["float",  "id" ,"=", "E",";", "Stmt'"], ["bool",  "id" ,"=", "B",";", "Stmt'"], ["string",  "id" ,"=", "S",";", "Stmt'"], None, None, None, None, None, None, None, None, None, None,None, None, None, None, None, None, None, None, None, None],                                                                                                                                                                                                                        
            [    "",     ["Stmt"],   ["Stmt"],       None,      None,         None,    "", ["Stmt"],      None,     ["Stmt"],      ["Stmt"],          None,      None,      ["Stmt"],          ["Stmt"],          ["Stmt"],              "",            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None, None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         None,          None,      None,         None,         ["end", "Stmt'"],         None,   None,     None,         None,   None,      None,      None,   None,   None,       ["else","Stmt","end","Stmt'"],            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         None,          None,      "",         None,         None,           None,     None,          ["arg","args'"],   None,      None,      ["arg","args'"],   ["arg","args'"],   ["arg","args'"],       None,            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         None,          None,      "",         None,         None,           None,     None,          None,              None,      None,      None,              None,              None,             None,     [",","args'"],   None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         None,          None,      None,         None,         None,           None,     None,          ["type","id"],     None,      None,      ["type","id"],     ["type","id"],     ["type","id"],    None,      None,            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         None,          None,      None,         None,         None,           None,     None,          ["int"],           None,      None,      ["float"],         ["bool"],          ["string"],           None,  None,            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         ["B1","B'"],   ["B1","B'"], None,     None,         None,         None, None,         None,     None,          None,              None,      None,      None,              None,              None,                  None,            None,                  None,                    ["B1","B'"],             ["B1","B'"],             ["B2","B1'"],            ["B1","B'"],                 None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["B1","B'"],             ["B1","B'"]],
            [    None,  None,         None,          None,        "",         None,         None,         None,     None,          None,              None,      "",      None,              None,              None,                  None,  None,          ["or","B1","B'"],      None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         ["B2","B1'"],  ["B2","B1'"], None,         None,         None,        None,     None,          None,              None,      None,      None,              None,              None,                  None,            None,                None,   None,                    ["B2","B1'"],            ["B2","B1'"],            ["B2","B1'"],            ["B2","B1'"],                None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["B2","B1'"],            ["B2","B1'"]],
            [    None,  None,         None,          None,        "",         None,         None,         None,     None,          None,              None,      "",      None,              None,              None,                  None,        None,    "",                  ["and","B2","B1'"],      None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         ["E","Relop","E"], ["E","Relop","E"],  None, None,   None, None,            None,     None,          None,              None,      None,      None,              None,              None,                  None,            None,                  None,            None,         ["not","B2"],            ["True"],                ["False"],               ["STRING","Relop","STRING"], None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["E","Relop","E"],       ["E","relop","E"]],
            [    None,  None,         None,          None,         None,         None,         None, None,        None,     None,          None,              None,      None,      None,              None,              None,                  None,           None,  None,                  None,                    None,                    None,                    None,                    None,                        ["=="],                  ["!="],                  [">"],                   ["<"],                   [">="],                  ["<="],                  None,                    None,                    None,                    None,                    None,                    None],
            [    None,  None,         ["T","E'"],      ["T","E'"], None, None,          None,         None,       None,     None,          None,              None,      None,      None,              None,              None,                  None,         None,   None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["T","E'"],              ["T","E'"]],
            [    None,  None,         None,          None,         "",         None, None,         None,        None,     None,          None,              None,      "",      None,              None,              None,                 None, None,            "",                  "",                    None,                    None,                    None,                    None,                        "",                    "",                    "",                    "",                    "",                    "",                    ["+","T","E'"],          ["-","T","E'"],          None,                    None,                    None],
            [    None,  None,         ["F","T'"],      ["F","T'"],  None,         None,         None,       None,     None,          None,              None,      None,      None,              None,              None,             None,    None,        None,     None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["F","T'"],              ["F","T'"]],
            [    None,  None,         None,          None,          "",         None, None,         None,       None,     None,          None,              None,      "",      None,              None,              None,                 None, None,            "",                  "",                    None,                    None,                    None,                    None,                        "",                    "",                    "",                    "",                    "",                    "",                    "",                    "",                    ["*","F","T'"],          ["/","F","T'"],          None,                    None],
            [    None,  None,         ["id"],          ["(","E",")"], None,          None,         None,    None,     None,          None,              None,      None,      None,              None,              None,                  None,            None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["num"],                 ["num"]],
            [    None,  None,         None,          None,            None,         None, None,         None,     None,     None,          None,              None,      None,      None,              None,              None,                  None,       None,     None,                  None,                    None,                    None,                    None,                    None,                        None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    None,                    ["INT"],                 ["FLOAT"]]
        ]
                
    def main(self, input):
        self.input = input
        
        
    def pushRule(self, rule):
        for i in range(len(rule) - 1, -1, -1):
            self.stack.append(str(rule[i]))
    
    
    def algorithm(self):
        self.stack.append("Stmt")
        token = self.read()
        old_token = token
        top = None
        try:
            while(True):
                if self.stack == deque([]):    
                    break
                
                top = self.stack.pop()
                
                if top in self.non_terminals:
                    rule = self.getRule(top, token)
                    
                    if rule != None:
                        self.pushRule(rule)
                    else:
                        return Lexer.InvalidSyntaxError(pos_start=token.pos_start.copy(), pos_end=token.pos_end.copy(), details="After ' "+str(value)+" ', expected ';', '(' or ')' and got: ' "+ token.value+" '")
                elif top in self.terminals:
                    value = token.value if token.type == Lexer.TT_KEYWORD or token.type == Lexer.TT_BOLEAN or token.type == 'PARSE' else token.type
                    if not (top == value):
                       # Error     
                        return Lexer.InvalidSyntaxError(pos_start=old_token.pos_start.copy(), pos_end=old_token.pos_end.copy(), details="Expected ' ; ' before: ' "+ old_token.value+" '")
                    elif token == "$":
                        continue
                    else:
                        old_token = token
                        token = self.read()
                else:
                    # Error
                    return Lexer.InvalidSyntaxError(pos_start=token.pos_start.copy(), pos_end=token.pos_end.copy(), details="Expected ' "+str(top)+" ' and got: ' "+ token.value+" '")
            if token.value == "$" and self.stack == deque([]):
                print("\nInput is ACCEPTED by LL1 Parser")
                return None
            else:
                return Lexer.InvalidSyntaxError(pos_start=token.pos_start.copy(), pos_end=token.pos_end.copy(), details="Expected ' "+str(top)+" ' and got: ' "+ token.value+" '")
        except Exception as e:
            # Error 
            # Input is NOT ACCEPTED by LL1 Parser
            value = old_token.value if old_token.type == Lexer.TT_KEYWORD or old_token.type == Lexer.TT_BOLEAN or old_token.type == 'PARSE' else old_token.type
            return Lexer.InvalidSyntaxError(pos_start=old_token.pos_start.copy(), pos_end=old_token.pos_end.copy(), details="Expected ' "+str(top)+" ' and got: ' "+ value+" '")
                
    def read(self):
        self.index +=1
        token = self.input[self.index]
        return token
        
    def getRule(self, non, token):
        
        term = token.value if token.type == Lexer.TT_KEYWORD or token.type == Lexer.TT_BOLEAN or token.type == 'PARSE' else token.type
        
        row = self.non_terminals.index(non)
        column = self.terminals.index(term)
        
        rule = self.table[row][column]

        return rule