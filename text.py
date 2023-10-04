with open('text_example.txt', 'r') as f:
    text: list = f.readlines()
    et_stack = []
    et_recur = []
    for s in text:
        if 'stack' in s:
            et = s.split(':')[-1].strip()
            et_stack.append(float(et))
        elif 'recur' in s:
            et = s.split(':')[-1].strip()
            et_recur.append(float(et))

    
def get_average(et: list):
    return round((sum(et)/len(et)), 4)
    
et_stack_mean = get_average(et_stack)
et_recur_mean = get_average(et_recur)

print(et_stack_mean)
print(et_recur_mean)