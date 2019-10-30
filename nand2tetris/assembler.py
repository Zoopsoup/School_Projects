import sys

input_file = sys.argv[1] # command line input for .asm file to be translated

# dest, comp, and jump are the three components of the C-instruction
dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
} # contains references to memory addresses

# formats all c-instruction as dest;comp;jump
def fix_line(c_instr):
    if '=' not in line:
        c_instr = "null=" + c_instr[:]
    if ';' not in line:
        c_instr = c_instr[:] + ";null"
    return c_instr

# splits c-instruction into a list
def split_line(c_instr):
    code_list = c_instr.replace('=', ';').split(';')
    return code_list

# removes whitespace and comments
def clean_line(line):
    count = 0
    line.strip()
    for char in line:
        if char == '/':
            line = line[:count]
        if char == ' ':
            line = line[:count] + line[count + 1:]
        else:
            count += 1
    return line

# checks if symbol is in symbol_table, adds it to the table if not
memory_counter = 16
def if_symbol(symbol):
    global memory_counter
    if symbol in symbol_table:
        return symbol_table[symbol]
    else:
        symbol_table[symbol] = memory_counter
        memory_counter += 1
        return symbol_table[symbol]

# opens asm. and .hack files, creates new hack file if not found
hack_file = open(input_file, 'r')
asm_file = open(input_file[:len(input_file) - 4] + ".hack", 'w')

# first pass, checks for labels which are added to symbol_table
global line_index
line_index = -1
for line in hack_file:
    line = line.strip()
    line = clean_line(line)
    if line != "":
        line_index += 1
        if line.startswith("("):
            line = line[1:len(line)-1]
            symbol_table[line] = line_index
            line_index -= 1

hack_file.seek(0)

# second pass, translates assembly to binary
for line in hack_file:
    line = line.strip()
    line = clean_line(line)
    if line != "":
        if line[0] != "(":
            if line[0] == '@': # handles A-instruction
                if line[1].isalpha():
                    line = "{}".format(if_symbol(line[1:]))
                else:
                    line = line[1:]
                dec_num = int(line[:])
                bin_num = bin(dec_num)
                bin_num = bin_num[2:]
                asm_file.write(bin_num.zfill(16))
                asm_file.write("\n")
            else: # handles C-instruction
                fixed_line = fix_line(line)
                fixed_list = split_line(fixed_line)
                asm_file.write("111" + comp[fixed_list[1]] +
                               dest[fixed_list[0]] + jump[fixed_list[2]])
                asm_file.write("\n")

hack_file.close()
asm_file.close()
