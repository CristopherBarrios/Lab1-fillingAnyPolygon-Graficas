#Cristopher jose Rodolfo Barrios Solis
#lab1
import struct
from collections import namedtuple
def char(c):
		return struct.pack('=c', c.encode('ascii'))

def word(c):
	return struct.pack('=h', c)
	
def dword(c):
	return struct.pack('=l', c)

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])


class Render(object):
    def __init__(self):
        self.framebuffer = []
        self.width = 520
        self.height = 300
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 500
        self.viewport_height = 500
        self.glClear()

    def glInit(self):
        return "Generando...\n"

    def glClear(self):
        self.framebuffer = [
            [color(0,0,0) for x in range(self.width)] for y in range(self.height)
        ]

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glClearColor(self, r=1, g=1, b=1):
        normalized = normalizeColorArray([r,g,b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glColor(self, r=0, g=0, b=0):
        normalized = normalizeColorArray([r,g,b])
        self.color = color(normalized[0], normalized[1], normalized[2])

    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glVertex(self, x, y):
        final_x = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        final_y = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(final_x, final_y)

    def glCord(self, value, is_vertical):
        real_coordinate = ((value+1) * (self.viewport_height/2) + self.viewport_y) if is_vertical else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(real_coordinate)

    def glLine(self, x0, y0, x1, y1) :
        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        y = y0
        threshold =  dx

        for x in range(x0, x1):
            self.point(y, x) if steep else self.point(x, y)
            
            offset += 2*dy

            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx
                
    def calculateVertices(self, poly_x_coords, poly_y_coords, count_vertices): 
        constants = []
        multipliers = []

        limit = count_vertices - 1;

        for i in range(count_vertices):
            poly_dx = poly_x_coords[limit] - poly_x_coords[i]
            poly_dy = poly_y_coords[limit] - poly_y_coords[i]

            if(poly_y_coords[limit] == poly_y_coords[i]):
                constants.append(poly_x_coords[i])
                multipliers.append(0)
            else:
                constants.append((poly_x_coords[i] * poly_dy - (poly_y_coords[i] * poly_x_coords[limit]) + (poly_y_coords[i] * poly_x_coords[i])) / poly_dy)
                multipliers.append(poly_dx / poly_dy) 

            limit = i;
            
        return (constants, multipliers)
    

    def isInsidePoly(self, x, y, PolyX, PolyY, Count):
        (constants, multipliers) = self.calculateVertices(PolyX, PolyY, Count)

        is_poly_inside = False
        current_node = PolyY[Count - 1] > y
        
        for i in range(Count):
            previous_node = current_node
            current_node = PolyY[i] > y; 
            if (current_node != previous_node):
                is_poly_inside ^= y * multipliers[i] + constants[i] < x
        
        return is_poly_inside
        

    def glDraw(self, vert):
        Count = len(vert)
        PolyX = [axis.x for axis in vert]
        PolyY = [axis.y for axis in vert]

        MinX = min(PolyX)
        MinY = min(PolyY)

        MaxX = max(PolyX)
        MaxY = max(PolyY)
        
        for y in range(MinY, MaxY):
            for x in range(MinX, MaxX):                 
                if self.isInsidePoly(x, y, PolyX, PolyY, Count):
                    self.point(x,y) 
    
    def glFinish(self, filename='out.bmp'):

        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

V = namedtuple('Vertex2', ['x', 'y'])
bitmap = Render()
print(bitmap.glInit())
bitmap.glCreateWindow(800, 600) 
bitmap.glClearColor(0, 0, 0) 
#1
bitmap.glColor(0.37, 0.157, 0.30) 
bitmap.glDraw([V(165, 380), V(185, 360), V(180, 330), V(207, 345), V(233, 330), V(230, 360), V(250, 380), V(220, 385), V(205, 410), V(193, 383)])
#2
bitmap.glColor(0.08, 0.255, 0.00)
bitmap.glDraw([V(321, 335), V(288, 286), V(339, 251), V(374, 302)])
#3
bitmap.glColor(0.88, 0.11, 0.56) 
bitmap.glDraw([V(377, 249), V(411, 197), V(436, 249)])
#4
bitmap.glColor(0.255, 0.01, 0.97) 
bitmap.glDraw([V(413, 177), V(448, 159), V(502, 88), V(553, 53), V(535, 36), V(676, 37), V(660, 52), V(750, 145), V(761, 179), V(672, 192), V(659, 214), V(615, 214), V(632, 230), V(580, 230), V(597, 215), V(552, 214), V(517, 144), V(466, 180)])
#5
bitmap.glColor(0,0,0)
bitmap.glDraw([V(682, 175), V(708, 120), V(735, 148), V(739, 170)])
bitmap.glFinish()