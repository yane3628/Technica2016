import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('Koala.jpg',0)

cv2.imshow('Koala', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
