import pyxel
import sdl2
import sdl2.sdlimage


def blta(x, y, img, u, v, w, h, angle=0, colkey=None):
    current_window = sdl2.SDL_GL_GetCurrentWindow()
    img_data = pyxel.image(img).data
    renderer = sdl2.SDL_GetRenderer(current_window)
    print(renderer)
