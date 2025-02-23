import pygame
import os
import random

pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1200, 1000
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fantasmas")
clock = pygame.time.Clock()
fps = 60

# Función para escalar imágenes
def escalar_img(image, scale):
    w, h = image.get_size()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

# Función para contar elementos en un directorio
def contar_elementos(directory):
    return len(os.listdir(directory))if os.path.exists(directory)else 0

# Función para obtener nombres de archivos en un directorio
def nombre_carpeta(directory):
    return os.listdir(directory) if os.path.exists(directory) else []

# Cargar animaciones de los enemigos
directory_enemigos = "assents/images/fantasmas"
tipo_enemigo = nombre_carpeta(directory_enemigos)
animaciones_enemigos = {}
print(nombre_carpeta(directory_enemigos))
print(contar_elementos(directory_enemigos))

for eni in tipo_enemigo:
    ruta_temp = os.path.join(directory_enemigos, eni)
    animaciones = {"izquierda": [], "derecha": [], "arriba": [], "abajo": []}
    for direccion in animaciones.keys():
        for i in range(2):  # Dos imágenes por dirección
            img_path = os.path.join(ruta_temp, f"{eni}_{direccion}_{i+1}.png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                animaciones[direccion].append(escalar_img(img, 1))
    animaciones_enemigos[eni] = animaciones

# Clase de los fantasmas
class Fantasmas:
    def __init__(self, x, y, tipo):
        self.x, self.y = x, y
        self.tipo = tipo
        self.animaciones = animaciones_enemigos.get(tipo, {"izquierda": [], "derecha": [], "arriba": [], "abajo": []})
        self.frame = 0
        self.velocidad = 2
        self.direccion = "derecha"  # Puede ser 'izquierda', 'derecha', 'arriba', 'abajo'
        self.shape = pygame.Rect(self.x, self.y, 50, 50)
        self.last_update = pygame.time.get_ticks()
    
    def mover(self):
        direcciones = ["izquierda", "derecha", "arriba", "abajo"]
        if random.randint(0, 100) > 98:  # Pequeña probabilidad de cambiar de dirección
            self.direccion = random.choice(direcciones)
        
        if self.direccion == "izquierda":
            self.x -= self.velocidad
        elif self.direccion == "derecha":
            self.x += self.velocidad
        elif self.direccion == "arriba":
            self.y -= self.velocidad
        elif self.direccion == "abajo":
            self.y += self.velocidad
        
        self.shape.topleft = (self.x, self.y)
    
    def actualizar_animacion(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 800:  # Cambia cada segundo
            self.last_update = now
            if self.animaciones[self.direccion]:
                self.frame = (self.frame + 1) % len(self.animaciones[self.direccion])
    
    def draw(self, ventana):
        if self.animaciones[self.direccion]:
            ventana.blit(self.animaciones[self.direccion][self.frame], self.shape.topleft)

# Crear instancias de los fantasmas
lista_enemigos = [
    Fantasmas(50, 50, "fantasma_azul"),
    Fantasmas(250, 50, "fantasma_naranja"),
    Fantasmas(450, 50, "fantasma_rojo"),
    Fantasmas(650, 50, "fantasma_rosa")
]

# Bucle principal del juego
run = True  
while run:
    ventana.fill((0, 0, 0))  # Limpiar pantalla
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for ene in lista_enemigos:
        ene.mover()
        ene.actualizar_animacion()
        ene.draw(ventana)
    
    pygame.display.update()
    clock.tick(fps)

pygame.quit()