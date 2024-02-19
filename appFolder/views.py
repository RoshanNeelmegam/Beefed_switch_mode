from django.shortcuts import render
from django.http import HttpResponse
from .main import initialize
import re, subprocess
# Create your views here.
# This is a request handler.

showtech = initialize('/Users/roshan/Desktop/Logs/Mingsoong/schedule/tech-support/uk-wat-eci-npmgmtsw02_tech-support_2023-12-06.0404.log.gz')

def page1(request):
    if request.method == 'POST':
        command = request.POST.get('commands')
        if command:
            output = '\n'
            try:
                switch_command = ''
                bash_command = ''
                command = re.sub(r' +', ' ', command) # removing white spaces between words if any
                try:
                    switch_command, bash_command = command.split('|', maxsplit=1)
                    switch_command = switch_command.rstrip()
                except ValueError as e:
                    switch_command = command
                if bash_command:
                    command_prior_pipe = showtech.command_processor(showtech.sed(switch_command))
                    input_data = command_prior_pipe.encode()
                    result = subprocess.run(bash_command, shell=True, input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    bash_output = result.stdout.decode()
                    bash_err = result.stderr.decode()
                    if bash_err:
                        output += bash_err
                    else:
                        output += bash_output
                    print(output)
                    return render(request=request, template_name='test.html', context={'output': output})
                else:
                    output += showtech.command_processor(showtech.sed(switch_command))
                    return render(request=request, template_name='test.html', context={'output': output})
            except ValueError as e:
                output += 'wrong input or / notation not supported'
                return render(request=request, template_name='test.html', context={'output': output})


    return render(request=request, template_name='test.html', context={'name': ''})
