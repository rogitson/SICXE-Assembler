#For formatting the strings
def format(str):
    str2=""
    for i in range(len(str)):
        if(str[i]==" "and str[i+1]==" "):
            continue
        else:
            str2+=str[i]
    return str2

def passOne():
    global base
    global baseFlag
    #checking for START 
    if(codearr[0][1].upper() != "START"):
        raise Exception("A very unspecific bad thing happened, but I won't tell you what it is.") 
    #Creating the files for pass 1
    locFile=open("out.txt","w")
    litable = open("litTable.txt", "w")
    symbFile=open("symbTable.txt","w")
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
                raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
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
    locFile.close()
    litable.close()
    symbFile.close()

def passTwo():
    objectCodeFile=open("Objectout.txt","w")
    global base, baseFlag
    if(baseFlag):
        base = int(getAddress(base), 16)
    Formats=["$","+","&"]
    AddressingTypes=["#","@","="]
    Literal_Pool=[]
    Registers = {"A":"0","X":"1","L":"2","B":"3","S":"4","T":"5","F":"6"}
    opCode=""
    Flags_Disp_Add=""
    Format_Flag=1
    Line_Number=0
    for i in codearr:#Make Condition for EQU
        if(debug):
            print(i)
        Flags_Disp_Add=""
        opCode=""
        if (i[1]=="START" or i[1]=="EQU" or i[1] == "BASE"):#No object Code
            Line_Number+=1
            continue
        elif(i[1]=="LTORG" or i[1]=="END"):#generate pool Tabel
            Line_Number+=1
            generateLiteral(Literal_Pool,ObjArr)
        elif(i[1]=="RSUB"):
            Line_Number+=1
            ObjArr.append("4F0000")
        elif(i[1]=="WORD"):
            Line_Number+=1
            ObjArr.append(hex((int(i[2])& (2**32-1)))[4:].zfill(6).upper())
        elif(i[1]=="BYTE"):
            Line_Number+=1
            data = i[2].split(",")
            j=data[0]
            if(j[0]=="C"):
                for z in j[1:]:
                    if(z != "'"):
                        Flags_Disp_Add+=hex(ord(z))[2:].upper()
            elif(j[0]=="X"):
                for z in j[1:]:
                    if(z != "'"):
                        Flags_Disp_Add+=z
            ObjArr.append(Flags_Disp_Add.upper())
        elif(i[1]=="RESW" or i[1]=="RESB"):
            Line_Number+=1
            continue
        else:
            Line_Number+=1
            #check for instruction first
            Format_Flag=1
            instruction=i[1]
            if(any(not c.isalnum() for c in instruction)):#stripping the special type to get the instruction
                instruction=instruction.translate({ord(x):'' for x in Formats})
                Format_Flag=0
            Label=i[2].translate({ord(x):'' for x in AddressingTypes})
            j = insDict[instruction]
            # for j in insarr:
            #     if(instruction==j[0]):#Doesn't need Stripping
            opCode=j[1]#any(AddressingTypes in i[2] for AddressingTypes in i[1])
            Flags_Disp_Add=""
            if(i[2][0]=="#"):
                opCode=hex(int(opCode,16)+1)[2:].zfill(2).upper()
            elif(i[2][0]=="@"):
                opCode=hex(int(opCode,16)+2)[2:].zfill(2).upper()
            else:
                opCode=hex(int(opCode,16)+3)[2:].zfill(2).upper()
            if(i[2][0]=="="):#literal , store it in the array
                if(not Literal_Pool):
                    Literal_Pool.append([i[2],None])
                elif(not i[2] in Literal_Pool[0]):
                    Literal_Pool.append([i[2],None])
                print(i[2])
                Flags_Disp_Add=calcAddress(Line_Number,i[2])
            elif(i[2][0]=="#" and i[2][1].isdigit()):#check if its constant
                Flags_Disp_Add=hex(int(i[2][1:]))[2:].zfill(4) #This needs to gooooooo
            elif(Format_Flag):#then we are format 3 or lower we check for addressing type now
                if(j[0]=="1" or j[0]=="2"):
                    opCode=j[1]# format 2 needs handling
                    if(j[0]=="2"):
                        sl=i[2].split(',')
                        if(len(sl)==1):
                            sl.append("A")
                        Flags_Disp_Add+=Registers[sl[0]] + Registers[sl[1]]
                    #ObjArr.append(opCode+Flags_Disp_Add)
                elif(j[0]=="34"):#format 3
                    Flags_Disp_Add=calcAddress(Line_Number,Label)
            else:#format 4 or special one
                Flags_Disp_Add=calcAddress(Line_Number,Label)
                if(i[1][0] == "&"):
                    if(int(Flags_Disp_Add[1:], 16) % 2 == 0):
                        opCode=hex(int(opCode,16)+2)[2:].zfill(2).upper() #This needs to go
                    if(twos_complement(int(Flags_Disp_Add[1:], 16), 3) < 0):
                        opCode=hex(int(opCode,16)+1)[2:].zfill(2).upper() #This needs to go
                # elif(Line_Number==codearr.__len__() and instruction!=j[0]):#doesn't exist
                #     raise Exception("Instruction Not Found")
            ObjArr.append(opCode+Flags_Disp_Add)
    #ObjArr.remove('') no need it was for =13 literal
    print(ObjArr)

