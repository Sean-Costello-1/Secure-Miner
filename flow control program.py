#Import necessary libraries
import subprocess   #Source: https://docs.python.org/3/library/subprocess.html
import time         #Source: https://docs.python.org/3/library/time.html
import pynvml       #Source: https://pypi.org/project/pynvml/

#Set OpenVPN executable location path
OpenVPN_exe_location_path = input("Enter the location path (default location: C:\\\\Program Files\\\\OpenVPN\\\\bin\\\\openvpn.exe) to the OpenVPN.exe: ")  #Note: The user will need to set this for the user's specific file location.

#Set OpenVPN configuration file location path
OpenVPN_config_location_path = input("Enter the location path (example: C:\\\\Users\\\\username\\\\OpenVPN\\\\config\\\\client\\\\client.ovpn) to the client's .ovpn configuration file: ")  #Note: The user will need to set this for the user's specific file location.

#Set Hyper-V VM Name
VM_Name = input("Enter the name (default name: Secure Miner) of the Hyper-V VM: ")    #Note: This is the default name given to the Hyper-V VM (change if necessary).

#Initialize program
def init():
    print("***************************************************************************")
    print("Welcome to Secure Miner!")
    print("Please do not close this Command Prompt window.")
    print("Ensure you are running this program with administrative privileges.")
    print("***************************************************************************\n")

#Establish OpenVPN connection
def start_openvpn_connection():
    try:
        print("Establishing OpenVPN client-server connection in a new window. Please do not close the new window.")
        #Start OpenVPN client-server connection in a nem Command Prompt Window
        command = f'cmd /c start cmd.exe /k "\"{OpenVPN_exe_location_path}\" --config \"{OpenVPN_config_location_path}\""'  #Source: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd
        subprocess.call(command, shell = True)  #Source: https://docs.python.org/3/library/subprocess.html#subprocess.call
        #Set wait time for connection in seconds and allow for password entry (adjust as needed)
        time.sleep(30)  #Source: https://docs.python.org/3/library/time.html#time.sleep
    except Exception as e:
        print(f"OpenVPN client-server connection failed: {e}")  #Source: https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/#

#Verify OpenVPN connection
def verify_openvpn_connection():
    try:
        print("Verifying OpenVPN client-server connection. Please wait...")
        #Get "ipconfig" command output
        ipconfig_output = subprocess.check_output("ipconfig", encoding = "utf-8")   #Source: https://docs.python.org/3/library/subprocess.html#subprocess.check_output
        #Check if OpenVPN network adapter is present
        if "OpenVPN" in ipconfig_output:
            print("OpenVPN connection likely established.")
        else:
            #Attempt to establish OpenVPN client-server connection
            print("OpenVPN client-server connection could not be established. Attempting to establish OpenVPN client-server connection. Please wait...")
            start_openvpn_connection()
    except Exception as e:
        print(f"OpenVPN client-server connection failed: {e}")

#Verify GPU availability
def verify_gpu_availability():
    print("Verifying GPU availability. Please wait..")
    try:
        #Initialize NVIDIA Management Library (NVML) Python wrapper     Source: https://developer.nvidia.com/nvidia-management-library-nvml
        pynvml.nvmlInit()
        #Get number of GPUs
        number_of_gpus = pynvml.nvmlDeviceGetCount()
        if number_of_gpus > 0:
            print(f"{number_of_gpus} GPU(s) detected.")
            for i in range(number_of_gpus):
                #Get name of each available GPU
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                print(f"{name}")
        else:
            print("No GPU(s) detected.")
    except pynvml.NVMLError as error:
        print(f"GPU availability verification check failed: {error}")
    finally:
        pynvml.nvmlShutdown()

#Verify Hyper-V VM is running
def verify_hyper_v_vm_is_running():
    try:
        print("Checking that the specified Hyper-V VM is running. Please wait..")
        #Construct PowerShell command to get VM state
        command = f"Get-VM -Name {VM_Name} | Select-Object -ExpandProperty State"   #Source: https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vm?view=windowsserver2022-ps
        command_output = subprocess.check_output(["powershell.exe", "-Command", command], encoding = "utf-8").strip()   #Source: https://www.w3schools.com/python/ref_string_strip.asp
        #Check command output for specified VM's current state
        if command_output == "Running":     #Source: https://stackoverflow.com/questions/44623440/possible-values-for-state-status-of-virtual-machines
            print(f"{VM_Name} is running.")
        elif command_output == "Off":
            print(f"{VM_Name} is off.")
        else:
            print(f"{VM_Name} is in an unknown state.")
    except Exception as e:
        print(f"{VM_Name} could not be found or an error occurred: {e}")

#Give user option to run whole program or only part of the program
def run():
    #Give user the option to run the full program or only verify that OpenVPN and the Hyper-V VM are running
    start_OpenVPN = input("Would you like to run entire program (Y/y) or just verify the OpenVPN connection is established and that the Hyper-V VM is running (N/n)? ")
    #Run the full program
    if start_OpenVPN == "Y" or start_OpenVPN == "y":
        init()
        start_openvpn_connection()
        verify_openvpn_connection()
        verify_gpu_availability()
        verify_hyper_v_vm_is_running()
    #Only verify that OpenVPN and the Hyper-V VM are running
    elif start_OpenVPN == "N" or start_OpenVPN == "n":
        init()
        verify_openvpn_connection()
        verify_hyper_v_vm_is_running()
    else:
        print("Please enter either Y or N.")
        run()

if __name__ == "__main__":
    run()
    print("\n*********************************************************************************************************************************************************************************************\n")
    print("Thank you for using Secure Miner. You may now close this Command Prompt window and begin mining. Please keep the other Command Prompt window open so OpenVPN can continue running.")
    print("\n*********************************************************************************************************************************************************************************************\n")