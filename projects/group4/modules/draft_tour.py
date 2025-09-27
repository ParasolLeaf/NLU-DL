from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()


async def search_for_destination(query, num_needed):
    """
    使用异步 Playwright 访问百度搜索结果，并抓取动态加载的内容。

    参数:
        query (str): 要搜索的关键词
        num_needed (int): 需要的景点数量

    返回:
        str: 包含景点信息的格式化结果
    """
    async with async_playwright() as p:
        # 启动浏览器（无头模式）
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/117.0.0.0 Safari/537.36"
        )

        try:
            # 访问百度搜索页面
            url = f"https://www.baidu.com/s?wd={query}"
            await page.goto(url)

            # 等待页面加载
            await page.wait_for_load_state("networkidle")

            # 使用 BeautifulSoup 解析页面内容
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # 提取搜索结果
            results = []
            for item in soup.find_all("div", class_="c-container"):
                title_tag = item.find("h3")
                link_tag = item.find("a")

                title = title_tag.get_text() if title_tag else "无标题"
                link = link_tag.get("href") if link_tag else "无链接"

                # 如果链接有效，则访问该链接并抓取内容
                if link != "无链接":
                    try:
                        await page.goto(link)
                        await page.wait_for_load_state("domcontentloaded")
                        page_content = await page.content()
                        page_soup = BeautifulSoup(page_content, 'html.parser')
                        page_text = page_soup.get_text(strip=True)[:1500]  # 只提取前 1500 字符
                    except Exception as e:
                        page_text = f"访问页面时出错：{e}"
                else:
                    page_text = "无效链接"

                results.append({"title": title, "link": link, "content": page_text})

            # 创建异步 OpenAI 客户端
            client = AsyncOpenAI(
                api_key=os.getenv("QWEN_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            messages = [
                {'role': 'system',
                 'content': f'判断哪些输入文本是有效的信息，而不是乱码或字符无逻辑的组合。通过含有有效信息的文本整合，从知名度/游览人数、当前是否营业、建议游玩时间筛选出最优的{num_needed}个景点('
                            '如有不足则以“待定”补充)，并以最优的景点为第一个依次写出景点名称、一两句话的景点介绍及“文本整合，从知名度/游览人数、当前是否营业（开放时间）、建议游玩时间”这几个方面的'
                            '信息，如果在输入文本中有的话，没有则标为未知。对于建议游玩时间，如果不在输入文本中提及，则根据景点类型预测大致需要多长的游玩时间，标记为未知--预计时间为...。如XX博物'
                            '馆未提及建议游玩时间，则根据一般博物馆推荐的游玩时间预测游玩时间。如果能判断出景点是室内游玩就标记为室内活动，如果是室外游玩就标记为室外活动，如博物馆一般是室内活动，判'
                            '断不出或室内室外都有的情况下标记为同时包括室内室外活动。'}
            ]
            # 打印搜索结果
            for result in results[:5]:  # 限制前5个结果避免过长
                messages.append({'role': 'user', 'content': result['content']})

            # 调用异步API
            completion = await client.chat.completions.create(
                model="qwen-max-latest",
                messages=messages,
                max_tokens=4096,
            )

            # 提取并返回结果
            response = completion.choices[0].message.content
            return f"=== {query} 景点搜索结果 ===\n{response}\n=== 结束 ==="

        except Exception as e:
            return f"搜索过程中出错：{str(e)}"

        finally:
            # 关闭浏览器
            await browser.close()


# 异步测试主函数
async def main():
    # 输入要搜索的关键词
    query = input("请输入要查询的城市名称：")
    query = query + ' 景点 名单 知名度 游览人数 当前是否营业 建议游玩时间'
    num_needed = int(input("请输入需要的景点数："))

    # 调用异步函数获取搜索结果
    search_results = await search_for_destination(query, num_needed)
    print(search_results)


if __name__ == "__main__":
    asyncio.run(main())
