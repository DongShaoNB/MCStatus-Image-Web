import PIL
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import ImageFont
from fastapi import *
import re
import cv2
from PIL import *
import numpy as np
from mcstatus import *
import requests
import os
import json
import logging
from starlette.responses import *
from loadconfig import *
import uvicorn
from typing import *

app = FastAPI(title="MCJEServerStatus-Image", description="MCJEServerStatus-Image", docs_url=None, redoc_url=None)


@app.get("/")
async def welcome():
    return {"Welcome": "欢迎使用MCJEServerStatus-Image，作者DongShaoNB，请在访问地址后加上在配置文件中设置的后缀以访问motd页面"}


@app.get(suffix)
async def main(ip: Optional[str] = None):
    # 获取服务器信息
    server = MinecraftServer.lookup(ip)
    status = server.status()

    # 图片处理
    openImage = cv2.imread("background.png")
    fontpath = "unifont-12.1.04.ttf"
    font = ImageFont.truetype(fontpath, 28)
    img_pil = Image.fromarray(openImage)
    draw = ImageDraw.Draw(img_pil)

    # 插入文字
    draw.text((18, 10), "MOTD:", font=font, fill=(255, 0, 0))
    draw.text((92, 10), "     MCJEServerStatus-Image", font=font, fill=(0, 0, 255))

    draw.text((18, 56), "协议版本:", font=font, fill=(255, 255, 255))
    draw.text((146, 56), f"{status.version.protocol}", font=font, fill=(255, 255, 255))

    draw.text((18, 106), "游戏版本:", font=font, fill=(255, 255, 255))
    draw.text((146, 106), f"{status.version.name}", font=font, fill=(255, 255, 255))

    draw.text((18, 156), "在线人数:", font=font, fill=(255, 255, 255))
    draw.text((146, 156), f"{status.players.online}/{status.players.max}", font=font, fill=(255, 255, 255))

    draw.text((18, 206), "介绍:", font=font, fill=(255, 255, 255))
    temp_status_description = re.sub('§[0-9a-z]', '', status.description)
    status_description = temp_status_description.replace(" ", "")
    draw.text((92, 206), status_description, font=font, fill=(255, 255, 255))

    draw.text((18, 256), "延迟:", font=font, fill=(255, 255, 255))
    draw.text((92, 256), f"{status.latency}ms", font=font, fill=(255, 255, 255))

    draw.text((18, 306), "              作者:DongShaoNB", font=font, fill=(0, 0, 255))

    # 保存图片
    main_img = np.array(img_pil)
    cv2.imwrite("cache.png", main_img)
    file_like = open('cache.png', mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port)
