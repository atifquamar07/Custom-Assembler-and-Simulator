opcodes = {'add':'00000' ,'sub':'00001' ,'mov':'00010' ,'mov':'00011' ,'ld':'00100' ,'st':'00101' ,'mul':'00110' ,'div':'00111' ,'rs':'01000' ,'ls':'01001' ,'xor':'01010' ,'or':'01011' ,'and':'01100' ,'not':'01101' , 'cmp':'01110' , 'jmp':'01111' , 'jlt':'10000' , 'jgt':'10001' , 'je':'10010' , 'hlt':'10011'}

reg = ['R0' , 'R1' , 'R2' , 'R3' , 'R4' , 'R5' , 'R6', 'FLAGS']

reg_opcodes = {0: '000', 1: '001', 2:'010', 3:'011', 4:'100', 5:'101', 6:'110', 7:'111'}    #7=flag

registers = [0,0,0,0,0,0,0] 
flag = '0000000000000000'

inputinst=[] #all given instructions
memory = []   #length of 256 loaded with all inputinst then storing mem

while True:
    try:
        x=input()
        inputinst.append(x)
    except EOFError:
        break

for i in range(0,256):
    memory.append("0000000000000000")

lastline=len(inputinst) #lastline of memory arr

def int_to_binary(x):
    x = int(x)
    x = bin(x)
    x = x[2:]
    trailing_zeroes = 16-len(x)
    out = trailing_zeroes*'0'
    out = out+x
    return out

def int_to_binary_for_pc(x):
    x = int(x)
    x = bin(x)
    x = x[2:]
    trailing_zeroes = 8-len(x)
    out = trailing_zeroes*'0'
    out = out+x
    return out

def binary_to_int(x):
    integer = int(x , 2)
    return integer


def addition(inp):
    #add r0 r1 r2
    
    st=str(inp)
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
    
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
        
        if inp[13:16]==reg_opcodes.get(i):
            r2=i
            
    summ=registers[r1]+registers[r2]
    registers[r0]=summ

    global flag

    if int(summ)>65535:
        flag = flag[:12] + '1' + flag[13:]

    elif int(summ)<0:
        flag = flag[:12] + '1' + flag[13:]      #setting flag

    else:
        flag = "0000000000000000"

def subtract(inp):
    #sub r0 r1 r2
    
    st=str(inp)
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
            
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
            
        if inp[13:16]==reg_opcodes.get(i):
            r2=i
            
    
    diff=registers[r1]-registers[r2]
    registers[r0]=diff

    global flag
    
    if int(diff)<0:
        flag = flag[:12] + '1' + flag[13:]     #setting flag

    else:
        flag = "0000000000000000"

    
def moveI(inp):
    st=str(inp)
    for i in reg_opcodes:
        if inp[5:8]==reg_opcodes.get(i):
            r0=i
            
    imm=binary_to_int(inp[8:16])  
    
    registers[r0]=imm

    global flag
    flag = "0000000000000000"

def moveR(inp):
    #mov r0 r1
    st=str(inp)

    global flag

    for i in reg_opcodes:
        if inp[10:13]==reg_opcodes.get(i):
            r0=i
        if inp[13:16]==reg_opcodes.get(i):
            r1=i
    if r1==7:
        registers[r0]=binary_to_int(flag)   #coverting flag value from binary to int     
    else:
        registers[r0]=registers[r1]

    
    flag = "0000000000000000"

def load(inp):
    #ld r0 mem
    for i in reg_opcodes:
        if inp[5:8]==reg_opcodes.get(i):
            r0=i
    registers[r0]=memory[binary_to_int(inp[8:16])]  #converting mem from binary to int and storing in given register
                                                    
                                                    
    global flag
    flag = "0000000000000000"
    
def store(inp):
    for i in reg_opcodes:
        if inp[5:8]==reg_opcodes.get(i):
            r0=i

    global lastline

    memory[lastline]=int_to_binary(registers[r0])  #storing the value at register[r0] in the memory arr at last line 
    lastline+=1      
    
    global flag
    flag = "0000000000000000"                                          # increase lastline after every call ??????????

def multiply(inp):
    # mul r0 r1 r2
    st=str(inp)
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
        
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
        
        if inp[13:16]==reg_opcodes.get(i):
            r2=i
            
    global flag

    mult=registers[r1]*registers[r2]
    registers[r0]=mult
    if mult<0:
        flag = flag[:12] + '1' + flag[13:]      #setting flag

    elif mult>65535:
        flag = flag[:12] + '1' + flag[13:]

    else:      
        flag = "0000000000000000"
    

def divide(inp):
    #div r0 r1
    st=str(inp)
    for i in reg_opcodes:
        if inp[10:13]==reg_opcodes.get(i):
            r3=i
        if inp[13:16]==reg_opcodes.get(i):
            r4=i

    registers[0]=int(registers[r3]/registers[r4])
    registers[1]=int(registers[r3]%registers[r4])

    global flag
    flag = "0000000000000000"

def rightshift(inp):
    for i in reg_opcodes:
        if inp[5:8] == reg_opcodes.get(i):
            r0 = i
            
    registers[r0] = int(registers[r0]/(2**(binary_to_int(inp[8:16]))))

    global flag
    flag = "0000000000000000"


def leftshift(inp):

    for i in reg_opcodes:
        if inp[5:8] == reg_opcodes.get(i):
            r0 = i

    registers[r0] = int(registers[r0]*(2**(binary_to_int(inp[8:16]))))

    global flag
    flag = "0000000000000000"

            
