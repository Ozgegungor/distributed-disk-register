import socket  
import os      
import grpc    
import family_pb2      
import family_pb2_grpc 
def read_tolerance():  #tolerance.conf dosyası burda okunuyor.
    if os.path.exists("tolerance.conf"):
        with open("tolerance.conf", "r") as f:
            val = f.read().strip()
            print(f"Lider Baslatildi. Hata Toleransi: {val}")
            return int(val)
    return 1 

def start_lider():
    tolerance_level = read_tolerance() 
    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 6666))
    server.listen(5)
    
    active_members = [] 

    print("Lider 6666 portunda istemci bekleniyor...")

    while True:
        client_sock, addr = server.accept()
        data = client_sock.recv(1024).decode('utf-8').strip()
        
        if data:
            parts = data.split(" ", 2) 
            command = parts[0].upper()

            if command == "SET":
                msg_id = parts[1]
                content = parts[2]
                print(f"SET istegi alindi. ID: {msg_id}, Mesaj: {content}")
                
                print(f"Mesaj {tolerance_level} adet üyeye kopyalanacak...") 
                
                client_sock.send("OK\n".encode('utf-8'))  

            elif command == "GET":
                msg_id = parts[1]
                print(f"GET istegi alindi. ID: {msg_id}")
                client_sock.send("MESAJ_ICERIGI\n".encode('utf-8'))

        client_sock.close()

if __name__ == "__main__":
    start_lider()