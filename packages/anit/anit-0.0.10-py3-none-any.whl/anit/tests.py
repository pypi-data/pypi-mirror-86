#!/usr/bin/env python

from pyfiglet import Figlet
import __init__ as anit
import click
import os


def loader(times):
    import time
    import sys

    animation = "|/-\\"

    for i in range(times):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()


def clear():
    os.system("clear")


@click.command()
@click.option('-i', default='main')
def main(i):
    if i == 'main':
        print('_____________________________________\n')
        f = Figlet()
        print(f.renderText(f'Anit'))
        print('FROM Animite Software Foundation')
        print('CREATED BY Shaurya Pratap Singh')
        print('VERSION '+anit.VERSION)
        print('OS: '+anit.OS)
        print('______________________________________')
    elif i == 'mailer':
        print("Mailer getting ready.")
        loader(50)
        os.system('clear')
        print('______________________________________\n')
        print('Anit Mailer '+anit.VERSION)
        email = input('Your Email: ')
        pwd = input('Your GMAIL password: ')
        to = input('To: ')
        subject = input('Subject: ')
        message = input('Message: \n')

        try:
            msg = anit.Message(subject, message)
            mailer = anit.Mailer(email, pwd)
            mailer.send_message(msg)
            mailer.send_to(to)
        except:
            raise anit.InvalidCredentialsOrSettingsNotConfigured(
                'Invalid details or enable allow insecure apps to send email here https://myaccount.google.com/lesssecureapps')

        print('sending to {}......'.format(to))
        loader(50)
        print('MAIL SENT SUCCESFULLY')
    elif i == 'read':
        print('ANIT FILE READER')
        file = input('File to read: ')
        print('\n')
        f = open(file, 'r')
        clear()
        print(f.read())
        f.close()
    elif i == 'install':
        print('loading installer....')
        loader(25)
        file = input('Requirements.txt: ')
        f = open(file, 'r')
        red = f.read()
        s = red.split('\n')
        anit.install(s)
        f.close()
    elif i == 'open':
        search = input('Search: ')
        anit.open_browser_url(search)
    elif i == 'package':
        name = input('Package name: ')
        anit.create_package(name)
        print('Creating package.')
        loader(50)
        print('Done!')
    elif i == 'version':
        print(anit.VERSION)
    elif i == 'learn_python':
        loader(45)
        anit.learn_python()
    elif i == 'date':
        print(anit.DATE)
    



main()
