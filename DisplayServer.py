from os import system

OBSTACLE = "xx"
FOOD = "@@"
HEAD = "aa"
BODY = "=="
EMPTY = "  "

class DisplayServer:
    framebuffer : []
    height: int
    width: int
    clearing: bool
    clearPixel: str
    
    def __init__(self, height: int, width: int, clearing: bool, clearPixel: str = EMPTY):
        self.height = height
        self.width = width
        self.clearing = clearing
        self.clearPixel = clearPixel
        self.clear()
    
    def clear(self):
        self.framebuffer = [[self.clearPixel for x in range(self.width)] for y in range(self.height)]
    
    def setArea(self, x_s, x_e, y_s, y_e, pixel):
        for y in range(y_s, y_e):
            for x in range(x_s, x_e):
                self.setPixel(x, y, pixel)
      
    def setPixel(self, x, y, pixel):
        self.framebuffer[y][x] = pixel
    
    def setText(self, x, y, text, keep_col):
        textBlocks = [text[i:i + 2] for i in range(0, len(text), 2)]
        x_cor = x
        y_cor = y
        while y_cor < self.height and len(textBlocks)!=0:
            while x_cor < self.width and len(textBlocks)!=0:
                self.framebuffer[y_cor][x_cor] = textBlocks.pop(0)
                x_cor += 1
            if keep_col:
                x_cor = x
            y_cor += 1
    
    def draw_optimised_two(self):
        # lines = [[self.framebuffer[y][x] for x in range(self.width)].append("\n") for y in range(self.height)]
    
        # text = "".join(lines) + "\n"
        
        lines = []
        for y in range(self.height):
            lines.append("".join(self.framebuffer[y][x] for x in range(self.width)))
    
        text = "\n".join(lines) + "\n"
        #print(text, end='')
    
    def draw_optimised(self):
        text = "\n".join("".join(self.framebuffer[y][x] for x in range(self.width)) for y in range(self.height))
        text += "\n"
        
        
    def draw_normal(self):
        text = ""
        for y in range(self.height):
            for x in range(self.width):
                text += self.framebuffer[y][x]
            text += "\n"
    
    def draw_old(self):
        if self.clearing:
            print("\033[H\033[J", end='')
        text = ""
        for y in range(self.height):
            for x in range(self.width):
                text += self.framebuffer[y][x]
            text += "\n"
        print(text, end='')
    
    def draw(self):
        if self.clearing:
            print("\033[H\033[J", end='')
        text = "\n".join("".join(self.framebuffer[y][x] for x in range(self.width)) for y in range(self.height)) + "\n"
        print(text, end='')