def andd(inp):
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
            
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
            
        if inp[13:16]==reg_opcodes.get(i):
            r2=i

    x = int_to_binary(registers[r1])
    y = int_to_binary(registers[r2])
            
    a=""

    for i in range(len(x)):
        if x[i]== "1" and y[i]== "1":
            a+="1"
        else:
            a+="0"

    registers[r0]=binary_to_int(a)

    global flag
    flag = "0000000000000000"


def xorr(inp):
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
            
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
            
        if inp[13:16]==reg_opcodes.get(i):
            r2=i
            
    x = int_to_binary(registers[r1])
    y = int_to_binary(registers[r2])
            
    a=""

    for i in range(len(x)):

        if x[i]== "1" and y[i]== "1":
            a+="0"
        elif x[i]== "0" and y[i]== "0":
            a+="0"
        else:
            a+="1"

    registers[r0]=binary_to_int(a)

    global flag
    flag = "0000000000000000"

def orr(inp):
    for i in reg_opcodes:
        if inp[7:10]==reg_opcodes.get(i):
            r0=i
            
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
            
        if inp[13:16]==reg_opcodes.get(i):
            r2=i
            
    
    x = int_to_binary(registers[r1])
    y = int_to_binary(registers[r2])
            
    a=""

    for i in range(len(x)):
        if x[i]== "0" and y[i]== "0":
            a+="0"
        else:
            a+="1"

    registers[r0]=binary_to_int(a)

    global flag
    flag = "0000000000000000"
    
    
def nott(inp):
    #not r1 r2
    st=str(inp)
    for i in reg_opcodes:
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
        if inp[13:16]==reg_opcodes.get(i):
            r2=i

    q = ""
    for i in st:
        if i=="0":
            q+="1"
        else:
            q+="0"

    registers[r1]=(q)

    global flag
    flag = "0000000000000000"

def compare(inp):
    #cmp r1 r2
    st=str(inp)
    for i in reg_opcodes:
        if inp[10:13]==reg_opcodes.get(i):
            r1=i
        if inp[13:16]==reg_opcodes.get(i):
            r2=i 

    global flag

    if registers[r1]<registers[r2]:
        flag = flag[:13] + '1' + flag[14:]
    
    elif registers[r1]>registers[r2]:
        flag = flag[:14] + '1' + flag[15:]

    elif registers[r1]==registers[r2]:
        flag = flag[:15] + '1'


def jump_unconditional(inp):
    st=str(inp)
    x = st[8:]
    int_x = binary_to_int(x)

    global flag
    flag = "0000000000000000"
    
    return int_x
    
    

def jump_less_than(inp):
    st=str(inp)
    x = st[8:]
    int_x = binary_to_int(x)

    global flag

    if flag[-3]=='1':
        flag = "0000000000000000"
        return int_x
    else:
        flag = "0000000000000000"
        return -1

    

def jump_greater_than(inp):

    st=str(inp)
    x = st[8:]
    int_x = binary_to_int(x)

    global flag
    
    if flag[-2]=='1':
        flag = "0000000000000000"
        return int_x
    else:
        flag = "0000000000000000"
        return -1


def jump_equal(inp):
    st=str(inp)
    x = st[8:]
    int_x = binary_to_int(x)

    global flag

    if flag[-1]=='1':
        flag = "0000000000000000"
        return int_x
    else:
        flag = "0000000000000000"
        return -1

    flag = "0000000000000000"

def print_values(pc):
    print(int_to_binary_for_pc(pc), end=" ")
    print(int_to_binary(registers[0]), end=" ")
    print(int_to_binary(registers[1]), end=" ")
    print(int_to_binary(registers[2]), end=" ")
    print(int_to_binary(registers[3]), end=" ")
    print(int_to_binary(registers[4]), end=" ")
    print(int_to_binary(registers[5]), end=" ")
    print(int_to_binary(registers[6]), end=" ")
    print(int_to_binary(flag))
    

cycle = []
mem = []

def execution_engine():

    pc=0
    cycle_no = 0

    for i in range(len(inputinst)):
        
        if pc==len(inputinst):
            break

        x = inputinst[pc]
        op_code = x[0:5]

        if op_code == '00000':     
            addition(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1  
            cycle_no+=1 

        elif op_code == '00001':
            subtract(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '00010':        
            moveI(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '00011':
            moveR(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '00100':
            load(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 
        
        elif op_code == '00101':
            store(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 
        
        elif op_code == '00110':
            multiply(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '00111':     
            divide(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01000':     
            rightshift(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01001':     
            leftshift(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01010':     
            xorr(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01011':     
            orr(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01100':     
            andd(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01101':     
            nott(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 

        elif op_code == '01110':
            compare(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 
            

        elif op_code == '01111':
            new_pc = jump_unconditional(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc = new_pc
            cycle_no+=1 

        elif op_code == '10000':
            new_pc = jump_less_than(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            if new_pc == (-1):
                pc+=1
                cycle_no+=1 
            else:
                pc = new_pc
                cycle_no+=1 

        elif op_code == '10001':
            new_pc = jump_greater_than(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            if new_pc ==(-1):
                pc+=1
                cycle_no+=1 
            else:
                pc = new_pc
                cycle_no+=1 

        elif op_code == '10010':
            new_pc = jump_equal(x)
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            if new_pc == (-1):
                pc+=1
                cycle_no+=1 
            else:
                pc = new_pc
                cycle_no+=1 

        elif op_code == '10011':
            global flag
            flag = "0000000000000000"
            print_values(pc)
            cycle.append(cycle_no)
            mem.append(pc)
            pc+=1
            cycle_no+=1 
            break 

    for i in range(len(inputinst)):
        memory[i] = inputinst[i]

    for i in range(0,256):
        print(memory[i])

    
execution_engine()
