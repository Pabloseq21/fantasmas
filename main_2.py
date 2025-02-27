import pygame
import os
import random

pygame.init()

# Configuración de la cuadrícula y la ventana
FILAS, COLUMNAS = 25, 26
TAM_CELDA = 40  # Tamaño fijo de cada celda
ANCHO, ALTO = COLUMNAS * TAM_CELDA, FILAS * TAM_CELDA  # Tamaño fijo de la ventana

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fantasmas")
clock = pygame.time.Clock()
fps = 10  # Velocidad de actualización

# Velocidades de movimiento
velocidad_pacman = 0.8
velocidad_fantasmas = 0.75

# Colores
CYAN = (0, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

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
                    img_path = os.path.join(ruta, f"{nombre}_{direccion}_{i+1}.png")
                    if os.path.exists(img_path):
                        img = pygame.image.load(img_path).convert_alpha()
                        img = pygame.transform.scale(img, (TAM_CELDA, TAM_CELDA))
                        animaciones_fantasmas[nombre][direccion].append(img)

cargar_imagenes()

# Dibujar la cuadrícula
def dibujar_celdas():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x, y = col * TAM_CELDA, fila * TAM_CELDA
            pygame.draw.rect(ventana, CYAN, (x, y, TAM_CELDA, TAM_CELDA), 1)

# Clase de Pac-Man
class Pacman:
    def __init__(self, fila, columna):
        self.x = columna * TAM_CELDA
        self.y = fila * TAM_CELDA
        self.direccion = None
        self.vivo = True
        self.casillas_ocupadas = [(fila, columna)]

    def mover(self, keys, ocupadas):
        nueva_x, nueva_y = self.x, self.y
        self.moviendo = False
        velocidad_actual = velocidad_pacman if any(keys) else 0  # Velocidad 0 si no hay teclas presionadas

        if keys[pygame.K_w]:
            self.direccion = "arriba"
            self.moviendo = True
        elif keys[pygame.K_s]:
            self.direccion = "abajo"
            self.moviendo = True
        elif keys[pygame.K_a]:
            self.direccion = "izquierda"
            self.moviendo = True
        elif keys[pygame.K_d]:
            self.direccion = "derecha"
            self.moviendo = True
        
        if self.direccion:
            if self.direccion == "arriba":
                nueva_y -= velocidad_actual * TAM_CELDA
            elif self.direccion == "abajo":
                nueva_y += velocidad_actual * TAM_CELDA
            elif self.direccion == "izquierda":
                nueva_x -= velocidad_actual * TAM_CELDA
            elif self.direccion == "derecha":
                nueva_x += velocidad_actual * TAM_CELDA

            nueva_fila, nueva_col = int(nueva_y // TAM_CELDA), int(nueva_x // TAM_CELDA)
            if (nueva_fila, nueva_col) not in ocupadas:
                self.x, self.y = nueva_x, nueva_y
                self.casillas_ocupadas.append((nueva_fila, nueva_col))
        else:
            # Ajustar a la celda más cercana
            self.x = round(self.x / TAM_CELDA) * TAM_CELDA
            self.y = round(self.y / TAM_CELDA) * TAM_CELDA
            self.direccion = None
    
    def draw(self):
        if self.vivo:
            pygame.draw.circle(ventana, (255, 255, 0), (int(self.x) + TAM_CELDA // 2, int(self.y) + TAM_CELDA // 2), TAM_CELDA // 2)

# Clase de los fantasmas
class Fantasmas:
    def __init__(self, fila, columna, tipo):
        self.x = columna * TAM_CELDA
        self.y = fila * TAM_CELDA
        self.tipo = tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.animaciones = animaciones_fantasmas.get(tipo, {})
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def mover(self, ocupadas):
        nueva_x, nueva_y = self.x, self.y
        if self.direccion == "arriba":
            nueva_y -= velocidad_fantasmas * TAM_CELDA
        elif self.direccion == "abajo":
            nueva_y += velocidad_fantasmas * TAM_CELDA
        elif self.direccion == "izquierda":
            nueva_x -= velocidad_fantasmas * TAM_CELDA
        elif self.direccion == "derecha":
            nueva_x += velocidad_fantasmas * TAM_CELDA

        nueva_fila, nueva_col = int(nueva_y // TAM_CELDA), int(nueva_x // TAM_CELDA)
        if (nueva_fila, nueva_col) not in ocupadas:
            self.x, self.y = nueva_x, nueva_y
        else:
            self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])

    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.last_update > 100:
            self.last_update = ahora
            if self.direccion in self.animaciones:
                self.frame = (self.frame + 1) % len(self.animaciones[self.direccion])

    def draw(self):
        if self.direccion in self.animaciones and self.animaciones[self.direccion]:
            ventana.blit(self.animaciones[self.direccion][self.frame], (int(self.x), int(self.y)))

# Crear lista de coordenadas de la cuadrícula
coordenadas_celdas = [(fila, col) for fila in range(FILAS) for col in range(COLUMNAS)]

# Definir casillas con colisión (obstáculos)
obstaculos = [(10, 10), (10, 11), (10, 12), (11, 10), (12, 10)]

fila_central = FILAS // 2
columna_central = COLUMNAS // 2

lista_enemigos = [
    Fantasmas(fila_central, columna_central, "fantasma_azul"),
    Fantasmas(fila_central - 1, columna_central, "fantasma_naranja"),
    Fantasmas(fila_central + 1, columna_central, "fantasma_rojo"),
    Fantasmas(fila_central, columna_central - 1, "fantasma_rosa")
]

pacman = Pacman(5, 5)

run = True
while run:
    ventana.fill(NEGRO)
    dibujar_celdas()
    
    # Dibujar obstáculos
    for obstaculo in obstaculos:
        x, y = obstaculo[1] * TAM_CELDA, obstaculo[0] * TAM_CELDA
        pygame.draw.rect(ventana, ROJO, (x, y, TAM_CELDA, TAM_CELDA))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    ocupadas = {(int(ene.y // TAM_CELDA), int(ene.x // TAM_CELDA)) for ene in lista_enemigos}
    ocupadas.update(obstaculos)  # Añadir obstáculos a las casillas ocupadas
    pacman.mover(keys, ocupadas)
    pacman.draw()

    for ene in lista_enemigos:
        ene.mover(ocupadas)
        ene.actualizar_animacion()
        ene.draw()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()