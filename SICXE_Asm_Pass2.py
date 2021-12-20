#import SICXE_Asm as PassOne
from os import replace
from SICXE_Asm import readFile

def objectCode():
    objectCodeFile=open("Objectout.txt","w")
    global base
    Formats=["$","+","&"]
    AddressingTypes=["#","@","="]
    Literal_Pool=[]
    Registers = {"A":"0","X":"1","L":"2","B":"3","S":"4","T":"5","F":"6"}
    opCode=""
    Flags_Disp_Add=""
    Format_Flag=1
    Line_Number=0
    for i in codearr:#Make Condition for EQU
        print(i)
        Flags_Disp_Add=""
        opCode=""
        if (i[1]=="START" or i[1]=="EQU"):#No object Code
            Line_Number+=1
            continue
        if(i[1]=="BASE"):#record base label address
            Line_Number+=1
            base=getBase(i[2])#sending the label infornt of base to get its address
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
            for j in insarr:
                if(instruction==j[0]):#Doesn't need Stripping
                    opCode=j[2]#any(AddressingTypes in i[2] for AddressingTypes in i[1])
                    Flags_Disp_Add=""
                    if (Format_Flag):#then we are format 3 or lower we check for addressing type now
                        if(any(not c.isalnum() for c in i[2]) and not (',' in i[2])):#we got special type , format 2 or up since format 1 have 0 operands
                            if(i[2][0]=="#"):
                                opCode=hex(int(opCode,16)+1)[2:].upper()
                                if(i[2][1].isdigit()):#check if its constant
                                    Flags_Disp_Add=hex(int(i[2][1:]))[2:].zfill(4)
                                else:#address
                                    Flags_Disp_Add=calcAddress(Line_Number,Label)
                                break
                            elif(i[2][0]=="@"):
                                opCode=hex(int(opCode,16)+2)[2:]
                                Flags_Disp_Add=calcAddress(Line_Number,Label)
                                break
                            elif(i[2][0]=="="):#literal , store it in the array
                                if(not Literal_Pool):
                                    Literal_Pool.append([i[2],None])
                                elif(not i[2] in Literal_Pool[0]):
                                    Literal_Pool.append([i[2],None])
                                Flags_Disp_Add=calcAddress(Line_Number,i[2])
                                continue
                                #break
                        else:#simple addressing and format 1,2 handling
                            if(j[1]=="1" or j[1]=="2"):
                                opCode=j[2]# format 2 needs handling
                                if(j[1]=="2"):
                                    sl=i[2].split(',')
                                    if(len(sl)==1):
                                        sl[1]="A"
                                    Flags_Disp_Add+=Registers[sl[0]] + Registers[sl[1]]
                                #ObjArr.append(opCode+Flags_Disp_Add)
                            elif(j[1]=="34"):#format 3
                                opCode=hex(int(opCode,16)+3)[2:].zfill(2).upper()
                                Flags_Disp_Add=calcAddress(Line_Number,Label)
                            break
                    else:#format 4 or special one
                        if(i[1][0] == "+" or i[1][0] == "$"):
                            opCode=hex(int(opCode,16)+3)[2:].zfill(2).upper() #This needs to go
                        Flags_Disp_Add=calcAddress(Line_Number,Label)
                        if(i[1][0] == "&"):
                            if(int(Flags_Disp_Add[1:], 16) % 2 == 0):
                                opCode=hex(int(opCode,16)+2)[2:].zfill(2).upper() #This needs to go
                            if(twos_complement(int(Flags_Disp_Add[1:], 16), 3) < 0):
                                opCode=hex(int(opCode,16)+1)[2:].zfill(2).upper() #This needs to go
                elif(Line_Number==codearr.__len__() and instruction!=j[0]):#doesn't exist
                    raise Exception("Instruction Not Found")
            ObjArr.append(opCode+Flags_Disp_Add)
    #ObjArr.remove('') no need it was for =13 literal
    print(ObjArr)

def HTE():
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
    elif(dest - src <= 2047): #PC relative
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


def getBase(Label):
    for i in symbarr:#check if label exists in the symbolTable
        if (i[0]==Label):
            return i[1][2:]


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

if __name__ == "__main__":
    instructionFile = "in_set.txt"
    codeFile='in.txt'
    symbolTable='symbTable.txt'
    locationCounter='out.txt'
    literalTable='litTable.txt'
    ins = open(instructionFile, "r")
    code = open(codeFile,"r")
    symTable = open(symbolTable,"r")
    locctr=open(locationCounter,"r")
    litTable=open(literalTable,"r")
    insarr = []
    codearr = []
    symbarr=[]
    locarr=[]
    litarr=[]
    base=""
    ObjArr=[]
    readFile(ins,insarr)
    readFile(code,codearr)
    readFile(symTable,symbarr)
    readFile(locctr,locarr)
    readFile(litTable,litarr)
    print(litarr)
    objectCode()

