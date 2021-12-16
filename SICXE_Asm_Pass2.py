#import SICXE_Asm as PassOne
from SICXE_Asm import readFile
def objectCode():
    objectCodeFile=open("Objectout.txt","w")
    Objcode=[];
    for i in codearr:
        for j in insarr:
            if(i[0][0]=="+" or i[0][0]=="$"):
                pass
            if (i[0][1:]==insarr[0]):
                Objcode.append(insarr[2])



def HTE():
    pass


instructionFile = "in_set.txt"
codeFile='in.txt'
symbolTable='symbTable.txt'
ins = open(instructionFile, "r")
code = open(codeFile,"r")
symTable = open(symbolTable,"r")
insarr = []
codearr = []
symbtable=[]
readFile(ins,insarr)
readFile(code,codearr)
readFile(symTable,symbtable)
print(symbtable)
objectCode()