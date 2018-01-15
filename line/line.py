# -*- coding: utf-8 -*-
import os
import sys, getopt


# 获得该路径下所有的obj文件
def file_name(file_dir):
    objfiles = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.obj':
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

    opts, args = getopt.getopt(sys.argv[1:], "i:", ["remove_obj_mtl"])
    for op, value in opts:
        if op == "-i":
            dir = value
        elif op == "--remove_obj_mtl":
            is_remove_obj_mtl = True

    if dir == "":
        exit("Error:Please enter dir and output_file!--> line.py -i [aaa] --remove_obj_mtl")
    objs = file_name(dir)
    for obj in objs:
        line = [
            # -----------减面工具-------------
            # "decimon D:\BalancernProandDecimon\Samples\\topfandisk.obj -o D:\BalancernProandDecimon\Samples\\result.obj -sp 10.0 -f -b",
            'decimon {input_file} -o {output_file} -sp 10.0 -f -b'
                .format(input_file=obj,
                        output_file=get_decimon_result_path(obj)),
            # ------------转二进制-----------
            "python F:\PythonPoj\PythonLearn\line\convert_obj_three.py "
            "-i {output_file} -o {result_file} -t binary"
                .format(output_file=get_decimon_result_path(obj),
                        result_file=get_convert_result_path(obj)),
        ]
        print(line)
        # 执行命令行
        for cmd in line:
            runCmd(cmd)
        # if is_remove_obj_mtl:
    # os.remove(obj)


def runCmd(cmd):
    p = os.popen(cmd)
    result = p.read()
    print(result)
    return result


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------------------
