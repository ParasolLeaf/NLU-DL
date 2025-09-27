import httpx
from bs4 import BeautifulSoup

def crawl_slang(topic, lang, native_lang):
    # 使用有道词典俚语页面，国内可访问
    url = f"https://dict.youdao.com/example/blng/eng/{topic}/#keyfrom=dict2.index.example"
    try:
        r = httpx.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        slangs = []
        # 抓取例句部分（有道俚语/例句）
        for item in soup.select("#bilingual ul li")[:5]:
            text = item.get_text(strip=True)
            link = url  # 有道例句无独立链接，统一用当前url
            slangs.append({"title": text, "url": link})
        return {"slangs": slangs}
    except Exception as e:
        return {"slangs": [], "error": str(e)} 