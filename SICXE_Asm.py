code = open("Input.txt", "r")
ins = open("Instruction_Set.txt", "r")

codearr = []
insarr = []
for line in code:
    col = line.split("^")
    col[0] = col[0].strip(" ")
    col[1] = col[1].strip(" ")
    col[2] = col[2].rstrip("\n")
    codearr.append(col)
for line in ins:
    col = line.split(" ")
    col[2] = col[2].rstrip("\n")
    insarr.append(col)
for e in codearr:
    for i in insarr:
        if(e[1] == i[0]):
            print(i[2], "\n")

print(codearr, "\n", insarr)