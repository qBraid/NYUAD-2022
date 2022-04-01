import qiskit
import cv2

# #path to the image.
# def callImage(path):
#     x1 = Image.open(
#         path).convert('L');
#     y1 = np.asarray(x1.getdata(), dtype=np.float64).reshape((x1.size[1], x1.size[0]));
#     y_dat1 = np.asarray(y1, dtype=np.uint8)     
#     return y_dat1

# #Resize image into n x n pixel ( pixel is an int)
# def imageResize(data,pixel):
#     image = Image.fromarray(data,'L')
#     image= image.resize((pixel, pixel))
#     image=np.asarray(image.getdata(), dtype=np.float64).reshape((image.size[1], image.size[0]))
#     image=np.asarray(image, dtype=np.uint8)    
#     return image

# data_img = callImage("image.jpg")
# plt.imshow(data_img)

image = cv2.imread("image(109).jpg")
# image=cv2.resize(image, (8,8))
window = 'image'
cv2.imshow(window, image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, 0.7)
print(gray)
cv2.imshow(window,gray)

(T, thresh) = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
cv2.imshow(window,thresh)
cv2.waitKey(2000)
# (T, threshInv) = cv2.threshold(gray, 155, 255,cv2.THRESH_BINARY_INV)
# cv2.imshow(window,threshInv)
# cv2.waitKey(2000)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow(window,closed)
cv2.waitKey(2000)

closed = cv2.erode(closed, None, iterations = 14)
closed = cv2.dilate(closed, None, iterations = 13)
cv2.imshow(window,closed)
cv2.waitKey(2000)
