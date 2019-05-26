import ply.lex as lex

# 处理保留字
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'default': 'DEFAULT',
    'def': 'DEF',
    'and': 'AND',
    'return': 'RETURN',
}
tokens = [
    'NUMBER',
    'ID',
    'special_word',
    'error_word'
] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

t_special_word = r'\+|-|\*|/|\(|\)|:|\'|=|\[|\]|,'

def t_error_word(t):
    r'[0-9]+[a-zA-Z_]+'
    print("Illegal character '%s',location:('%d', '%d')" % (t.value, t.lexer.lineno, find_column(data, t)))
    t.lexer.skip(1)

def t_error(t):
    print("Illegal character '%s',location:('%d', '%d')" % (t.value[0], t.lexer.lineno, find_column(data, t)))
    t.lexer.skip(1)

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    print('start = ', line_start, ' end = ', token.lexpos)
    return (token.lexpos - line_start) + 1

t_ignore = ' \t'


lexer = lex.lex()

data = '''
def f_copy(data):
	data = data + 2
a = [1, 2]
for i in range(len(a)):
	a[i] = f_copy(a[i])
print(a)
1a
 '''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
