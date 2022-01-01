#For formatting the strings

def format(str):
    str2=""
    for i in range(len(str)):
        if(str[i]==" "and str[i+1]==" "):
            continue
        else:
            str2+=str[i]
    return str2

# Creates a dictionary containing all the Instructions and their data
def createInsDict(File):
    Dict = {}
    for line in File:
        instruction = line.split()
        Dict[instruction[0]] = [instruction[1], instruction[2]]
    return Dict

# For reading the input code
def readCode(File):
    global directives
    Array = []
    for line in File:
        if(line[0] == '.'):
            continue
        col = line.split()
        if(len(col) == 1):
            col = ["", col[0].rstrip("\n"), ""]


        elif(len(col) == 2):
            col[1] = col[1].rstrip("\n")
            if col[1] in insDict or col[1] in directives:
                col = [col[0], col[1], ""]
            else:
                col = ["", col[0], col[1]]


        else:
            col[2] = col[2].rstrip("\n")
        Array.append(col)

    return Array

# For reading the symbol table and literal table
def readSym(File):
    Array = []
    for line in File:
        if(line[0] == '.'):
            continue
        col = line.split()
        col[1] = col[1].rstrip("\n")
        Array.append(col)
    return Array

# For reading the location counter
def readLoc(File):
    global directives
    Array = []
    for line in File:
        if(line[0] == '.'):
            continue
        col = line.split()


        if(len(col) == 2):
            col = [col[0], "", col[1].rstrip("\n"), ""]

        elif(len(col) == 3):
            col[2] = col[2].rstrip("\n")
            if col[2] in insDict or col[2] in directives:
                col = [col[0], col[1], col[2], ""]
            else:
                col = [col[0], "", col[1], col[2]]

        else:
            col[3] = col[3].rstrip("\n")
        Array.append(col)
    return Array

# Read the object code
def readObj(File):
    global directives
    Array = []
    for line in File:
        if(line[0] == '.' or '-' in line):
            continue
        col = line.split()
        if(col[1] in directives):
            if(col[1] == "RESW" or col[1]=="RESB"):
                Array.append(["RESERVED","BORW"])
            continue
        col = [col[0], col[len(col) - 1]]
        Array.append(col)

    return Array

def passOne():
    global base, baseFlag, symbolTable, locationCounter, literalTable
    # Checking for START 
    if(codearr[0][1].upper() != "START"):
        raise Exception("Program doesn't have a START") 
    # Creating the files for pass 1
    locFile=open(locationCounter,"w")
    litable = open(literalTable, "w")
    symbFile=open(symbolTable,"w")
    lit = []
    start_address=int(codearr[0][2], 16)
    current_address=hex(start_address)
    for i in codearr:
        if(debug):
            print(i)
        locFile.write("{:<8}{:<8}{:8}{:8}{}".format("0x" + current_address[2:].zfill(4),i[0],i[1],i[2],'\n'))
        steps = 0
        if(i[1] == "START"):
            continue
        elif(i[1] == "LTORG" or i[1] == "END"):
            for e in lit:
                if(e[1] == ''):
                    steps = 0
                    e[1] = current_address
                    if(e[0][1]=="C"):
                        for z in e[0][2:]:
                            if(z != "'"):
                                steps += 1
                    else:
                        steps += 1
                    current_address = hex(int(current_address,16) + steps)
                    litable.write("{:8}{:8}{}".format(e[0],"0x" + e[1][2:].zfill(4),'\n'))
            continue
        elif(i[1]=="EQU"):
            continue
        elif(i[1] == "BASE"):
            if(i[2] == "*"):
                base = int(current_address,16)
                baseFlag = 0
            else:
                base = i[2]
            continue
        elif(i[1][0] == "+"):
            steps += 4
        elif(i[1][0] == "&"):
            steps += 3
        elif(i[1][0] == "$"):
            steps += 4
        elif(i[1]=="WORD"):
            data = i[2].split(",")
            for j in data:
                steps += 3
        elif(i[1]=="BYTE"):
            data = i[2].split(",")
            for j in data:
                if(j[0]=="C"):
                    for z in j[1:]:
                        if(z != "'"):
                            steps += 1
                else:
                    steps += 1
        elif(i[1]=="RESW"):
            steps += int(i[2]) * 3
        elif(i[1]=="RESB"):
            steps += int(i[2])
        elif(i[1] == "RSUB"):
            if(i[2] != ''):
                raise Exception("Address next to RSUB")
            steps += 3
        elif(insDict[i[1]][0]=="1"):
            steps += 1
        elif(insDict[i[1]][0]=="2"):
            steps += 2
        elif(insDict[i[1]][0]=="34"):
            steps += 3
        if(i[2] != '' and i[2][0] == "="):
            flag = True
            for e in lit:
                if(i[2] == e[0]):
                    flag = False
            if(flag):
                lit.append([i[2],''])
        if(i[0]!=""):
            symbFile.write("{:10}{:10}{}".format(i[0],"0x" + current_address[2:].zfill(4),'\n'))
        current_address = hex(int(current_address,16) + steps)
    # Closing all open files
    locFile.close()
    litable.close()
    symbFile.close()

