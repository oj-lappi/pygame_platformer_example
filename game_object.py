class GameObject:
	def __init__(self,x,y,hastighet_x=0,hastighet_y=0,acceleration_x=0,acceleration_y=0,time_to_live=-1,image=None):
		self.x = x
		self.y = y
		self.hastighet_x = hastighet_x
		self.hastighet_y = hastighet_y
		self.acceleration_x = acceleration_x
		self.acceleration_y = acceleration_y
		self.image = image
		self.time_to_live = time_to_live
		
		self.collisionBox = image.get_rect()
	
	def update(self,screen):
		self.x += self.hastighet_x
		self.y += self.hastighet_y
		
		self.collisionBox.x = self.x
		self.collisionBox.y = self.y
		
		window_height = screen.get_height()
		window_width = screen.get_width()
		
		if self.time_to_live != 0:
			screen.blit( self.image, (self.x,self.y) )
			#screen.blit( self.image, (self.x%window_width-window_width,self.y%window_height-window_height) )
			self.time_to_live -= 1
		else:
			del self
	