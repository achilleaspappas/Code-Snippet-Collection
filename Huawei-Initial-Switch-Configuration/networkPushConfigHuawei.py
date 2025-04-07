import serial 
import time
import os
from netmiko import ConnectHandler
import paramiko
from scp import SCPClient
import logging
#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

# Initialize variables
serial_port = "COM5" 
baud_rate = 9600
username = "admin"
password = "admin@12345"
passwordDefault = "admin@huawei.com"
currentFolder = "Huawei\Switch_Initial_Config"
switchESN = "NULL"
device = {
    'device_type': 'huawei',
    'host': '172.16.0.1',
    'username': 'admin',
    'password': 'admin@12345',
    'port': 22
}

def funcSerial():
    # PySerial - Change Default Password
    print("Action: Initializing switch")
    with serial.Serial(serial_port, baudrate=baud_rate, timeout=1) as ser:
        try :
            ser.write(f"\n".encode())
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Username:" in prompt: 
                    print("Detected: Username")
                    ser.write(f"{username}\n".encode()) 
                    break
                time.sleep(1) 
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Password:" in prompt: 
                    print("Detected: Password")
                    ser.write(f"{passwordDefault}\n".encode())  
                    break
                time.sleep(1) 
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Change now? [Y/N]:" in prompt:
                    print ("Detected: Change now? [Y/N]")
                    ser.write(f"Y\n".encode())
                    break
                time.sleep(1)
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Please enter old password:" in prompt:
                    print ("Detected: Please enter old password")
                    ser.write(f"{passwordDefault}\n".encode())
                    break
                time.sleep(1)
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Please enter new password:" in prompt:
                    print ("Detected: Please enter new password")
                    ser.write(f"{password}\n".encode())
                    break
                time.sleep(1)
            while True:
                prompt = ser.readline().decode('utf-8')
                if "Please confirm new password:" in prompt:
                    print ("Detected: Please confirm new password")
                    ser.write(f"{password}\n".encode())
                    break
                time.sleep(1)
            while True:
                prompt = ser.readline().decode('utf-8')
                if "The password has been changed successfully." in prompt:
                    print ("Detected: The password has been changed successfully")
                    ser.write(f"\n".encode())
                    break
                time.sleep(1)

            # PySerial - Enable Temporary Management
            print("Action: Initializing management interface")
            ser.write(f"system-view\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"interface vlanif1\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"ip address 172.16.0.1 255.255.255.0\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"quit\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"stelnet server enable\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"scp server enable\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"user-interface vty 0 4\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"authentication-mode aaa\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"protocol inbound ssh\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"quit\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"aaa\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"local-user admin service-type terminal ssh http\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"quit\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"run save all\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
            ser.write(f"Y\n".encode())
            prompt = ser.readline().decode('utf-8')
            print("Detected:" + prompt)
            time.sleep(1)
        except:
            print("Detected: Connection closed by remote host.")
    ser.close()

def funcReadESN():
    # Read ESN from switch
    print("Action: Requesting ESN")
    with ConnectHandler(**device) as net_connect:
        global switchESN
        output = net_connect.send_command("display esn")
        switchESN = output.replace(" ", "")
        switchESN = switchESN.strip().split(':')[1]
        print("Detected: " + switchESN)
        if switchESN=="NULL":
            print("Error: Failed to detect ESN")
            exit(1)
    net_connect.disconnect()

def funcStackConfiguration():
    # Setup Stack Configuration
    print("Action: Applying stack configuration")
    with ConnectHandler(**device) as net_connect:
        esnStatus="NULL"
        stackStatusFile = os.path.join(currentFolder, "config_stack_status.txt") 
        print("File: " + stackStatusFile) 
        with open(stackStatusFile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(switchESN):
                    esnStatus = line.strip().split(':')[1] 
                    break
            if esnStatus != "1" and esnStatus != "0":
                print("Error: Cannot detect slot for " + switchESN)
                exit(1)
            print("Action: Applying stack configuration for slot " + esnStatus)
            while True:
                try: 
                    if esnStatus == "0" :
                        output = net_connect.send_command(command_string="sys\n", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack slot 0 priority 200", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack reserved-vlan 4093", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack timer mac-address switch-delay 10", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="interface stack-port 0/1", expect_string=r"-stack-port0/1]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="port interface GigabitEthernet0/0/47 enable", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"-stack-port0/1]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="interface stack-port 0/2", expect_string=r"-stack-port0/2]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="port interface GigabitEthernet0/0/48 enable", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"-stack-port0/2]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="quit", expect_string=r"HUAWEI]" , strip_prompt=False, strip_command=False)
                        break
                    elif esnStatus == "1" :
                        output = net_connect.send_command(command_string="sys\n", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack slot 0 renumber 1", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack slot 0 priority 180", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack reserved-vlan 4093", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="stack timer mac-address switch-delay 10", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="interface stack-port 0/1", expect_string=r"-stack-port0/1]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="port interface GigabitEthernet0/0/47 enable", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"-stack-port0/1]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="interface stack-port 0/2", expect_string=r"-stack-port0/2]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="port interface GigabitEthernet0/0/48 enable", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="Y", expect_string=r"-stack-port0/2]", strip_prompt=False, strip_command=False)
                        output = net_connect.send_command(command_string="quit", expect_string=r"HUAWEI]", strip_prompt=False, strip_command=False)
                        break
                    else:
                        print("Error: Slot was neither 0 or 1.")
                        break
                except:
                    print("Error: Failure while applying retrying...")
        f.close()
        print("Detected: Stack configuration completed.") 
    net_connect.disconnect()
    
