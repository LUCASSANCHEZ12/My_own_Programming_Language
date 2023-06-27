import string
################################################
# CONSTANTS
################################################

ILEGALCHARS = '$?`'
DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
LETTERS_DIGITS = LETTERS + DIGITS

################################################
# TOKENS
################################################

TT_STRING  = 'STRING'
TT_BOLEAN  = 'BOLEAN'
TT_INT     = 'INT'
TT_FLOAT   = 'FLOAT'
TT_PLUS    = '+'
TT_MINUS   = '-'
TT_MUL     = '*'
TT_DIV     = '/'
TT_LPAREN  = '('
TT_RPAREN  = ')'
TT_ID      = 'id'
TT_OPASIGN = '='
TT_OPGT    = '>'
TT_OPLT    = '<'
TT_OPEQ    = '=='
TT_OPGTEQ  = '>='
TT_OPLTEQ  = '<='
TT_OPNEQ   = '!='
TT_KEYWORD = 'KEYWORD'
TT_ENDLINE = ';'
TT_EOF     = 'EOF'

BOLEANS = [
    'True',
    'False'
]



OPERATORS = [
    '=',
    '>',
    '<',
    '!',
    '*',
    '/',
    '-',
    '+',
]

BOOL_OPERATORS = [
    '==',
    '>',
    '<',
    '!=',
    '<=',
    '>='
]
BIN_OPERATORS = OPERATORS + BOOL_OPERATORS

MATH_OPERATORS = [
    '*',
    '/'
    '-',
    '+',
    '^',
    '(',
    ')'
]

KEYWORDS = [
    'int',
    'float',
    'bool',
    'string',
    'while',
    'do',
    'end',
    'if',
    'else',
    'then',
    'def'
]


class Token:
    def __init__(self, type_, value_ = None, pos_start = None, pos_end = None):
        self.type = type_
        self.value = value_
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end.copy()
            
    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'
    
################################################
# ERRRORS
################################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.file_name}: line {self.pos_start.line +1} , column {self.pos_start.column +1}'
        result += '\n\n' + self.string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result
    
    def string_with_arrows(self, text, pos_start, pos_end):
        result = ''
        # Calculate indices
        idx_start = max(text.rfind('\n', 0, pos_start.index), 0)
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

        # Generate each line
        line_count = pos_end.line - pos_start.line + 1
        for i in range(line_count):
            # Calculate line columns
            line = text[idx_start:idx_end]
            col_start = pos_start.column if i == 0 else 0
            col_end = pos_end.column if i == line_count - 1 else len(line) - 1

            # Append to result
            result += line + '\n'
            result += ' ' * col_start + '^' * (col_end - col_start)

            # Re-calculate indices
            idx_start = idx_end
            idx_end = text.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(text)

        return result.replace('\t', '')
    
class IllegalCharError(Error):
    def __init__(self,  pos_start, pos_end, details):
        super().__init__( pos_start, pos_end, "Illegal Character", details)

class InvalidSyntaxError(Error):
    def __init__(self,  pos_start, pos_end, details):
        super().__init__( pos_start, pos_end, "Invalid Syntax", details)
        
################################################
# POSITION
################################################

class Position:
    
    def __init__(self, index, ln, col, fn, ftxt):
        self.index = index 
        self.line = ln
        self.column = col
        self.file_name = fn
        self.file_text = ftxt
        
    def advance(self, current_char=None):
        self.index +=1
        self.column +=1
        
        if current_char == '\n':
            self.line +=1
            self.column = 0
            
        return self
    
    def copy(self):
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

################################################
# LEXER
################################################

class Lexer:
    def __init__(self, fn, text):
        self.file_name = fn
        self.text = text
        self.pos = Position(-1, 0, -1,self.file_name, self.text)
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
        
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char == '"':
                token, error = self.make_string()
                if token:
                    tokens.append(token)
                else:
                    return [], error
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char in DIGITS:
                token, error = (self.make_number())
                if error: return [], error
                else: tokens.append(token)
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char in LETTERS :
                tokens.append(self.make_word())
            elif self.current_char in OPERATORS:
                bin_op = self.makeBinOperator()
                if bin_op:
                    tokens.append(bin_op)
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, "' " + char + " '")
            elif self.current_char == ';':
                tokens.append(Token(TT_ENDLINE, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "' " + char + " '")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
    
    def make_string(self):
        pos_start = self.pos.copy()
        str_tok = self.current_char
        self.advance()
        copy_char = ''
        while self.current_char != None and self.current_char != '"':
            str_tok += self.current_char
            copy_char = self.current_char
            self.advance()
        
        if self.current_char == None:
            return None, IllegalCharError(pos_start, self.pos, "' " + copy_char + " '")
        else:
            str_tok += self.current_char
            self.advance()
            return Token(TT_STRING, str_tok, pos_start, self.pos), None
        
    def skip_comment(self):
        
        while self.current_char != '\n' and self.current_char != None:
            self.advance()
            
        if self.current_char != None:
            self.advance()
    
    def makeBinOperator(self):
        op_str = ''
        pos_start = self.pos.copy()
        tok_type = None
        copy_char = ''
        while self.current_char != None and self.current_char in OPERATORS:
            op_str += self.current_char
            copy_char = self.current_char
            self.advance()

        if op_str not in BIN_OPERATORS:
            tok_type = None
            self.current_char = copy_char
        else:
            tok_type = op_str            
        return Token(tok_type, pos_start = self.pos) if tok_type != None else tok_type
            
    def make_word(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        if id_str in KEYWORDS:
            tok_type = TT_KEYWORD
        elif id_str in BOLEANS:
            tok_type = TT_BOLEAN
        else:
            tok_type = TT_ID
        return Token(tok_type, id_str, pos_start, self.pos)
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in DIGITS+'.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if self.current_char != ' ' and self.current_char in LETTERS:
            return None, IllegalCharError(pos_start, self.pos, "' " + self.current_char + " '")
        if dot_count == 0:
            return Token(TT_INT,int(num_str), pos_start, self.pos), None
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos), None


################################################
# RUN
################################################
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    ####################################
    #parser = Parser(tokens)
    #ast = parser.parse()
    #print(ast)
    #return ast.node, ast.error
    return tokens, error