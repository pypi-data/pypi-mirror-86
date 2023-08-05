import pygame
import moderngl


HEAT2D_VERSION = "0.0.4"
HEAT2D_VERSION_TUPLE = (0, 0, 4)
HEAT2D_VERSION_STATE = "alpha"
HEAT2D_LICENSE = "GNU General Public License v3.0"

PYGAME_VERSION = pygame.version.ver
PYGAME_VERSION_TUPLE = pygame.version.vernum
SDL_VERSION = pygame.get_sdl_version()

MODERNGL_VERSION = moderngl.__version__
ctx = moderngl.create_standalone_context(size=(1, 1), require=None)
OPENGL_VERSION = ctx.version_code
ctx.release()


del pygame, moderngl, ctx
