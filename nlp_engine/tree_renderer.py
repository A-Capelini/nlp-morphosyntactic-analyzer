import svgling
from nltk.tree import Tree

# Tamanho de fonte maior que o padrão do svgling (16px) para melhorar a
# legibilidade das árvores, já que elas são o conteúdo pedagógico principal
# da tela.
DEFAULT_FONT_SIZE = 22
DEFAULT_TEXT_COLOR = "#0F172A"

def render_tree_to_svg(tree: Tree, font_size: int = DEFAULT_FONT_SIZE,
                        text_color: str = DEFAULT_TEXT_COLOR) -> str:
    """
    Converte uma árvore sintática do NLTK em uma string SVG estruturada.
    A substituição do método nativo Tree.draw() pelo svgling garante o
    funcionamento do portfólio em ambientes headless como o Streamlit Cloud.
    
    Args:
        tree (Tree): Objeto de árvore gerado pelos parsers do NLTK.
        font_size (int): Tamanho da fonte em px usada nos nós/folhas da árvore.
        text_color (str): Cor (hex) do texto dos nós/folhas da árvore.
        
    Returns:
        str: String contendo o código HTML/SVG para injeção na interface.
    """
    try:
        # A função draw_tree monta o layout e _repr_svg_ extrai o código vetorial puro
        svg_layout = svgling.draw_tree(tree, font_size=font_size, text_color=text_color)
        return svg_layout._repr_svg_()
    except Exception as e:
        return f"<div style='color: red;'>Erro na renderização visual: {e}</div>"

if __name__ == "__main__":
    # Teste de isolamento para verificar a extração correta da string SVG
    from nltk.tree import Tree
    
    # Simulação rápida de uma árvore para não depender do parser completo neste teste
    test_tree = Tree.fromstring("(S (NP (NN Teste)) (VP (VBD Concluido)))")
    svg_output = render_tree_to_svg(test_tree)
    
    if "<svg" in svg_output:
        print("Módulo de renderização SVG testado com sucesso. Código gerado inicia com:")
        print(svg_output[:100] + "...")
    else:
        print("Falha na geração do SVG.")
