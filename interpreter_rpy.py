import sys
import os

# ------function numbers-------
LD_INT = 1
LD_CINT = 2
ST_INT = 3
PLS_INT = 4
SUB_INT = 5
MUL_INT = 6
DIV_INT = 7
MOD_INT = 8
LSS_INT = 9
GRT_INT = 10
EQ_INT = 11
AND = 12
OR = 13
NOT = 14
JUMP = 15
JMPIF = 16
PRINT = 17
# -----------------------------

# ------interpret part---------
# interpreter body
def interpret(code):
    temp_int = []
    data_int = []
    codesize = len(code)
    pc = 0
    while pc < codesize:
        instr = code[pc]
        if instr[0] == LD_INT:
            temp_int.append(data_int[instr[1]])
        elif instr[0] == LD_CINT:
            temp_int.append(instr[1])
        elif instr[0] == ST_INT:
            if len(data_int) <= instr[1] :
                data_int.append(0)
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
            temp_int.append(int(x / y))
        elif instr[0] == MOD_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(x % y)
        elif instr[0] == LSS_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(int(x < y))
        elif instr[0] == GRT_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(int(x > y))
        elif instr[0] == EQ_INT:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(int(x == y))
        elif instr[0] == AND:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(int(x and y))
        elif instr[0] == OR:
            y = temp_int.pop()
            x = temp_int.pop()
            temp_int.append(int(x or y))
        elif instr[0] == NOT:
            x = temp_int.pop()
            temp_int.append(int(not x))
        elif instr[0] == JUMP:
            pc = instr[1]
            continue
        elif instr[0] == JMPIF:
            if temp_int.pop():
                pc = instr[1]
                continue
        elif instr[0] == PRINT:
            print(temp_int.pop())
        pc+=1

# -----------------------------

# ------decode part------------
# source code->List type program
def getprogram(filename):
    fp = os.open(filename, os.O_RDONLY, 0777)
    program = ""
    while True:
        r = os.read(fp, 4096)
        if not r:
            break
        program += r
    os.close(fp)
    return program

# devide with sep and erase ''
def devidecode(program,sep):
    program = program.split(sep)
    program = [s for s in program if s != '']
    return program

# intermediate language->intermediate representation
def decode_iml(filename):
    program = devidecode(getprogram(filename),"\r\n")
    code = []
    for p in program:
        instr = p.split(" ")
        if len(instr) < 2:
            print(instr[0])
            print("Instr size Wrong!!!!!!!")
        if instr[1] == '_':
            instr[1] = '0'
        # if len(instr) > 2:
        #     print("comment")
        #     print(instr[2:])
        codenumber = 0
        if instr[0] == "ld_cint":
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
        elif instr[0] == "lss_int":
            codenumber = LSS_INT
        elif instr[0] == "grt_int":
            codenumber = GRT_INT
        elif instr[0] == "eq_int":
            codenumber = EQ_INT
        elif instr[0] == "and":
            codenumber = AND
        elif instr[0] == "or":
            codenumber = OR
        elif instr[0] == "not":
            codenumber = NOT
        elif instr[0] == "jump":
            codenumber = JUMP
        elif instr[0] == "jmpif":
            codenumber = JMPIF
        elif instr[0] == "print":
            codenumber = PRINT
        else :
            print(instr[0])
            print("Wrong!!!!!!!")
        code.append((codenumber,int(instr[1])))
    return code

# -----------------------------

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "Need a filename."
        return 1
    # code = decode(filename)
    code = decode_iml(filename)
    interpret(code)
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)











#---------------------------
