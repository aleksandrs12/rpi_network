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

    # 1. Kill AP services
    print("Stopping AP services...")
    run("sudo systemctl stop hostapd dnsmasq")

    # 2. Start NetworkManager
    print("Starting NetworkManager...")
    run("sudo systemctl start NetworkManager")
    time.sleep(2) # Give it a beat to initialize

    # 3. DISCONNECT from whatever it automatically grabbed
    print("Dropping auto-connections...")
    run("sudo nmcli device disconnect wlan0")

    # 4. Connect to the SPECIFIC network
    print(f"Connecting to {ssid}...")
    # Use --wait to ensure the script doesn't move on until it's done
    cmd = f"sudo nmcli --wait 10 device wifi connect '{ssid}' password '{password}'"
    result = run(cmd)

    if result.returncode == 0:
        print("Success!")
        # Make NM the default for next boot so updates work
        run("sudo systemctl enable NetworkManager")
    else:
        print("Failed. Reverting...")
        run("sudo systemctl stop NetworkManager")
        run("sudo systemctl start hostapd")

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