# from instrumental.drivers.cameras import uc480
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import timeloop

cam = cv2.VideoCapture(1)
run = False

def take_photo():
    ret, frame = cam.read()
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.show()
    cam.release()

def capture_images(interval, save_path, num_images):
    # Open the default camera (usually 0)
    # Check if the camera is opened successfully
    if not cam.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        # Capture images
        for i in range(num_images):
            # Capture frame-by-frame
            ret, frame = cam.read()

            # Save the captured frame
            image_path = f"{save_path}/image_{i}.jpg"
            cv2.imwrite(image_path, frame)

            print(f"Image {i+1} captured")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Interrupted")

    # Release the camera
    cam.release()
    cv2.destroyAllWindows()
# capture_images(60, 'C:/Users/Berco/OneDrive/Documents/Projeto F 014/Fotos do experimento', 50)
def open_camera():
    while cam.isOpened():
        ret, frame = cam.read()

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
open_camera() 

def acha_centro():
    img = cv2.imread('Foto_3.png')
    # cv2.imshow('cu', img)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = (0, 0, 0) # lower range of red color in HSV
    upper_range = (0, 0, 255) # upper range of red color in HSV
    mask = cv2.inRange(hsv_img, lower_range, upper_range)

    color_image = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow('color_image', color_image)
    cv2.waitKey(0)


def acha_vermelho():
    img = cv2.imread('Foto_3.png')
    # cv2.imshow('cu', img)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    
    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv_img, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv_img, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    color_image = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow('color_image', color_image)
    cv2.waitKey(0)

def open_camera_laser():
    global run
    run = True
    while cam.isOpened() and run:
        ret, frame = cam.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = (0, 0, 0) # lower range of red color in HSV
        upper_range = (0, 0, 255) # upper range of red color in HSV
        mask = cv2.inRange(hsv_frame, lower_range, upper_range)

        color_frame = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('Camera', color_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            run = False
            break
    cam.release()
    cv2.destroyAllWindows()

def open_camera_red():
    None
    # global run
    # run = True
    # while cam.isOpened() and run:
    #     ret, frame = cam.read()
    #     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #     # lower mask (0-10)
    #     lower_red = np.array([0,50,50])
    #     upper_red = np.array([10,255,255])
    #     mask0 = cv2.inRange(hsv_frame, lower_red, upper_red)

    #     # upper mask (170-180)
    #     lower_red = np.array([170,50,50])
    #     upper_red = np.array([180,255,255])
    #     mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)

    #     # saturated mask
    #     lower_range = (0, 0, 0) # lower range of saturated color in HSV
    #     upper_range = (0, 0, 255) # upper range of saturated color in HSV
    #     mask2 = cv2.inRange(hsv_frame, lower_range, upper_range)

    #     # Black mask
    #     lower_black = (0, 0, 0)
    #     upper_black = (180, 255, 30)
    #     mask3 = cv2.inRange(hsv_frame, lower_black, upper_black)
       

    #     # White mask
    #     lower_white = (0, 0, 200)
    #     upper_white = (145, 60, 255)
    #     mask4 = cv2.inRange(hsv_frame, lower_white, upper_white)

    #     # join my masks
    #     mask = mask3 + mask2

    #     #Edge detection method
    #     edges = cv2.Canny(frame, 50, 100)

        
    #     # color_frame = cv2.bitwise_and(frame, frame, mask=mask)
    #     # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #     # cv2.imshow('Camera', color_frame)
    #     # cv2.imshow('edges', edges)
    #     cv2.imshow('camera normal', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         run = False
    #         break
    # cam.release()
    # cv2.destroyAllWindows()

