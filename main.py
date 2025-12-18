import pygame
from pygame import *
from app import App
from constants import *

pygame.init()

display = pygame.display.set_mode((WIDTH , HEIGHT))

game = App(display)