import requests
from fpdf import FPDF
from PIL import Image

# 配置文件
PAGES = 66  # PPT总页数
FILENAME = "IS4-1.pdf" # 保存的文件名
FirstPngUrl = '''https://s3.ananas.chaoxing.com/doc/f1/6d/33/279b85bfceab58f32b9a7c5bed92e874/thumb/1.png'''  # 网页上第一个ppt图片的url
#请确保存在PPTPIC文件夹,内部已清空

def Crawler():
    for page in range(1, PAGES + 1):
        url = FirstPngUrl.replace('1.png', '{}.png'.format(page))
        print("\r正在爬取第{}/{}张图片....".format(page, PAGES), end="")
        r = requests.get(url)
        with open('PPTPIC/{}.png'.format(page), 'wb') as f:
            f.write(r.content)
    print("图片爬取完成！")


def makePdf(pdfFileName, listPages):
    cover = Image.open(listPages[0])
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(page, 0, 0)
        print("\r正在整合图片{}到PDF...".format(page), end="")

    pdf.output(pdfFileName, "F")


def main():
    try:
        Crawler()
        print("爬取图片成功,图片保存到PPTPIC文件夹中")
    except:
        print("爬取图片失败")
        return
    try:
        imageList = []
        for i in range(1, PAGES + 1):
            imageList.append("PPTPIC/{}.png".format(i))
        makePdf(FILENAME, imageList)
    except:
        print("生成PDF失败")
    print("完成!已保存到{}".format(FILENAME))


if __name__ == '__main__':
    main()
    print("End.")
