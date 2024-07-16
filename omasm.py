import sys

bytecode = bytearray()

regs = ["r0", "r1", "r2", "r3", "taa", "tba", "tca", "dao", "dbo", "dco", "ddo"]
variables = []

OP_PUSH = 1
OP_POP = 2
OP_SUM = 3
OP_SUB = 4
OP_SYSCALL = 5
OP_PUSHSTR = 6
OP_PUSHREG = 7
OP_GET = 8
OP_LABEL = 9
OP_JMP = 10
OP_INTSET = 11
OP_PUSHVAR = 12
OP_RET = 13
OP_CALL = 14
OP_CMP = 15
OP_JE = 16
OP_JNE = 17
OP_JL = 18
OP_JG = 19
OP_JLE = 20
OP_JGE = 21
OP_REGSET = 22

def compiler(code):
    lines = code.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        i += 1
        parts = line.split()
    
        if parts:
            if parts[0] == "ipush":
                value = int(parts[1])
                bytecode.append(OP_PUSH)
                bytecode.append(value)
            elif parts[0] == "pop":
                reg = parts[1]
                if reg in regs:
                    bytecode.append(OP_POP)
                    bytecode.append(len(reg))
                    bytecode.extend(reg.encode("utf-8"))
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif parts[0] == "sum":
                bytecode.append(OP_SUM)
            elif parts[0] == "sub":
                bytecode.append(OP_SUB)
            elif parts[0] == "syscall":
                bytecode.append(OP_SYSCALL)
            elif parts[0] == "spush":
                bytecode.append(OP_PUSHSTR)
                bytecode.append(len(" ".join(parts[1:]).replace("\\n", "\n").replace("\\s", " ")))
                bytecode.extend(" ".join(parts[1:]).replace("\\n", "\n").replace("\\s", " ").encode("utf-8"))
            elif parts[0] == "rpush":
                reg = parts[1]
                if reg in regs:
                    bytecode.append(OP_PUSHREG)
                    bytecode.append(len(reg))
                    bytecode.extend(reg.encode("utf-8"))
            elif parts[0] == "get":
                reg = parts[1]
                if reg in regs:
                    bytecode.append(OP_GET)
                    bytecode.append(len(reg))
                    bytecode.extend(reg.encode("utf-8"))
            elif parts[0].endswith(":"):
                labelname = parts[0].split(":")[0].strip()
                bytecode.append(OP_LABEL)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jmp":
                labelname = parts[1]
                bytecode.append(OP_JMP)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "lend":
                bytecode.append(ord("l"))
                bytecode.append(ord("e"))
                bytecode.append(ord("n"))
                bytecode.append(ord("d"))
            elif parts[0] == "iset":
                name = parts[1].replace(",","")
                value = parts[2]
                variables.append(name)
                bytecode.append(OP_INTSET)
                bytecode.append(len(name))
                bytecode.extend(name.encode("utf-8"))
                bytecode.extend(int(value).to_bytes(4, byteorder='big', signed=False))
            elif parts[0] == "vpush":
                name = parts[1]
                if name in variables:
                    bytecode.append(OP_PUSHVAR)
                    bytecode.append(len(name))
                    bytecode.extend(name.encode("utf-8"))
                else:
                    print(f"Error: unknown variable -> {name}")
                    sys.exit(1)
            elif parts[0] == "ret":
                bytecode.append(OP_RET)
            elif parts[0] == "call":
                labelname = parts[1]
                bytecode.append(OP_CALL)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "cmp":
                reg1 = parts[1].replace(",", "")
                reg2 = parts[2]
                bytecode.append(OP_CMP)
                bytecode.append(len(reg1))
                bytecode.extend(reg1.encode("utf-8"))
                bytecode.append(len(reg2))
                bytecode.extend(reg2.encode("utf-8"))
            elif parts[0] == "je":
                labelname = parts[1]
                bytecode.append(OP_JE)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jne":
                labelname = parts[1]
                bytecode.append(OP_JNE)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jl":
                labelname = parts[1]
                bytecode.append(OP_JL)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jg":
                labelname = parts[1]
                bytecode.append(OP_JG)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jle":
                labelname = parts[1]
                bytecode.append(OP_JLE)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "jge":
                labelname = parts[1]
                bytecode.append(OP_JGE)
                bytecode.append(len(labelname))
                bytecode.extend(labelname.encode("utf-8"))
            elif parts[0] == "rset":
                name = parts[1].replace(",","")
                reg = parts[2]
                variables.append(name)
                bytecode.append(OP_REGSET)
                bytecode.append(len(name))
                bytecode.extend(name.encode("utf-8"))
                bytecode.append(len(reg))
                bytecode.extend(reg.encode("utf-8"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [input] [output.om]")
    else:
        inputf = sys.argv[1]
        outputf = sys.argv[2]
        with open(inputf, "r") as f:
            compiler(f.read())
        if outputf.endswith(".om"):
            with open(outputf, "wb") as f:
                f.write(bytecode)
        else:
            print("Error: use .om has output file name")
            sys.exit(1)
