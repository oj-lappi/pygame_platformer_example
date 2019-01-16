import pygame
import pygame.locals
import math
from game_object import GameObject
pygame.init()


display_info = pygame.display.Info()

window_width = 1024
window_height = 640

#screen = pygame.display.set_mode( (window_width,window_height), 0, 32)
screen = pygame.display.set_mode( (window_width,window_height), 0,32)

pygame.display.set_caption("Hello, world!")

#Define filepaths to iamges
background_image_filepath = "Koala.jpg"
mouse_cursor_image_filepath = "green.png"
enemy_image_filepath = "angryface.png"
platform_image_filepath = "pink_platform.png"

#Load image resources
background = pygame.image.load( background_image_filepath ).convert()
character_image = pygame.image.load( mouse_cursor_image_filepath ).convert_alpha()
bullet_image = pygame.transform.scale(character_image ,(10,10) )
enemy_image = pygame.image.load( enemy_image_filepath ).convert()
platform_image = pygame.image.load( platform_image_filepath ).convert()
platform_image = pygame.transform.scale(platform_image ,(300,30) )

background_resolution =  ( window_width, window_height)
background = pygame.transform.scale(background, background_resolution )


#The bullet class

class Platform(GameObject):
	def __init__(self,x,y):
		GameObject.__init__(self,x,y,image=platform_image)

class Bullet(GameObject):
	def __init__(self,x,y,hastighet_x,hastighet_y):
		GameObject.__init__(self,x,y,hastighet_x,hastighet_y,image=bullet_image,time_to_live=450)
		
class Enemy(GameObject):
	
	speed = 0.2
	
	def __init__(self,x,y,hastighet_x=0,hastighet_y=0,target=None):
		GameObject.__init__(self,x,y,hastighet_x,hastighet_y,image=enemy_image)
		self.target = target
	
	def update(self,screen):
		#Ändra hastigheten, så att vi följer spelaren
		x_dist = self.target.x - self.x
		y_dist = self.target.y - self.y
		distance = math.hypot(x_dist,y_dist)
		
		self.hastighet_x = self.speed*x_dist/distance
		self.hastighet_y = self.speed*y_dist/distance
		
		GameObject.update(self,screen)

character = GameObject(x=window_width / 2,
					   y=window_height /2,
					   image = character_image )

enemy = Enemy(x=window_width / 4,
			  y=window_height /4,
			  target=character)

platforms = [
		Platform(25,window_height-70),
		Platform(window_width / 2,170),
		Platform(window_width -100,window_height-70),
]
			  
#Define some variables for our game
exit = False
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False
space_pressed = False

bullet_speed = 2

movement_acceleration = 0.01
max_hastighet = 1.9
brake_factor = 0.041

jump_speed = max_hastighet
gravity = 0.01
ground_level = screen.get_size()[1] - character_image.get_size()[1]
#brake_factor = 1 #=> stannar genast
#brake_factor = 0 #=> stannar inte alls

def handle_events():
	global left_pressed
	global right_pressed
	global up_pressed
	global down_pressed
	global space_pressed
	global exit
	
	for event in pygame.event.get():
		if event.type == pygame.locals.QUIT:
			pygame.display.quit()
			pygame.quit()
			exit = True
		#Input
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				left_pressed = True
				right_pressed = False
			elif event.key == pygame.K_RIGHT:
				right_pressed = True
				left_pressed = False
			elif event.key == pygame.K_UP:
				up_pressed = True
				down_pressed = False
			elif event.key == pygame.K_DOWN:
				down_pressed = True
				up_pressed = False
			elif event.key == pygame.K_SPACE:
				space_pressed = True
				
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				left_pressed = False
			elif event.key == pygame.K_RIGHT:
				right_pressed = False
			elif event.key == pygame.K_UP:
				up_pressed = False
			elif event.key == pygame.K_DOWN:
				down_pressed = False
			elif event.key == pygame.K_SPACE:
				space_pressed = False

def can_jump(character):
	
	if character.can_jump:
		return True
		
	if abs(character.y - ground_level) < 2:
		return True

def do_jump_physics(character):

	character.can_jump = False
	
	if(character.y > ground_level):
		character.y = ground_level
		character.can_jump = True
		
	for plat in platforms:
		if plat.collisionBox.colliderect(character.collisionBox):
			character.y = plat.collisionBox.y -character.image.get_size()[1]
			character.can_jump = True
		
				
def player_movement_from_input(character):
	global left_pressed
	global right_pressed
	global up_pressed
	global down_pressed
	
	global movement_acceleration
	global brake_factor

	
	if up_pressed:
		if can_jump(character):
			character.hastighet_y = -jump_speed
	else:
		character.acceleration_y = gravity
	
	if left_pressed:
		character.acceleration_x = -movement_acceleration
	elif right_pressed:
		character.acceleration_x = movement_acceleration
	else:
		character.acceleration_x = -character.hastighet_x*brake_factor

		
def do_physics(character):

	global max_hastighet
	
	character.hastighet_x = character.hastighet_x + character.acceleration_x
	character.hastighet_y = character.hastighet_y + character.acceleration_y
	
	if abs(character.hastighet_x) >= max_hastighet:
		if character.hastighet_x > 0:
			character.hastighet_x = max_hastighet
		else:
			character.hastighet_x = -max_hastighet
		
	if abs(character.hastighet_y) >= max_hastighet:
		if character.hastighet_y > 0:
			character.hastighet_y = max_hastighet
		else:
			character.hastighet_y = -max_hastighet
	
	do_jump_physics(character)



bullet_list = []	

next_bullet_hastighet_x = bullet_speed
next_bullet_hastighet_y = bullet_speed

while True:
	
	#Checking for quit event
	handle_events()
			
	if exit:
		break
	
	player_movement_from_input(character)
	
	
	#Drawing background
	screen.blit(background,(0,0))
	#screen.fill(color=0)

	#Calculating character physics
	do_physics(character)
	
	
	if left_pressed or right_pressed or up_pressed or down_pressed:
		if left_pressed:
			next_bullet_hastighet_x = -bullet_speed
		elif right_pressed:
			next_bullet_hastighet_x = bullet_speed
		else:
			next_bullet_hastighet_x = 0
		
		if down_pressed:
			next_bullet_hastighet_y = bullet_speed
		elif up_pressed:
			next_bullet_hastighet_y = -bullet_speed
		else:
			next_bullet_hastighet_y = 0
	
	if space_pressed:
		new_bullet = Bullet(x=character.x,
							y=character.y,
							hastighet_x=next_bullet_hastighet_x,
							hastighet_y=next_bullet_hastighet_y)
		bullet_list.append(new_bullet)
	
	
	for b in bullet_list:
		b.update(screen)
	
	character.update(screen)
	enemy.update(screen)
	for platform in platforms:
		platform.update(screen)
	
	pygame.display.update()

