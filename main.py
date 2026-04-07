import subprocess
import time
import sys

AP_IP = "10.3.141.1"

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def enable_ap_boot():
    print("Ensuring AP is default on boot...")
    run("sudo systemctl enable hostapd")
    run("sudo systemctl enable dnsmasq")
    run("sudo systemctl disable NetworkManager")

def start_ap_now():
    print("Starting hotspot...")
    run('sudo bash -c "sleep 3; systemctl stop NetworkManager; systemctl restart hostapd; systemctl restart dnsmasq" &')
    print(f"Reconnect via hotspot (usually {AP_IP})")

def connect_wifi():
    ssid = input("SSID: ")
    password = input("Password: ")

    print("Transitioning to WiFi Client mode...")
    
    # Create a small shell script on the fly to handle the transition 
    # independent of this Python process
    transition_cmd = (
        f"sleep 2 && "
        f"systemctl stop hostapd dnsmasq && "
        f"systemctl start NetworkManager && "
        f"nmcli dev wifi connect '{ssid}' password '{password}'"
    )
    
    # Run this in the background and exit immediately
    subprocess.Popen(['sudo', 'bash', '-c', transition_cmd])
    
    print("Commands sent. Connection will drop now.")
    print("Check your phone's hotspot list in 15 seconds.")
    sys.exit()

def menu():
    enable_ap_boot()

    print("\nWiFi / Hotspot Manager")
    print("----------------------")
    print("1) Start hotspot now")
    print("2) Connect to WiFi")
    print("3) Exit")

    choice = input("Choice: ")

    if choice == "1":
        start_ap_now()

    elif choice == "2":
        connect_wifi()

    else:
        sys.exit()

if __name__ == "__main__":
    menu()