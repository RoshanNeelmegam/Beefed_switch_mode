import re        

def shrunsec(contents, command):
    section_input = re.split('sec(?:t(?:i(?:on?)?)?)?', command)[-1].strip()
    section_output = ''
    relevant_section = False
    content = ''
    for line in contents.splitlines():
        if not line.startswith(' '):
            if relevant_section:
                content += section_output.rstrip() 
                if line.startswith('!'):
                    content += '\n' + line.rstrip() + '\n'
            relevant_section = False
            section_output = ''
        if re.match('.*' + section_input + '.*', line, re.I):
            relevant_section = True
        section_output += line +'\n'
    return content

def shrunint(contents, command):
    matched = False
    try:
        interface = re.findall(r'show running-config sanitized interfaces (\w.+)', command)
        interface = re.sub(' ', '', interface[0])
        if not re.search(r'[0-9]', interface):
            return('Please enter a valid interface')
        content = ''
        for lines in contents.splitlines():
            if matched:
                if re.search(r'^!', lines):
                    return content
                content += lines + '\n'
            if not matched:
                match = re.search(rf'^interface\b {interface}\b', lines, re.IGNORECASE)
                if match:
                    content += lines + '\n'
                    matched = True
        if content == '':
            return('interface does not exist')
    except IndexError as e:
        return('Please enter the interface')



