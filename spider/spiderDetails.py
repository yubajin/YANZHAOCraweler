from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selectQuery import *

class SpiderDetails:
    # DETAILS_COLLECTION = "details"

    # browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    def __init__(self):
        self.url = set()

    def index_page(self,url,_985,_211):
        """
        抓取索引页
        """
        try:
            SpiderDetails.browser.get(url)
            html = SpiderDetails.browser.page_source
            soup = BeautifulSoup(str(html), 'html.parser')

            zsml_condition = soup.select('.zsml-condition')

            table1 = BeautifulSoup(str(zsml_condition), 'html.parser')
            tr0 = table1.find_all('tr')[0]
            school = BeautifulSoup(str(tr0),'html.parser').find_all('td')[1].get_text()
            TestType = BeautifulSoup(str(tr0), 'html.parser').find_all('td')[3].get_text()

            tr1 = table1.find_all('tr')[1]
            department = BeautifulSoup(str(tr1), 'html.parser').find_all('td')[1].get_text()

            tr2 = table1.find_all('tr')[2]
            major = BeautifulSoup(str(tr2), 'html.parser').find_all('td')[1].get_text()
            studyType = BeautifulSoup(str(tr2), 'html.parser').find_all('td')[3].get_text()

            tr3 = table1.find_all('tr')[3]
            direction = BeautifulSoup(str(tr3), 'html.parser').find_all('td')[1].get_text()

            tr4 = table1.find_all('tr')[4]
            rawNumber = BeautifulSoup(str(tr4), 'html.parser').find_all('td')[1].get_text()
            zhaosheng_number = rawNumber.split('：')[1].split('(')[0]

            tuimian_number=''
            print(school+','+TestType+','+department+','+major+','+studyType+','+direction+','+zhaosheng_number)

            example_scope =  ''
            zsml_result = soup.select('.zsml-result')
            zsml_result_items = BeautifulSoup(str(zsml_result), 'html.parser').select('.zsml-res-items')
            for zsml_result_item in zsml_result_items:
                zsml_result_item_tds = BeautifulSoup(str(zsml_result_item), 'html.parser').find_all('td')

                for zsml_result_item_td in zsml_result_item_tds:
                    example_scope += zsml_result_item_td.get_text() + ','

                example_scope = example_scope.replace('\n','').replace(' ','').replace('见招生简章','')
                example_scope += ';'

            cur_sql_users_value ="('" + school + "','" + str(_985) + "','"+ str(_211) + "','"+ department + "','"+ major + "','" + direction+ "','"+ str(zhaosheng_number) + "','"+ str(tuimian_number) + "','"+ example_scope+ "')"
            print(cur_sql_users_value)
            # cur_sql_users= "insert into " + '(db)' + "(school,_985,_211,department,major,direction,zhaosheng_number,tuimian_number,example_scope) values"  + cur_sql_users_value
            # print("sql语句为:" + cur_sql_users)

        except TimeoutException:
            print("爬取院校失败")

if __name__ == '__main__':
    spider = SpiderDetails()
    url = 'https://yz.chsi.com.cn/zsml/kskm.jsp?id=1000121001025100001'

    spider.index_page(url,True,True)
