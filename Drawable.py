import pygame
import abc
import math

class Drawable(metaclass = abc.ABCMeta):
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.color=255, 255, 255

    def getLoc(self):
    	return (self.x, self.y)

    def setLoc(self,p):
    	self.x = p[0]
    	self.y = p[1]


    @abc.abstractmethod
    def draw(self,surface):
    	pass

class Circle(Drawable):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.radius = 13
        self.width = 2

    def draw(self,screen,size):
        pygame.draw.circle(screen,self.color,[self.x,self.y],self.radius,self.width)


class Cross(Drawable):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.length=26
        self.width = 2
        self.offset=math.sqrt(math.pow(self.length,2)/8)

    def draw(self,screen,size):
        pygame.draw.line(screen,self.color,[(self.x-self.offset),(self.y-self.offset)],[(self.x+self.offset),(self.y+self.offset)],self.width)
        pygame.draw.line(screen,self.color,[(self.x-self.offset),(self.y+self.offset)],[(self.x+self.offset),(self.y-self.offset)],self.width)
class Grid(Drawable):
    def __init__(self,l):
        self.color=143, 255, 144
        self.length=l
        self.width=1
    #TODO:
    #Implement getGridLoc; returns 2-D array of addresses
    def getGridLoc(self):
        pass

    def draw(self,screen,size):
        pygame.draw.line(screen,self.color,[(size[0]/2-self.length/2),(size[1]/2-self.length/6)],[(size[0]/2+self.length/2),(size[1]/2-self.length/6)],self.width)
        pygame.draw.line(screen,self.color,[(size[0]/2-self.length/2),(size[1]/2+self.length/6)],[(size[0]/2+self.length/2),(size[1]/2+self.length/6)],self.width)
        pygame.draw.line(screen,self.color,[(size[0]/2-self.length/6),(size[1]/2-self.length/2)],[(size[0]/2-self.length/6),(size[1]/2+self.length/2)],self.width)
        pygame.draw.line(screen,self.color,[(size[0]/2+self.length/6),(size[1]/2-self.length/2)],[(size[0]/2+self.length/6),(size[1]/2+self.length/2)],self.width)
