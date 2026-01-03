import grpc
from concurrent import futures
import os
import family_pb2
import family_pb2_grpc
class UyeServisi(family_pb2_grpc.FamilyServiceServicer):
    def __init__(self, port):
        self.port = port
        self.mesaj_sayisi = 0
        # Her üye için ayrı bir klasör oluşturulabilir
        if not os.path.exists(f"data_{port}"):
            os.makedirs(f"data_{port}")

    # Liderden gelen mesajı alma ve kaydetme
    def ReceiveChat(self, request, context):
        # Diske yazma işlemi (Puan tablosundaki IO gereksinimi için)
        file_path = f"data_{self.port}/{request.text[:5]}.txt"
        with open(file_path, "w") as f:
            f.write(request.text)
        
        self.mesaj_sayisi += 1
        print(f"Mesaj alindi ve kaydedildi. Toplam: {self.mesaj_sayisi}")
        return family_pb2.Empty()

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    family_pb2_grpc.add_FamilyServiceServicer_to_server(UyeServisi(port), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Üye {port} portunda baslatildi...")
    server.wait_for_termination()

if __name__ == "__main__":
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "5555"
    serve(port)