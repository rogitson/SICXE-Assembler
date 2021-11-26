from os import replace
import string as str
code = open("Input.txt", "r")
ins = open("Instruction_Set.txt", "r")
codearr = []
insarr = []
#For formatting the strings
def format(str):
    str2=""
    for i in range(len(str)):
        if(str[i]==" "and str[i+1]==" "):
            continue
        else:
            str2+=str[i]
    return str2
#For Reading the files , Instructions and Code Input reading
def readFile(File,Array):
    for line in File:
        line=format(line)
        col=line.split(" ")
        col[2]=col[2].rstrip("\n")
        Array.append(col)

        
readFile(code,codearr)   
readFile(ins,insarr)


def location_counter():
    Locctr=open("Locctr.txt","w")
    start_address=int(codearr[0][2], 16)
    start_address=hex(start_address) 
    temp=start_address
    for i in codearr:
        Locctr.write(start_address + '\n')
        print(start_address,"\t\t",i[1])
        for j in insarr:
            if(i[1]==j[0]):
                if(j[1]=="1"):
                    start_address = hex(int(start_address,16) + 1)
                elif(j[1]=="2"):
                    start_address = hex(int(start_address,16) + 2)
                elif(j[1]=="34"):
                    if(i[1][0]=="+"):
                        start_address = hex(int(start_address,16) + 4)
                    else:
                        start_address = hex(int(start_address,16) + 3)
        if(i[1]=="WORD"):
            start_address = hex(int(start_address,16) + 3)
        elif(i[1]=="BYTE"):
            if(i[2][0]=="C"):
                for z in i[2][1:]:
                    if(z=="'"):
                        start_address = hex(int(start_address,16) + 0)
                    else:
                        start_address = hex(int(start_address,16) + 1)
        elif(i[1]=="RESW"):
            value = hex(int(i[2]))
            value = value[2:]
            start_address = hex(int(start_address,16) + int(value,16) * 3)
        elif(i[1]=="RESB"):
            value = hex(int(i[2]))
            value = value[2:]
            start_address = hex(int(start_address,16) + int(value,16))
        print(start_address)

location_counter()



def symbol_table():
    counter=0
    symbol_tablefile=open("Symbol_Table.txt","w")
    Locctr=open("Locctr.txt","r")
    Counter_Array= []
    for i in Locctr:
        Counter_Array.append(i)
    for i in codearr:
        if(i[0]!=""):
            symbol_tablefile.write(i[0]+"\t"+Counter_Array[counter])
        counter=counter+1
symbol_table()



def hex_to_decimal(number):
    number=int(hex(number).split('x')[-1])
    print(number)
#hex_to_decimal(4096)


