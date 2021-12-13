from bs4 import BeautifulSoup
import json
import pandas as pd
import requests

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


def get_world_url(res):
    world_url = []
    soup = BeautifulSoup(res, 'html5lib')
    htmlBodyText = soup.body.text
    worldDataText = htmlBodyText[
        htmlBodyText.find('window.getListByCountryTypeService2true = '):]
    worldDataStr = worldDataText[worldDataText.find('[{'):worldDataText.
                                 find('}catch')]
    worldDataJson = json.loads(worldDataStr)
    for i in range(0, len(worldDataJson)):
        a = worldDataJson[i]['provinceName'], worldDataJson[i][
            'countryFullName'], worldDataJson[i]['statisticsData']
        world_url.append(a)

    return world_url


def save_sql(world_url):
    name = ['名称', '全称', '地址']
    df = pd.DataFrame(data=world_url, columns=name)

    df.to_sql(name='worldurl',
              con=engine,
              if_exists='append',
              index=False,
              index_label=False)


def main():
    res = open_url()
    world_url = get_world_url(res)
    save_sql(world_url)


if __name__ == '__main__':
    main()
