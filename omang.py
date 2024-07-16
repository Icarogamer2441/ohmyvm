import sys

functions = []

def compiler(code):
    tokens = code.split()
    tokenpos = 0
    in_func = [False]
    in_string = [False]
    funcname = [""]
    out = [""]
    finalstr = []
    variables = []

    while tokenpos < len(tokens):
        token = tokens[tokenpos]
        tokenpos += 1

        if not in_func[0]:
            if token == "def":
                token = tokens[tokenpos]
                tokenpos += 1
                out[0] += f"{token}:\n"
                functions.append(token)
                while tokenpos < len(tokens) and not token.endswith(":"):
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.endswith(":"):
                        if len(token.replace(":", "")):
                            name = token.replace(":", "")
                            out[0] += "  pop r2\n"
                            out[0] += f"  rset {name}, r2\n"
                            variables.append(name)
                        break
                    else:
                        out[0] += "  pop r2\n"
                        out[0] += f"  rset {token}, r2\n"
                        variables.append(token)
                in_func[0] = True
        elif in_func[0]:
            if token == "end":
                in_func[0] = False
                out[0] += "lend\n"
            else:
                if not in_string[0]:
                    if token.isdigit():
                        out[0] += f"  ipush {int(token)}\n"
                    elif token == "print":
                        out[0] += "  ipush 1\n"
                        out[0] += "  pop r0\n"
                        out[0] += "  pop r1\n"
                        out[0] += "  syscall\n"
                    elif token.startswith('"'):
                        if token.endswith("\""):
                            string = token.replace("\"", "")
                            out[0] += f"  spush {string}\n"
                        else:
                            finalstr.append(token.replace("\"",""))
                            in_string[0] = True
                    elif token in variables:
                        out[0] += f"  vpush {token}\n"
                    elif token in functions:
                        out[0] += f"  call {token}"
                    else:
                        print(f"Error: unknown token: {token}")
                        sys.exit(1)
                elif in_string[0]:
                    if token.endswith("\""):
                        finalstr.append(token.replace("\"",""))
                        string = " ".join(finalstr)
                        out[0] += f"  spush {string}\n"
                        finalstr.clear()
                        in_string[0] = False
                    else:
                        finalstr.append(token.replace("\"",""))

    return out[0]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [input.ola] [output.oasm]")
        sys.exit(1)
    else:
        if sys.argv[1].endswith(".ola"):
            if sys.argv[2].endswith(".oasm"):
                with open(sys.argv[1], "r") as inp:
                    output = compiler(inp.read())
                with open(sys.argv[2], "w") as out:
                    out.write(output)
            else:
                print("Error: use .oasm file extension for output file!")
                sys.exit(1)
        else:
            print("Error: use .ola file extension for input file!")
            sys.exit(1)
