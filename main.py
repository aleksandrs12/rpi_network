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

    print("Attempting WiFi connection...")

    # ensure NetworkManager is running temporarily
    run("sudo systemctl start NetworkManager")

    # try connecting
    cmd = f"nmcli dev wifi connect '{ssid}' password '{password}'"
    result = run(cmd)

    if result.returncode != 0:
        print("WiFi connection failed.")
        print("Keeping AP mode as boot default.")
        print(result.stderr.strip())
        return

    print("Connected successfully.")

    # schedule switch so SSH doesn't die immediately
    run('sudo bash -c "sleep 5; systemctl stop hostapd; systemctl stop dnsmasq; systemctl enable NetworkManager; systemctl restart NetworkManager" &')

    print("Switching to WiFi mode in ~5 seconds.")
    print("SSH will reconnect via your router.")

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