from View_and_Interface import view as vw
from http.server import HTTPServer
import signal
import sys

def main():
    print("Iniciando Serviço de Biblioteca...\n")
    
    servidor = HTTPServer(("localhost", 8000), vw.BibliotecaView)
    print("Servidor rodando em http://localhost:8000")
    print("Acesse: http://localhost:8000/emprestimos")
    print("Pressione Ctrl+C para encerrar\n")
    
    # Trata Ctrl+C para parar o servidor
    def parar_servidor(sig, frame):
        print("\n\n🛑 Encerrando servidor...")
        servidor.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, parar_servidor)
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor encerrado!")
        sys.exit(0)

if __name__ == "__main__":
    main()