def check_format(m: str):
    if len(m) == 4:
        return True

def check_E_I(c: str):
    if c in ['E','e']:
        return 'E xtraversion'
    elif c in ['I','i']:
        return 'I ntroversion'
    else:
        return 'error'

def check_S_N(c: str):
    if c in ['S','s']:
        return 'S ensing'
    elif c in ['N','n']:
        return 'i N tuition'
    else:
        return 'error'
        
def check_T_F(c: str):
    if c in ['T','t']:
        return 'T hinking'
    elif c in ['F','f']:
        return 'F eeling'
    else:
        return 'error'

def check_J_P(c: str):
    if c in ['J','j']:
        return 'J udging'
    elif c in ['P','p']:
        return 'P erceiving'
    else:
        return 'error'


if __name__ == "__main__":

    while(True):
        s = input("Please enter your mbti: ")

        if not check_format(s):
            print("Please enter four characters.")
            print()
            continue

        ei = check_E_I(s[0])
        sn = check_S_N(s[1])
        tf = check_T_F(s[2])
        jp = check_J_P(s[3])

        if 'error' in [ei, sn, tf, jp]:
            print("Please enter correct mbti type.")
            print()
            continue

        print("== Your mbti is :: < ", s.upper(), " > ==")
        space = '  ' if 'N' in sn else ''
        print(space+ei)
        print(sn)
        print(space+tf)
        print(space+jp)
        break
