from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

from link import engine

def open_url():
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    res = requests.get("https://ncov.dxy.cn/ncovh5/view/pneumonia",
                       headers=headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    return res.text


def get_china_url(res):
    china_url = []
    soup = BeautifulSoup(res, 'html5lib')
    htmlBodyText = soup.body.text
    provinceDataText = htmlBodyText[htmlBodyText.find('window.getAreaStat = '
                                                      ):]
    provinceDataStr = provinceDataText[
        provinceDataText.find('[{'):provinceDataText.find('}catch')]
    provinceDataJson = json.loads(provinceDataStr)
    for i in range(0, len(provinceDataJson)):
        a = provinceDataJson[i]['provinceShortName'], provinceDataJson[i][
            'statisticsData']
        china_url.append(a)
    return china_url


def save_sql(china_url):
    name = ['省份', '地址']
    df = pd.DataFrame(data=china_url, columns=name)
    df.to_sql(name='chinaurl',
              con=engine,
              if_exists='append',
              index=False,
              index_label=False)


def main():
    res = open_url()
    china_url = get_china_url(res)
    save_sql(china_url)


if __name__ == '__main__':
    main()
