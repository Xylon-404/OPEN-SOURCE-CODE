# Metadata Viewer Tool (Decoded from marshal)
# Author: Mohammad Rayhan Khan
# Github: https://github.com/lucifer-fernandez/MD-VIEWER.git

import os
import sys
import time
import subprocess

# Colors
RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
CYAN    = "\033[1;36m"
YELLOW  = "\033[1;33m"
MAGENTA = "\033[1;35m"
RESET   = "\033[0m"

PASSWORD = "RK4u"

def slow_print(text, delay=0.01):
    """Slow typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    clear()
    print(GREEN + """

 _______  _______ _________ _______  ______   _______ _________ _______ 
(       )(  ____ \__   __/(  ___  )(  __  \ (  ___  )\__   __/(  ___  )
| () () || (    \/   ) (   | (   ) || (  \  )| (   ) |   ) (   | (   ) |
| || || || (__       | |   | (___) || |   ) || (___) |   | |   | (___) |
| |(_)| ||  __)      | |   |  ___  || |   | ||  ___  |   | |   |  ___  |
| |   | || (         | |   | (   ) || |   ) || (   ) |   | |   | (   ) |
| )   ( || (____/\   | |   | )   ( || (__/  )| )   ( |   | |   | )   ( |
|/     \|(_______/   )_(   |/     \|(______/ |/     \|   )_(   |/     \|

         _________ _______           _______  _______                   
|\     /|\__   __/(  ____ \|\     /|(  ____ \(  ____ )                  
| )   ( |   ) (   | (    \/| )   ( || (    \/| (    )|                  
| |   | |   | |   | (__    | | _ | || (__    | (____)|                  
( (   ) )   | |   |  __)   | |( )| ||  __)   |     __)                  
 \ \_/ /    | |   | (      | || || || (      | (\ (                     
  \   /  ___) (___| (____/\| () () || (____/\| ) \ \__     Fucked By Xylon             
   \_/   \_______/(_______/(_______)(_______/|/   \__/                  

""" + CYAN + "======================================================================\n" +
    f"    Tools Author: {YELLOW}Mohammad Rayhan Khan\n"
    f"    {CYAN}Version     : {YELLOW}1.0\n"
    f"    {CYAN}Tool Name   : {YELLOW}Metadata Viewer\n"
    f"    {CYAN}Facebook    : {YELLOW}https://www.facebook.com/azad.farabi.2024\n"
    f"    {CYAN}Github      : {YELLOW}https://github.com/lucifer-fernandez/MD-VIEWER.git\n" +
    CYAN + "======================================================================\n"
    + RESET)

def auth():
    pwd = input(MAGENTA + "[*] Enter tool password: " + YELLOW)
    if pwd == PASSWORD:
        print(GREEN + "✔ Successfully accessed!" + RESET)
        return True
    else:
        print(RED + "✘ Incorrect password! You can't access the tool.\n" + RESET)
        return False

def get_metadata(file_path):
    """Run exiftool and return metadata"""
    try:
        result = subprocess.run(
            ["exiftool", file_path],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        print(RED + "[ERROR] " + str(e) + RESET)
        sys.exit(1)

def extract_gps(metadata):
    """Extract GPS coordinates if available"""
    gps_lat, gps_lon = None, None
    for line in metadata.split("\n"):
        if "-gpslatitude" in line.lower():
            gps_lat = line.split(":")[-1].strip()
        if "-gpslongitude" in line.lower():
            gps_lon = line.split(":")[-1].strip()

    if gps_lat and gps_lon:
        print(GREEN + "[+] GPS Location Found:" + RESET)
        print(f"    📍 Latitude : {gps_lat}")
        print(f"    📍 Longitude: {gps_lon}")
        print(f"    🌍 Google Maps: https://www.google.com/maps?q={gps_lat},{gps_lon}")
    else:
        print(RED + "[!] No GPS data found." + RESET)

def clean_metadata(file_path):
    """Remove all metadata and keep a backup"""
    backup_path = file_path + "_backup"
    os.system(f"cp '{file_path}' '{backup_path}'")
    os.system(f"exiftool -all= '{file_path}'")
    print(GREEN + "[✔] Metadata removed successfully." + RESET)
    print(YELLOW + f"[i] Backup saved at: {backup_path}" + RESET)

def main():
    banner()
    if not auth():
        return

    file_path = input(CYAN + "[?] Enter file path (e.g., /sdcard/DCIM/Camera/IMG_20246286_72528.jpg): " + RESET)

    if not os.path.isfile(file_path):
        print(RED + "[!] File not found!" + RESET)
        return

    print(YELLOW + "\n[*] Select an option:" + RESET)
    print("[1] View Metadata")
    print("[2] Remove Metadata (Privacy Mode)")

    choice = input("Enter choice (1/2): ")

    if choice == "1":
        print(GREEN + "\n[+] Reading file metadata...\n" + RESET)
        metadata = get_metadata(file_path)
        print("\t\t--- FILE METADATA ---")
        print(metadata)
        print("\t\t--- GPS INFO ---")
        extract_gps(metadata)
        print(GREEN + "✔ System closed..." + RESET)

    elif choice == "2":
        confirm = input(YELLOW + "\n[?] Are you sure you want to remove all metadata? (y/n): " + RESET).lower()
        if confirm == "y":
            clean_metadata(file_path)
        else:
            print(RED + "[-] Operation cancelled." + RESET)

    else:
        print(RED + "[!] Invalid choice." + RESET)


if __name__ == "__main__":
    main()
