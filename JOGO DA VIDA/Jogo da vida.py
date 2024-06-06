import random
import pygame
import json
import os

# Constantes do jogo
LARGURA_GRID = 50
ALTURA_GRID = 25
TAMANHO_CELULA = 20
LARGURA_JANELA = LARGURA_GRID * TAMANHO_CELULA
ALTURA_JANELA = ALTURA_GRID * TAMANHO_CELULA + 40  # Espaço extra para controles

# Cores
COR_FUNDO = (0, 0, 0)
COR_CELULA_VIVA = (255, 255, 255)
COR_GRADE = (40, 40, 40)
COR_TEXTO = (255, 255, 255)

def inicializar_grid():
    """Inicializa o grid com células mortas."""
    return [[0 for _ in range(LARGURA_GRID)] for _ in range(ALTURA_GRID)]

def contar_vizinhos_vivos(grid, x, y):
    """Conta os vizinhos vivos de uma célula específica."""
    vizinhos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    contagem = 0
    for dx, dy in vizinhos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ALTURA_GRID and 0 <= ny < LARGURA_GRID:
            contagem += grid[nx][ny]
    return contagem

def atualizar_grid(grid):
    """Atualiza o grid de acordo com as regras do Jogo da Vida."""
    novo_grid = [[0 for _ in range(LARGURA_GRID)] for _ in range(ALTURA_GRID)]
    for x in range(ALTURA_GRID):
        for y in range(LARGURA_GRID):
            vizinhos_vivos = contar_vizinhos_vivos(grid, x, y)
            if grid[x][y] == 1:
                if vizinhos_vivos < 2 or vizinhos_vivos > 3:
                    novo_grid[x][y] = 0
                else:
                    novo_grid[x][y] = 1
            else:
                if vizinhos_vivos == 3:
                    novo_grid[x][y] = 1
    return novo_grid

def exibir_grid(screen, grid, velocidade, fonte, mensagem):
    """Exibe o grid e informações na janela do pygame."""
    screen.fill(COR_FUNDO)
    for x in range(ALTURA_GRID):
        for y in range(LARGURA_GRID):
            if grid[x][y] == 1:
                pygame.draw.rect(screen, COR_CELULA_VIVA,
                                 (y * TAMANHO_CELULA, x * TAMANHO_CELULA + 40, TAMANHO_CELULA, TAMANHO_CELULA))
            pygame.draw.rect(screen, COR_GRADE,
                             (y * TAMANHO_CELULA, x * TAMANHO_CELULA + 40, TAMANHO_CELULA, TAMANHO_CELULA), 1)
    pygame.draw.rect(screen, COR_GRADE, (0, 0, LARGURA_JANELA, 40))
    texto_controles = fonte.render(f"Espaço: Iniciar/Pausar | C: Limpar | S: Salvar | L: Carregar | ↑: Aumentar Velocidade | ↓: Diminuir Velocidade", True, COR_TEXTO)
    texto_velocidade = fonte.render(f"Velocidade: {velocidade}", True, COR_TEXTO)
    screen.blit(texto_controles, (10, 10))
    screen.blit(texto_velocidade, (10, 30))
    if mensagem:
        texto_mensagem = fonte.render(mensagem, True, COR_TEXTO)
        screen.blit(texto_mensagem, (10, 50))
    pygame.display.flip()

def salvar_grid(grid, nome_arquivo):
    """Salva o estado do grid em um arquivo JSON."""
    with open(nome_arquivo, 'w') as f:
        json.dump(grid, f)

def carregar_grid(nome_arquivo):
    """Carrega o estado do grid de um arquivo JSON."""
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            return json.load(f), None
    else:
        return None, f"Arquivo '{nome_arquivo}' não encontrado."

def obter_nome_arquivo(screen, fonte, titulo):
    """Obtém o nome do arquivo do usuário através da interface gráfica."""
    input_box = pygame.Rect(10, ALTURA_JANELA - 30, 140, 32)
    cor_input_box = pygame.Color('lightskyblue3')
    ativo = False
    texto = ''
    mensagem = titulo

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    ativo = not ativo
                else:
                    ativo = False
                cor_input_box = pygame.Color('dodgerblue2') if ativo else pygame.Color('lightskyblue3')
            elif event.type == pygame.KEYDOWN:
                if ativo:
                    if event.key == pygame.K_RETURN:
                        return texto
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += event.unicode

        screen.fill(COR_FUNDO)
        txt_surface = fonte.render(texto, True, cor_input_box)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, cor_input_box, input_box, 2)

        exibir_grid(screen, grid, velocidade, fonte, mensagem)
        pygame.display.flip()

def jogo_da_vida():
    """Executa o loop principal do Jogo da Vida."""
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Jogo da Vida de Conway")
    fonte = pygame.font.Font(None, 24)

    grid = inicializar_grid()
    clock = pygame.time.Clock()

    rodando = False
    desenhando = True
    velocidade = 10
    mensagem = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and desenhando:
                x, y = event.pos
                if y >= 40:  # Ignora clique na área de controle
                    grid[(y - 40) // TAMANHO_CELULA][x // TAMANHO_CELULA] = 1 - grid[(y - 40) // TAMANHO_CELULA][x // TAMANHO_CELULA]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rodando = not rodando
                    desenhando = not rodando
                elif event.key == pygame.K_c:
                    grid = inicializar_grid()
                    rodando = False
                    desenhando = True
                elif event.key == pygame.K_s:
                    nome_arquivo = obter_nome_arquivo(screen, fonte, "Salvar grid como")
                    if nome_arquivo:
                        salvar_grid(grid, nome_arquivo)
                        mensagem = f"Grid salvo como '{nome_arquivo}'"
                elif event.key == pygame.K_l:
                    nome_arquivo = obter_nome_arquivo(screen, fonte, "Carregar grid de")
                    if nome_arquivo:
                        grid_carregado, erro = carregar_grid(nome_arquivo)
                        if grid_carregado:
                            grid = grid_carregado
                            rodando = False
                            desenhando = True
                            mensagem = f"Grid carregado de '{nome_arquivo}'"
                        else:
                            mensagem = erro
                elif event.key == pygame.K_UP:
                    velocidade += 1
                elif event.key == pygame.K_DOWN:
                    velocidade -= 1

        if rodando:
            grid = atualizar_grid(grid)

        exibir_grid(screen, grid, velocidade, fonte, mensagem)
        clock.tick(velocidade)

if __name__ == "__main__":
    jogo_da_vida()
