import pygame
import os
import random
import math

pygame.init()

# Configuración de la cuadrícula y la ventana
MARGEN = 70
FILAS, COLUMNAS = 21, 19
TAM_CELDA = 35
ANCHO, ALTO = COLUMNAS * TAM_CELDA + 2 * MARGEN, FILAS * TAM_CELDA + 2 * MARGEN

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fantasmas")
clock = pygame.time.Clock()
fps = 30

# Velocidades
pasos_pacman = 5  # Pac-Man se mueve cada 4 fotogramas
pasos_fantasmas = 18  # Los fantasmas se mueven cada 5 fotogramas

# Contadores
contador_pacman = 0
contador_fantasmas = 0

# Colores
CYAN, NEGRO, ROJO, AMARILLO = (0, 255, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0)

mapa =  [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

excepciones_circulos = [(10,8),(10,9),(10,10),(8,18),(8,16),(8,17),(12,18),(12,16),(12,17),(12,1),(12,2),(12,0),(8,1),(8,2),(8,0)] 
def dibujar_mapa():
    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            color = (0, 0, 255) if mapa[fila][col] == 1 else (0, 0, 0)
            pygame.draw.rect(ventana, color, (col * TAM_CELDA + MARGEN, fila * TAM_CELDA + MARGEN, TAM_CELDA, TAM_CELDA))
            if mapa[fila][col] == 0 and (fila, col) not in excepciones_circulos:
                pygame.draw.circle(ventana, (255, 255, 0), (col * TAM_CELDA + MARGEN + TAM_CELDA // 2, fila * TAM_CELDA + MARGEN + TAM_CELDA // 2), TAM_CELDA // 4)

# Cargar imágenes de fantasmas
DIRECTORIO_FANTASMAS = "assents/images/fantasmas"
animaciones_fantasmas = {}

def cargar_imagenes():
    for nombre in os.listdir(DIRECTORIO_FANTASMAS):
        ruta = os.path.join(DIRECTORIO_FANTASMAS, nombre)
        if os.path.isdir(ruta):
            animaciones_fantasmas[nombre] = {}
            for direccion in ["izquierda", "derecha", "arriba", "abajo"]:
                animaciones_fantasmas[nombre][direccion] = []
                for i in range(2):
                    imagen_path = os.path.join(ruta, f"{nombre}_{direccion}_{i+1}.png")
                    if os.path.exists(imagen_path):
                        imagen = pygame.image.load(imagen_path).convert_alpha()
                        imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
                        animaciones_fantasmas[nombre][direccion].append(imagen)
cargar_imagenes()

# Pac-Man
DIRECTORIO_PACMAN = "assents/images/pacman"
animaciones_pacman = {}

def cargar_imagenes_pacman():
    for direccion in ["izquierda", "derecha", "arriba", "abajo"]:
        animaciones_pacman[direccion] = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(DIRECTORIO_PACMAN, f"pacman_{direccion}_{i+1}.png")).convert_alpha(),
                (TAM_CELDA, TAM_CELDA)
            ) for i in range(3) if os.path.exists(os.path.join(DIRECTORIO_PACMAN, f"pacman_{direccion}_{i+1}.png"))
        ]

cargar_imagenes_pacman()

def dibujar_celdas():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            pygame.draw.rect(ventana, CYAN, (col * TAM_CELDA + MARGEN, fila * TAM_CELDA + MARGEN, TAM_CELDA, TAM_CELDA), 1)

# ...existing code...

