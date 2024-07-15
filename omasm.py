import sys

bytecode = bytearray()

regs = ["r0", "r1", "r2", "r3", "r4", "r5"]
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

def compiler(code):
    lines = code.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        i += 1

        if line.startswith("ipush "):
            value = int(line.split(" ")[1])
            bytecode.append(OP_PUSH)
            bytecode.append(value)
        elif line.startswith("pop "):
            reg = line.split(" ")[1].strip()
            if reg in regs:
                bytecode.append(OP_POP)
                bytecode.append(len(reg))
                bytecode.extend(reg.encode("utf-8"))
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        elif line == "sum":
            bytecode.append(OP_SUM)
        elif line == "sub":
            bytecode.append(OP_SUB)
        elif line == "syscall":
            bytecode.append(OP_SYSCALL)
        elif line.startswith("spush "):
            bytecode.append(OP_PUSHSTR)
            bytecode.append(len(line[6:].replace("\\n", "\n").replace("\\s", " ")))
            bytecode.extend(line[6:].replace("\\n", "\n").replace("\\s", " ").encode("utf-8"))
        elif line.startswith("rpush "):
            reg = line.split(" ")[1]
            if reg in regs:
                bytecode.append(OP_PUSHREG)
                bytecode.append(len(reg))
                bytecode.extend(reg.encode("utf-8"))
        elif line.startswith("get "):
            reg = line.split(" ")[1]
            if reg in regs:
                bytecode.append(OP_GET)
                bytecode.append(len(reg))
                bytecode.extend(reg.encode("utf-8"))
        elif line.endswith(":"):
            labelname = line.split(":")[0].strip()
            bytecode.append(OP_LABEL)
            bytecode.append(len(labelname))
            bytecode.extend(labelname.encode("utf-8"))
        elif line.startswith("jmp "):
            labelname = line.split(" ")[1]
            bytecode.append(OP_JMP)
            bytecode.append(len(labelname))
            bytecode.extend(labelname.encode("utf-8"))
        elif line == "lend":
            bytecode.append(ord("l"))
            bytecode.append(ord("e"))
            bytecode.append(ord("n"))
            bytecode.append(ord("d"))
        elif line.startswith("iset "):
            name = line.split(" ")[1].split(",")[0].strip("\"\'")
            value = line.split(",")[1].strip("\"\'")
            variables.append(name)
            bytecode.append(OP_INTSET)
            bytecode.append(len(name))
            bytecode.extend(name.encode("utf-8"))
            bytecode.extend(int(value).to_bytes(4, byteorder='big', signed=False))
        elif line.startswith("vpush"):
            name = line.split(" ")[1]
            if name in variables:
                bytecode.append(OP_PUSHVAR)
                bytecode.append(len(name))
                bytecode.extend(name.encode("utf-8"))
            else:
                print(f"Error: unknown variable -> {name}")
                sys.exit(1)

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
