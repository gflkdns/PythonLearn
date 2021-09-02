rm -rf apk_dump.spec
rm -rf build
rm -rf dist

pyinstaller -F --uac-admin apk_dump.py -i .\icon.ico