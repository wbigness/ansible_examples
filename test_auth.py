import time
import argparse
import paramiko
from getpass import getpass


my_parser = argparse.ArgumentParser(description="arg parser hidden password input.")
my_parser.add_argument('-u', 
                       '--username',
                       required=True,
                       dest='username',
                       help='Username on the device')

my_parser.add_argument('-i', 
                       '--ip-address',
                       required=True,
                       dest='ip',
                       help='IP address of the device') 

#define variables from args
args = my_parser.parse_args()
my_user = args.username
my_ip = args.ip

# define password via getpass()
my_pass = getpass()

# commands to run
commands = ['ls -al', 'pwd']

# setup the paramiko client connection
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

# auto accept in known_hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("logging in now")
ssh_login = ssh.connect(my_ip, port=22, 
                        username=my_user, 
                        password=my_pass, 
                        timeout=60, 
                        banner_timeout=30)

# starts an interactive session
channel = ssh.invoke_shell() 
# set buffer size via nbytes
out = channel.recv(9999)

# loop through the commands above, requires concat'ed '\n'
for command in commands:
    channel.send(command+'\n')
    

while not channel.recv_ready():
    time.sleep(1)
    
out = channel.recv(9999)
print(out.decode("ascii"))


print("closing connection now")
ssh.close()