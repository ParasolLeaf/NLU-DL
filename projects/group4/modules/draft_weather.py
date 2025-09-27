import os
import asyncio
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()


async def search_baidu_and_scrape_with_playwright(query):
    """
    使用异步Playwright访问百度搜索结果
    """
    async with async_playwright() as p:
        # 启动浏览器（异步）
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/117.0.0.0 Safari/537.36 "
        )

        try:
            # 访问百度
            url = f"https://www.baidu.com/s?wd={query}"
            await page.goto(url)

            # 获取页面内容
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            results = []
            for item in soup.find_all("div", class_="c-container"):
                title_tag = item.find("h3")
                link_tag = item.find("a")

                title = title_tag.get_text() if title_tag else "无标题"
                link = link_tag.get("href") if link_tag else "无链接"

                if link != "无链接":
                    try:
                        # 异步访问链接
                        await page.goto(link)
                        page_content = await page.content()
                        page_soup = BeautifulSoup(page_content, 'html.parser')
                        page_text = page_soup.get_text(strip=True)[:1500]
                    except Exception as e:
                        page_text = f"访问页面时出错：{e}"
                else:
                    page_text = "无效链接"

                results.append({"title": title, "link": link, "content": page_text})

            # 创建异步OpenAI客户端
            client = AsyncOpenAI(
                api_key=os.getenv("QWEN_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            messages = [
                {'role': 'system', 'content':
                    '判断哪些输入文本是有效的信息，而不是乱码或字符无逻辑的组合。通过含有有效信息的文本整合给出未来天气的逐天预测，在能确保准确性的基础上预报未来14'
                    '天的天气。根据天气描述在每天的预报后标注适合室内活动或户外运动，无需解释原因。将答案以“1. '
                    '2025年07月07日（星期一）：阵雨转多云，气温范围21°C至29°C，适合室内活动。”的格式输出。'},
            ]

            for result in results:
                messages.append({'role': 'user', 'content': result['content']})

            # 异步调用API
            completion = await client.chat.completions.create(
                model="qwen-max-latest",
                messages=messages,
            )

            response = completion.choices[0].message.content
            return f"=== 搜索整合结果 ===\n{response}\n=== 结束 ==="

        finally:
            await browser.close()


# 异步测试主函数
async def main():
    query = input("请输入要查询的城市名称：") + '天气'
    results = await search_baidu_and_scrape_with_playwright(query)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
