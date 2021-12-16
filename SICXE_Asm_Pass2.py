#import SICXE_Asm as PassOne
from SICXE_Asm import readFile

def objectCode():
    objectCodeFile=open("Objectout.txt","w")
    ObjArr=[]
    Line_Number=0
    for i in codearr:
        Objcode=[]
        if(i[1] == "BASE" or i[1]=="START" or i[1]=="END" or i[1]=="LTORG" or i[1]=="RSUB"):
            Line_Number += 1
            continue
        for j in insarr:
            if(i[1][0]=="+" or i[1][0]=="$"):#Direct Addressing
                pass
            if (i[1]==j[0]):#PC or Base relative #or i[1][0] =="&"
                Objcode=list(j[2])
                if(i[2][0]=="#"):
                    Objcode[1]=hex(int(Objcode[1],16)+1)[2:]
                    pass
                elif(i[2][0]=="@"):
                    Objcode[1]=hex(int(Objcode[1],16)+2)[2:]
                    pass
                elif(i[2][0]=="="):
                    pass
                else:
                    Objcode[1]=hex(int(Objcode[1],16)+3)[2:]
                    pass
                Objcode.append(calcAddress(Line_Number,i[2]))
                if(',X' in i[2]):#"".join(Objcode)
                    temp="".join(Objcode)
                    Objcode = list(temp)
                    Objcode[2]=hex(int(Objcode[2],16)+8)[2:]
                Objcode="".join(Objcode)
        Line_Number += 1
        ObjArr.append(Objcode)
    print(ObjArr)


def HTE():
    pass
 

def calcAddress(Line_Number,Label):
    print(Line_Number)
    if(',X' in Label):
        Label=Label.rstrip(',X')
    if (Label[0] == "="):
        return ""
    flag=1
    base=getBase()
    src=int(locarr[Line_Number + 1][0][2:],16)
    for i in symbarr:
        if(Label==i[0]):
            dest=int(i[1][2:],16)
            flag=0
    if(flag):
        raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
    if(dest - src <= 2047):
        return "2" + hex(dest-src)[2:].zfill(3)
    elif(dest-base <= 4095):
        pass
    pass
def getBase():
    for i in locarr:
        if (i[2]=="BASE"):
            return int(i[0][2:])
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

