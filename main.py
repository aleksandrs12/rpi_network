import os
import subprocess
import time

# Yes, this was vibecoded 
HOSTAPD_SERVICE = "hostapd"
DNSMASQ_SERVICE = "dnsmasq"
NETWORK_MANAGER = "NetworkManager"

def run(cmd):
    subprocess.run(cmd, shell=True)

def start_hotspot():
    print("Switching to hotspot mode...")

    run("sudo systemctl disable NetworkManager")
    run("sudo systemctl enable hostapd")
    run("sudo systemctl enable dnsmasq")

    # delayed execution so SSH session doesn't die immediately
    run('sudo bash -c "sleep 5; systemctl stop NetworkManager; systemctl restart hostapd; systemctl restart dnsmasq" &')

    print("Hotspot starting in ~10 seconds.")
    print("Reconnect to hotspot network afterwards.")

def connect_wifi():
    ssid = input("Enter WiFi SSID: ")
    password = input("Enter WiFi password: ")

    print("Configuring WiFi...")

    # create wpa config
    config = f'''
country=LV
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}
'''

    with open("/tmp/wpa_supplicant.conf", "w") as f:
        f.write(config)

    run("sudo mv /tmp/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")

    run("sudo systemctl enable NetworkManager")
    run("sudo systemctl disable hostapd")
    run("sudo systemctl disable dnsmasq")

    run('sudo bash -c "sleep 5; systemctl stop hostapd; systemctl stop dnsmasq; systemctl start NetworkManager" &')

    print("Connecting to WiFi in ~10 seconds.")
    print("SSH will reconnect via the router.")

def menu():
    print("\nWiFi Mode Selector")
    print("------------------")
    print("1) Start Hotspot (default on boot)")
    print("2) Connect to WiFi network")
    print("3) Exit")

    choice = input("Select option: ")

    if choice == "1":
        start_hotspot()

    elif choice == "2":
        connect_wifi()

    else:
        print("Exiting")

if __name__ == "__main__":
    menu()