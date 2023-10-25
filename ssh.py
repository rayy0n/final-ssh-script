import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Create the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password: ', pexpect.TIMEOUT, pexpect.EOF])

# Check for errors
if result != 0:
    print('---FAILURE! creating session for: ', ip_address)
    exit()

# Session expecting password
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# Check for error
if result != 0:
    print('---FAILURE! entering password: ', password)
    exit()

# Capture the running configuration
session.sendline('show running-config')
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error
if result != 0:
    print('---FAILURE! capturing running configuration')

# Save the running configuration to a file locally
with open('running-config.txt', 'w') as config_file:
    config_file.write(session.before)

# Change hostname of router

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# CHECK FOR ERROR
if result != 0:
    print('FAILURE! entering enable mode')
    exit()

# Send enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error
if result != 0:
    print('FAILURE! entering enable mode after sending password')
    exit()

#change to configuration mode on the router
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

#check for error
if result != 0:
    print('FAILURE! entering config mode')
    exit()

# Change the hostname to 'R1' 
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

#check for error
if result != 0:
    print('---FAILURE! setting hostname')

# Exit config mode 
session.sendline('exit')

# Exit enable mode 
session.sendline('exit')

# Display success message
print('-----------------------------------------')
print('')
print('---Success! connecting to: ', ip_address)
print('---                Username: ', username)
print('---                Password: ', password)
print('')
print('-----------------------------------------')

# Terminate SSH session
session.close()
