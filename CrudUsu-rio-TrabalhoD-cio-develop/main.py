"""
SGBU - Sistema de Gerenciamento de Biblioteca Universitária
TecLearn Tabajara

Arquivo principal para iniciar o servidor.
Execute este arquivo para rodar o sistema.

Uso:
    python main.py
    
Acesse:
    http://localhost:8000/cadastro
"""

import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from View_and_Interface.view import run_server


def main():
    """Função principal que inicia o servidor"""
    print("=" * 60)
    print("  SGBU - Sistema de Gerenciamento de Biblioteca")
    print("  Universidade Tabajara - TecLearn")
    print("=" * 60)
    print()
    
    try:
        run_server(port=8000)
    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado com sucesso!")
        print("Até logo! 👋")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
