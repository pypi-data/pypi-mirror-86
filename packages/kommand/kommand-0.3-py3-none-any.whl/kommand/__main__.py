from kommand import control


if __name__ == '__main__':
    kom = {
        'build': {
            'exec': 'kommand.build',
            'help': 'Build you command post instantly as json.'
        }
    }
    control(**kom)
