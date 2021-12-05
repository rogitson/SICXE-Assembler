# import sys, getopt

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
        if(line[0] == '.'):
            continue
        line=format(line)
        col=line.split(" ")
        if(len(col) == 1):
            continue
        elif(len(col) == 2):
            col[1] = col[1].rstrip("\n")
            col.append('')
        else:
            col[2] = col[2].rstrip("\n")
        Array.append(col)
def passOne():
    if(codearr[0][1].upper() != "START"):
        raise Exception("A very unspecific bad thing happened, but I won't tell you what it is.") 
    locFile=open("out.txt","w")
    litable = open("litTable.txt", "w")
    lit = []
    start_address=int(codearr[0][2], 16)
    current_address=hex(start_address)
    for i in codearr:
        #Out.write("{:<8}{:<6}".format(hex(Loc),line))
        locFile.write("{:<8}{:<8}{:8}{:8}{}".format(current_address,i[0],i[1],i[2],'\n'))
        # print(current_address,"\t\t",i[1])
        steps = 0
        if(i[1] == "LTORG" or i[1] == "END"):
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
                    litable.write(e[0] + "\t" + e[1] + "\n")
            continue
        elif(i[1] == "BASE"):
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
        for j in insarr:
            if(i[1]==j[0]):
                if(i[1] == "RSUB"):
                    if(i[2] != ''):
                        raise Exception("A very specific bad thing happened, but I won't tell you what it is.")
                if(j[1]=="1"):
                    steps += 1
                elif(j[1]=="2"):
                    steps += 2
                elif(j[1]=="34"):
                    steps += 3
        if(i[2] != '' and i[2][0] == "="):
            flag = True
            for e in lit:
                if(i[2] == e[0]):
                    flag = False
            if(flag):
                lit.append([i[2],''])
        current_address = hex(int(current_address,16) + steps)
    locFile.close()
    litable.close()
    symbol_table()
def symbol_table():
    counter=0
    symbFile=open("symbTable.txt","w")
    locFile=open("out.txt","r")
    Counter_Array= []
    for i in locFile:
        row=i.split(' ')
        Counter_Array.append(row[0])
    for i in codearr:
        if(i[0]!=""):
            symbFile.write("{:10}{:10}{}".format(i[0],Counter_Array[counter],'\n'))
        counter += 1
    symbFile.close()
    locFile.close()

# def main(argv):
#     try:
#         opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#     except getopt.GetoptError:
#         print ('test.py -i <inputfile> -o <outputfile>')
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt in ('-h', "--help"):
#             print("-h, --help\t-\tprint the help message\n" +
#             "-i, --input\t-\tinput file\n" +
#             "-s, --set\t-\tinstruction set file\n" +
#             "-o, --output\t-\toutput file")
#             sys.exit()
#         elif opt in ("-i", "--input"):
#             inputfile = arg
#         elif opt in ("-s", "--set"):
#             instructionFile = arg
#         elif opt in ("-o", "--output"):
#             outputfile = arg

if __name__ == "__main__":
    inputFile = "in.txt"
    instructionFile = "in_set.txt"
    # inputFile = ''
    # instructionFile = ''
    # main(sys.argv[1:])

    code = open(inputFile, "r")
    ins = open(instructionFile, "r")
    codearr = []
    insarr = []
            
    readFile(code,codearr)
    readFile(ins,insarr)

    passOne()
    print("Success!")
    code.close()
    ins.close()

def hex_to_decimal(number):
    number=int(hex(number).split('x')[-1])
    print(number)
#hex_to_decimal(4096)