def funcReboot():
    # Reboot the switch
    print("Action: Rebooting switch " + switchESN)
    with ConnectHandler(**device) as net_connect:
        try:
            output = net_connect.send_command(command_string="reboot", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
            output = net_connect.send_command(command_string="Y", expect_string=r"Y/N]", strip_prompt=False, strip_command=False)
            output = net_connect.send_command(command_string="Y", expect_string=r"Requesting system reboot", strip_prompt=False, strip_command=False)
        except:
            print("Detected: Connection closed by remote host.")
    net_connect.disconnect()

def funcTranferFiles():
    # Transfer files
    with ConnectHandler(**device) as net_connect:
        # Transfer configuration file to switch
        print("Action: Transfering Files")
        configurationsFolder = os.path.join(currentFolder, "Configurations")
        switchConfig = os.path.join(configurationsFolder, switchESN)
        switchConfig = switchConfig + ".txt"
        remote_file_config = 'flash:/vrpcfgnew_m.cfg'
        print("File: " + switchConfig)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(device['host'], username=device['username'], password=device['password'], port=device['port'])
        scp = SCPClient(ssh_client.get_transport())
        scp.put(switchConfig, remote_path=remote_file_config)
        print(f"Detected: File {switchConfig} successfully copied to {remote_file_config}")

        # Transfer cc file to switch
        switchCC = os.path.join(currentFolder, "S5735-L_V200R022C00SPC500.cc") 
        remote_file_cc = 'flash:/S5735-L_V200R022C00SPC500.cc'
        print("File: " + switchCC)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(device['host'], username=device['username'], password=device['password'], port=device['port'])
        scp = SCPClient(ssh_client.get_transport())
        scp.put(switchCC, remote_path=remote_file_cc)
        print(f"Detected: File {switchCC} successfully copied to {remote_file_cc}")
    
        # Transfer the file to switch
        switchPAT = os.path.join(currentFolder, "S5735-L-V200R022SPH150.pat")
        remote_file_pat = 'flash:/S5735-L-V200R022SPH150.pat'
        print("File: " + switchPAT)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(device['host'], username=device['username'], password=device['password'], port=device['port'])
        scp = SCPClient(ssh_client.get_transport())
        scp.put(switchPAT, remote_path=remote_file_pat)
        print(f"Detected: File {switchPAT} successfully copied to {remote_file_pat}")
    net_connect.disconnect()

def funcApplySoftware():
    # Apply software patches
    print("Action: Applying Firmware")
    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command(command_string="startup system-software S5735-L_V200R022C00SPC500.cc all")
        print("Detect: Firmware applied")
        output = net_connect.send_command(command_string="startup patch S5735-L-V200R022SPH150.pat slot 0")  
        print("Detect: Patch applied")
    net_connect.disconnect()

def funcApplyConfig():
    # Apply configuration
    print("Action: Applying Configuration")
    with ConnectHandler(**device) as net_connect:
        # Set tranfered configuration as startup configuration
        output = net_connect.send_command(command_string="startup saved-configuration vrpcfgnew_m.cfg") 
        print(f"Detected: Configuration applied")
    net_connect.disconnect()

def funcWait():
    # Wait for switch to reboot
    print("Action: Waiting for switch to come back online...")
    while True:
        try: 
            with ConnectHandler(**device) as net_connect:
                print("Detect: Device is online.")
            net_connect.disconnect()
            break
        except:
            time.sleep(10)

### Start ###
funcSerial()                # Inisialize switch and managemnt interface
funcWait()                  # Wait for switch to go online
funcReadESN()               # Read esn from switch
funcStackConfiguration()    # Apply stack configuration
funcTranferFiles()          # Transfer files
funcApplySoftware()         # Apply software
funcApplyConfig()           # Apply configuration
funcReboot()                # Reboot switch
print("!!! Success !!!")
### End ###