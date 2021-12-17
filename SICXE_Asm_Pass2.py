#import SICXE_Asm as PassOne
from SICXE_Asm import readFile

# def objectCode():
    # objectCodeFile=open("Objectout.txt","w")
    # ObjArr=[]
    # Line_Number=0
    # print(codearr[16][0][0])
    # for i in codearr:
    #     Objcode=[]
    #     if(i[1] == "BASE" or i[1]=="START" or i[1]=="END" or i[1]=="LTORG"):
    #         Line_Number += 1
    #         continue
    #     for j in insarr:
    #         if(i[1][0]=="+" or i[1][0]=="$"):#Direct Addressing
    #             pass
    #         if (i[1]==j[0]):#PC or Base relative #or i[1][0] =="&"
    #             Objcode=list(j[2])
    #             if(i[2][0]=="#"):
    #                 Objcode[1]=hex(int(Objcode[1],16)+1)[2:]
    #                 pass
    #             elif(i[2][0]=="@"):
    #                 Objcode[1]=hex(int(Objcode[1],16)+2)[2:]
    #                 pass
    #             elif(i[2][0]=="="):
    #                 pass
    #             else:
    #                 Objcode[1]=hex(int(Objcode[1],16)+3)[2:]
    #                 pass
    #             Objcode.append(calcAddress(Line_Number,i[2]))
    #             if(',X' in i[2]):#"".join(Objcode)
    #                 temp="".join(Objcode)
    #                 Objcode = list(temp)
    #                 Objcode[2]=hex(int(Objcode[2],16)+8)[2:]
    #             Objcode="".join(Objcode)
    #     Line_Number += 1
    #     ObjArr.append(Objcode)
    # print(ObjArr)
def objectCode():
    objectCodeFile=open("Objectout.txt","w")
    ObjArr=[]
    Formats=["$","+","&"]
    AddressingTypes=["#","@","="]
    Literal_Pool=[]
    opCode=""
    Flags_Disp_Add=""
    Format_Flag=1
    Line_Number=0
    for i in codearr:#Make Condition for EQU
        if (i[1]=="START" or i[1]=="END" or i[1]=="EQU"):#No object Code
            Line_Number+=1
            continue
        if(i[1]=="BASE"):#record base label address
            Line_Number+=1
            base=getBase(i[2])#sending the label infornt of base to get its address
        elif(i[1]=="LTORG" or i[1]=="END"):#generate pool Tabel
            Line_Number+=1
        elif(i[1]=="RSUB"):
            Line_Number+=1
            ObjArr.append("4F0000")
        elif(i[1]=="WORD"):
            Line_Number+=1
            ObjArr.append(hex((int(i[2])& (2**32-1)))[2:].zfill(6))
        elif(i[1]=="BYTE"):
            Line_Number+=1
            #needs the EOF CODE AGAIN , I HATE MY LIFE
            #ObjArr.append()
            #print(hex(int(i[2])&(2**32-1)))
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
                    #get the opcode and handel it first.
                    opCode=j[2]#any(AddressingTypes in i[2] for AddressingTypes in i[1])
                    Flags_Disp_Add=""
                    if (Format_Flag):#then we are format 3 or lower we check for addressing type now
                        if(any(not c.isalnum() for c in i[2])):#we got special type , format 2 or up since format 1 have 0 operands
                            if(i[2][0]=="#"):
                                opCode=hex(int(opCode,16)+1)[2:]
                                Flags_Disp_Add=calcAddress(Line_Number,Label)
                                break
                            elif(i[2][0]=="@"):
                                opCode=hex(int(opCode,16)+2)[2:]
                                Flags_Disp_Add=calcAddress(Line_Number,Label)
                                break
                            elif(i[2][0]=="="):#literal , store it in the array
                                Literal_Pool.append(i)
                                break
                        else:#simple addressing and format 1,2 handling
                            if(j[1]=="1" or j[1]=="2"):
                                opCode=j[2]# format 2 needs handling
                            elif(j[1]=="34"):#format 3
                                opCode=hex(int(opCode,16)+3)[2:].zfill(2)
                                Flags_Disp_Add=calcAddress(Line_Number,Label)#needs adjusting for normal addressing
                                print(Line_Number)
                                print(opCode,Flags_Disp_Add)
                            break
                    else:#format 4 or special one
                        pass
                    # if(any(Formats in i[1] for Formats in i[1])):#check for the type of format
                    #     pass#format4 or mystery format

                    # else:#format 3 or lower
                    #     pass
                elif(Line_Number==codearr.__len__() and instruction!=j[0]):#doesn't exist
                    raise Exception("Instruction Not Found")
                #  if(Formats in i[1]):#we are using special format or format 4
                #      if(i[1][0]=="+"):#format 4 Direct Addresing
           # print(i[1])
        sstring=opCode+Flags_Disp_Add
        print(sstring)
    print(ObjArr)


def HTE():
    pass

def calcAddress(Line_Number,Label):
    if(',X' in Label):
        Label=Label.rstrip(',X')
        Index=8
    if (Label[0] == "="):
        return ""
    flag=1
    base=getBase(Label)
    src=int(locarr[Line_Number ][0][2:],16)
    for i in symbarr:
        if(Label==i[0]):
            dest=int(i[1][2:],16)
            flag=0
    if(flag):
        raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
    if(dest - src <= 2047):
        if(dest-src <0):
            return "2" + hex((dest-src) & (2**32-1))[7:]
        else:
            return "2" + hex(dest-src)[2:].zfill(3)#something is not right with LDL instruciton for address calculating
    elif(dest-base <= 4095):
        print("OutOfBounds")
        pass
    pass
def getBase(Label):
    for i in symbarr:
        if (i[0]==Label):
            return i[1][2:]
instructionFile = "in_set.txt"
codeFile='in.txt'
symbolTable='symbTable.txt'
locationCounter='out.txt'
ins = open(instructionFile, "r")
code = open(codeFile,"r")
symTable = open(symbolTable,"r")
locctr=open(locationCounter,"r")
insarr = []
codearr = []
symbarr=[]
locarr=[]
readFile(ins,insarr)
readFile(code,codearr)
readFile(symTable,symbarr)
readFile(locctr,locarr)
objectCode()

