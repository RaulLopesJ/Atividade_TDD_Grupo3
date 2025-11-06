from View_and_Interface import view as vw
from http.server import HTTPServer

def main():
    print("Iniciando Serviço de Biblioteca...\n")
    
    servidor = HTTPServer(("localhost", 8000), vw.BibliotecaController)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()

if __name__ == "__main__":
    main()