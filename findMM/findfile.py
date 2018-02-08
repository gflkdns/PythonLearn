import cv2


def nothing(x):
    pass


# 载入图像
img_mb = cv2.imread("./mb.png", 1)
img_temp = cv2.imread("./IMG20170910141515.jpg", 1)
# 创建展示窗口
cv2.namedWindow("image_window", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("result_window", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('R', 'result_window', 0, 255, nothing)
cv2.waitKey(0)
