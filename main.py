import cv2
import numpy as np
import pyautogui
import math 
import src.constants as constants

def get_game_image():
    coordinates = list()
    for i in range(2):
        item = i+1
        file_addr_complete = "assets/borde/borde" + str(item) + ".jpg"
        coordinates_n = pyautogui.locateOnScreen(file_addr_complete, confidence = 0.9)
        if coordinates_n != None:
            coordinates.append(coordinates_n)

    border_place = coordinates[len(coordinates)-1]
    img = pyautogui.screenshot(region=(border_place.left,border_place.top,constants.WIDTH,constants.HEIGHT))
    return img

def save_image(name, img):
    cv2.imwrite(name,img)

def show_image(img):
    cv2.imshow("demo",img)
    cv2.waitKey(0)

def find_coordinates_objects_in_image(asset_addr,image,confidence):
    return list(pyautogui.locateAll(asset_addr, image, grayscale=False, confidence=confidence))


def draw_object(img, coordinates, matrix, color, number):
    to_compare = list()
    for i in range(len(coordinates)) :
        left = coordinates[i].left
        top = coordinates[i].top
        if(not find_coord_in_list(to_compare,(left,top))):
            cv2.circle(img,(coordinates[i].left+constants.SIZE_HALF,coordinates[i].top+constants.SIZE_HALF),constants.RADIUS,color,-1)
            x = math.ceil((coordinates[i].left+constants.SIZE_HALF)/constants.WIDTH_SUB)
            y = math.ceil((coordinates[i].top+constants.SIZE_HALF)/constants.HEIGHT_SUB)
            matrix[y-1][x-1] = number
            to_compare.append((left,top))

def draw_diamonds(img, coordinates_diamonds,matrix):
    to_compare = list()
    for i in range(len(coordinates_diamonds)) :
        left = coordinates_diamonds[i].left
        top = coordinates_diamonds[i].top
        x = math.ceil((coordinates_diamonds[i].left+constants.SIZE_HALF)/constants.WIDTH_SUB)
        y = math.ceil((coordinates_diamonds[i].top+constants.SIZE_HALF)/constants.HEIGHT_SUB)
        if(not find_coord_in_list(to_compare,(left,top))):
            if y == 1:
                if x == 6:
                    continue #skip diamond of the game title
            cv2.circle(img,(coordinates_diamonds[i].left+constants.SIZE_HALF,coordinates_diamonds[i].top+constants.SIZE_HALF),constants.RADIUS,constants.CYAN,-1)
            matrix[y-1][x-1] = constants.DIAMOND
            to_compare.append((left,top))


def fill_lines(img,matrix):
    for i in range(2):
        for j in range(10):
            matrix[i][j]=constants.WALL
            cv2.circle(img,(j*constants.SIZE+constants.SIZE_HALF,i*constants.SIZE+constants.SIZE_HALF),constants.RADIUS,constants.BROWN,-1)

def coordinates_many_same(number, file_addr, image, confidence):
    coordinates = list()
    for i in range(number):
        item = i+1
        file_addr_complete = file_addr + str(item) + ".jpg"
        coordinates_n = find_coordinates_objects_in_image(file_addr_complete, image, confidence)
        coordinates.extend(coordinates_n)
        #add_list_to_list(coordinates,coordinates_n)
    return coordinates

def find_coord_in_list(list:list,coord:tuple):
    value =constants.SIZE-5
    for item in list:
        if coord[0]+value>= item[0] and coord[0]-value<=item[0] :
            if coord[1]+value>= item[1] and coord[1]-value<=item[1] :
                return True
    return False

def add_list_to_list(a:list,b:list):
    for item in b:
        if(not item in a):
            a.append(item)

image = get_game_image()
image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
save_image("images/gameScreen.jpg",image)

coordinates_wall = coordinates_many_same(56,"assets/pared/pared", image,0.8)
coordinates_player = coordinates_many_same(2,"assets/jugador/jugador",image,0.8)
coordinates_diamonds = coordinates_many_same(4,"assets/diamante/diamante", image,0.9)
coordinates_keys = find_coordinates_objects_in_image("assets/llave.jpg",image,0.8)
coordinates_doors = find_coordinates_objects_in_image("assets/puerta.jpg",image,0.8)
coordinates_exit = coordinates_many_same(2,"assets/salida/salida",image,0.8)
coordinates_skewers = find_coordinates_objects_in_image("assets/pinchos.jpg", image,0.75)
coordinates_stones = find_coordinates_objects_in_image("assets/piedra.jpg", image,0.9)
coordinates_holes = find_coordinates_objects_in_image("assets/hueco.jpg", image,0.8)
coordinates_lava = coordinates_many_same(13,"assets/lava/lava", image,0.9)
coordinates_grid = find_coordinates_objects_in_image("assets/reja.jpg", image,0.8)
coordinates_button = find_coordinates_objects_in_image("assets/boton.jpg", image,0.8)

img = np.zeros((constants.HEIGHT,constants.WIDTH,3),np.uint8)
matrix = np.zeros((constants.MATRIX_Y,constants.MATRIX_X))

draw_object(img,coordinates_wall,matrix,constants.BROWN,constants.WALL)
draw_object(img,coordinates_player, matrix,constants.GREEN,constants.PLAYER)
draw_diamonds(img,coordinates_diamonds, matrix)
draw_object(img,coordinates_skewers,matrix,constants.PURPLE,constants.SKEWERS)
draw_object(img,coordinates_exit,matrix,constants.RED,constants.EXIT)
draw_object(img,coordinates_keys,matrix,constants.YELLOW,constants.KEY)
draw_object(img,coordinates_doors,matrix,constants.GRAY,constants.DOOR)
draw_object(img,coordinates_stones,matrix,constants.BLUE,constants.STONE)
draw_object(img,coordinates_holes,matrix,constants.BLUE_2,constants.HOLE)
draw_object(img,coordinates_lava,matrix,constants.ORANGE,constants.LAVA)
draw_object(img,coordinates_grid,matrix,constants.PINK,constants.GRID)
draw_object(img,coordinates_button,matrix,constants.WHITE,constants.BUTTON)


fill_lines(img,matrix)
print(np.matrix(matrix))
save_image("images/dots.jpg",img)
show_image(img)
