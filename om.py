import sys

regs = {"r0": 0, "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0}
variables = {}
labels = {}

stack = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
compare = []

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
    sp = [0]
    while ip < len(bytecode):
        byte = bytecode[ip]
        ip += 1

        if sp[0] > len(stack) - 1:
            print("Warning: stack over flow")
            sp[0] -= 1
        elif sp[0] < 0:
            print("Warning: stack under flow")
            sp[0] += 1

        if byte == OP_PUSH:
            value = bytecode[ip]
            ip += 1
            stack[sp[0]] = value
            sp[0] += 1
            reomasmedcode[0] += f"  ipush {value}\n"
        elif byte == OP_POP:
            reglen = bytecode[ip]
            ip += 1
            regname = bytecode[ip:ip + reglen].decode('utf-8')
            ip += reglen
            sp[0] -= 1
            regs[regname] = stack[sp[0]]
            stack[sp[0]] = 0
            reomasmedcode[0] += f"  pop {regname}\n"
        elif byte == OP_SUM:
            if sp[0] >= 2:
                sp[0] -= 1
                a = stack[sp[0]]
                stack[sp[0]] = 0
                sp[0] -= 1
                b = stack[sp[0]]
                stack[sp[0]] = b + a
                sp[0] += 1
                reomasmedcode[0] += f"  sum\n"
            else:
                print("Warning: you need to have 2 items or more inside the stack to do sum")
        elif byte == OP_SUB:
            if sp[0] >= 2:
                sp[0] -= 1
                a = stack[sp[0]]
                stack[sp[0]] = 0
                sp[0] -= 1
                b = stack[sp[0]]
                stack[sp[0]] = b - a
                sp[0] += 1
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
            stack[sp[0]] = value
            sp[0] += 1
            reomasmedcode[0] += f"  spush {value}\n"
        elif byte == OP_PUSHREG:
            strlen = bytecode[ip]
            ip += 1
            reg = bytecode[ip:ip + strlen].decode("utf-8")
            stack[sp[0]] = regs[reg]
            ip += strlen
            sp[0] += 1
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
            stack[sp[0]] = variables[name]
            sp[0] += 1
            reomasmedcode[0] += f"  vpush {name}\n"
        elif byte == OP_RET:
            break
        elif byte == OP_CALL:
            namelen = bytecode[ip]
            ip += 1
            label = bytecode[ip:ip + namelen].decode("utf-8")
            ip += namelen
            execute2(label)
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
            reomasmedcode[0] += f"  rset {regname}\n"

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
