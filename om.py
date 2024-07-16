import sys

regs = {"r0": 0, "r1": 0, "r2": 0, "r3": 0, "taa": 0, "tba": 0, "tca": 0, "dao": 0, "dbo": 0, "dco": 0, "ddo": 0}
variables = {}
labels = {}

stack = []
compare = []
for arg in sys.argv[::-1]:
    if arg == sys.argv[0]:
        break
    else:
        stack.append(arg)
stack.append(len(sys.argv[1:]))

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
in_label = [False]
reomasmedcode = [""]

def execute2(bytecode):
    ip = 0
    while ip < len(bytecode):
        byte = bytecode[ip]
        ip += 1

        if byte == OP_PUSH:
            value = bytecode[ip]
            ip += 1
            stack.append(value)
            reomasmedcode[0] += f"  ipush {value}\n"
        elif byte == OP_POP:
            reglen = bytecode[ip]
            ip += 1
            regname = bytecode[ip:ip + reglen].decode('utf-8')
            ip += reglen
            regs[regname] = stack.pop()
            reomasmedcode[0] += f"  pop {regname}\n"
        elif byte == OP_SUM:
            if sp[0] >= 2:
                a = stack.pop()
                b = stack.pop()
                stack.append(b + a)
                reomasmedcode[0] += f"  sum\n"
            else:
                print("Warning: you need to have 2 items or more inside the stack to do sum")
        elif byte == OP_SUB:
            if sp[0] >= 2:
                a = stack.pop()
                b = stack.pop()
                stack.append(b - a)
                reomasmedcode[0] += f"  sub\n"
            else:
                print("Warning: you need to have 2 items or more inside the stack to do sub")
        elif byte == OP_SYSCALL:
            if regs["r0"] == 1:
                print(regs["r1"], end="")
                regs["r0"] = 0
                regs["r1"] = 0
            elif regs["r0"] == 2:
                sys.exit(regs["r1"])
            reomasmedcode[0] += f"  syscall\n"
        elif byte == OP_PUSHSTR:
            strlen = bytecode[ip]
            ip += 1
            value = bytecode[ip:ip + strlen].decode("utf-8")
            ip += strlen
            stack.append(value)
            valuetoreoasm = value.replace(" ", "\\s").replace("\n", "\\n")
            reomasmedcode[0] += f"  spush {valuetoreoasm}\n"
        elif byte == OP_PUSHREG:
            strlen = bytecode[ip]
            ip += 1
            reg = bytecode[ip:ip + strlen].decode("utf-8")
            ip += strlen
            stack.append(regs[reg])
            reomasmedcode[0] += f"  rpush {reg}\n"
        elif byte == OP_GET:
            reglen = bytecode[ip]
            ip += 1
            reg = bytecode[ip:ip + reglen].decode("utf-8")
            ip += reglen
            regs[reg] = input()
            reomasmedcode[0] += f"  get {reg}\n"
        elif byte == OP_JMP:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            execute2(labels[labelname])
            break
        elif byte == OP_INTSET:
            namelen = bytecode[ip]
            ip += 1
            name = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            value = int.from_bytes(bytecode[ip:ip + 4], byteorder='big', signed=False)
            ip += 4
            variables[name] = value
            reomasmedcode[0] += f"  iset {name}, {value}\n"
        elif byte == OP_PUSHVAR:
            namelen = bytecode[ip]
            ip += 1
            name = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            stack.append(variables[name])
            reomasmedcode[0] += f"  vpush {name}\n"
        elif byte == OP_RET:
            break
        elif byte == OP_CALL:
            namelen = bytecode[ip]
            ip += 1
            label = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            execute2(labels[label])
        elif byte == OP_CMP:
            reg1len = bytecode[ip]
            ip += 1
            reg1name = bytecode[ip:ip + reg1len].decode("utf-8")
            ip += reg1len
            reg2len = bytecode[ip]
            ip += 1
            reg2name = bytecode[ip:ip + reg2len].decode("utf-8")
            ip += reg2len
            if reg1name in regs.keys():
                if reg2name in regs.keys():
                    compare = [regs[reg1name], regs[reg2name]]
                elif reg2name in variables.keys():
                    compare = [regs[reg1name], variables[reg2name]]
            elif reg1name in variables.keys():
                if reg2name in regs.keys():
                    compare = [variables[reg1name], regs[reg2name]]
                elif reg2name in variables.keys():
                    compare = [variables[reg1name], variables[reg2name]]
        elif byte == OP_JE:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] == compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if equal")
                sys.exit(1)
        elif byte == OP_JNE:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] != compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if not equal")
                sys.exit(1)
        elif byte == OP_JL:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] < compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if not equal")
                sys.exit(1)
        elif byte == OP_JG:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] > compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if not equal")
                sys.exit(1)
        elif byte == OP_JLE:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] <= compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if not equal")
                sys.exit(1)
        elif byte == OP_JGE:
            namelen = bytecode[ip]
            ip += 1
            labelname = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            if len(compare) == 2:
                if compare[0] >= compare[1]:
                    execute2(labels[labelname])
                    break
                else:
                    pass
            else:
                print("Error: No registers to do jump if not equal")
                sys.exit(1)
        elif byte == OP_REGSET:
            namelen = bytecode[ip]
            ip += 1
            name = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            reglen = bytecode[ip]
            ip += 1
            regname = bytecode[ip:ip + reglen].decode("utf-8")
            ip += reglen
            variables[name] = regs[regname]
            reomasmedcode[0] += f"  rset {name}, {regname}\n"

def execute1(bytecode):
    ip = 0
    labelname = [""]
    while ip < len(bytecode):
        byte = bytecode[ip]
        ip += 1
    
        if not in_label[0]:
            if byte == OP_LABEL:
                namelen = bytecode[ip]
                ip += 1
                name = bytecode[ip:ip + namelen].decode("utf-8")
                ip += namelen
                labels[name] = bytearray()
                labelname[0] = name
                in_label[0] = True
        elif in_label[0]:
            if byte == ord("l") and bytecode[ip] == ord("e") and bytecode[ip + 1] == ord("n") and bytecode[ip + 2] == ord("d"):
                in_label[0] = False
                ip += 3
            else:
                labels[labelname[0]].append(byte)
    execute2(labels["main"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [input.om]")
        sys.exit(1)
    else:
        if sys.argv[1].endswith(".om"):
            with open(sys.argv[1], "rb") as f:
                execute1(f.read())
            if "--debug" in sys.argv:
                print(f"""
------+
STACK | = {stack}
------+
""")
                print(f"""
------+
REGS  | = {regs}
------+
""")
            if "--reoasm" in sys.argv:
                print("main:")
                print(reomasmedcode[0])
                print("lend")
        else:
            print("Error: use .om file extension!")
            sys.exit(1)
