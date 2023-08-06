## Kommand!

![GitHub](https://img.shields.io/github/license/kzulfazriawan/kommand?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/kzulfazriawan/kommand?style=for-the-badge)

This is your kommand!, this package is used to interactively control your
function in CL.

### Get started
Requirement:
- Python >= 3.6
- colorama *(just for color in command line)*

How to install kommand:
```shell script
python setup.py install
```

How to use kommand:
```shell script
# this will build json templates for your command information.
python -m kommand build
```

after that you just have to fill your command information in your json file.
```json
{
    "name": "myapp",
    "version": "0.1",
    "description": "kom test",
    "author": "kzulfazriawan",
    "email": "kzulfazriawan@gmail.com",
    "command": {
        "your_command": {
            "exec": "module_to_exec",
            "help": "help information"
        },
        "your_command2": {
            "exec": "module_to_exec2",
            "help": "help information2"
        }
    }
}
```

In your script python you can add
```python
from kommand import control

if __name__ == '__main__':
    control(json_file='your_file.json')
    # OR you can use with dictionary arguments
    control(
        name='your_project_name',
        version='0.1',
        your_command={'exec': 'your_module_exec', 'help': 'help information'},
        your_command2={'exec': 'your_module_exec2', 'help': 'help information2'},...
    )
```

Then start execute your script in command line:
```shell script
python myscript.py

# to see help
python myscript.py help

# to execute
python myscript.py your_command your_command2
python myscript.py your_command2 your_command
python myscript.py your_command2
python myscript.py your_command

# if use parameter
python myscript.py your_command='p1,p2,...'
```