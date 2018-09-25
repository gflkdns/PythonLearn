# !/usr/bin/python3
# coding: utf-8

from ftp import ftp_config

import ftplib
import os


# 获取连接
def getConnect(host, port, username, password):
    """
    :param host: FTP ip
    :param port: FTP port
    :param username: FTP userName
    :param password: FTP password
    :return: ftp
    """
    print("FTP connection...")
    result = [1, ""]

    try:
        ftp = ftplib.FTP()
        # ftp.set_debuglevel(2)
        ftp.connect(host, port)
        ftp.login(username, password)

        result = [1, "connection success", ftp]

    except Exception as e:
        result = [-1, "connection fail, reason:{0}".format(e)]

    return result


# 下载
def download(ftp, remotePath, localAbsDir):
    """
    :param ftp:
    :param remotePath: 服务端文件或文件夹的绝对或相对路径
    :param localAbsDir: 客户端文件夹的绝对路径，如E:/FTP/downDir/
    :return:
    """
    result = [1, ""]

    try:
        remotePath = formatPath(remotePath)
        localAbsDir = formatPath(localAbsDir)

        remoteRel = ""
        if remotePath == "":
            remotePath = ftp_config.homeDir
        else:
            if remotePath.startswith(ftp_config.homeDir):
                remoteRel = remotePath.replace(ftp_config.homeDir, "/")
                remoteRel = formatPath(remoteRel)
            else:
                remoteRel = remotePath

        if localAbsDir == "":
            localAbsDir = ftp_config.localDir
            localAbsDir = formatPath(localAbsDir)

        remoteAbs = formatPath(ftp_config.homeDir, remoteRel)  # 服务端文件或文件夹的绝对路径

        if os.path.isdir(remoteAbs):
            rs = downloadDir(ftp, remoteRel, localAbsDir)
        else:
            rs = downloadFile(ftp, remoteRel, localAbsDir)

        if rs[0] == -1:
            result[0] = -1
        result[1] = result[1] + "\n" + rs[1]
    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# 下载指定文件夹下的所有
def downloadDir(ftp, remoteRelDir, localAbsDir):
    """
    :param ftp:
    :param remoteRelDir: 服务端文件的相对路径,含文件后缀，如/srcDir/
    :param localAbsDir: 客户端文件夹的绝对路径，如E:/FTP/downDir/
    :return:
    """
    print("start download dir by use FTP...")
    result = [1, ""]

    try:
        remoteRelDir = formatPath(remoteRelDir)
        localAbsDir = formatPath(localAbsDir)

        files = []  # 文件
        dirs = []  # 文件夹
        remotePaths = ftp.nlst(remoteRelDir)
        if len(remotePaths) > 0:
            for remotePath in remotePaths:
                remotePath = formatPath(remotePath)

                if isDir(ftp, remotePath):
                    dirs.append(remotePath)
                else:
                    files.append(remotePath)

        ftp.cwd("")  # 切回homeDir
        if len(files) > 0:
            for rrp in files:  # rrp is relPath
                rs = downloadFile(ftp, rrp, localAbsDir)
                if rs[0] == -1:
                    result[0] = -1
                result[1] = result[1] + "\n" + rs[1]

        if len(dirs) > 0:
            for rrd in dirs:  # rrd is relDir
                dirName = lastDir(rrd)
                localAbsDir = formatPath(localAbsDir, dirName)
                rs = downloadDir(ftp, rrd, localAbsDir)
                if rs[0] == -1:
                    result[0] = -1
                result[1] = result[1] + "\n" + rs[1]

    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# 下载指定文件
def downloadFile(ftp, remoteRelPath, localAbsDir):
    """
    :param ftp:
    :param remoteRelPath: 服务端文件的相对路径,含文件后缀，如/srcDir/file.txt
    :param localAbsDir: 客户端文件夹的绝对路径，如E:/FTP/downDir/
    :return:
    """
    print("start download file by use FTP...")
    result = [1, ""]

    try:
        fileName = os.path.basename(remoteRelPath)  # 文件名

        localAbsPath = formatPath(localAbsDir, fileName)
        splitPaths = os.path.split(localAbsPath)

        lad = splitPaths[0]
        lad = formatPath(lad)
        if not os.path.exists(lad):
            os.makedirs(lad)

        handle = open(localAbsPath, "wb")
        ftp.retrbinary("RETR %s" % remoteRelPath, handle.write, 1024)
        handle.close()

        result = [1, "download " + splitPaths[1] + " success"]
    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# 上传
