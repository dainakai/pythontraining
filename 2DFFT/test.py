import cv2

img = cv2.imread("unnamed.jpg",1)

cv2.imshow("test",img)
cv2.waitKey(0)
cv2.destroyAllwindows()