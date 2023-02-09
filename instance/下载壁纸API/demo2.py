# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: 下载壁纸
# http://www.51testing.com/html/24/n-7794924.html
# *****************************************************************
# https://www.bing.com/th?id=OHR.AiringGrievances_EN-US3147113419_1920x1080.jpg&w=1920

import asyncio, aiohttp, aiofiles, os
from lxml import etree

from PO.BeautifulsoupPO import *


def main():
    if os.path.exists('d://4k') is False:
        os.makedirs('d://4k')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(run())


async def run():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

#         创建个TCPConnector来限制下TCP得连接数、太快受不鸟~(limit为总数量默认为100、limit_per_host为一个host得总数量、要清楚、看怎么用)

    async with aiohttp.TCPConnector(limit=20) as conn:

#             创建个session(官方推荐用同一个session、可以传递状态哦、headers和cookie也可在此定义、后面调用得时候就不用再赋值啦)，把上面得conn传进来还有headers
        async with aiohttp.ClientSession(connector=conn, headers=headers) as session:

    #                    创建个task任务列表，把要执行得任务都丢进去~(get_page就是我们要执行得获取列表页)
            tasks = [get_page(session, _ + 101) for _ in range(10)]

    #                     启动我们得task任务，这里await会阻塞到全部执行完毕并返回
            await asyncio.gather(*tasks)
    print("111111111111111")

# 再来创建获取列表页函数：
async def get_page(session: aiohttp.ClientSession, page: int):

#  这里弄个try捕获可能发生得异常
    try:
        # async with session.get(f'https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page={str(page)}') as response:
        async with session.get(f'https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page=3') as response:

            # 这里要注意(后面一样)，获取返回是一个比较耗时得操作、所以要用await阻塞
            result = await response.text()
            # print(result)
            # 这里就常规xpath了
            result = etree.HTML(result)
            print(result)
            img_list = result.xpath('//div[@class="boxgrid"]/a/@href')
            print(img_list)

            Beautifulsoup_PO = BeautifulsoupPO("https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page=3")

            # # print('1,获取标签属性的值, 获取div id=post_content_87286618651下img src的值'.center(100, "-"))
            img_list = Beautifulsoup_PO.soup.find("div", {'class': 'boxgrid'}).find_all('a')[0].attrs['href']
            print(img_list)

            # 获取到图片页面地址后再来个task让它继续并发去执行(get_img_url, 下一步就要获取图片页面得地址啦)
            task = [get_img_url(session, f'https://wall.alphacoders.com/{_}') for _ in img_list]

            print(task)
            await asyncio.gather(*task)
    except Exception as e:
        print(f'第{page}页获取失败!, {e}')

    print("22222222222")

# 取图片地址
#
#     这里还是一样得操作、就不多余复述了

async def get_img_url(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as response:
            result = await response.text()
            result = etree.HTML(result)
            # img_url = result.xpath('//div[@class="center img-container-desktop"]/a/@href')[0]
            img_url = result.xpath('//div[@class="center img-container-desktop"]/img/@src')

            # 取出图片得下载地址(down_img，就要下载图片啦)
            print(img_url)
            await down_img(session, img_url)
    except Exception:
        pass

    print("33")

# 下载图片

async def down_img(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as response:

            # 这里我把url分割了，目的是为了取出图片得名字、如果你跟着步骤来、你就发现图片名是啥了
            filename = url.split('/')
            filename = filename[-1]

            # 这里还是一样、取返回是耗时操作、await
            result = await response.read()

            # 既然是异步下载、当然少不了异步files.open啦（aiofiles）
            async with aiofiles.open('d://4k//' + filename, 'wb') as file:

                #     写数据一样耗时、await
                await file.write(result)
            print(f'图片: {filename}, 下载完毕!')
    except Exception:
        pass

# 这样一个异步下载图片就完成啦~~~
#
# 这时候运行、你会发现啥都没得~
#
# 少了入口函数啦

if __name__ == '__main__':
    main()