def passTwo():
    global base, baseFlag, objCodeFile
    obj = open(objCodeFile,"w")
    objarr = []
    if(baseFlag and base):
        base = int(getAddress(base), 16)
    Formats=["$","+","&"]
    AddressingTypes=["#","@","="]
    Literal_Pool=[]
    Registers = {"A":"0","X":"1","L":"2","B":"3","S":"4","T":"5","F":"6"}
    opCode=""
    Flags_Disp_Add=""
    Format_Flag=1
    PC = 0
    for line in codearr:#Make Condition for EQU
        PC += 1
        if(debug):
            try:
                print(line, "\t", locarr[PC])
            except:
                print(line)
        Flags_Disp_Add=""
        opCode=""
        #just for formatting
        if(PC>1):
            obj.write("-"*50+"\n")

        if (line[1]=="START" or line[1]=="EQU" or line[1] == "BASE"):#No object Code
            obj.write("{:10}{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],"","\n"))
            continue


        elif(line[1]=="LTORG" or line[1]=="END"):#generate pool Table
            obj.write("{:10}{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],"","\n"))
            generateLiteral(Literal_Pool, obj, objarr, PC)
            continue


        elif(line[1]=="RSUB"):
            objarr.append("4F0000")
            obj.write("{:10}{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],objarr[len(objarr)-1],"\n"))


        elif(line[1]=="WORD"):
            objarr.append(hex((int(line[2])& (2**32-1)))[2:].zfill(6).upper())# issue here with negative and positive[2:] or [4:]
            obj.write("{:10}{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],objarr[len(objarr)-1],"\n"))


        elif(line[1]=="BYTE"):#T_Con+="{s:{n}}.".format(s=e[1],n=len(e[1]))
            obj.write("{0:10}{1:10}{2:{n}}".format(locarr[PC - 1][0][2:],line[1],line[2],n=len(line[2])+5))#20 needs to go
            data = line[2].split(",")
            extraBytes = 0
            for z in data:
                extraBytes+=1
                Flags_Disp_Add=""
                if(z[0]=="C"):
                    for x in z[1:]:
                        if(x != "'"):
                            Flags_Disp_Add+=hex(ord(x))[2:].upper()
                elif(z[0]=="X"):
                    for x in z[1:]:
                        if(x != "'"):
                            Flags_Disp_Add+=x
                objarr.append(Flags_Disp_Add.upper())
                if(extraBytes==len(data)):
                    obj.write("{}".format(objarr[len(objarr)-1].upper()))
                else:
                    obj.write("{}".format(objarr[len(objarr)-1].upper())+".")#ADD MULTIPLE BYTES OBJECT CODE
            obj.write("\n")


        elif(line[1]=="RESW" or line[1]=="RESB"):
            obj.write("{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],"\n"))
            continue


        else:
            Format_Flag=1
            instruction=line[1]
            #stripping the special type to get the instruction
            if(any(not c.isalnum() for c in instruction)):
                instruction=instruction.translate({ord(x):'' for x in Formats})
                Format_Flag=0
            Label=line[2].translate({ord(x):'' for x in AddressingTypes})
            j = insDict[instruction]
            opCode=j[1]
            Flags_Disp_Add=""


            if(line[2] and line[2][0]=="#"):
                opCode_Increment=1 
            elif(line[2] and line[2][0]=="@"):
                opCode_Increment=2 
            else:
                opCode_Increment=3
            opCode=hex(int(opCode,16)+opCode_Increment)[2:].zfill(2).upper()


            if(line[2] and line[2][0]=="="):
                litFlag = 1
                if(Literal_Pool):   # Check existence of Lit Pool
                    for element in Literal_Pool:
                        if(line[2] == element[0]):   # If current element already in Lit Pool;
                            litFlag = 0     # Do not append it again to the Lit Pool
                if(litFlag):
                    Literal_Pool.append([line[2],None])
                Flags_Disp_Add=calcAddress(PC,line[2])


            elif(Format_Flag):#then we are format 3 or lower we check for addressing type now
                if(j[0]=="1" or j[0]=="2"):
                    opCode=j[1]# format 2 needs handling
                    if(j[0]=="2"):
                        sl=line[2].split(',')
                        if(len(sl)==1):
                            sl.append("A")
                        Flags_Disp_Add+=Registers[sl[0]] + Registers[sl[1]]

                elif(j[0]=="34"):#format 3
                    if(line[2] and line[2][0]=="#" and line[2][1].isdigit()):#check if its constant
                        Flags_Disp_Add=hex(int(line[2][1:]))[2:].zfill(4) #This needs to gooooooo
                    else:
                        Flags_Disp_Add=calcAddress(PC,Label)


            else:#format 4 or special one
                if(line[1][0] == "&" and line[2][0] in ["#","@"]):
                            raise Exception("Format 5 neither supports immediate nor indirect addressing modes.")
                elif(line[2] and line[2][0]=="#" and line[2][1].isdigit()):#check if its constant
                    Flags_Disp_Add=hex(int(line[2][1:]))[2:].zfill(4) #This needs to gooooooo
                else:
                    Flags_Disp_Add=calcAddress(PC,Label)
                    opCode_Increment = 0
                    if(line[1][0] == "&"):
                        opCode_Increment = -3
                        if(int(Flags_Disp_Add[1:], 16) % 2 == 0):
                            opCode_Increment += 2
                        if(twos_complement(int(Flags_Disp_Add[1:], 16), 3) < 0):
                            opCode_Increment += 1
                    opCode=hex(int(opCode,16)+opCode_Increment)[2:].zfill(2).upper() 
            #write to array and file
            objarr.append(opCode+Flags_Disp_Add)
            obj.write("{:10}{:10}{:10}{:10}{}".format(locarr[PC - 1][0][2:],line[1],line[2],objarr[len(objarr)-1],"\n"))
    obj.close()
    HTE()

def HTE():
    global objCodeFile, objFile
    obj = open(objCodeFile, "r")
    objarr = readObj(obj)
    obj.close()
    obj = open(objFile, "w")
    if(debug):
        print(objarr)
    HR="H."+ "{:6}".format(codearr[0][0].upper()).replace(" ", "_") + "." + locarr[len(locarr) - 1][0][2:].zfill(6).upper()
    T_Size=0
    T_Flag=1
    T_Rec=[]
    BORW_Flag=1
    lineNumber=0
    while(lineNumber < len(objarr)):
        e=objarr[lineNumber]
        if(e[1]=="*" or e[1]=="0"):
            lineNumber+=1
            continue
        if (e[1] == "BORW"):
            if(BORW_Flag):
                T_Con=T_Con[:len(T_Con)-1]
                T_Rec.append((T_Start+"{:2}.".format(hex(T_Size)[2:].zfill(2))+T_Con).upper())
            T_Flag=1
            T_Size=0
            BORW_Flag=0
            lineNumber+=1
            continue
        elif((T_Size + len(e[1]) / 2) > 30):
            T_Flag=1
            T_Con=T_Con[:len(T_Con)-1]
            T_Rec.append((T_Start+"{:2}.".format(hex(T_Size)[2:].zfill(2))+T_Con).upper())
            T_Size=0
            continue
        if(T_Flag):
            T_Flag=0
            BORW_Flag=1
            T_Start="T.{:6}.".format(e[0].zfill(6))
            T_Con=""
        else:
            T_Con += "{}.".format(e[1])
            T_Size+=len(e[1])//2
            lineNumber+=1
        if(lineNumber == len(objarr)):
            T_Con=T_Con[:len(T_Con)-1]
            T_Rec.append((T_Start+"{:2}.".format(hex(T_Size)[2:].zfill(2))+T_Con).upper())
    M_Rec=[]
    M_Address=""
    M_Bytes=""
    i=0
    for  e in objarr:
        if(len(e[1])==8):
            M_Address=hex(int(e[0],16) + 1)[2:].zfill(6)
            M_Bytes=5
            M_Rec.append("M.{:6}.{:2}+{:6}".format(M_Address.zfill(6),hex(M_Bytes)[2:].zfill(2),codearr[0][0]))
        i+=1 
    ER="E."+getFirstExe()
    for element in [HR,*T_Rec,*M_Rec, ER,]:
        #print(element)
        obj.write(element + '\n')
    obj.close()

def getFirstExe():
    for i in locarr:
        if i[2] in insDict:
            return i[0][2:].zfill(6).upper()


def calcAddress(PC,Label):
    Flags="2"#PC by default
    Flags_Disp=""#Calculate PC or Base
    flag=1
    src=int(locarr[PC][0][2:],16)
    dest=""
    if(',X' in Label):#Check for ,X
        Label=Label.rstrip(',X')
        Flags=Flags.replace(Flags,hex(int(Flags,16) + 8)[2:].upper())


    if (Label[0] == "="):#literal addressing
        for i in litarr:#check for label in the literal
            if (Label==i[0]):
                flag=0
                dest=int(i[1][2:],16)


    for i in symbarr:#check for symbol in symbol table first
        if(Label==i[0]):
            dest=int(i[1][2:],16)
            flag=0


    if(flag):#symbol not found
        raise Exception("Label not found in Symbol Table")

    if(codearr[PC-1][1][0] == "+"): #Format 4
        Flags=Flags.replace(Flags,hex(int(Flags,16) -2 + 1)[2:].upper()) #-p +e
        Flags_Disp = Flags + hex(dest)[2:].zfill(5).upper()


    elif(codearr[PC-1][1][0] == "$"): #Mystery 6
        flagsIncrement=-3
        if(dest % 2 != 0):
            flagsIncrement=4
        if(dest != 0):
            flagsIncrement=2
        if(dest != base):
            flagsIncrement=1
        Flags=Flags.replace(Flags,hex(int(Flags,16) + flagsIncrement)[2:].upper()) #+F6
        Flags_Disp = Flags + hex(dest)[2:].zfill(5).upper()


    elif(dest - src <= 2047 and dest - src >= -2048): #PC relative
        if(dest-src <0):
            Flags_Disp=Flags + hex((dest-src) & (2**32-1))[7:].upper()
        else:
            Flags_Disp=Flags + hex(dest-src)[2:].zfill(3).upper()


    elif(dest-base <= 4096): #Base relative
        Flags=Flags.replace(Flags,hex(int(Flags,16) + 4 - 2)[2:].upper())#-2 are the PC relative
        Flags_Disp=Flags + hex(dest-base)[2:].zfill(3).upper()

    else:
        raise Exception("Address is unreachable")

    if(codearr[PC-1][1][0] == "&"): #Mystery 5
        if(Flags_Disp[1:] == "000"):
            Flags_Disp=hex(int(Flags_Disp[0], 16) + 1)[2:] + "000"
    return Flags_Disp

def getAddress(Label):
    for i in symbarr:#check if label exists in the symbolTable
        if (i[0]==Label):
            return i[1][2:]
    if(debug):
        print(Label)
    raise Exception("Label not found in Symbol Table")

def generateLiteral(Literalpool, obj, objarr, PC):
    prevAddress = int(locarr[PC - 1][0][2:], 16)
    currentAddress = prevAddress
    for i in Literalpool:
        if i[1] == None:
            i[1]=""

            if(i[0][1]=="C"):
                for z in i[0][2:]:
                     if(z != "'"):
                        i[1]+=hex(ord(z))[2:].upper()
                        currentAddress += 1


            elif(i[0][1]=="X"):
                counter = 0
                for z in i[0][2:]:
                    if(z != "'"):
                        i[1]+=z
                        counter += 1
                        if(counter % 2 == 0):
                            currentAddress += 1

            else:#normal decimal
                i[1] += hex(int(i[0][1:]))[2:].upper()
            objarr.append(i[1])
            obj.write("-"*50+"\n") # Formatting
            obj.write("{:10}{:20}{:10}{}".format(hex(prevAddress)[2:].zfill(4), i[0], objarr[len(objarr)-1].zfill(2),"\n"))
            prevAddress = currentAddress

def twos_complement(value,hbits):
    bits = hbits * 4
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

import os

if __name__ == "__main__":
    debug = 0
    base = 0
    baseFlag = 1 
    directives = ["START", "END", "BASE", "LTORG", "RESW", "RESB","EXTDEF","EXTREF"] # Array of directives for the read functions

    if not os.path.exists('out'):
        os.makedirs('out')

    codeFile = "in/in.txt"
    instructionFile = "in/in_set.txt"
    symbolTable='out/symbTable.txt'
    locationCounter='out/out.txt'
    literalTable='out/litTable.txt'
    objCodeFile = 'out/objCode.txt'
    objFile = 'out/out.obj'

    ins = open(instructionFile, "r")
    code = open(codeFile,"r")  
    insDict = createInsDict(ins)  
    codearr = readCode(code)    
    ins.close()
    code.close()
    passOne()
    if(debug):
        print("Pass One successfully completed!")

    locctr = open(locationCounter,"r")
    symTable = open(symbolTable,"r")
    litTable = open(literalTable,"r")
    locarr = readLoc(locctr)
    symbarr = readSym(symTable)
    litarr = readSym(litTable)
    symTable.close()
    locctr.close()
    litTable.close()
    passTwo()
    if(debug):
        print("Pass Two successfully completed!")

    print("Assembly Success!")