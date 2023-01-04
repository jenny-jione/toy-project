def check_format(m: str):
    if len(m) == 4:
        return True

def check_E_I(c: str):
    if c == 'E' or c == 'e':
        return 'Extraversion'
    elif c == 'I' or c == 'i':
        return 'Introversion'
    else:
        return 'error'

def check_S_N(c: str):
    if c == 'S' or c == 's':
        return 'Sensing'
    elif c == 'N' or c == 'n':
        return 'iNtuition'
    else:
        return 'error'
        
def check_T_F(c: str):
    if c == 'T' or c == 't':
        return 'Thinking'
    elif c == 'F' or c == 'f':
        return 'Feeling'
    else:
        return 'error'

def check_J_P(c: str):
    if c == 'J' or c == 'j':
        return 'Judgement'
    elif c == 'P' or c == 'p':
        return 'Perception'
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

        print("Your mbti is", s.upper(), "==")
        print(ei)
        print(sn)
        print(tf)
        print(jp)
        break
