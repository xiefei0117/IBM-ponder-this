"""
Take input.txt and convert it to data.dat for processing by vaccine.py

example input.txt:
    0a8301b11b01
    1bda41b24d78
    37c09e8d5998
    60473283d3b8
    13279043d9bc
    371bf4c021c1
    1d122e800ee1
    5bc967265d88
    5f1998f5915d
    628dff094034
    39effbe6ecc8
    2c440c20e0a0
"""

text_file = open("input.txt", "r")
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

outF = open("data_file.dat", "w")
outF.write('param m := ' + str(rows) + ";\n")
outF.write('param n := ' + str(cols) + ";\n")
outF.write('param t_length := ' + str(rows*cols) + ";\n")
outF.write('set K := N E S W;\n')
outF.write('param D := \n')

direction_dict = {
        0: 'N',
        1: 'E',
        2: 'S',
        3: 'W'
        }

for i in range(0, rows):
    for j in range(0, cols):
        for m in range(0, 4):
            outF.write(str(i + 1) + " " + str(j + 1) + " " + direction_dict[m] + " " + A_binary[i][j][m] + "\n")
outF.write(";\n")





outF.close()