from PIL import Image
im=Image.open("C:/Users/t54/Pictures/b4ee294c220f04d5bff66ecf2afa9933.jpg")
print(im.mode)


from PIL import ImageFilter                         ## 调取ImageFilter
bluF = im.filter(ImageFilter.BLUR)                ##均值滤波
conF = im.filter(ImageFilter.CONTOUR)             ##找轮廓
edgeF = im.filter(ImageFilter.FIND_EDGES)         ##边缘检测
im.show()
bluF.show()
conF.show()
edgeF.show()
