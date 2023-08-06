import os
import sys
import importlib
import json
from colorama import init, Fore, Back, deinit, Style


VERSION = '0.4'
NAME = 'Kommand'
DESCRIPTION = 'Command everything with kommand'
AUTHOR = 'kzulfazriawan'
EMAIL = 'kzulfazriawan@gmail.com'


def build():
    '''
    ____it's just build json template, if you prefer using command with json and not bother with
    dictionary kwargs and stuff____
    '''
    init()
    q = {
        'name': f'{Fore.GREEN}Your project name:{Style.RESET_ALL} ',
        'version': f'{Fore.GREEN}Your project version:{Style.RESET_ALL} ',
        'description': f'{Fore.GREEN}Your project Description:{Style.RESET_ALL} ',
        'author': f'{Fore.GREEN}Your name:{Style.RESET_ALL} ',
        'email': f'{Fore.GREEN}Your email:{Style.RESET_ALL} ',
        'command': f'{"".join([Style.BRIGHT, Back.GREEN])} SETUP FINISHED !{Style.RESET_ALL}'
    }
    r = {'name': '',
         'version': '',
         'description': '',
         'author': '',
         'email': '',
         'command': {'your_command': dict(exec='MYFUNC', help='MYHELP')}}
    for k, v in q.items():
        if k != 'command':
            r[k] = input(v)
        else:
            name = r['name'] if 'name' in r else 'command'
            with open(os.path.join(os.getcwd(), f'{name}.json'), 'w') as f:
                json.dump(r, f, indent=4)
                f.close()
            sys.stdout.write(v)
    deinit()


def control(**kwargs):
    init()

    '''
    ____this is your kommand!. this function is created to manage arguments in CLI, just like apps that needs
    arguments in CLI to run some options or modules, for example: python kommand.py test more-test. the script
    will run function that registered on it from first command to second.____
    '''
    argv = sys.argv
    app_name = NAME
    app_version = VERSION
    app_description = DESCRIPTION
    app_author = AUTHOR
    app_email = EMAIL

    if 'json_file' in kwargs:
        path_root = os.path.dirname(sys.modules['__main__'].__file__)
        with open(os.path.join(path_root, kwargs['json_file']), 'r') as f:
            d = json.load(f)
            app_name = d['name']
            app_version = d['version']
            app_description = d['description']
            app_author = d['author']
            app_email = d['email']
            kwargs = d['command']
            f.close()
    else:
        if 'name' in kwargs:
            app_name = kwargs['name']
            del kwargs['name']

        if 'version' in kwargs:
            app_version = kwargs['version']
            del kwargs['version']

        if 'description' in kwargs:
            app_description = kwargs['description']
            del kwargs['description']
            
        if 'author' in kwargs:
            app_author = kwargs['author']
            del kwargs['author']
            
        if 'email' in kwargs:
            app_email = kwargs['email']
            del kwargs['email']

    # ____first I'll find the biggest string from kwargs, it'll be used as biggest edge of space in string____
    big_len = len(max([i for i in kwargs.keys()], key=len))

    head = f'{Style.BRIGHT + app_name + Style.RESET_ALL} by {app_author} <{app_email}>'
    body = f'{Style.BRIGHT}Version {app_version + Style.RESET_ALL}'
    foot = Style.DIM + app_description + Style.RESET_ALL

    big_head = len(head) if len(head) > len(foot) else len(foot)

    border = f"+{''.join(['-' for z in range(0, big_head)])}+\n"

    stdout = Fore.GREEN + border
    stdout += f'|{head + "".join([" " for y in range(0, big_head - len(head))])}|\n'
    stdout += f'|{body + "".join([" " for y in range(0, big_head - len(body))])}|\n'
    stdout += f'|{foot + "".join([" " for y in range(0, big_head - len(foot))])}|\n'
    stdout += border + Fore.RESET

    stdout_help = ''

    for k, v in kwargs.items():
        h_key = f'{k}'

        # ____if the key is smaller than the biggest one, then it fill with spaces leftover. otherwise pass____
        if len(k) < big_len:
            space = ''.join([' ' for x in range(0, big_len - len(k))])
            h_key = f'{k}{space}'

        stdout_help += f'{Style.BRIGHT + h_key + Style.RESET_ALL} {v["help"]}\n'

    if isinstance(argv, list):
        # ____delete argv[0] because it's name file____
        # file = argv[0]
        del argv[0]

        # ____if help is show help, otherwise run the function that need to be run____
        stdout_help = f'Usage: [Options]="[Argument]" \nOptions: \n---\n{stdout_help}'
        try:
            if argv[0] == 'help':
                sys.stdout.write(stdout + stdout_help)
            else:
                for z in argv:
                    com_split = z.split('=')
                    parameters = None

                    # ____checking the command if there's parameter on it____
                    com_x = com_split[0]
                    if len(com_split) > 1:
                        parameters = com_split[1].strip('\"').strip('\'')

                    if com_x in kwargs:
                        execute = kwargs[com_x]['exec']

                        # ____for now it's just import via modules cannot do directly in files____
                        if '.' in execute:
                            data = kwargs[com_x]['exec'].split('.')
                            execute = getattr(importlib.import_module('.'.join(data[:-1])), data[-1])
                        else:
                            raise ImportError

                        if callable(execute):
                            if parameters is not None:
                                execute(*parameters.split(','))
                            else:
                                execute()
        except IndexError:
            sys.stdout.write(stdout + stdout_help)
    deinit()
