opcodes = {'add':'00000' ,'sub':'00001' ,'mov':'00010' ,'mov':'00011' ,'ld':'00100' ,'st':'00101' ,'mul':'00110' ,'div':'00111' ,'rs':'01000' ,'ls':'01001' ,'xor':'01010' ,'or':'01011' ,'and':'01100' ,'not':'01101' , 'cmp':'01110' , 'jmp':'01111' , 'jlt':'10000' , 'jgt':'10001' , 'je':'10010' , 'hlt':'10011'}

reg = ['R0' , 'R1' , 'R2' , 'R3' , 'R4' , 'R5' , 'R6', 'FLAGS']
reg_mem={}

for i in reg:
    reg_mem[i]=None

reg_opcode = {'R0': '000', 'R1': '001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}

registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']

labels = {}

def bomb(s):
    if s in opcodes.keys():
        return False
    if type(s) == int or type(s) == float:
            return False
    for i in s:
        
        if (i.isalnum() == False and i!= "_" ):
            return False
    return True


def binary(num):
     
    x=(bin(num))
    x=x[2:]
    len_bin=len(x)
    trailing_zeroes=8-len_bin
    zeroes='0'*trailing_zeroes
    eightbit=zeroes+x
    return(eightbit)



flags = "0000000000000000"
arr = []
variableskey=[]    #list of all valid variables
valuess={}   #key values dict for load and store (saved variables with line no)
values={}   #key values dict line no after halt soteed in each variable
condition = True

while True:
    try:
        x=input()
        arr.append(x)
    except EOFError:
        break

line_no=0
line_label=0
for j in range (len(arr)):
    q = arr[j].split() #each input in list
    if len(q)>0:
        st = str(q[0])
        ch = st[-1]
        st_duplicate = st
        st_duplicate=st_duplicate[:-1]
        if ch==":" and st_duplicate.isalnum():
            aa = binary(line_label)
            st=st[:-1]
            if st in labels.keys():
                print("General Syntax Error: Duplicate labels not allowed")
                condition = False
            dictt={st : aa}
            labels.update(dictt)
        if q[0]!=('var'):
            line_label+=1

check_wala = 0
var_condition = True
ll = arr[0].split(" ")
if (condition == True):
    if (ll[0] == "var" and len(ll) == 2 and bomb(ll[1])):
        for j in range(len(arr)):
            lis = arr[j].split(" ")
            if (lis[0] == "var"and len(lis)== 2 and bomb(ll[1])  and check_wala == 0):
                continue
            if (lis[0] != "var"):
                check_wala += 1
            if (check_wala >0 and len(lis) == 2 and lis[0] == "var"and  bomb(lis[1])):
                condition = False
                var_condition = False
                print("All variables not defined at the beginning of the input file")
                break          
    else:
        for j in range(1,len(arr)):
            lis = arr[j].split(" ")
            if (lis[0] == "var"and len(lis) == 2 and bomb(lis[1])):
                condition = False
                var_condition = False
                print("All variables not defined at the beginning of the input file")
                break 
if (var_condition == True and condition == True):  
    
    for j in range(len(arr)):
        if(arr[j] == ''):
            continue
        lst  = arr[j].split()
        lastlst = arr[len(arr)-1].split()
        if (lst[0]== "hlt" and j!= len(arr)-1):
            condition = False
            print("'hlt' command is present at between of the input file")
            break
        p = len(lst[0])-1
        pp = len(lastlst[0])-1
        
        if ((j != len(arr)-1) and (bomb(lst[0][:p]) and len(lst) >1 and lst[0][-1]== ":" and lst[1] == "hlt")):
            condition = False
            print("'hlt' command is present at between of the input file")
            break
        if (arr[len(arr)-1] != "hlt" and len(lastlst) == 1):
            condition = False
            print("'hlt' command not present at the end of the file")
            break
        if (bomb(lastlst[0][:pp]) == False and lastlst[0][-1] == ":"  and (lastlst[1] != "hlt")):
            condition = False
            print("'hlt' command not present at the end of the file")
            break

def lastline(arr): #to find the last line in program
    line=0
    for i in range (len(arr)):
        x = arr[i]
        lst = x.split()
        if len(lst)==2 and lst[0]=='var' and bomb(lst[1]):
            line+=0
        else:
            line+=1
    return line

if condition == True:
    for i in range (len(arr)):
        if arr[i]=="":
            line_no+=1
            continue
        output=''
        x = arr[i]
        lst = x.split()
        ll = lst[0]
        if ll[-1]==":":
            lst.remove(ll)
        if (len(lst) == 0):
            print("label must have an instruction ")
            line_no += 1
            continue
        operation = lst[0]
        
        operation_copy = operation
        if operation_copy[-1]==":":
            
            operation_copy = operation_copy[:-1]
        
        # stroring variable
        if operation =='var' and len(lst) != 2 :
            print("Error in line no ",line_no,"and variable instruction is not correct")
            line_no += 1
            continue
        if operation=='var' and bomb(lst[1]):
            variableskey.append(lst[1])  
            continue
        for k in range(len(variableskey)):  #for setting the last line as value in varibles in order of var declaration
            #valuess={}   #key values dict line no after halt soteed in each variable
            lineno=lastline(arr)          
            valuess[variableskey[k]]=lineno
            lineno+=1

        if operation in opcodes.keys():
            output = ''
            if operation=='add':
                output=output+'00000'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg3 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break
                else:
                    print("Error in line ",line_no)
    
                line_no+=1
                if len(output)== 16:
                        print(output)
            
            if operation=='sub':
                output=output+'00001'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg3 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break
                else:
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)== 16:
                        print(output)  
            
            def check(k,p):
                try:
                    j  = int(k)
                    if (j>= 0 and j< 256) and p=='$':
                        return 1        #str(bin(j))[2:]  
                    else:
                        return 0
                except:
                    return 0
             #Move
             
            if operation=='mov':
                if len(lst)==3:
                    k=str(lst[2])
                    if check(k[1:],lst[2][0]) ==1:
                        output=output+'00010'
                        for i in range(1):
                            reg1 = lst[1]
                            if reg1 in reg_opcode.keys(): 
                                
                                output=output+str(reg_opcode[reg1])
                            else:
                                print("Error in line ",line_no)
                                output=''
                                break
                            j=int(k[1:])
                            output=output+str(binary(j))
                        
                
                    elif True:   
                        output=output+'00011' 
                        output=output+'00000'  #unused            
                        for i in range(1):
                            reg1 = lst[1]
                            if reg1 in reg_opcode.keys(): 
                                output=output+str(reg_opcode[reg1])
                            else:
                                print("Error in line ",line_no)
                                break
                                
                            reg2 = lst[2]
                            if reg2 in reg_opcode.keys():
                                output=output+str(reg_opcode[reg2])
                            else:
                                print("Error in line ",line_no)
                                break
                    else:
                        
                        print("Error in line ",line_no)
                        break

                else: 
                    
                    print("Error in line ",line_no)         
                line_no+=1
                if len(output)==16:
                        print(output)

            # LOAD 
            if operation=='ld':
                output=output+'00100'
                if len(lst)==3:
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                        if lst[2] in valuess.keys(): 
                            k=binary(valuess[lst[2]])
                            output=output+k
                        else:
                            print("Error in line ",line_no)
                            break                        
                        
    
                else:
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)== 16:
                        print(output)                           
            
            # STORE
            if operation=='st':
                output=output+'00101'
                if len(lst)==3:
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                        if lst[2] in valuess.keys(): 
                            k=binary(valuess[lst[2]])
                            output=output+k
                        else:
                            print("Error in line ",line_no)
                            break                                 
                else:
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)== 16:
                        print(output)    
    
            # MULTIPLY
            if operation=='mul':
                output=output+'00110'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg3 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break
                else:
                    print("Error in line ",line_no)
    
                line_no+=1
                if len(output)== 16:
                        print(output)  
    
            # DIVIDE
            if operation=='div':
                output=output+'00111'
                if len(lst)==3:
                    output=output+'00000'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                else:
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)== 16:
                        print(output)  

                  
            if operation == 'rs':
                  output=output+'01000'
                  if len(lst)==3:
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        
                        k = lst[2][1:]
                        if k[0:1] =="$":
                            try:
                                j  = int(k)
                                if j>= 0 and j< 256:
                                    output +=str(binary(j))  
                                else :
                                    print("Error in line ",line_no)
                                    break
                            except:
                                print("Error in line ",line_no)
                                break
                        else :
                            print("Error in line ",line_no)
                            break
                        
                  else :
                    print("Error in line ",line_no)
                    
                  line_no+=1
                  if len(output)==16:
                        print(output)


            if operation == 'ls':
                output=output+'01001'
                if len(lst)==3:
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        k = lst[2][1:]
                        if k[0:1] =="$":
                            try:
                                j  = int(k)
                                if j>= 0 and j< 256:
                                    output +=str(binary(j))  
                                else :
                                    print("Error in line ",line_no)
                                    break
                            except:
                                print("Error in line ",line_no)
                                break
                        else :
                            print("Error in line ",line_no)
                            break
                else :
                    print("Error in line ",line_no)
                    
                line_no+=1
                if len(output)==16:
                        print(output)

            if operation=='xor':
                output=output+'01010'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break
                else :
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)==16:
                        print(output)



            if operation=='or':
                output=output+'01011'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break

                else :
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)==16:
                        print(output)


            if operation=='and':
                output=output+'01100'
                if len(lst)==4:
                    output=output+'00'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break
                    
                        reg3 = lst[3]
                        if reg2 in reg_opcode.keys():
                            output=output+str(reg_opcode[reg3])
                        else:
                            print("Error in line ",line_no)
                            break

                else :
                    print("Error in line ",line_no)
                           
                line_no+=1
                if len(output)==16:
                        print(output)

            # NOT

            if operation=='not':
                output=output+'01101'
                if len(lst)==3:
                    output=output+'00000'
                    for i in range(1):     
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
            
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break

                else :
                    print("Error in line ",line_no)
                            
                line_no+=1
                if len(output)==16:
                    print(output)

            #COMPARE

            if operation=='cmp':
                output=output+'01110'
                if len(lst)==3:
                    output=output+'00000'
                    for i in range(1):
                        reg1 = lst[1]
                        if reg1 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg1])
                        else:
                            print("Error in line ",line_no)
                            break
            
                        reg2 = lst[2]
                        if reg2 in reg_opcode.keys(): 
                            output=output+str(reg_opcode[reg2])
                        else:
                            print("Error in line ",line_no)
                            break

                else :
                    print("Error in line ",line_no)
                      
                line_no+=1
                if len(output)==16:
                    print(output)


            if operation=='jmp':
                output=output+'01111'
                if len(lst)==2:
                    output=output+'000'
                    xx=lst[1]
                    if xx in labels.keys():    
                        line = labels[xx]
                        output=output+line
                        if len(output)==16:
                            print(output)
                    else:
                        print("Predefined label not used in line no" , line_no)
                        line_no+=1
                        continue
                else:
                    print("Error in line ",line_no)
                line_no+=1

            if operation=='jlt':
                output=output+'10000'
                if len(lst)==2:
                    output=output+'000'
                    xx=lst[1]
                    if xx in labels.keys():    
                        line = labels[xx]
                        output=output+line
                        if len(output)==16:
                            print(output)
                    else:
                        print("Predefined label not used in line no" , line_no)
                        line_no+=1
                        continue
                else:
                    print("Error in line ",line_no)
                line_no+=1

            if operation=='jgt':
                output=output+'10001'
                if len(lst)==2:
                    output=output+'000'
                    xx=lst[1]
                    if xx in labels.keys():    
                        line = labels[xx]
                        output=output+line
                        if len(output)==16:
                            print(output)
                    else:
                        print("Predefined label not used in line no" , line_no)
                        line_no+=1
                        continue
                else:
                    print("Error in line ",line_no)
                line_no+=1

            if operation=='je':
                output=output+'10010'
                if len(lst)==2:
                    output=output+'000'
                    xx=lst[1]
                    if xx in labels.keys():    
                        line = labels[xx]
                        output=output+line
                        if len(output)==16:
                            print(output)
                    else:
                        print("Predefined label not used in line no" , line_no)
                        line_no+=1
                        continue
                else:
                    print("Error in line ",line_no)
                line_no+=1

            if operation=='hlt':
                print(str(1001100000000000))

           
        else:
            print("Error in line ",line_no)
            line_no+=1