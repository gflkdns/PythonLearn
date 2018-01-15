import cv2

imgArray = [
    "./mohu.jpg",
    "./qingxi.jpg",
]
for img in imgArray:
    imgc = cv2.imread(img)
    img1gray = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
    img2Var = cv2.Laplacian(img1gray, cv2.CV_64F).var()
    print(img, "清晰度为", img2Var)