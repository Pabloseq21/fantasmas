import pygame
import os

pygame.init()

height = 1000
width = 1200 
ventana = pygame.display.set_mode((width, height))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("fantasmas")
clock = pygame.time.Clock()

#funcion para escalar imagen
def escalar_img (image,scale):
    w = image.get_width()
    h =image.get_height()
    new_image = pygame.transform.scale(image,(w*scale,h*scale))
    return new_image 

#funsion contar elementos
def contar_elementos(directory):
    return len (os.listdir(directory))

#funsion nombrar elementos 
def nombre_carpeta(directory):
    return os.listdir(directory)

#enemigos 
directory_enemigos = "assents/images/personajes/enemigos"
tipo_enemigo = nombre_carpeta(directory_enemigos)
animacion_enemigo = []
for eni in tipo_enemigo:
    lista_temp = []
    ruta_temp = f"assents/images/personajes/enemigos/{eni}"
    num_animacion = contar_elementos(ruta_temp)
    for i in range (num_animacion):
        img_enemigo = pygame.image.load (f"{ruta_temp}/{eni}_{i+1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo,1) 
        lista_temp.append(img_enemigo)    
    animacion_enemigo.append(lista_temp)

#clase de los fantasmas     
class Fantasmas:
    def __init__(self, x, y,image):
        self.image =image 
        self.shape = pygame.Rect(0, 0, 50, 50)
        self.shape.center = (x, y)

def draw(self, ventana):
    ventana.blit(self.image, self.rect.topleft)  # Usa topleft si rect es un pygame.Rect

        #pygame.draw.rect(ventana, (0,255,255), self.shape)
        
                
# Crear instancias de los fantasmas
fant_azul = Fantasmas(50, 50,animacion_enemigo[0])
fant_naranja = Fantasmas(250, 50,animacion_enemigo[1])
fant_rojo = Fantasmas(450, 50,animacion_enemigo[2])
fant_rosa = Fantasmas(650, 50,animacion_enemigo[3])

#crear lista de enemigos 
lista_enemigos = []
lista_enemigos.append(fant_azul)
lista_enemigos.append(fant_naranja)
lista_enemigos.append(fant_rojo)
lista_enemigos.append(fant_rosa)
print(lista_enemigos)

run = True  

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            run = False
            
    for ene in lista_enemigos:
        ene.draw(ventana)
        
    for ene in lista_enemigos:
        ene.update()
        
    pygame.display.update()
    clock.tick(60)
    
    pygame.display.update() 

pygame.quit()
