import pygame 
import os
import datetime

_image_library = {}
def get_image(path):
    global _image_library 
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace("/",os.sep).replace("\\",os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[canonicalized_path] = image
    return image

def blitRotate(screen, img, pos, angle, scale=1.0):

    new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
    scaled_img = pygame.transform.scale(img, new_size)

    
    rotated_img = pygame.transform.rotate(scaled_img, angle)

    new_rect = rotated_img.get_rect(center=scaled_img.get_rect(center=pos).center)

    screen.blit(rotated_img, new_rect.topleft)


pygame.init()
done = False

screen = pygame.display.set_mode((1200,800))
w , h = screen.get_size()
bg = pygame.transform.scale(get_image("lab7/images/mainclock.png"), (w,h))
pygame.display.set_caption("Mickey's Clock")


angle_min = 0
angle_sec = 0
global topleft
topleft = (w//2 , h//2 )

while not done :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            done = True

    today = datetime.datetime.now()
    minutes = int(datetime.datetime.strftime(today,'%M'))
    seconds = int(datetime.datetime.strftime(today,'%S')) 
    pos = (screen.get_width()/2 , screen.get_height()/2 )
    screen.blit( bg , (0,0) )

    blitRotate(screen , get_image("lab7/images/leftarm.png") , pos , angle_sec, scale=1.5)
    blitRotate(screen , get_image("lab7/images/rightarm.png"), pos , angle_min, scale=1.5)

    angle_min = -6*minutes-53
    angle_sec = -6*seconds
    pygame.display.flip()