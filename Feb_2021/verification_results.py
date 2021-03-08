import copy

text_file = open("input_42.txt", "r")
lines = text_file.read().splitlines()
text_file.close()

hex_to_binary = {
        '0':'0000',
        '1':'0001',
        '2':'0010',
        '3':'0011',
        '4':'0100',
        '5':'0101',
        '6':'0110',
        '7':'0111',
        '8':'1000',
        '9':'1001',
        'a':'1010',
        'b':'1011',
        'c':'1100',
        'd':'1101',
        'e':'1110',
        'f':'1111'
            }

rows = len(lines)
cols = len(lines[0])

A_binary = []
for i in range(0, rows):
    new = []
    for j in range(0, cols):
        new.append(hex_to_binary[lines[i][j]])
        print(str(i) + "," + str(j) + ": " + lines[i][j] + " to " + hex_to_binary[lines[i][j]])
    A_binary.append(new)



text_file = open("solutions.txt", "r")
lines = text_file.read().splitlines()
text_file.close()

transition_lines = []
for i in range(0, rows):
    new = []
    for j in range(0, cols):
        new.append(int(lines[i][j]))
    transition_lines.append(new)

for step in range(0,20):
    print(step)
    for i in range(0, rows):
        temp = ""
        for j in range(0, cols):
            temp = temp + str(transition_lines[i][j])
        print(temp)
    lines_copy = copy.deepcopy(transition_lines)
    for i in range(0, rows):
        for j in range(0, cols):
            if i == 0 and j == 4:
                print(temp)
            if transition_lines[i][j] == 0:
                temp = True
                if int(A_binary[i][j][0]) == 1 and i - 1 >= 0:
                    if transition_lines[i - 1][j] == 0:
                        temp = False
                if int(A_binary[i][j][1]) == 1 and j + 1 < cols:
                    if transition_lines[i][j+1] == 0:
                        temp = False
                if int(A_binary[i][j][2]) == 1 and i + 1 < rows:
                    if transition_lines[i+1][j] == 0:
                        temp = False
                if int(A_binary[i][j][3]) == 1 and j - 1 >= 0:
                    if transition_lines[i][j-1] == 0:
                        temp = False
                if temp == True:
                    lines_copy[i][j] = 1
                    
    transition_lines = copy.deepcopy(lines_copy)

transition_lines = []
for i in range(0, rows):
    new = []
    for j in range(0, cols):
        new.append(int(lines[i][j]))
    transition_lines.append(new)
    
outF = open("output.txt", "w")
outF.write("[")
for i in range(0, rows):
    for j in range(0, cols):
        if transition_lines[i][j] == 1:
            outF.write("(" + str(j + 1) + "," + str(rows - i) + "),")
outF.write("]")
outF.close()