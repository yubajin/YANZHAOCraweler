import pymssql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from config import *
from utils.RequestShengfen import *
from utils.RequestLingyu import *
from utils.RequestZhuanye import *
from utils.RequestMenLei import *
from utils.MSSQL import *
import os

'''
有研招网硕士目录查询进入学校招生单位查询
'''
class SpiderSchool:

    @staticmethod
    def getWebDriver():
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
        tbodyRaw = soup.find('tbody')
        tbody = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

        trr = BeautifulSoup(str(tbodyRaw), 'html.parser').find('tr')
        if '很抱歉' in trr.get_text():
            print('没有数据')
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

            cur_sql_users_value = "('"+scCode + "','" + sc + "','" + local + "','" + _985 + "','" + _211 + "','" + mlName + "','" + zyName + "','" + link + "')"
            cur_sql = "insert into " + db + "(Aca_No,Aca_Name,Aca_city,Aca_985,Aca_211,Aca_category,Aca_professionalName,Dep_Url) values" + cur_sql_users_value
            # print(cur_sql)

            mssql = MSSQL()

            try:
                mssql.ExecNonQuery(cur_sql)
                print("招生单位信息插入数据库成功")
            except Exception:
                print("招生单位信息插入数据库失败")

    def getSchoolList(self):
        '''
        按（省份,门类类别，学科类别，专业名称）获得想要爬取的页面，并解析获取内容
        :return:
        '''

        url = URL
        browser = SpiderSchool.getWebDriver()

        db = SCHOOLS_COLLECTION_P  # 是专硕还是学硕的数据库

        try:
            # 按门类类别选择
            requestMenlei = RequestMenlei()
            if(requestMenlei.ismenleiCodesEmpty()):
                requestMenlei.spider_parse()
            mlCodes = requestMenlei.get_menleiCodes()

            for mlCodeIndex in range(len(mlCodes)): # 按门类类别选择
                mlCode = mlCodes[mlCodeIndex]
                str2 = self.selectByMLLBOption2(mlCode)
                print('mlCode:'+mlCode)
                # requestMenlei.remove_menleiCode(mlCode)#爬取过的门类类别移除，方便记录爬取到的位置

                # 选取学科类别(专业领域)，专业领域的获取依赖门类类别
                requestLingyu = RequestLingyu()
                if(requestLingyu.isLingyuCodesEmpty()):
                    requestLingyu.spider_parse(mlCode)
                lingyuCodes = requestLingyu.get_lingyuCodes()

                for lyCodesIndex in range(len(lingyuCodes)): # 按学科类别(专业领域)选择
                    lyCode = lingyuCodes[lyCodesIndex]
                    str3 =self.selectByZYLYOption3(lyCode)
                    print('lyCode:'+lyCode)
                    # requestLingyu.remove_lingyuCode(lyCode)

                    #选取专业名称，专业名称的获取依赖专业领域代码
                    requestZhuanye = RequestZhuanye()
                    if(requestZhuanye.isZhuanyeNameEmpty()):
                        requestZhuanye.spider_parse(lyCode)
                    zyNames = requestZhuanye.get_zhuanyeNames()

                    for zyNameIndex in range(len(zyNames)):# 按专业名称选择
                        zyName = zyNames[zyNameIndex]
                        str4 = self.selectByZYMCOption4(zyName)
                        print('zyName:'+zyName)
                        # requestZhuanye.remove_zhuanyeName(zyName)

                        requestShengfen = RequestShengfen()# 按省份轮流查询
                        if(requestShengfen.isSfCodesEmpty()):
                            requestShengfen.spider_parse()
                        sfCodes = requestShengfen.get_sfCodes()

                        for sfCodeIndex in range(len(sfCodes)):# 按省份轮流查询
                            sfCode = sfCodes[sfCodeIndex]
                            str1 = self.selectBySFCode1(sfCode)
                            execStr = str1 + str2 + str3 + str4
                            # print(execStr)
                            # requestShengfen.remove_sfCode(sfCode)

                            # browser.get(url)
                            # browser.execute_script(execStr) # 调转到要爬取的页面
                            #
                            # #页面解析
                            # html = browser.page_source
                            # doc = pq(html)
                            # self.resolvePageAndInsert(mlName,zyName,doc,db)

        except TimeoutException:
            print("获取文档失败")

if __name__ == '__main__':
    spiderSchool = SpiderSchool()
    spiderSchool.getSchoolList()

    # spiderSchool.main(0)# 爬取学硕信息

#     spiderSchool.main(1)# 爬取专硕信息
