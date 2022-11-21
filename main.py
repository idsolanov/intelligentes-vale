import cv2
import numpy as np
import pyautogui
import math 
import constants

def get_game_image():
    border_place = pyautogui.locateOnScreen("assets/borde.jpg",confidence=0.9)
    img = pyautogui.screenshot(region=(border_place.left,border_place.top,428,641))
    return img

def save_image(name, img):
    cv2.imwrite(name,img)

def show_image(img):
    cv2.imshow("demo",img)
    cv2.waitKey(0)

def find_coordinates_objects_in_image(asset_addr,image,confidence):
    return list(pyautogui.locateAll(asset_addr, image, grayscale=False, confidence=confidence))


def draw_object(img, coordinates, matrix, color, number):
    for i in range(len(coordinates)) :
        cv2.circle(img,(coordinates[i].left,coordinates[i].top),constants.RADIUS,color,-1)
        x = math.ceil(coordinates[i].left/constants.SIZE)
        y = math.ceil(coordinates[i].top/constants.SIZE)
        matrix[y-1][x-1] = number

def draw_diamonds(img, coordinates_diamonds,matrix):
    for i in range(len(coordinates_diamonds)) :
        x = math.ceil(coordinates_diamonds[i].left/constants.SIZE)
        y = math.ceil(coordinates_diamonds[i].top/constants.SIZE)
        if y == 1:
            if x == 5:
                continue #skip diamond of the game title
        cv2.circle(img,(coordinates_diamonds[i].left,coordinates_diamonds[i].top),constants.RADIUS,constants.CYAN,-1)
        matrix[y-1][x-1] = constants.DIAMOND

def fill_first_lines(matrix):
    for i in range(3):
        for j in range(10):
            matrix[i][j]=2

def coordinates_many_same(number, file_addr, image, confidence):
    coordinates = list()
    for i in range(number):
        item = i+1
        file_addr_complete = file_addr + str(item) + ".jpg"
        coordinates_n = find_coordinates_objects_in_image(file_addr_complete, image, confidence)
        coordinates.extend(coordinates_n)
    return coordinates


image = get_game_image()
image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
save_image("screenshot.jpg",image)

coordinates_player = find_coordinates_objects_in_image("assets/jugador.jpg",image,0.8)
coordinates_diamonds = find_coordinates_objects_in_image("assets/diamante.jpg", image,0.8)
coordinates_keys = find_coordinates_objects_in_image("assets/llave.jpg",image,0.8)
coordinates_doors = find_coordinates_objects_in_image("assets/puerta.jpg",image,0.8)
coordinates_exit = find_coordinates_objects_in_image("assets/salida.jpg",image,0.8)
coordinates_skewers = find_coordinates_objects_in_image("assets/pinchos.jpg", image,0.75)
coordinates_stones = find_coordinates_objects_in_image("assets/piedra.jpg", image,0.8)
coordinates_holes = find_coordinates_objects_in_image("assets/hueco.jpg", image,0.8)
coordinates_lava = coordinates_many_same(10,"assets/lava/lava", image,0.9)


img = np.zeros((641,428,3),np.uint8)
matrix = np.zeros((15,10))

#draw_edge(img,coordinates_edges)
draw_object(img,coordinates_player, matrix,constants.GREEN,constants.PLAYER)
draw_diamonds(img,coordinates_diamonds, matrix)
draw_object(img,coordinates_skewers,matrix,constants.PURPLE,constants.SKEWERS)
draw_object(img,coordinates_exit,matrix,constants.RED,constants.EXIT)
draw_object(img,coordinates_keys,matrix,constants.YELLOW,constants.KEY)
draw_object(img,coordinates_doors,matrix,constants.GRAY,constants.DOOR)
draw_object(img,coordinates_stones,matrix,constants.BLUE,constants.STONE)
draw_object(img,coordinates_holes,matrix,constants.BLUE_2,constants.HOLE)
draw_object(img,coordinates_lava,matrix,constants.ORANGE,constants.LAVA)


fill_first_lines(matrix)
print(np.matrix(matrix))
save_image("lines.jpg",img)

