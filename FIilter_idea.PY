import cv2
import numpy as np
import random

WIDTH, HEIGHT = 800, 800

CELL = 12

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"
drops = [random.randint(-50,0)
        for _ in range(WIDTH // CELL)]
mode = "BLUE"
while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Edges filter
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    black = edges * 0
    if mode == "BLUE":
        neon_lines = cv2.merge([edges,black,black])
    elif mode == "CYAN":
        neon_lines = cv2.merge([edges,edges,black])
    elif mode == "RED":
        neon_lines = cv2.merge([black,black,edges])
    elif mode == "PINK":
        neon_lines = cv2.merge([edges,black,edges])
    elif mode == "GREEN":
        neon_lines = cv2.merge([black,edges,black])


    #Matrix filter
    canvas = np.zeros_like(frame)
    for col in range(len(drops)):
        x = col * CELL
        for row in range(HEIGHT//CELL):
            y = row * CELL

            brightness = gray[y, x]

            if brightness > 50:
                char = random.choice(chars)
                green = int(brightness)

                cv2.putText(canvas, char, (x,y), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,green,0), 1)

    y = drops[col] * CELL

    drops[col] += 1

    if y > HEIGHT:
        drops[col] = random.randint(-20 ,20)

    canvas = cv2.add(canvas, neon_lines)

    cv2.imshow("edges", canvas)

    key = cv2.waitKey(30) & 0xff
    if key == ord('q'):
        break
    if key == ord('1'):
        mode = "RED"
    if key == ord('2'):
        mode = "BLUE"
    if key == ord('3'):
        mode = "CYAN"
    if key == ord('4'):
        mode = "PINK"
    if key == ord('5'):
        mode = "GREEN"

cap.release()
cv2.destroyAllWindows()

