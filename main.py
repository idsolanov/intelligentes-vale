import cv2
import numpy as np
import pyautogui

def get_game_image():
    border_place = pyautogui.locateOnScreen("assets/borde.jpg",confidence=0.9)
    img = pyautogui.screenshot(region=(border_place.left,border_place.top,428,641))
    return img

def save_image(name, img):
    cv2.imwrite(name,img)

def show_image(img):
    cv2.imshow("demo",img)
    cv2.waitKey(0)



image = get_game_image()
image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
save_image("screenshot.jpg",image)
show_image(image)
coordinates_diamonds = pyautogui.locateAll("assets/diamante.jpg", image, grayscale=False, confidence=0.9)


# cv2.imwrite("screenshot.png", image)
# Convert to graycsale
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png",img_gray)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

# Canny Edge Detection
edges = cv2.Canny(image=img_gray, threshold1=100, threshold2=200) # Canny Edge Detection
cv2.imwrite("edges.png",edges)
cv2.imshow("bordes",edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Display Canny Edge Detection Image

