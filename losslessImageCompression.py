import os
import shutil
from PIL import Image

dirName = "压缩后图片"


def imgToProgressive(path, dir, mode):
    if not path.split('.')[-1:][0] in ['png', 'jpg', 'jpeg']:  # if path isn't a image file,return
        return
    if os.path.isdir(path):
        return

    # transform img to progressive
    img = Image.open(path)

    destination = path.split('.')[:-1][0] + '_destination.' + path.split('.')[-1:][0]

    try:
        print(path.split('\\')[-1:][0], '开始转换图片')
        if ".png" in path:
            img = img.quantize(colors=256)
            img.save(destination)
        else:
            img.save(destination, "JPEG", quality=50, optimize=True, progressive=True)  # 转换就是直接另存为
        print(path.split('\\')[-1:][0], '转换完毕')
    except IOError:
        PIL.ImageFile.MAXBLOCK = img.size[0] * img.size[1]
        if ".png" in path:
            img = img.quantize(colors=256)
            img.save(destination)
        else:
            img.save(destination, "JPEG", quality=50, optimize=True, progressive=True)
        print(path.split('\\')[-1:][0], '转换完毕')
    # print('开始重命名文件')
    if mode:
        os.remove(path)
        os.rename(destination, path)
    else:
        os.rename(path, path + ".backup")
        os.rename(destination, path)
        if os.path.exists(dir + os.path.basename(path)):
            os.remove(dir + os.path.basename(path))
        shutil.move(path, dir)
        os.rename(path + ".backup", path)


def compressImage(mode):
    for root, _, fl in os.walk(os.getcwd()):  # 遍历目录下所有文件
        print(root)
        flag = True
        dir = root + "\\" + dirName + "\\"
        if modeSelect:
            dir = root
        else:
            if root == os.getcwd():
                if not os.path.isdir(dirName):
                    os.mkdir(root + '\\' + dirName)
            else:
                #  判断是否是已压缩过的文件夹
                if len(root[len(os.getcwd())+1:]) != 0:
                    print(len(root[len(os.getcwd()):]))
                    for d in root[len(os.getcwd())+1:].split('\\'):
                        print('1:{}'.format(d))
                        if d == dirName:
                            print('2:{}'.format(d))
                            flag = False
                            break
                        else:
                            flag = True
                if flag:
                    if os.path.abspath("..\\" + root).split('\\')[-1] != dirName:
                        if not os.path.isdir(root + '\\' + dirName):
                            os.mkdir(root + '\\' + dirName)

        if flag:
            for f in fl:
                try:
                    imgToProgressive(root + '\\' + f, dir, mode)
                except:
                    pass


if __name__ == '__main__':
    keyIn = input("按回车:保留原图压缩, 输入 Cover：覆盖原图压缩\n")
    if keyIn == "":
        modeSelect = False
        compressFlag = True
    elif keyIn.lower() == "cover":
        modeSelect = True
        compressFlag = True
    elif '/' in keyIn:
        dirName = keyIn[1:]
        # print(dirName)
        modeSelect = False
        compressFlag = True
    else:
        modeSelect = False
        compressFlag = False
    if compressFlag:
        compressImage(modeSelect)
        input("压缩完毕,按任意键结束")
    else:
        input("再见~")
