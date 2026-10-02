import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def add_box(ax, center, text, width=0.24, height=0.12, facecolor="#D9EAF7", edgecolor="#1F4E79"):
    x, y = center
    rect = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        linewidth=2,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=11, color="#0B1F33", wrap=True)
    return rect


fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Nodos principais do fluxo
add_box(ax, (0.12, 0.88), "1. Início\npytest / execução dos testes", 0.22, 0.12)
add_box(ax, (0.38, 0.88), "2. conftest.py\nlimpeza de artefatos\nChrome + logs + setup", 0.28, 0.16)
add_box(ax, (0.64, 0.88), "3. LoginPage\nabre URL e faz login", 0.22, 0.12)
add_box(ax, (0.87, 0.88), "4. InventoryPage\nprodutos + carrinho", 0.24, 0.12)

add_box(ax, (0.50, 0.62), "5. Testes\ntest_login.py\ntest_inventory.py", 0.28, 0.16)
add_box(ax, (0.50, 0.40), "6. Validações\nasserts + mensagens de erro", 0.28, 0.14)
add_box(ax, (0.26, 0.18), "7. Evidências\nAllure + screenshots + logs", 0.30, 0.14)
add_box(ax, (0.74, 0.18), "8. Resultado\nSucesso ou falha final", 0.24, 0.12)

# Fluxo principal
arrows = [
    ((0.23, 0.88), (0.25, 0.88)),
    ((0.49, 0.88), (0.51, 0.88)),
    ((0.75, 0.88), (0.76, 0.88)),
    ((0.50, 0.78), (0.50, 0.70)),
    ((0.50, 0.54), (0.50, 0.47)),
    ((0.42, 0.40), (0.35, 0.25)),
    ((0.58, 0.40), (0.65, 0.25)),
]

for start, end in arrows:
    arrow = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=18, linewidth=1.8, color="#2E6F9A")
    ax.add_patch(arrow)

# Fluxo adicional: LoginPage -> Testes -> InventoryPage
arrow1 = FancyArrowPatch((0.64, 0.82), (0.58, 0.70), arrowstyle='-|>', mutation_scale=16, linewidth=1.8, color="#2E6F9A")
arrow2 = FancyArrowPatch((0.87, 0.82), (0.60, 0.70), arrowstyle='-|>', mutation_scale=16, linewidth=1.8, color="#2E6F9A")
ax.add_patch(arrow1)
ax.add_patch(arrow2)

# Título
ax.text(0.50, 0.98, "Fluxograma do Projeto de Automação Web - SauceDemo", ha="center", va="center", fontsize=18, fontweight="bold", color="#123B59")

output = "fluxograma_projeto.pdf"
plt.savefig(output, format="pdf", bbox_inches="tight", dpi=200)
print(f"PDF gerado: {output}")
