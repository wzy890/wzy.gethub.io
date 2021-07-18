'''
思路：
1、拿到主页面的页面源代码，找到ifream
2、从ifream的页面源代码中拿到m3u8文件
3、下载第一层m3u8文件 -> 下载第二层m3u8文件
4、下载视频
5、下载秘钥，进行解密操作
6、合并所有ts文件为一个mp4文件
'''
import re
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES
import os

def get_ifream_src(url):
    resp = requests.get(url)
    main_page = BeautifulSoup(resp.text)
    src = main_page.find("ifream").get("src")
    return src

def get_first_m3u8_url(url):
    resp = requests.get(url)
    print(resp.text)
    obj = re.compile(r'var main = "(?P<m3u8_url>.*?)";', re.S)
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    #print(m3u8_url)
    return m3u8_url

def download_m3u8_file(url, name):
    resp = requests.get(url)
    with open(name, mode="wb") as f:
        f.write(resp.content)
        f.close()
    resp.close()

async def download_ts(url, name, session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video2/{name}", mode="wb") as f:
            await f.write(await resp.content.read()) #把下载的内容写到文件中
    print(f"{name}下载完毕")

async def aio_download(up_url):
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open("越狱第一季第一集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                else:
                    line = line.strip()
                    #拼接真正的ts路径
                    ts_url = up_url + line
                    task = asyncio.create_task(download_ts(ts_url, line, session)) #创建任务
                    tasks.append(task)
            await asyncio.wait(tasks)#等待任务结束

def get_key(url):
    resp = requests.get(url)
    #print(resp.text)
    return resp.text

async def dec_ts(name, key):
    aes = AES.new(key=key, IV='0000000000000000', mode=AES.MODE_CBC)
    async with aiofiles.open(f"video/{name}", mode="rb") as f1,\
        aiofiles.open(f"video/temp_{name}", mode="wb") as f2:
            bs = await f1.read() #从源文件中读取内容
            await f2.write(aes.decrypt(bs))#把解密好的内容存到f2
    print(f"文件{name}处理完毕")


async def aio_dec(key):
    #解密
    tasks = []
    async with aiofiles.open("越狱第一季第一集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            name = line.rsplit("/", 1)[-1]
            task = asyncio.create_task(dec_ts(name, key))
            tasks.append(task)
        await asyncio.wait(tasks)

def merge_ts():
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    list = []
    with open("越狱第一季第一集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            name = line.rsplit("/", 1)[-1]
            list.append(f"temp_{name}")
            s = " ".join(list)
            os.system(f"cat {s} > movie.mp4")
            print("搞定！")

def main(url):
    #拿到页面的源代码，找到ifream对应的url
    ifream_src = get_ifream_src(url)
    #拿到第一层的m3u8文件的下载地址
    first_m3u8_url = get_first_m3u8_url(ifream_src)
    #拿到ifream的域名
    ifream_domain = ifream_src.split("/share")[0]
    #拼接出真正的m3u8文件下载地址
    first_m3u8_url = ifream_domain + first_m3u8_url
    #print(first_m3u8_url)
    #下载第一层m3u8文件
    download_m3u8_file(first_m3u8_url, "越狱第一季第一集_first_m3u8.txt")
    #下载第二层m3u8文件
    with open("越狱第一季第一集_first_m3u8.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            else:
                line = line.strip()
            #准备拼接第二层m3u8地址
                second_m3u8_url = first_m3u8_url.split("index.m3u8")[0] + line
                download_m3u8_file(second_m3u8_url, "越狱第一季第一集_second_m3u8.txt")
                #print("第二层下载完毕")
    #4、下载视频
    second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")
    #异步协程
    asyncio.run(aio_download(second_m3u8_url_up))
    #5、拿到秘钥
    key_url = second_m3u8_url_up + "key.key"
    key = get_key(key_url)
    #解密
    asyncio.run(aio_dec(key))
    #合并ts文件为mp4文件
    merge_ts()


if __name__ == '__main__':
    url = ""
    main(url)
