import requests 
url = "http://api.soyiji.com//news_jpg"
resp = requests.get(url)

headers = {
    "Referer": "safe.soyiji.com"
}

jpg_url = resp.json()["url"]
resp1 = requests.get(jpg_url, headers=headers)
# with open("1.jpg", mode="wb") as f:
#     f.write(resp1.content)
#     f.close()
with open("1.txt", mode="wb") as f:
    f.write(resp1.content)
resp.close()
resp1.close()

