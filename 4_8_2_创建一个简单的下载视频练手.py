'''
流程：
1、拿到页面源代码
2、从源代码中下载m3u8的url
3、下载m3u8
4、从m3u8读取，下载视频
5、合并视频
'''
import requests
import re

# url = "https://www.91kanju.com/vod-play/54812-1-1.html"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
# }
# obj = re.compile(r"url: '(?P<url>.*?)',", re.S) #用来提取m3u8的地址
# resp = requests.get(url, headers=headers)
#
# m3u8_url = obj.search(resp.text).group("url")#拿到m3u8的地址
# # print(m3u8_url)
# resp.close()
#
# #下载m3u8文件
#
# resp1 = requests.get(m3u8_url, headers=headers)
# with open("哲人王后.m3u8", mode="wb") as f:
#     f.write(resp1.content)
#     f.close()
#
# resp1.close()
# print("m3u8缓存完毕")

n = 1
with open("video/哲人王后.m3u8", mode="r", encoding="utf-8") as f:
    for line in f:
        line = line.strip() #去掉空格，空白，换行符
        if line.startswith("#"):#不要以#开头的行
            continue
        #下载视频片段
        resp3 = requests.get(line)
        f = open(f"video/{n}.ts", mode="wb")
        f.write(resp3.content)
        f.close()
        print(f"下载完成了{n}个.ts文件")
        n += 1
        resp3.close()