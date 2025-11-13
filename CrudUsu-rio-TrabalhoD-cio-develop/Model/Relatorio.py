"""
Model: Relatorio
Módulo 4 - Relatórios

Este arquivo deve ser implementado pelos alunos usando TDD (Test Driven Development).

Requisitos:
- Classe Relatorio com métodos para gerar relatórios e estatísticas
- Métodos:
  * livros_mais_emprestados(limite=10)
  * usuarios_mais_ativos(limite=10)
  * livros_por_categoria()
  * taxa_ocupacao()
  * emprestimos_por_periodo(data_inicio, data_fim)
  * total_emprestimos_ativos()
  * emprestimos_em_atraso()

Exemplos de testes a implementar:
- test_livros_mais_emprestados()
- test_usuarios_mais_ativos()
- test_calcular_taxa_ocupacao()
- test_filtrar_emprestimos_por_periodo()
- test_contar_emprestimos_ativos()
- test_listar_emprestimos_atrasados()
"""

from Model import Livro as l
from Model import Usuario as u
from Model import Emprestimo as e

class Relatorio:
    """
    Classe responsável por gerar relatórios e estatísticas do sistema.
    Espera receber listas de objetos (usuarios, livros, emprestimos)
    vindos de outros módulos do projeto.
    """

    def __init__(self, usuarios, livros, emprestimos):
        self.usuarios = usuarios or []
        self.livros = livros or []
        self.emprestimos = emprestimos or []

    def get_livros(self) -> list[l.Livro]:
        return self.livros

    def get_usuarios(self) -> list[u.Usuario]:
        return self.usuarios
    
    def get_emprestimos(self) -> list[e.Emprestimo]:
        return self.emprestimos

    def set_livros(self, livros):
        self.livros = livros or []

    def set_usuarios(self, usuarios):
        self.usuarios = usuarios or []

    def set_emprestimos(self, emprestimos):
        self.emprestimos = emprestimos or []

    # ========== MÉTODOS DE RELATÓRIO ==========

    def livros_mais_emprestados(self, limite=10):
        """
        Retorna os livros mais emprestados.
        
        Args:
            limite: Número máximo de livros a retornar
            
        Returns:
            Lista de dicts com formato: 
            [{'livro': Livro, 'quantidade': int}, ...]
        """
        from collections import Counter
        
        if not self.emprestimos:
            return []
        
        # Conta quantas vezes cada livro foi emprestado
        isbn_counter = Counter(emp.livro.isbn for emp in self.emprestimos)
        mais_emprestados = isbn_counter.most_common(limite)
        
        # Cria mapa de ISBN para Livro
        isbn_para_livro = {livro.isbn: livro for livro in self.livros}
        
        # Retorna resultado com objeto Livro e quantidade
        resultado = []
        for isbn, qtd in mais_emprestados:
            if isbn in isbn_para_livro:
                resultado.append({
                    'livro': isbn_para_livro[isbn],
                    'quantidade': qtd
                })
        
        return resultado

    def usuarios_mais_ativos(self, limite=10):
        """
        Retorna os usuários com mais empréstimos.
        
        Args:
            limite: Número máximo de usuários a retornar
            
        Returns:
            Lista de dicts com formato:
            [{'usuario': Usuario, 'quantidade': int}, ...]
        """
        from collections import Counter
        
        if not self.emprestimos:
            return []
        
        # Conta quantas vezes cada usuário fez empréstimo
        usuario_counter = Counter(emp.usuario.matricula for emp in self.emprestimos)
        mais_ativos = usuario_counter.most_common(limite)
        
        # Cria mapa de matrícula para Usuario
        matricula_para_usuario = {u.matricula: u for u in self.usuarios}
        
        # Retorna resultado com objeto Usuario e quantidade
        resultado = []
        for matricula, qtd in mais_ativos:
            if matricula in matricula_para_usuario:
                resultado.append({
                    'usuario': matricula_para_usuario[matricula],
                    'quantidade': qtd
                })
        
        return resultado

    def taxa_ocupacao(self):
        """
        Calcula a taxa de ocupação (percentual de livros emprestados).
        
        Returns:
            Dict com:
            - 'total_livros': Total de livros no catálogo
            - 'livros_emprestados': Quantidade de livros em empréstimo
            - 'taxa_percentual': Taxa em percentual (0-100)
            - 'taxa_decimal': Taxa decimal (0-1)
        """
        if not self.livros:
            return {
                'total_livros': 0,
                'livros_emprestados': 0,
                'taxa_percentual': 0,
                'taxa_decimal': 0
            }
        
        # Conta livros em empréstimo (status = "emprestado")
        livros_emprestados = len([l for l in self.livros if l.status and l.status.lower() == 'emprestado'])
        
        total_livros = len(self.livros)
        taxa_decimal = livros_emprestados / total_livros if total_livros > 0 else 0
        taxa_percentual = taxa_decimal * 100
        
        return {
            'total_livros': total_livros,
            'livros_emprestados': livros_emprestados,
            'taxa_percentual': round(taxa_percentual, 2),
            'taxa_decimal': round(taxa_decimal, 4)
        }

    def emprestimos_por_periodo(self, data_inicio, data_fim):
        """
        Retorna empréstimos em um período específico.
        
        Args:
            data_inicio: Data inicial (datetime ou string 'YYYY-MM-DD')
            data_fim: Data final (datetime ou string 'YYYY-MM-DD')
            
        Returns:
            Lista de empréstimos no período
        """
        from datetime import datetime
        
        # Converte strings para datetime se necessário
        if isinstance(data_inicio, str):
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        if isinstance(data_fim, str):
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        
        # Filtra empréstimos no período
        emprestimos_filtrados = []
        for emp in self.emprestimos:
            if hasattr(emp.loan_date, 'date'):
                data_emp = emp.loan_date.date()
            else:
                data_emp = emp.loan_date
            
            if data_inicio.date() <= data_emp <= data_fim.date():
                emprestimos_filtrados.append(emp)
        
        return emprestimos_filtrados

    def total_emprestimos_ativos(self):
        """
        Retorna total de empréstimos com status ATIVO.
        
        Returns:
            Int com quantidade de empréstimos ativos
        """
        return len([emp for emp in self.emprestimos if emp.status == 'ATIVO'])

    def emprestimos_em_atraso(self):
        """
        Retorna empréstimos que estão atrasados.
        
        Returns:
            Lista de empréstimos atrasados
        """
        return [emp for emp in self.emprestimos if emp.esta_em_atraso()]

    def estatisticas_gerais(self):
        """
        Retorna estatísticas gerais do sistema.
        
        Returns:
            Dict com métricas gerais
        """
        return {
            'total_usuarios': len(self.usuarios),
            'total_livros': len(self.livros),
            'total_emprestimos': len(self.emprestimos),
            'emprestimos_ativos': self.total_emprestimos_ativos(),
            'emprestimos_atrasados': len(self.emprestimos_em_atraso()),
            'taxa_ocupacao': self.taxa_ocupacao(),
            'livro_mais_emprestado': self.livros_mais_emprestados(1)[0] if self.livros_mais_emprestados(1) else None,
            'usuario_mais_ativo': self.usuarios_mais_ativos(1)[0] if self.usuarios_mais_ativos(1) else None
        }

    def relatorio_completo(self):
        """
        Gera relatório completo com todas as métricas.
        
        Returns:
            Dict com todas as informações do sistema
        """
        return {
            'estatisticas_gerais': self.estatisticas_gerais(),
            'livros_mais_emprestados': self.livros_mais_emprestados(10),
            'usuarios_mais_ativos': self.usuarios_mais_ativos(10),
            'taxa_ocupacao': self.taxa_ocupacao(),
            'emprestimos_ativos': self.total_emprestimos_ativos(),
            'emprestimos_atrasados': self.emprestimos_em_atraso()
        }
