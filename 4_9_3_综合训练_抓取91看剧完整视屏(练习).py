'''
思路：
1、拿到主页面的页面源代码，找到ifream
2、从ifream的页面源代码中拿到m3u8文件
3、下载第一层m3u8文件 -> 下载第二层m3u8文件
4、下载视频
5、下载秘钥，进行解密操作
6、合并所有ts文件为一个mp4文件
'''
# url = "https://vod.bunediy.com/20210715/PrYG1Aqa/index.m3u8"
# import requests
#
# resp = requests.get(url)
# with open("video/index.m3u8", mode="wb") as f:
#     f.write(resp.content)
#     f.close()
# resp.close()
# print("m3u8 download over")

import aiohttp
import asyncio
import aiofiles

async def ts_download(url, name, session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video/{name}", mode="wb") as f:
            await f.write(await resp.content.read())
    print(f"{name}下载完毕")

async def aio_download():
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open("video/index.m3u8", mode="r", encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                else:
                    line = line.strip()
                    name = line.rsplit("/", 1)[-1]
                    task = asyncio.create_task(ts_download(line, name, session))
                    tasks.append(task)
            await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(aio_download())
    print("越狱第一集下载完毕")


