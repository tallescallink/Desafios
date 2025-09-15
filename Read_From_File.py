# VERSÃO ATUALIZADA PARA LER O CONTO, OU SEJA LER LETRAS E NÚMEROS COMO PALAVRAS (DESCONSIDERA PONTUAÇÃO)
import re
from collections import Counter

with open('Dracula.txt', 'r', encoding='utf-8') as file:
    text = file.read().split()
    #words = re.findall(r'\w+', text, flags=re.UNICODE)
    words =[]
    #count = Counter(words)
    for i in text:
        words.append(i)
print(Counter(words))




# 1ª VERSÃO
# from collections import Counter
# with open('Dracula.txt', 'r', encoding='utf-8') as file:
#     content = file.read().split()
#     list_count = Counter(content)
#     for word, mount in list_count.items():
# #print(f'{word}: {mount}')  # Opicional
#         print('--- File Content ---')
# print(content)


# DEEPSEEK
from collections import Counter
import re
from rich.console import Console
from rich.table import Table
from rich import box
import matplotlib.pyplot as plt
import numpy as np

console = Console()

def analise_profunda_texto():
    """Análise profunda e visual do texto"""
    
    try:
        # Leitura do arquivo com tratamento elegante
        with open('Dracula.txt', 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            
            console.print("\n[bold cyan]📖 TEXTO COMPLETO:[/bold cyan]")
            console.print("═" * 80)
            console.print(conteudo)
            console.print("═" * 80)
            
            # Análise avançada
            palavras = re.findall(r'\b\w+\b', conteudo.lower())
            contador = Counter(palavras)
            
            # Tabela elegante com rich
            tabela = Table(title="📊 ANÁLISE ESTATÍSTICA DAS PALAVRAS", box=box.ROUNDED)
            tabela.add_column("Palavra", style="cyan", no_wrap=True)
            tabela.add_column("Frequência", style="magenta")
            tabela.add_column("Percentual", style="green")
            
            total_palavras = sum(contador.values())
            
            for palavra, freq in contador.most_common(15):
                percentual = (freq / total_palavras) * 100
                tabela.add_row(palavra, str(freq), f"{percentual:.2f}%")
            
            console.print(tabela)
            
            # Estatísticas gerais
            console.print(f"\n[bold yellow]📈 ESTATÍSTICAS GERAIS:[/bold yellow]")
            console.print(f"• Total de palavras: [green]{total_palavras}[/green]")
            console.print(f"• Palavras únicas: [blue]{len(contador)}[/blue]")
            console.print(f"• Palavra mais comum: [red]'{contador.most_common(1)[0][0]}'[/red]")
            
            # Análise de sentenças
            sentencas = re.split(r'[.!?]+', conteudo)
            console.print(f"• Número de sentenças: [cyan]{len([s for s in sentencas if s.strip()])}[/cyan]")
            
    except FileNotFoundError:
        console.print("[bold red]❌ Arquivo não encontrado![/bold red]")
    except Exception as e:
        console.print(f"[bold red]⚠️ Erro: {e}[/bold red]")

def visualizacao_grafica():
    """Cria visualização gráfica dos dados"""
    try:
        with open('Dracula.txt', 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            palavras = re.findall(r'\b\w+\b', conteudo.lower())
            contador = Counter(palavras)
            
            # Prepara dados para o gráfico
            top_10 = contador.most_common(10)
            palavras_top = [item[0] for item in top_10]
            frequencias = [item[1] for item in top_10]
            
            # Cria gráfico
            plt.figure(figsize=(12, 8))
            bars = plt.barh(palavras_top, frequencias, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D', '#6A0572'])
            plt.xlabel('Frequência')
            plt.title('TOP 10 PALAVRAS MAIS FREQUENTES - AS NOIVAS DO CONDE')
            plt.gca().invert_yaxis()
            
            # Adiciona valores nas barras
            for bar in bars:
                width = bar.get_width()
                plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                        f'{width}', ha='left', va='center')
            
            plt.tight_layout()
            plt.show()
            
    except Exception as e:
        console.print(f"[red]Erro na visualização: {e}[/red]")

if __name__ == "__main__":
    console.print("[bold magenta]🔮 ANÁLISE PROFUNDA DO TEXTO 'AS NOIVAS DO CONDE'[/bold magenta]")
    console.print("🌙" * 30)
    
    analise_profunda_texto()
    
    # Pergunta se quer ver gráfico
    if console.input("\n📊 Deseja ver visualização gráfica? (s/n): ").lower() == 's':
        visualizacao_grafica()
    
    console.print("\n[bold green]✅ Análise concluída![/bold green]")