class Pacman:
    def __init__(self, fila, columna):
        self.fila, self.columna, self.direccion = fila, columna, "izquierda"
        self.frame, self.last_update = 0, pygame.time.get_ticks()

    def mover(self, keys, ocupadas):
        global contador_pacman
        contador_pacman += 1
        if contador_pacman < pasos_pacman:
            return
        contador_pacman = 0
        nueva_fila, nueva_col = self.fila, self.columna
        if keys[pygame.K_w]:
            self.direccion, nueva_fila = "arriba", self.fila - 1
        elif keys[pygame.K_s]:
            self.direccion, nueva_fila = "abajo", self.fila + 1
        elif keys[pygame.K_a]:
            self.direccion, nueva_col = "izquierda", self.columna - 1
        elif keys[pygame.K_d]:
            self.direccion, nueva_col = "derecha", self.columna + 1
        if (nueva_fila, nueva_col) not in ocupadas and 0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS and mapa[nueva_fila][nueva_col] != 1:
            self.fila, self.columna = nueva_fila, nueva_col

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update, self.frame = now, (self.frame + 1) % len(animaciones_pacman[self.direccion])
        ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))
        if animaciones_pacman[self.direccion]:  # Asegura que existan animaciones
            ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))

class Fantasmas:
    def __init__(self, fila, columna, tipo, persigue, embosca, rodear):
        self.fila, self.columna, self.tipo = fila, columna, tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.frame, self.last_update = 0, pygame.time.get_ticks()
        self.persigue = persigue
        self.embosca = embosca
        self.rodear = rodear
        self.contador_movimiento = 0

    def mover(self, ocupadas, pacman):
        self.contador_movimiento += 1
        if self.contador_movimiento < pasos_fantasmas:
            return
        self.contador_movimiento = 0

        # Definir objetivo según el comportamiento del fantasma
        objetivo_fila, objetivo_col = pacman.fila, pacman.columna

        if self.rodear:
            if pacman.direccion == "arriba":
                objetivo_fila += 2
            elif pacman.direccion == "abajo":
                objetivo_fila -= 2
            elif pacman.direccion == "izquierda":
                objetivo_col += 2
            elif pacman.direccion == "derecha":
                objetivo_col -= 2

        if self.embosca:
            if pacman.direccion == "arriba":
                objetivo_fila -= 2
            elif pacman.direccion == "abajo":
                objetivo_fila += 2
            elif pacman.direccion == "izquierda":
                objetivo_col -= 2
            elif pacman.direccion == "derecha":
                objetivo_col += 2

        # Definir las opciones de movimiento
        opciones = [
            (self.fila - 1, self.columna, "arriba"),
            (self.fila + 1, self.columna, "abajo"),
            (self.fila, self.columna - 1, "izquierda"),
            (self.fila, self.columna + 1, "derecha")
        ]

        ocupadas_tem = ocupadas.copy()
        ocupadas_tem.remove((self.fila, self.columna))

        # Filtrar opciones válidas
        opciones_validas = [
            (fila, col, dir)
            for fila, col, dir in opciones
            if 0 <= fila < FILAS and 0 <= col < COLUMNAS and (fila, col) not in ocupadas and mapa[fila][col] != 1
        ]

        if self.persigue or self.rodear or self.embosca:
            self.fila, self.columna, self.direccion = min(opciones_validas, key=lambda pos: math.sqrt((pos[0] - objetivo_fila) ** 2 + (pos[1] - objetivo_col) ** 2))
        else:
            self.fila, self.columna, self.direccion = random.choice(opciones_validas)

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update, self.frame = now, (self.frame + 1) % len(animaciones_fantasmas[self.tipo][self.direccion])
        ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
        if animaciones_fantasmas[self.tipo][self.direccion]:
            ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
            
pacman = Pacman(1, 1)  # Nueva posición inicial de Pac-Man
fantasmas = [
    Fantasmas(10, 9, "fantasma_azul", False, False, False),
    Fantasmas(8, 10, "fantasma_rojo", True, False, False),
    Fantasmas(10, 12, "fantasma_naranja", False, False, True),
    Fantasmas(10, 13, "fantasma_rosa", False, True, False)
]

def main():
    run = True
    while run:
        ventana.fill(NEGRO)
        dibujar_celdas()
        dibujar_mapa()
        ocupadas = {(f.fila, f.columna) for f in fantasmas}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        pacman.mover(keys, ocupadas)
        pacman.draw()
        for fantasma in fantasmas:
            fantasma.mover(ocupadas,pacman)
            fantasma.draw()
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()