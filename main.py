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

    print("Prepping interface (Stopping AP)...")
    # 1. Stop the AP services first so the hardware is free
    run("sudo systemctl stop hostapd")
    run("sudo systemctl stop dnsmasq")
    
    print("Starting NetworkManager...")
    run("sudo systemctl start NetworkManager")
    
    # 2. Give the radio a moment to wake up
    time.sleep(2) 

    print(f"Attempting to connect to {ssid}...")
    # 3. Use --ask or explicit variables to ensure it targets the right one
    cmd = f"sudo nmcli device wifi connect '{ssid}' password '{password}'"
    result = run(cmd)

    if result.returncode != 0:
        print("WiFi connection failed. Reverting to AP...")
        run("sudo systemctl stop NetworkManager")
        run("sudo systemctl start hostapd")
        return

    print("Connected successfully.")
    # 4. Make it permanent for this session
    run("sudo systemctl enable NetworkManager") 
    print("Switching complete. Use 'ifconfig' to find your new IP.")

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