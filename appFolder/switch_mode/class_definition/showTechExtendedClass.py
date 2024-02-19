import re
import sys
import os
import gzip
import readline

class showTechExtended:
    def __init__(self, file):
        self.cmd_dictionary = {}
        self.allCommands = []
        if os.path.isfile(file):
            file_type = os.path.splitext(file)[1]
            if file_type == '.gz':
                with gzip.open(file) as f:
                    self.file_content = f.read().decode()
            else:
                with open(file) as f:
                    self.file_content = f.read()
        else:
            print(f"wrong file provided or file doesn't exist")
            sys.exit()

    def command_collector(self):
        self.allCommands = re.findall(r'------------- (show .*) -------------', self.file_content)
        mod_commands = ['show bgp evpn route-type <route-type> <cr>', 'show bgp evpn route-type <route-type> detail <cr>', 'show bgp evpn route-type <route-type> <route> <cr>', 'show bgp evpn route-type <route-type> <route> detail', 'show bgp evpn route-type <route-type> <route> vni <vni> <cr>', 'show bgp evpn route-type <route-type> <route> rd <rd> <cr>', 'show bgp evpn route-type <route-type> <route> rd <rd> detail <cr>', 'show bgp evpn route-type <route-type> <route> rd <rd> <cr>', 'show bgp evpn route-type <route-type> rd <rd> <cr>', 'show bgp evpn route-type <route-type> vni <vni> <cr>', 'show bgp evpn route-type <route-type> rd <rd> detail <cr>', 
            'show bgp evpn vni <vni> <cr>', 'show bgp evpn vni <vni> next-hop <next-hop> <cr>',
            'show bgp evpn rd <rd> <cr>', 'show bgp evpn rd <rd> vni <vni> <cr>', 'show bgp evpn rd <rd> vni <vni> next-hop <next-hop> <cr>', 'show bgp evpn rd <rd> detail <cr>',
            'show bgp evpn next-hop <next-hop> <cr>']
        self.allCommands.extend(mod_commands)
        for command in self.allCommands:
            temp = self.cmd_dictionary
            for part in command.split(' '):
                if part not in temp:
                    temp[part] = {}
                    temp = temp[part]
                else:
                    temp = temp[part]

    def sed(self, commands):
        # sanitizing the output
        sanitized_command = re.sub(r"\b^sh(o(w?)?)?\b", "show", commands)
        sanitized_command = re.sub(r"\bevp(n?)?\b", "evpn", sanitized_command)
        sanitized_command = re.sub(r"\brout(e(-(t(y(p(e?)?)?)?)?)?)?\b", "route-type", sanitized_command)
        sanitized_command = re.sub(r"\bnext(-(h(o(p?)?)?)?)?\b", "next-hop", sanitized_command)
        return sanitized_command
    
    def command_modifier(self, commands):
        mod_commands = commands.split()
        if 'show bgp evpn' in commands:
            for command in mod_commands[:-1]:
                current_ind = mod_commands.index(command)
                if command not in ['show', 'bgp', 'evpn', 'route-type', 'rd', 'vni', 'detail', 'next-hop']:
                    if mod_commands[current_ind - 1] == '<route-type>':
                        mod_commands[current_ind] = '<route>'
                    else:
                        mod_commands[current_ind] = f'<{mod_commands[current_ind-1]}>'
        return mod_commands
        
    def command_searcher(self, commands):
        pattern = fr'------------- {commands} -------------'
        first_match = re.search(pattern, self.file_content)
        # if there's any match for the command
        if first_match:
            next_pattern = r'------------- (show).*'
            second_match = re.search(next_pattern, self.file_content[first_match.end():])
            if second_match:
                output = self.file_content[first_match.start():(first_match.end() + second_match.start() - 1)]
                return output
            else:
                output = self.file_content[first_match.start():]
                return output
        else:
            return ('wrong command')

    def EvpnOutput(self, route_type=None, route=None, vni=None, RD=None, next_hop=None, detail=False):
        # show bgp evpn route-type <type> <route> RD <rd> <detail>
        if (route_type and route and RD and detail==True):
            output = ''
            ptr = 0
            for lines in self.file_content.splitlines():
                if ptr == 1:
                    if re.search(fr'BGP routing table entry for .*', lines):
                        ptr = 0
                        if re.search(fr'BGP routing table entry for {route_type}.*{route}.*Route Distinguisher: {RD}', lines):
                            ptr = 1
                        else:
                            continue
                    output += lines + '\n'
                else:
                    match = re.search(fr'BGP routing table entry for {route_type}.*{route}.*Route Distinguisher: {RD}', lines)
                    if match:
                        ptr = 1
                        output += lines + '\n'
            return output
        # show bgp evpn route-type <type> <route> <detail>
        elif (route_type and route and detail==True):
            output = ''
            ptr = 0
            for lines in self.file_content.splitlines():
                if ptr == 1:
                    if re.search(fr'BGP routing table entry for .*', lines):
                        ptr = 0
                        if re.search(fr'BGP routing table entry for {route_type}.*{route}.*', lines):
                            ptr = 1
                        else:
                            continue
                    output += lines + '\n'
                else:
                    match = re.search(fr'BGP routing table entry for {route_type}.*{route}.*', lines)
                    if match:
                        ptr = 1
                        output += lines + '\n'
            return output
        # show bgp evpn route-type <type> <detail>
        elif (route_type and detail==True):
            output = ''
            ptr = 0
            for lines in self.file_content.splitlines():
                if ptr == 1:
                    if re.search(fr'BGP routing table entry for .*', lines):
                        ptr = 0
                        if re.search(fr'BGP routing table entry for.*Route Distinguisher: {RD}', lines):
                            ptr = 1
                        else:
                            continue
                    output += lines + '\n'
                else:
                    match = re.search(fr'BGP routing table entry for.*Route Distinguisher: {RD}', lines)
                    if match:
                        ptr = 1
                        output += lines + '\n'
            return output
        # show bgp evpn RD <rd> <detail>
        elif (RD and detail==True):
            output = ''
            ptr = 0
            for lines in self.file_content.splitlines():
                if ptr == 1:
                    if re.search(fr'BGP routing table entry for .*', lines):
                        ptr = 0
                        if re.search(fr'BGP routing table entry for.*Route Distinguisher: {RD}', lines):
                            ptr = 1
                        else:
                            continue
                    output += lines + '\n'
                else:
                    match = re.search(fr'BGP routing table entry for {route_type}.*', lines)
                    if match:
                        ptr = 1
                        output += lines + '\n'
            return output        
        # show bgp evpn route-type <type> <route> RD <rd> vni <vni> next-hop <next-hop>
        elif (route_type and route and RD and vni and next_hop):
            output = ''
            match = re.findall(rf'.*RD: {RD}.*{route_type}.*{vni}.*{route}.*\n.*{next_hop}.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> <route> RD <rd> vni <vni>
        elif (route_type and route and RD and vni):
            output = ''
            match = re.findall(rf'.*RD: {RD}.*{route_type}.*{vni}.*{route}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output       
        # show bgp evpn route-type <type> <route> vni <vni>
        elif (route_type and route and vni):
            output = ''
            match = re.findall(rf'.*RD:.*{route_type}.*{vni}.*{route}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> <route> RD <rd> 
        elif (route_type and route and RD):
            output = ''
            match = re.findall(rf'.*RD: {RD}.*{route_type}.*{route}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> <route> next-hop <next-hop>
        elif (route_type and route and next_hop):
            output = ''
            match = re.findall(rf'.*RD.*{route_type}.*{route}.*\n.*{next_hop}.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> <route>
        elif (route_type and route):
            output = ''
            match = re.findall(rf'.*RD.*{route_type}.*{route}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> vni <vni>
        elif (route_type and vni):
            output = ''
            match = re.findall(rf'.*RD:.*{route_type}.*{vni}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type <type> rd <rd>
        elif (route_type and RD):
            output = ''
            match = re.findall(rf'.*RD: {RD}.*{route_type}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn route-type next-hop <next-hop>
        elif (route_type and next_hop):
            output = ''
            match = re.findall(rf'.*RD.*{route_type}.*\n.*{next_hop}.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn vni <vni> rd <rd>
        elif (vni and RD):
            output = ''
            match = re.findall(rf'.*RD: {RD}.*{vni}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output              
        # show bgp evpn route-type <type>
        elif (route_type):
            output = ''
            match = re.findall(rf'.*RD.*{route_type}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn nexthop <nexthop>
        elif (next_hop):
            output = ''
            match = re.findall(rf'.*RD.*\n.*{next_hop}.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
        # show bgp evpn vni <vni>
        elif (vni):
            output = ''
            match = re.findall(rf'.*RD:.*{vni}.*\n.*', self.file_content)
            for line in match:
                output += line + '\n'
            return output
  
    def command_processor(self, commands):
        if commands.lower() == 'exit':
            sys.exit()
        # if user presses ?
        elif commands == '?':
            content = '\n'
            for keys in self.cmd_dictionary:
                content += keys + '\n'
            return content
        # for viewing all show/bash commands
        elif '??' in commands:
            commands = commands.replace('??', '')
            question_pattern = re.compile(fr'.*{commands}.*')
            question_matches = question_pattern.findall('\n'.join(self.allCommands))
            content = ''
            question_matches = sorted(question_matches)
            for line in question_matches:
                if line != '':
                   content += line + '\n'
            return content.strip('\n')
        # is ? is pressed along with any previous string like show ip ?
        elif re.match('(.*[\s]\?)', commands):
            mod_commands = self.command_modifier(commands)
            temp_dict = {}
            try:
                for cmd in mod_commands[:-1]:
                    if cmd in ['bash', 'show']:
                        temp_dict = self.cmd_dictionary[cmd]
                    else: # searching the inner dicitonary for the keys. For eg if user does show ip ?, temp_dict will be eventually {interfaces: {}, route {}, ..}
                        temp_dict1 = temp_dict.copy()
                        temp_dict = {}
                        temp_dict = temp_dict1[cmd].copy()
                content = ''
                for keys in sorted(temp_dict):
                    content += keys + '\n'
                return content.strip('\n')
            except KeyError as e:
                return('wrong command')
            
        # is ? is pressed along with any previous string like show ip?
        elif re.match('(.*[^\s]\?)', commands):
            temp_dict = {}
            for cmd in commands.split()[:-1]:
                if cmd in ['bash', 'show']:
                    temp_dict = self.cmd_dictionary[cmd]
                else:
                    temp_dict1 = temp_dict.copy()
                    temp_dict = {}
                    temp_dict = temp_dict1[cmd.replace('?', '')].copy() # we are not considering the last element in the command meaning in show ip?, we only are concerned with keys starting with ip in the dict['show'] returned dictionary
            content = ''
            for keys in temp_dict:
                if keys.startswith(commands.split()[-1].replace('?', '')):
                    content += keys + '\n'
            return content.strip('\n')   
        elif re.search(r'show bgp evpn (route-type|vni|rd|next-hop|detail).+', commands ):
            route_type = None; route = None; vni = None; RD = None; next_hop = None; detail = False
            if ('detail' in commands and ('next-hop' in commands or 'vni' in commands)):
                return('detail ouput not supported with keywords vni and nexthop')
            elif (re.search(r'show bgp evpn .*', commands)):
                try:
                    route_type = re.findall(r'.*route-type (\S+).*', commands)[0]
                except IndexError as e:
                    route_type = None
                try:
                    next_hop = re.findall(r'.*next-hop (\S+).*', commands)[0]
                except IndexError as e:
                    next_hop = None
                try:
                    vni = re.findall(r'.*vni (\S+).*', commands)[0]
                except IndexError as e:
                    vni = None
                try:
                    RD = re.findall(r'.*rd (\S+).*', commands)[0]
                except IndexError as e:
                    RD = None
                if 'detail' in commands:
                    detail = True
                if re.findall(r"show bgp evpn route-type (\S*) (\S*) detail", commands) or re.findall(r"show bgp evpn route-type (\S*) (\S*) next-hop.*", commands) or re.findall(r"show bgp evpn route-type (\S*) (\S*) vni.*", commands) or re.findall(r"show bgp evpn route-type (\S*) (\S*) rd.*", commands):
                    route = re.findall(r"show bgp evpn route-type (\S*) (\S*).*", commands)[0][1]
                elif ('detail' not in commands and 'next-hop' not in commands and 'vni' not in commands and 'rd' not in commands and re.findall(r"show bgp evpn route-type (\S*) (\S*)$", commands)):
                    route = re.findall(r"show bgp evpn route-type (\S*) (\S*)$", commands)[0][1]
                return(self.EvpnOutput(route_type=route_type, route=route, vni=vni, RD=RD, next_hop=next_hop, detail=detail))
        else:
            return self.command_searcher(commands)


    def complete(self, text, state):
        # autocompleter
        ori_command = readline.get_line_buffer().lower()
        mod_ori_command = ori_command.split() # get the previously entered commands
        mod_ori_command[0] = self.sed(mod_ori_command[0]) 
        if len(mod_ori_command) <= 1 and not re.search('\s$', ori_command): # if no commands entered yet, show all options
            options = ['show'] 
        elif mod_ori_command[0] in ['show']: # narrow down options based on 'show' or 'bash' command
            if len(mod_ori_command) == 2 and not re.search('\s$', ori_command):
                options = ['bgp']
            elif len(mod_ori_command) == 3 and not re.search('\s$', ori_command):
                options = ['evpn']            
            elif len(mod_ori_command) == 4 and not re.search('\s$', ori_command):
                options = ['route-type', 'next-hop', 'detail']
            elif len(mod_ori_command) == 5 and mod_ori_command[3] == 'route-type' and not re.search('\s$', ori_command):
                options = ['auto-discovery', 'ethernet-segment', 'imet', 'ip-prefix', 'mac-ip', 'smet', 'join-sync', 'leave-sync', 'spmsi']
            elif len(mod_ori_command) == 6 and mod_ori_command[3] == 'route-type' and 'next-hop' not in mod_ori_command and 'detail' not in mod_ori_command and not re.search('\s$', ori_command):
                options = ['next-hop', 'detail']
            elif len(mod_ori_command) == 7 and mod_ori_command[3] == 'route-type' and 'next-hop' not in mod_ori_command and 'detail' not in mod_ori_command and not re.search('\s$', ori_command) and 'next-hop' not in mod_ori_command:
                options = ['detail', 'next-hop']
            else:
                options = []

        else: # no options for other commands
            options = []
        results = [x for x in options if x.startswith(text)] + [None]
        return results[state]
        

