# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/11/18

import re
import requests
from bs4 import BeautifulSoup
# from textblob import TextBlob
import time
import random
import pandas as pd


class GoogleNews():

    def __init__(self):
        self.url = 'https://news.google.com'
        self.base = 'https://news.google.com/search?q={:s}&hl=en-US&gl=US&ceid=US%3Aen'
        self.proxy={'https':'127.0.0.1:1080'}
        self.keywords=None
        self.df_search=None
        self.df_detail=None


    # 发送Get请求
    def requests_get(self, url):
        response = None
        try:
            print(url)
            # time.sleep(random.random() * 0.5 + 0.1)  # 暂停随机数
            response=requests.get(url, proxies=self.proxy, timeout=10)
        except Exception as e:
            print(e)
        finally:
            return response

    # 搜索新闻
    def search_news(self, keywords):
        self.keywords=keywords
        search_url = self.base.format(keywords.replace(' ','%20'))
        result=None
        try:
            self.df_search = pd.DataFrame(columns=["Keywords", "Title", "Url", "Summary", "Source", "Stamp"])
            response = self.requests_get(search_url)
            if response is None:
                return result
            # print(response)
            soup = BeautifulSoup(response.text, "html.parser")
            NiLAwe = soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc', jslog='93789')
            # print(NiLAwe.__len__())
            for item in NiLAwe:
                ipQwMb = item.find('h3', class_='ipQwMb ekueJc RD0gLb')
                news_title=ipQwMb.a.text.strip()
                news_url = self.url+ipQwMb.a['href'][1:]
                jVqMGc = item.find('div', class_='Da10Tb Rai5ob', jsname='jVqMGc')
                news_summary=jVqMGc.span.text.strip()
                SVJrMe = item.find('div', class_='SVJrMe', jsname='Hn1wIf')
                news_source=SVJrMe.a.text.strip()
                try:
                    news_stamp = SVJrMe.time['datetime']
                except:
                    news_stamp = ""

                row=[keywords, news_title, news_url, news_summary, news_source, news_stamp]
                self.df_search.loc[len(self.df_search)]=row
                # print(row)
            result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 查看详情
    def news_detail(self, top):
        result=None
        try:
            if self.df_search is None:
                print('self.df_search is None, self.search_news() first')
                return
            self.df_detail = pd.DataFrame(columns=["Keywords", "Title", "Url", "Summary", "Source", "Stamp", "Content"])
            for index, row in self.df_search.iterrows():
                if index>=top:
                    continue
                try:
                    response = self.requests_get(row['Url'])
                    if response is None:
                        row['Content']="error"
                    else:
                        row['Content']=self.html_text(response.text)
                    # row['CleanedData'] = self.datacleaning(row['Content'], self.keywords)
                    # row['Sentiment'] = self.textblob_sentiment(row['CleanedData'])
                    # soup = BeautifulSoup(response.text, "html.parser")
                    # gettext = soup.get_text().strip()
                    # row['html'] = response
                    # row['text'] = gettext

                    self.df_detail.loc[len(self.df_detail)] = row
                except Exception as e:
                    print(e)
                    continue

            result = self.df_detail

        except Exception as e:
            print(e)
        finally:
            return result

    # 保存
    def news_save(self):
        if self.df_detail is not None:
            self.df_detail.to_csv('detail_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_detail.to_excel('detail_{:s}.xlsx'.format(self.keywords))
            return
        if self.df_search is not None:
            self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_search.to_excel('search_{:s}.xlsx'.format(self.keywords))


    # 获取网页文本
    def html_text(self, web_content):
        result=None
        try:
            soup = BeautifulSoup(web_content, "html.parser")
            result=soup.get_text().strip()
        except Exception as e:
            print(e)
        finally:
            return result

    def extract_article(self, web_content):
        # 防止遇到error卡退
        result="error"
        try:
            soup = BeautifulSoup(web_content, 'lxml')
            articleContent = soup.find_all('p')
            article = []
            for p in articleContent:
                article.append(p.text)
            result = '\n'.join(article)
        except Exception as e:
            print(e)
        finally:
            return result


    def datacleaning(self, text, keyword):
        pattern = re.compile("[,;.，；。]+[^,;.，；。]*" + keyword + "+[^,;.，；。]*[,;.，；。]+")
        result = re.findall(pattern, text)
        for i in range(len(result)):
            result[i] = result[i].replace("\xa0", " ")
            result[i] = result[i].replace("\n", "")
        str = '>>'.join(result)
        return str

    # def textblob_sentiment(self, text):
    #     blob = TextBlob(text)
    #     return blob.sentiment


    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):

        df_search=self.search_news('Didi financial crisis')
        print(df_search)

        df_detail=self.news_detail(10)
        print(df_detail)

        self.news_save()


if __name__ == '__main__':

    ac=GoogleNews()
    ac.start()