def upload(ftp, remoteRelDir, localPath):
    """
    :param ftp:
    :param remoteRelDir: 服务端文件夹相对路径，可以为None、""，此时文件上传到homeDir
    :param localPath: 客户端文件或文件夹路径，当路径以localDir开始，文件保存到homeDir的相对路径下
    :return:
    """
    result = [1, ""]

    try:
        remoteRelDir = formatPath(remoteRelDir)
        localPath = formatPath(localPath)

        localRelDir = ""
        if localPath == "":
            localPath = ftp_config.localDir
            localPath = formatPath(localPath)
        else:
            if localPath.startswith(ftp_config.localDir):  # 绝对路径
                localRelDir = localPath.replace(ftp_config.localDir, "/")
                localRelDir = formatPath(localRelDir)
            else:  # 相对(localDir)路径
                localPath = formatPath(ftp_config.localDir, localPath)

        if remoteRelDir == "":
            remoteRelDir = formatPath("/uploadFiles/", localRelDir)
        else:
            if remoteRelDir.startswith(ftp_config.homeDir):
                remoteRelDir = remoteRelDir.replace(ftp_config.homeDir, "/")
                remoteRelDir = formatPath(remoteRelDir)

        if os.path.isdir(localPath):  # isDir
            rs = uploadDir(ftp, remoteRelDir, localPath)
        else:  # isFile
            rs = uploadFile(ftp, remoteRelDir, localPath)

        if rs[0] == -1:
            result[0] = -1
        result[1] = result[1] + "\n" + rs[1]

    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


# 上传指定文件夹下的所有
def uploadDir(ftp, remoteRelDir, localAbsDir):
    """
    :param ftp:
    :param remoteRelDir: 服务端文件夹相对路径，可以为None、""，此时文件上传到homeDir
    :param localAbsDir: 客户端文件夹路径，当路径以localDir开始，文件保存到homeDir的相对路径下
    :return:
    """
    print("start upload dir by use FTP...")
    result = [1, ""]

    try:
        for root, dirs, files in os.walk(localAbsDir):
            if len(files) > 0:
                for fileName in files:
                    localAbsPath = localAbsDir + fileName
                    rs = uploadFile(ftp, remoteRelDir, localAbsPath)
                    if rs[0] == -1:
                        result[0] = -1
                    result[1] = result[1] + "\n" + rs[1]

            if len(dirs) > 0:
                for dirName in dirs:
                    rrd = formatPath(remoteRelDir, dirName)
                    lad = formatPath(localAbsDir, dirName)
                    rs = uploadDir(ftp, rrd, lad)
                    if rs[0] == -1:
                        result[0] = -1
                    result[1] = result[1] + "\n" + rs[1]

            break
    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


# 上传指定文件
def uploadFile(ftp, remoteRelDir, localAbsPath):
    """
    :param ftp:
    :param remoteRelDir: 服务端文件夹相对路径，可以为None、""，此时文件上传到homeDir
    :param localAbsPath: 客户端文件路径，当路径以localDir开始，文件保存到homeDir的相对路径下
    :return:
    """
    print("start upload file by use FTP...")
    result = [1, ""]

    try:
        try:
            ftp.cwd(remoteRelDir)
        except ftplib.error_perm:
            try:
                ftp.mkd(remoteRelDir)
            except ftplib.error_perm:
                print("U have no authority to make dir")

        fileName = os.path.basename(localAbsPath)
        remoteRelPath = formatPath(remoteRelDir, fileName)

        handle = open(localAbsPath, "rb")
        ftp.storbinary("STOR %s" % remoteRelPath, handle, 1024)
        handle.close()

        result = [1, "upload " + fileName + " success"]
    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


# 判断remote path isDir or isFile
def isDir(ftp, path):
    try:
        ftp.cwd(path)
        ftp.cwd("..")
        return True
    except:
        return False


# return last dir'name in the path, like os.path.basename
def lastDir(path):
    path = formatPath(path)
    paths = path.split("/")
    if len(paths) >= 2:
        return paths[-2]
    else:
        return ""


# 格式化路径或拼接路径并格式化
def formatPath(path, *paths):
    """
    :param path: 路径1
    :param paths: 路径2-n
    :return:
    """
    if path is None or path == "." or path == "/" or path == "//":
        path = ""

    if len(paths) > 0:
        for pi in paths:
            if pi == "" or pi == ".":
                continue
            path = path + "/" + pi

    if path == "":
        return path

    while path.find("\\") >= 0:
        path = path.replace("\\", "/")
    while path.find("//") >= 0:
        path = path.replace("//", "/")

    if path.find(":/") > 0:  # 含磁盘符 NOT EQ ZERO, OS.PATH.ISABS NOT WORK
        if path.startswith("/"):
            path = path[1:]
    else:
        if not path.startswith("/"):
            path = "/" + path

    if os.path.isdir(path):  # remote path is not work
        if not path.endswith("/"):
            path = path + "/"
    elif os.path.isfile(path):  # remote path is not work
        if path.endswith("/"):
            path = path[:-1]
    elif path.find(".") < 0:  # maybe it is a dir
        if not path.endswith("/"):
            path = path + "/"
    else:  # maybe it is a file
        if path.endswith("/"):
            path = path[:-1]

    # print("new path is " + path)
    return path
