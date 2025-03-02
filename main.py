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
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
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

excepciones_circulos = [(8,0),(8,1),(8,2),(8,6),(8,7),(8,8),(8,9),(8,10),(8,11),(8,12),(8,13),(8,16),(8,18),(8,17),
                        (9,6),(9,9),(9,12),
                        (10,0),(10,1),(10,2),(10,3),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(12,10),(10,11),(10,12),(10,13),(10,15),(10,16),(10,18),(10,17),
                        (11,6),(11,12),
                        (12,0),(12,1),(12,2),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),(12,16),(12,18),(12,17),
                        (13,6),(13,12)
                        ]
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
            
        if self.fila == 10:
            if nueva_col < 0:
                nueva_col = COLUMNAS - 1
            elif nueva_col >= COLUMNAS:
                nueva_col = 0

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update, self.frame = now, (self.frame + 1) % len(animaciones_pacman[self.direccion])
        ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))
        if animaciones_pacman[self.direccion]:  # Asegura que existan animaciones
            ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))

class Fantasmas:
    def __init__(self, fila, columna, tipo, persigue, embosca, rodear,tiempo_salida):
        self.fila, self.columna, self.tipo = fila, columna, tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.frame, self.last_update = 0, pygame.time.get_ticks()
        self.persigue = persigue
        self.embosca = embosca
        self.rodear = rodear
        self.contador_movimiento = 0
        self.tiempo_salida = tiempo_salida
        self.inicio = pygame.time.get_ticks()
        
        

    def mover(self, ocupadas, pacman):
        if pygame.time.get_ticks() - self.inicio < self.tiempo_salida:
            return
        
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
        
        #Direcciones opuestas 
        direcciones_opuestas ={"arriba":"abajo",
                               "abajo":"arriba",
                               "izquierda":"derecha",
                               "derecha":"izquierda"}

        # Filtrar opciones válidas
        opciones_validas = [
            (fila, col, dir)
            for fila, col, dir in opciones
            if 0 <= fila < FILAS and 0 <= col < COLUMNAS and (fila, col) not in ocupadas and mapa[fila][col] != 1 and dir != direcciones_opuestas[self.direccion]
        ]
        if self.persigue or self.rodear or self.embosca:
            self.fila, self.columna, self.direccion = min(opciones_validas, key=lambda pos: math.sqrt((pos[0] - objetivo_fila) ** 2 + (pos[1] - objetivo_col) ** 2))
        else:
            self.fila, self.columna, self.direccion = random.choice(opciones_validas)
            
        if self.fila == 9 and self.columna == 9:
            opciones_validas = [opcion for opcion in opciones_validas if opcion[2] != "abajo"]
            
        if self.persigue or self.rodear or self.embosca:
            self.fila, self.columna, self.direccion = min(opciones_validas, key=lambda pos: math.sqrt((pos[0] - objetivo_fila) ** 2 + (pos[1] - objetivo_col) ** 2))
        else:
            self.fila, self.columna, self.direccion = random.choice(opciones_validas)
            
        if self.fila == 10:
            if self.columna == 0 and self.direccion == "izquierda":
                self.columna = COLUMNAS - 1
            elif self.columna == COLUMNAS - 1 and self.direccion == "derecha":
                self.columna = 0
        

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update, self.frame = now, (self.frame + 1) % len(animaciones_fantasmas[self.tipo][self.direccion])
        ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
        if animaciones_fantasmas[self.tipo][self.direccion]:
            ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
            
pacman = Pacman(16, 9)  #poscicion inicial de pacman
fantasmas = [
    Fantasmas(10, 8, "fantasma_azul", False,False, False,15000),
    Fantasmas(8, 9, "fantasma_rojo", True, False, False,0),
    Fantasmas(10, 10, "fantasma_naranja", False, False, True,5000),
    Fantasmas(10, 9, "fantasma_rosa", False, True, False,1000)]

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