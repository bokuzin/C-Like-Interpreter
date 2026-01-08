import sys

# ------function numbers-------
DECL_INT = 1
LD_INT = 2
LD_CINT = 3
ST_INT = 4
PLS_INT = 5
SUB_INT = 6
MUL_INT = 7
DIV_INT = 8
MOD_INT = 9
PRINT = 10
# -----------------------------

# ------operator list----------
OPERATOR = ['=','+','-','*','/','%','(',')']
# -----------------------------

# ------reserved keyword-------
KEYWORD = ["int","print","if","else","while","for"]
# -----------------------------

# ------interpret part---------
# interpreter body
def interpret(code):
    temp_int = []
    data_int = []
    codesize = len(code)
    for i in range(codesize):
        # print(i)
        # print(code[i])
        # print(temp_int)
        # print(data_int)
        # print("")
        instr = code[i]
        if instr[0] == DECL_INT:
            data_int.append(0)
        elif instr[0] == LD_INT:
            temp_int.append(data_int[instr[1]])
        elif instr[0] == LD_CINT:
            temp_int.append(instr[1])
        elif instr[0] == ST_INT:
            data_int[instr[1]] = temp_int.pop()
        elif instr[0] == PLS_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(x + y)
        elif instr[0] == SUB_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(x - y)
        elif instr[0] == MUL_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(x * y)
        elif instr[0] == DIV_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            print(x)
            print(y)
            temp_int.append(int(x / y))
        elif instr[0] == MOD_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(x % y)
        elif instr[0] == PRINT:
            print(data_int[instr[1]])

# -----------------------------

# ------decode part------------
# source code->List type program
def getprogram(filename):
    f = open(filename, 'r')
    return f.read()

# devide with sep and erase ''
def devidecode(program,sep):
    program = f.read().split(sep)
    program = [s for s in program if s != '']
    return program

# operator devision->space devision
def insertspace(p):
    for op in OPERATOR:
        p = p.replace(op, ' ' + op + ' ')
    return p

# decode error
def decodeERR(instr,message):
    print(instr)
    raise SyntaxError("decode error." + message)

# program->intermediate representation
def decode(filename):
    program = devidecode(getprogram(filename),';')
    code = []
    variablemap = {}
    for p in program:
        instr = insertspace(p).replace("\r\n"," ").split()
        if instr[1] == '(':
            if instr[0] == "print":
                # check [print,(,_,)] and existance of variable
                if len(instr) == 4 and instr[3] == ')' and instr[2] in variablemap:
                    code.append((PRINT,variablemap[instr[2]]))
                else:
                    decodeERR(instr,"wrong print syntax")
            else:
                decodeERR(instr,"unknown function")
        elif instr[1] == '=':
            if instr[0] in variablemap:
                calc(code,instr[2:])


# intermediate language->intermediate representation
def decode_iml(filename):
    program = devidecode(getprogram(filename),"\r\n")
    # print(program)
    code = []
    for p in program:
        instr = p.split()
        if len(instr) < 2 or instr[1] == '_':
            instr[1] = '0'
        codenumber = 0
        if instr[0] == "decl_int":
            codenumber = DECL_INT
        elif instr[0] == "ld_cint":
            codenumber = LD_CINT
        elif instr[0] == "ld_int":
            codenumber = LD_INT
        elif instr[0] == "st_int":
            codenumber = ST_INT
        elif instr[0] == "pls_int":
            codenumber = PLS_INT
        elif instr[0] == "sub_int":
            codenumber = SUB_INT
        elif instr[0] == "mul_int":
            codenumber = MUL_INT
        elif instr[0] == "div_int":
            codenumber = DIV_INT
        elif instr[0] == "mod_int":
            codenumber = MOD_INT
        elif instr[0] == "print":
            codenumber = PRINT
        else :
            print(instr[0])
            print("Wrong!!!!!!!")
        code.append((codenumber,int(instr[1])))
    return code

# -----------------------------

if __name__ == "__main__":
    filename = sys.argv[1]
    # code = decode(filename)
    code = decode_iml(filename)
    interpret(code)











#---------------------------
