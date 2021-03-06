import pymssql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from config import *
from utils.RequestLingyu import *
from utils.RequestZhuanye import *
from utils.RequestMenLei import *
from utils.MSSQL import *
from utils.MyLog import *
import os

'''
有研招网硕士目录查询进入学校招生单位查询
'''
class SpiderSchool:

    browser = webdriver.Chrome()

    def getWebDriver(self):
        '''
        获得浏览器连接驱动
        :return:
        '''
        browser = webdriver.Chrome()
        # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        return browser

    def selectBySFCode1(self,ssCode='36'):
        '''
        按省份代码硕士专业目录
        :param ssCode:省份代码,参数为字符串
        :return:jumpToSchool_part1和jumpToSchool_part2组成的部分js代码
        '''
        result = ''
        curPath = os.path.abspath(os.path.dirname(__file__))
        filename = curPath + '\\js\\jumpToSchool_part1.txt'
        file = open(filename,'rb')
        str1 = file.read().decode('utf-8')

        filename_part = curPath + '\\js\\jumpToSchool_part2.txt'
        file_part = open(filename_part, 'rb')
        str3 = file_part.read().decode('utf-8')

        result = str1 + str(ssCode) + str3

        return  result

    def selectByMLLBOption2(self,mlCode='zyxw'):
        '''
         按门类类别选择硕士专业目录
        :param mlCode:门类类别代码，参数为字符串 zyxw表示专业学位
        :return:和jumpToSchool_part3组成的部分js代码
        '''
        result = ''
        curPath = os.path.abspath(os.path.dirname(__file__))
        filename_part = curPath + '\\js\\jumpToSchool_part3.txt'
        file_part = open(filename_part, 'rb')
        jsStr = file_part.read().decode('utf-8')

        result = mlCode + jsStr

        return result

    def selectByZYLYOption3(self,zyly='0852'):
        '''
         按具体专业名称查找硕士专业目录
        :param zyly:专业领域代码，参数为字符串 0852表示软件工程
        :return:和jumpToSchool_part4组成的部分js代码
        '''
        result = ''
        curPath = os.path.abspath(os.path.dirname(__file__))
        filename_part = curPath + '\\js\\jumpToSchool_part4.txt'
        file_part = open(filename_part, 'rb')
        jsStr = file_part.read().decode('utf-8')

        result = zyly + jsStr

        return result

    def selectByZYMCOption4(self,zymc="'软件工程'"):
        '''
         按专业领域查找硕士专业目录
        :param zymc:专业名称，参数为字符串
        :return:和jumpToSchool_part5组成的部分js代码
        '''
        result = ''
        curPath = os.path.abspath(os.path.dirname(__file__))
        filename_part = curPath + '\\js\\jumpToSchool_part5.txt'
        file_part = open(filename_part, 'rb')
        jsStr = file_part.read().decode('utf-8')

        result = "'"+ zymc + "'" + jsStr

        return result

    def resolvePageAndInsert(self, mlName,zyName,doc, db):
        '''
        将传进来的门类类别和专业名称参数，和对获得的网页doc进行解析得到的一条一条信息组合,并逐条处理，插入数据库中
        :param mlName:门类类别名称
        :param zyName:专业名称代码
        :param doc:要解析的网页文档
        :param db:要插入的数据库名称
        :return:
        '''
        soup = BeautifulSoup(str(doc), 'html.parser')
        page = soup.find(class_='ch-table')

        next = True&(page!=None)
        if(page==None):
            MyLog.warning(mlName +  ',' + zyName + '没有数据')

        while next:
            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            tbody = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            trr = BeautifulSoup(str(tbodyRaw), 'html.parser').find('tr')


            if '很抱歉' in trr.get_text():
                MyLog.warning('tbody没有数据')
                return

            for item in tbody:
                # print('item\n', item)
                typeItems = item.select('.ch-table-center')[0]
                typespans = BeautifulSoup(str(typeItems), 'html.parser').find_all('span')

                types = ''
                for typespan in typespans:
                    types += typespan.get_text() + ','

                _985 = False
                _211 = False
                type_open = types.split(',')
                if (len(type_open) > 1):
                    if type_open[0] == '985':
                        _985 = True
                    if type_open[1] == '211':
                        _211 = True
                schoolAndCode = item.find('a').get_text().lstrip('(').split(')',1)
                school = {
                    'link': 'http://yz.chsi.com.cn/' + item.find('a').get('href'),
                    'schoolCode':schoolAndCode[0],
                    'school': schoolAndCode[1],
                    'local': item.find_all('td')[1].get_text(),
                    '_985': _985,
                    '_211': _211
                }

                sc = school['school']
                scCode = school['schoolCode']
                local = school['local']
                _985 = str(school['_985'])
                _211 = str(school['_211'])
                link = school['link']

                MyLog.info(mlName + ',' + zyName + ','  + local + ',' + sc)
                cur_sql_users_value = "('"+scCode + "','" + sc + "','" + local + "','" + _985 + "','" + _211 + "','" + mlName + "','" + zyName + "','" + link + "')"
                cur_sql = "insert into " + db + "(Aca_No,Aca_Name,Aca_city,Aca_985,Aca_211,Aca_category,Aca_professionalName,Dep_Url) values" + cur_sql_users_value
                # print(cur_sql)

                mssql = MSSQL()

                try:
                    mssql.ExecNonQuery(cur_sql)
                    print("招生单位信息插入数据库成功")
                    MyLog.info("招生单位信息插入数据库成功")
                except Exception:
                    print("招生单位信息插入数据库失败")

            ##################下一个解析及其操作#######################
            pageBoxRaw = soup.find(class_='ch-page')  # 找到包含页码的盒子
            pageBox = BeautifulSoup(str(pageBoxRaw), 'html.parser')

            currentPageIndex = pageBox.find(class_='lip selected')  # 找到当前页面页码

            nextPageIndex = currentPageIndex.next_sibling  # 下一页面页码
            nextliText = nextPageIndex.string
            MyLog.info('下一页页码:' + nextliText)

            next = (str(nextliText)).isdigit()
            ##################下一个解析及其操作#######################

            if next:
                curPath = os.path.abspath(os.path.dirname(__file__))
                filename = curPath + '\\js\\nextSchoolPage.txt'
                file = open(filename, 'rb')
                execStr = file.read().decode('utf-8')

                SpiderSchool.browser.execute_script(execStr)  # 调转到要爬取的页面

                # 页面解析
                html = SpiderSchool.browser.page_source
                doc = pq(html)

    def getSchoolList(self):
        '''
        按（省份,门类类别，学科类别，专业名称）获得想要爬取的页面，并解析获取内容
        :return:
        '''

        url = URL
        db = SCHOOLS_COLLECTION  # 是专硕还是学硕的数据库

        try:
            # 按门类类别选择
            requestMenlei = RequestMenlei()
            if(requestMenlei.ismenleiCodesEmpty()):
                requestMenlei.spider_parse()

            #移除前面，直至工学,纯手工代码操作
            #######################################
            for i in range(8):
                requestMenlei.remove_menleiHead()
            #######################################

            mls = requestMenlei.get_menlei()
            # print(mls)

            for mlCodeIndex in range(len(mls)): # 按门类类别选择
                ml = mls[mlCodeIndex]
                mlCode = ml['dm']
                mlName = ml['mc']
                str2 = self.selectByMLLBOption2(mlCode)
                MyLog.info('mlCode:'+mlCode)

                # 选取学科类别(专业领域)，专业领域的获取依赖门类类别
                requestLingyu = RequestLingyu()
                if(requestLingyu.isLingyuCodesEmpty()):
                    requestLingyu.spider_parse(mlCode)

                # 移除已爬取xx门类中已爬取的学科门类（专业领域），直至专业名称为xxx,纯手工代码操作
                #######################################
                if str(mlCode) == '08':
                    MyLog.info('如果门类是在08门类中，移除直至轻工技术与工程')
                    for i in range(21):
                        requestLingyu.remove_lingyuCodeHead()
                #######################################

                lingyuCodes = requestLingyu.get_lingyuCodes()

                for lyCodesIndex in range(len(lingyuCodes)): # 按学科类别(专业领域)选择
                    lyCode = lingyuCodes[lyCodesIndex]
                    str3 =self.selectByZYLYOption3(lyCode)
                    MyLog.info('lyCode:'+lyCode)

                    #选取专业名称，专业名称的获取依赖专业领域代码
                    requestZhuanye = RequestZhuanye()
                    if(requestZhuanye.isZhuanyeNameEmpty()):
                        requestZhuanye.spider_parse(lyCode)

                    # 移除已爬的学科门类（专业领域），直至转化专业名为xxx,纯手工代码操作
                    #######################################
                    if str(lyCode) == '0822':
                        MyLog.info('如果学科类别(领域)在0822，一直移除至制浆造纸张工程')
                        for i in range(15):
                            requestZhuanye.remove_zhuanyeNameHead()
                    #######################################

                    if requestZhuanye.isZhuanyeNameEmptyAferSpider():#专业名称手动置为空
                        MyLog.info(lyCode + ',专业名称空')
                        requestZhuanye.setEmpty()

                    zyNames = requestZhuanye.get_zhuanyeNames()

                    for zyNameIndex in range(len(zyNames)):# 按专业名称选择
                        zyName = zyNames[zyNameIndex]
                        str4 = self.selectByZYMCOption4(zyName)
                        MyLog.info('zyName:'+zyName)

                        str1 = self.selectBySFCode1()
                        execStr = str1 + str2 + str3 + str4

                        SpiderSchool.browser.get(url)
                        SpiderSchool.browser.execute_script(execStr) # 调转到要爬取的页面

                        # 页面解析
                        html = SpiderSchool.browser.page_source
                        doc = pq(html)
                        self.resolvePageAndInsert(mlName,zyName,doc,db)

        except TimeoutException:
            MyLog.error("获取文档失败")

if __name__ == '__main__':
    spiderSchool = SpiderSchool()
    spiderSchool.getSchoolList()




