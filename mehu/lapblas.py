import cv2

imgArray = [
    "./mohu.jpg",
    "./qingxi.jpg",
]
for img in imgArray:
    imgc = cv2.imread(img)
    img1gray = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
    img2Var = cv2.Laplacian(img1gray, cv2.CV_64F).var()
    cv2.namedWindow('图片模糊值计算')
    cv2.imshow('图片模糊值计算',img1gray)
    cv2.waitKey(0)
    print(img, "清晰度为", img2Var)


cv2.destroyAllWindows()