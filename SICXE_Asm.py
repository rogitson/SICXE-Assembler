#For formatting the strings
def format(str):
    str2=""
    for i in range(len(str)):
        if(str[i]==" "and str[i+1]==" "):
            continue
        else:
            str2+=str[i]
    return str2
# For Reading the files , Instructions and Code Input reading
def readFile(File,Array):
    for line in File:
        line=format(line)
        col=line.split(" ")
        col[2]=col[2].rstrip("\n")
        Array.append(col)
def passOne():
    locFile=open("out.txt","w")
    litable = open("litTable.txt", "w")
    lit = []
    start_address=int(codearr[0][2], 16)
    start_address=hex(start_address) 
    for i in codearr:
        locFile.write(start_address + '\n')
        print(start_address,"\t\t",i[1])
        if(i[1] == "LTORG" or i[1] == "END"):
            for e in lit:
                if(e[1] == ''):
                    e[1] = start_address
                    if(e[0][1]=="C"):
                        for z in e[0][2:]:
                            if(z != "'"):
                                start_address = hex(int(start_address,16) + 1)
                    else:
                        start_address = hex(int(start_address,16) + 1)  
                    litable.write(e[0] + "\t" + e[1] + "\n")   
        elif(i[1][0] == "+"):
            start_address = hex(int(start_address,16) + 4)
        elif(i[1][0] == "&"):
            start_address = hex(int(start_address,16) + 3)
        elif(i[1][0] == "$"):
            start_address = hex(int(start_address,16) + 4)
        elif(i[1]=="WORD"):
            data = i[2].split(",")
            for j in data:
                start_address = hex(int(start_address,16) + 3)
        elif(i[1]=="BYTE"):
            data = i[2].split(",")
            for j in data:
                if(j[0]=="C"):
                    for z in j[1:]:
                        if(z != "'"):
                            start_address = hex(int(start_address,16) + 1)
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
        for j in insarr:
            if(i[1]==j[0]):
                if(i[1] == "RSUB"):
                    if(i[2] != ''):
                        raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
                if(j[1]=="1"):
                    start_address = hex(int(start_address,16) + 1)
                elif(j[1]=="2"):
                    start_address = hex(int(start_address,16) + 2)
                elif(j[1]=="34"):
                    start_address = hex(int(start_address,16) + 3)
        if(i[2] != '' and i[2][0] == "="):
            flag = True
            for e in lit:
                if(i[2] == e[0]):
                    flag = False
            if(flag):
                lit.append([i[2],''])
    locFile.close()
    litable.close()
    symbol_table()
def symbol_table():
    counter=0
    symbFile=open("symbTable.txt","w")
    locFile=open("out.txt","r")
    Counter_Array= []
    for i in locFile:
        Counter_Array.append(i)
    for i in codearr:
        if(i[0]!=""):
            symbFile.write(i[0]+"\t"+Counter_Array[counter])
        counter += 1
    symbFile.close()
    locFile.close()

code = open("in.txt", "r")
ins = open("Instruction_Set.txt", "r")
codearr = []
insarr = []
        
readFile(code,codearr)   
readFile(ins,insarr)

passOne()

code.close()
ins.close()

def hex_to_decimal(number):
    number=int(hex(number).split('x')[-1])
    print(number)
#hex_to_decimal(4096)
