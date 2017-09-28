import sys


def decode(type, key):
    找到所有的文件
    if type == '-d':
    # 加密

    elif type == '-u':
    # 解密

    else:
        print('error:Please follow (FileLock.py dir -[option] [key]) the format of the input parameters.')
    pass


def main():
    args = sys.argv
    if len(args) < 3:
        print('error:Please follow (FileLock.py -[option] [key]) the format of the input parameters.')
        return
    filedir = args[1]
    type = args[2]
    key = args[3]
    decode(filedir, type, key)


main()
