import pygame
import os
import random

pygame.init()

# Configuración de la cuadrícula y la ventana
MARGEN = 50
FILAS, COLUMNAS = 20, 20  # Tamaño reducido de la cuadrícula
TAM_CELDA = 35  # Ajuste del tamaño de cada celda para mejor visualización
ANCHO, ALTO = COLUMNAS * TAM_CELDA + 2 * MARGEN, FILAS * TAM_CELDA + 2 * MARGEN  # Tamaño de la ventana con margen

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fantasmas")
clock = pygame.time.Clock()
fps = 10  # Velocidad de actualización

# Velocidades de movimiento
velocidad_pacman = 0.8
velocidad_fantasmas = 0.4  # Ajuste de la velocidad de los fantasmas a la mitad

# Contadores de movimiento
contador_pacman = 0
contador_fantasmas = 0

# Colores
CYAN = (0, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Cargar imágenes de fantasmas
DIRECTORIO_FANTASMAS = "assets/images/fantasmas"
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
                        print(f"Imagen cargada: {img_path}")
                    else:
                        print(f"Imagen no encontrada: {img_path}")

cargar_imagenes()

# Dibujar la cuadrícula
def dibujar_celdas():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x, y = col * TAM_CELDA + MARGEN, fila * TAM_CELDA + MARGEN
            pygame.draw.rect(ventana, CYAN, (x, y, TAM_CELDA, TAM_CELDA), 1)

# Clase de Pac-Man
class Pacman:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def mover(self, keys, ocupadas):
        global contador_pacman
        contador_pacman += velocidad_pacman
        if contador_pacman < 1:
            return
        contador_pacman = 0

        nueva_fila, nueva_col = self.fila, self.columna
        
        if keys[pygame.K_w]:
            nueva_fila -= 1
        elif keys[pygame.K_s]:
            nueva_fila += 1
        elif keys[pygame.K_a]:
            nueva_col -= 1
        elif keys[pygame.K_d]:
            nueva_col += 1
        
        if (nueva_fila, nueva_col) not in ocupadas and 0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS:
            self.fila, self.columna = nueva_fila, nueva_col
    
    def draw(self):
        x = self.columna * TAM_CELDA + MARGEN + TAM_CELDA // 2
        y = self.fila * TAM_CELDA + MARGEN + TAM_CELDA // 2
        pygame.draw.circle(ventana, AMARILLO, (x, y), TAM_CELDA // 2)

# Clase de los fantasmas
class Fantasmas:
    def __init__(self, fila, columna, tipo):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.animaciones = animaciones_fantasmas.get(tipo, {})
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def mover(self, ocupadas):
        global contador_fantasmas
        contador_fantasmas += velocidad_fantasmas
        if contador_fantasmas < 1:
            return
        contador_fantasmas = 0

        direcciones_validas = []
        for direccion in ["arriba", "abajo", "izquierda", "derecha"]:
            nueva_fila, nueva_col = self.fila, self.columna
            if direccion == "arriba":
                nueva_fila -= 1
            elif direccion == "abajo":
                nueva_fila += 1
            elif direccion == "izquierda":
                nueva_col -= 1
            elif direccion == "derecha":
                nueva_col += 1

            if (nueva_fila, nueva_col) not in ocupadas and 0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS:
                direcciones_validas.append((nueva_fila, nueva_col, direccion))

        if direcciones_validas:
            self.fila, self.columna, self.direccion = random.choice(direcciones_validas)

    def draw(self):
        x = self.columna * TAM_CELDA + MARGEN
        y = self.fila * TAM_CELDA + MARGEN
        if self.animaciones:
            now = pygame.time.get_ticks()
            if now - self.last_update > 200:
                self.last_update = now
                self.frame = (self.frame + 1) % len(self.animaciones[self.direccion])
            ventana.blit(self.animaciones[self.direccion][self.frame], (x, y))
        else:
            pygame.draw.rect(ventana, ROJO, (x, y, TAM_CELDA, TAM_CELDA))

# Instancias
pacman = Pacman(5, 5)
fantasmas = [
    Fantasmas(10, 10, "fantasma_azul"),
    Fantasmas(10, 11, "fantasma_rojo"),
    Fantasmas(10, 12, "fantasma_naranja"),
    Fantasmas(10, 13, "fantasma_rosa")
]

# Bucle principal
def main():
    global run
    run = True
    while run:
        ventana.fill(NEGRO)
        dibujar_celdas()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        ocupadas = {(f.fila, f.columna) for f in fantasmas}
        pacman.mover(keys, ocupadas)
        pacman.draw()
        
        for fantasma in fantasmas:
            fantasma.mover(ocupadas)
            fantasma.draw()

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()