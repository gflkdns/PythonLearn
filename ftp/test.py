# !/usr/bin/python3
# coding: utf-8
from ftp import ftp_config
from ftp import ftp_client

import sys

if __name__ == '__main__':
    result = ftp_client.getConnect(
        host=ftp_config.host,
        port=ftp_config.port,
        username=ftp_config.username,
        password=ftp_config.password
    )

    if result[0] != 1:
        print(result[1])
        sys.exit()
    else:
        print("connection success")

    ftp = result[2]

    result = ftp_client.uploadFile(
        ftp=ftp,
        # remoteRelDir="/kubo/test/",
        localAbsPath="D:/looooog.lm"
    )

    # result = ftp_client.upload(
    #     ftp=ftp,
    #     remoteRelDir=remotePath,
    #     localPath=localPath
    # )

    ftp.quit()

    print("全部成功" if result[0] == 1 else "部分失败")
    print(result[1])
    sys.exit()
