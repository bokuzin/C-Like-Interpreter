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
JUMPIF = 16
PRINT = 17
# -----------------------------

# ------interpret part---------
def get_printable_location(codesize, pc, stack_alloc, stack_size, code, stack):
    return "pc = %d instr = %d" % (pc, code)


from rpython.rlib.jit import JitDriver
jitdriver = JitDriver(greens=['codesize', 'pc', 'stack_alloc', 'stack_size', 'code', 'stack'], reds=['reg'], get_printable_location=get_printable_location)

def stack_push(stack, alloc, size, n):
    if alloc <= size:
        stack.append(-1)
        alloc += 1
    stack[size] = n
    size+=1
    return (alloc,size)

def stack_pop(stack, alloc, size):
    size-=1
    poped=stack[size]
    return (alloc, size, poped)

def interpreter_debug(pc,code,stack,stack_alloc,stack_size,reg):
    print("pc   : " + str(pc))
    print("stack : " + str(stack))
    print("stackalloc : " + str(stack_alloc))
    print("stacksize : " + str(stack_size))
    print("reg : " + str(reg))
    print("")

STACKBASESIZE = 5
# interpreter body
def interpret(code):
    codesize = len(code)
    pc = 0
    stack = [-1]*STACKBASESIZE
    stack_alloc = STACKBASESIZE
    stack_size = 0
    reg = []
    while pc < codesize:
        jitdriver.jit_merge_point(codesize=codesize, pc=pc, stack_alloc=stack_alloc, stack_size=stack_size, code=code, stack=stack, reg=reg)
        instr = code[pc]
        # interpreter_debug(pc,code,stack,stack_alloc,stack_size,reg)
        if instr[0] == LD_INT:
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, reg[instr[1]])
        elif instr[0] == LD_CINT:
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, instr[1])
        elif instr[0] == ST_INT:
            if len(reg) <= instr[1] :
                reg.append(0)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            reg[instr[1]] = x
        elif instr[0] == PLS_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, x + y)
        elif instr[0] == SUB_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, x - y)
        elif instr[0] == MUL_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, x * y)
        elif instr[0] == DIV_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x / y))
        elif instr[0] == MOD_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, x % y)
        elif instr[0] == LSS_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x < y))
        elif instr[0] == GRT_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x > y))
        elif instr[0] == EQ_INT:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x == y))
        elif instr[0] == AND:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x and y))
        elif instr[0] == OR:
            stack_alloc, stack_size, y = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(x or y))
        elif instr[0] == NOT:
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            stack_alloc, stack_size = stack_push(stack, stack_alloc, stack_size, int(not x))
        elif instr[0] == JUMP:
            target = instr[1]
            pc = target
            continue
        elif instr[0] == JUMPIF:
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            if x:
                target = instr[1]
                pc = target
                continue
        elif instr[0] == PRINT:
            stack_alloc, stack_size, x = stack_pop(stack, stack_alloc, stack_size)
            print(x)
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
        elif instr[0] == "jumpif":
            codenumber = JUMPIF
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
        print("Need a filename.")
        return 1
    # code = decode(filename)
    code = decode_iml(filename)
    interpret(code)
    return 0

def target(*args):
    return entry_point, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__ == "__main__":
    entry_point(sys.argv)











#---------------------------
