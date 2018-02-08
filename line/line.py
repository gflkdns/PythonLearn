# -*- coding: utf-8 -*-
import os
import sys, getopt


# 获得该路径下所有的obj文件
def find_files(file_dir, fiter):
    objfiles = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == fiter:
                objfiles.append(os.path.join(root, file))
    print(objfiles)
    return objfiles


def get_decimon_result_path(obj):
    return os.path.abspath(os.path.dirname(obj) + os.path.sep + ".") + "\\result.obj"


def get_convert_result_path(obj):
    return os.path.abspath(os.path.dirname(obj) + os.path.sep + ".") + "\\result.js"


def main():
    # 要减面文件路径
    dir = ""
    # 完成后删掉_obj_mtl
    is_remove_obj_mtl = False
    # 分辨率长宽.
    width = "1080"
    height = "1080"
    opts, args = getopt.getopt(sys.argv[1:], "i:w:h:", ["remove_obj_mtl"])
    for op, value in opts:
        if op == "-i":
            dir = value
        elif op == "--remove_obj_mtl":
            is_remove_obj_mtl = True
        elif op == "-w":
            width = value
        elif op == "-h":
            height = value

    if dir == "":
        exit("Error:Please enter dir and output_file!--> line.py -i [aaa] --remove_obj_mtl")
    # --------------------------------------------------降分辨率------------------------------------------------------
    imgs = find_files(dir, ".jpg")
    # imgs.append(find_files(dir, ".png"))
    for img in imgs:
        if img != "":
            line = [
                "php {root_path}\\texsqueezer.php {imagepath} {width} {height}"
                    .format(
                    root_path=os.path.abspath(os.path.join(sys.path[0], os.path.pardir)),
                    imagepath=img,
                    width=width,
                    height=height),
            ]
            print(line)
            # 执行命令行
            for cmd in line:
                runCmd(cmd)
    # --------------------------------------------------降分辨率------------------------------------------------------
    exit()
    objs = find_files(dir, ".obj")
    for obj in objs:
        line = [
            # -----------减面工具-------------
            # "decimon D:\BalancernProandDecimon\Samples\\topfandisk.obj -o D:\BalancernProandDecimon\Samples\\result.obj -sp 10.0 -f -b",
            'decimon {input_file} -o {output_file} -sp 10.0 -f -b'
                .format(input_file=obj,
                        output_file=get_decimon_result_path(obj)),
            # ------------转二进制-----------
            "{root_path}\convert_obj_three.py "
            "-i {output_file} -o {result_file} -t binary"
                .format(root_path=sys.path[0],
                        output_file=get_decimon_result_path(obj),
                        result_file=get_convert_result_path(obj)),
        ]
        print(line)
        # 执行命令行
        for cmd in line:
            runCmd(cmd)
    if is_remove_obj_mtl:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if os.path.splitext(file)[1] != '.js' \
                        and os.path.splitext(file)[1] != '.bin' \
                        and os.path.splitext(file)[1] != '.jpg' \
                        and os.path.splitext(file)[1] != '.jpeg' \
                        :
                    os.remove(os.path.join(root, file))


def runCmd(cmd):
    p = os.popen(cmd)
    result = p.read()
    print(result)
    return result


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------------------
