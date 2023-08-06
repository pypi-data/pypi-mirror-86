"""
___________________________________

This package is created by a 
kid who wanted to make
a package which helps everyone
in coding with python.

© Copyrights registered 
___________________________________
"""

VERSION = '0.0.10'

import logging
import platform
import webbrowser
import datetime
import math
import os
import json
import yagmail as yag

# imports

log = False

if log is True:
    logging.basicConfig(filename='anit/anit.log', level=logging.DEBUG)
else:
    pass

def current_timestamp():
    """
    For sql purposes and I forget the code everytime.
    """
    try:
        x = datetime.datetime.now()
        return x
    except:
        logging.error(f'Unknown error')
        raise YourGuessIsGoodAsMine('I have no idea how that happened.')

logging.info(f'{current_timestamp()} :: Anit has been imported')

def current_date():
    """
    returns the date in the way which humans can read
    """
    try:
        x = datetime.datetime.now()
        return x.strftime("%d %B, %Y")
    except:
        logging.error(f'Unknown error')
        raise YourGuessIsGoodAsMine('I have no idea how that happened.')

DATE = current_date()
OS = None
TIMESTAMP = current_timestamp()

def get_version():
    return '0.0.1'


if platform.system() == 'Darwin':
    OS = 'MacOS'
elif platform.system() == 'Windows':
    OS = 'Windows'
else:
    OS = 'Linux'

# errors
class SubjectTooLongError(Exception):
    pass


class InvalidCredentialsOrSettingsNotConfigured(Exception):
    pass


class ErrorInReadingOrCreatingFile(Exception):
    pass


class YourGuessIsGoodAsMine(Exception):
    pass


class InstallationError(Exception):
    pass


class FileTypeWrong(Exception):
    pass


# code

# mailing classes made with yagmail

class Message:
    """
    Instructions to use class:\n
    msg1 = Message(subject here, message here)\n

    You can also pass in a html file path like,\n
    msg1 = Message('Hello World!', 'test.html')
    """

    def __init__(self, subject, message):
        self.subject = subject
        self.message = message
        self.is_file = None
        if len(self.subject) > 150:
            raise SubjectTooLongError('The Subject is too long!')
        if message.endswith('.html'):
            try:
                import codecs
                f = codecs.open(self.message, 'r')
                self.message = f.read()
                self.is_file = True
                f.close()

            except:
                logging.error(f'Error reading or creating file {self.message}')
                raise ErrorInReadingOrCreatingFile(
                    'There was a error in reading the file')

        else:
            self.is_file = False



class MessageMixin:
    subject = None
    message = None

    def __init__(self):
        self.is_file = None
        if len(self.subject) > 150:
            raise SubjectTooLongError('The Subject is too long!')
        if self.message.endswith('.html'):
            try:
                import codecs
                f = codecs.open(self.message, 'r')
                self.message = f.read()
                self.is_file = True
            except:
                logging.error(f'Error reading or creating file {self.message}')
                raise ErrorInReadingOrCreatingFile(
                    'There was a error in reading the file')

        else:
            self.is_file = False


class Mailer:
    """
    Instructions to use class:\n
    mailer = Mailer(email, password)\n
    mailer.send_message(msg1)\n
    Note :You have to pass in the Message class \n
    mailer.send_to(reciever)\n
    Done!
    """

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd
        try:
            self.mailer = yag.SMTP(self.email, self.pwd)
        except:
            logging.error(f'INVALID CREDENTIALS or settings unconfigured')
            raise InvalidCredentialsOrSettingsNotConfigured(
                'Invalid details or enable allow insecure apps to send email here https://myaccount.google.com/lesssecureapps')

    def send_message(self, msg):
        self.message = msg.message
        self.subject = msg.subject

    def send_to(self, person):
        self.person = person
        self.mailer.send(self.person, self.subject, self.message)


class MailerMixin:
    """
    Instructions to use class:\n
    mailer = Mailer(email, password)\n
    mailer.send_message(msg1)\n
    Note :You have to pass in the Message class \n
    mailer.send_to(reciever)\n
    Done!
    """
    email = None
    pwd = None
    person = None

    def __init__(self):
        try:
            self.mailer = yag.SMTP(self.email, self.pwd)
        except:
            logging.error(f'INVALID CREDENTIALS or settings unconfigured')
            raise InvalidCredentialsOrSettingsNotConfigured(
                'Invalid details or enable allow insecure apps to send email here https://myaccount.google.com/lesssecureapps')

    def send_message(self, msg):
        self.message = msg.message
        self.subject = msg.subject

    def send(self):
        self.mailer.send(self.person, self.subject, self.message)


# dates and times



def current_timestamp():
    """
    For sql purposes and I forget the code everytime.
    """
    try:
        x = datetime.datetime.now()
        return x
    except:
        logging.error(f'Unknown error')
        raise YourGuessIsGoodAsMine('I have no idea how that happened.')


def return_pi():
    """
    Used to return pi for completely no reason
    """
    x = math.pi
    return x


def open_browser_url(search):
    try:
        webbrowser.open(f'https://www.google.com/search?q={search}')
    except:
        logging.error(f'Unknown error')
        raise YourGuessIsGoodAsMine('I have no clue. how that happened.')


def install(packages):
    """
    Installs the packages passed in the list like

    install(['package_helper', 'numpy', 'requests'])
    """
    try:
        for x in packages:
            os.system(f'pip install {x}')
    except KeyboardInterrupt:
        logging.error(f'Keyboard interrupt')
        raise InstallationError('There was a problem in installing.')


def create_package(i):
    """
    Used to create a package structure. From the help of the author of package_helper.
    """
    try:
        os.system("mkdir pkg")
        os.system("cd pkg")
        os.system(f"mkdir pkg/{i}")
        d = open("pkg/README.md", 'w+')
        d.write(f"{i} documentation\n write some stuff here!")
        f = open("pkg/setup.py", "w+")
        f.write(f"""
        import setuptools

        with open("README.md", "r") as fh:
            long_description = fh.read()

        setuptools.setup(
            name="{i}",
            version="0.0.1",
            author="Your name",
            author_email="Your email",
            description="may the force be with you",
            long_description=long_description,
            long_description_content_type="text/markdown",
            url="github url from a internet far, far away!",
            packages=setuptools.find_packages(),
            install_requires=[
                #packages_needed
            ]
        )
        """)

        t = open("pkg/open_me.txt", 'w+')
        t.write('''
            open_me.txt
        _______________________________________________________________________________________________________

        Hello! To start creating the package, create a file in your package name folder called:
        __init__.py

        Now, when you have inserted your files, now go to the setup.py file and fill the information there

        After you have done that, create a pypi account and do the following cmds:

        python setup.py sdist bdist_wheel

        after that install "twine" using pip
        and insert this in command line:

        python3 -m twine upload dist/*

        it will ask your pypi username and pwd, just type them
        Done!

        _______________________________________________________________________________________________________
        ''')

        # r.close()
        f.close()
        d.close()
    except:
        logging.error('Error creating package')


def create_json_file(dicti, filename):
    """
    Used to create a json file with dictionary
    create_json_file(dictionary, 'main.json')
    """
    if filename.endswith('.json'):
        try:
            f = open(filename, 'w+')
            d = json.dumps(dicti)
            f.write(d)
            f.close()
        except:
            logging.error('error in creating or reading file.')
            raise ErrorInReadingOrCreatingFile(
                f'There was an error creating {filename}')
    else:
        logging.error('FileTypeError: Does not end with .json')
        raise FileTypeWrong('The file should be a json file')


def learn_python():
    webbrowser.open('https://www.w3schools.com/python/')