def HTE():
    HR="H."+ codearr[0][2].zfill(6).upper() + "." + locarr[len(locarr) - 1][0][2:].zfill(6).upper()
    ER="E."+ codearr[0][2].zfill(6).upper()
    pass

def calcAddress(Line_Number,Label):
    Flags="2"#PC by default
    Flags_Disp=""#Calculate PC or Base
    flag=1
    src=int(locarr[Line_Number][0][2:],16)
    dest=""
    if(',X' in Label):#Check for ,X
        Label=Label.rstrip(',X')
        Flags=Flags.replace(Flags,hex(int(Flags,16) + 8)[2:].upper())
    if (Label[0] == "="):#literal addressing
        for i in litarr:#check for label in the literal
            if (Label==i[0]):
                flag=0
                dest=int(i[1][2:],16)
    # elif (Label[0] in ["#","@","="]):
    #     Label = Label[1:]
    for i in symbarr:#check for symbol in symbol table first
        if(Label==i[0]):
            dest=int(i[1][2:],16)
            flag=0
    if(flag):#symbol not found
        raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
    if(codearr[Line_Number-1][1][0] == "+"): #Format 4
        Flags=Flags.replace(Flags,hex(int(Flags,16) -2 + 1)[2:].upper()) #-p +e
        Flags_Disp = Flags + hex(dest)[2:].zfill(5).upper()
    elif(codearr[Line_Number-1][1][0] == "$"): #Mystery 6
        Flags=Flags.replace(Flags,hex(int(Flags,16) - 2)[2:].upper()) #-p
        if(dest % 2 != 0):
            Flags=Flags.replace(Flags,hex(int(Flags,16) + 4)[2:].upper()) #+F4
        if(dest != 0):
            Flags=Flags.replace(Flags,hex(int(Flags,16) + 2)[2:].upper()) #+F5
        if(dest != base):
            Flags=Flags.replace(Flags,hex(int(Flags,16) + 1)[2:].upper()) #+F6
        Flags_Disp = Flags + hex(dest)[2:].zfill(5).upper()
    elif(dest - src <= 2047 and dest - src >= -2047): #PC relative
        if(dest-src <0):
            Flags_Disp=Flags + hex((dest-src) & (2**32-1))[7:].upper()
        else:
            Flags_Disp=Flags + hex(dest-src)[2:].zfill(3).upper()
    elif(dest-base <= 4095): #Base relative
        Flags=Flags.replace(Flags,hex(int(Flags,16) + 4 - 2)[2:].upper())#-2 are the PC relative
        Flags_Disp=Flags + hex(dest-base)[2:].zfill(3).upper()
    else:
        raise Exception("invalid address , unreachable")
    if(codearr[Line_Number-1][1][0] == "&"): #Mystery 5
        if(Flags_Disp[1:] == "000"):
            Flags_Disp=hex(int(Flags_Disp[0], 16) + 1)[2:] + "000"
    return Flags_Disp

def getAddress(Label):
    for i in symbarr:#check if label exists in the symbolTable
        if (i[0]==Label):
            return i[1][2:]
    raise Exception("Label not found in Symbol Table")

def generateLiteral(Literalpool,Objarr):
    for i in Literalpool:
        if i[1] == None:
            i[1]=""
            if(i[0][1]=="C"):
                for z in i[0][2:]:
                     if(z != "'"):
                        i[1]+=hex(ord(z))[2:].upper()
            elif(i[0][1]=="X"):
                 for z in i[0][2:]:
                     if(z != "'"):
                        i[1]+=z
            ObjArr.append(i[1])

def twos_complement(value,hbits):
    bits = hbits * 4
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def createInsDict(File, Dict):
    for line in File:
        instruction = line.split()
        Dict[instruction[0]] = [instruction[1], instruction[2]]

# For reading the input code
def readCode(File,Array):
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

# For reading the symbol table and literal table
def readSym(File,Array):
    for line in File:
        if(line[0] == '.'):
            continue
        col = line.split()
        col[1] = col[1].rstrip("\n")
        Array.append(col)

# For reading the location counter
def readLoc(File,Array):
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

if __name__ == "__main__":
    debug = 1
    base = 0
    baseFlag = 1 
    directives = ["START", "END", "BASE", "LTORG", "RESW", "RESB"]

    codeFile = "in.txt"
    instructionFile = "in_set.txt"
    symbolTable='symbTable.txt'
    locationCounter='out.txt'
    literalTable='litTable.txt'

    ins = open(instructionFile, "r")
    code = open(codeFile,"r")  
    insDict = {}  
    codearr = []
    createInsDict(ins, insDict)       
    readCode(code,codearr)
    ins.close()
    code.close()
    passOne()
    if(debug):
        print("Pass One successfully completed!")

    ObjArr=[]
    locctr=open(locationCounter,"r")
    symTable = open(symbolTable,"r")
    litTable=open(literalTable,"r")
    locarr=[]
    symbarr=[]
    litarr=[]
    readLoc(locctr,locarr)
    readSym(symTable,symbarr)
    readSym(litTable,litarr)
    symTable.close()
    locctr.close()
    litTable.close()
    passTwo()
    if(debug):
        print("Pass Two successfully completed!")

    print("Assembly Success!")