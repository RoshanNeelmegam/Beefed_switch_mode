import re

def perVlan(content, command):
    vlan = re.findall(r'show vlan (\w+)', command)[0]
    output = ''
    ptr = 0
    for lines in content.splitlines():
        if ptr != 0:
            if not re.search(r'^[\d]+.+', lines):
                output += lines + '\n'
            else:
                ptr = 0
                return output
        if re.search(fr'^{vlan} .+', lines):
            output += lines + '\n'
            ptr = 1
    return ('Vlan does not exists')

