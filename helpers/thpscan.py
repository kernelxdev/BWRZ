import socket
import threading
import sys

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        if s.connect_ex((ip, port)) == 0:
            print(f"\033[32m[+] Port {port} is open\033[0m")
        s.close()
    except:
        pass

def pscan(ip, maximum_scan, num_threads):
    threads = []
    for port in range(1, maximum_scan + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <IP>")
        print("Example: python script.py 192.168.1.1")
        sys.exit(1)
    
    ip = sys.argv[1]
    
    try:
        maximum_scan = int(input("\nEnter the port number to scan up to: "))
        num_threads = int(input("\nEnter the number of threads to use: "))
        
        if num_threads > 120:
            print("Number of threads too high. Setting to 20.")
            num_threads = 20
        if maximum_scan > 65535:
            print("Maximum amount of ports too high! Setting to 8080")
            maximum_scan = 8080
            
        print(f"\nScanning {ip} from port 1 to {maximum_scan} with {num_threads} threads...")
        pscan(ip, maximum_scan, num_threads)
        
    except ValueError:
        print("Error: Please enter valid numbers")
        sys.exit(1)

if __name__ == "__main__":
    main()