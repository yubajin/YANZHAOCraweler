from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from utils.MSSQL import *
from utils.MyLog import *
from config import *

class SpiderMajor:
    def  __init__(self):
        self.departmentInfo = []#记录着academyInfo,是tuple的集合,tuple有哪些值参考addDepUrlHundred()函数
        self.MAXSIZE=200#一次取出的最大值

    # browser = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    def getDepUrlHead(self):
        '''
        返回从数据库中查询的MAXSIZE条数据
        :return:
        '''
        acaIdAndDepUrl = {}
        try:
            depRawUrlHead = self.departmentInfo[0]
            try:
                AcaId = depRawUrlHead[1]
                depUrl = depRawUrlHead[2]
                acaIdAndDepUrl = {'AcaId':AcaId,'depUrl':depUrl}

                return acaIdAndDepUrl
            except Exception:
                print('DepUrlHead Error')
                MyLog.error('DepUrlHead Error')
                return -2

        except Exception:
            print('DepRawUrlHead Error')
            MyLog.error('DepRawUrlHead Error')
            return -1

    def removeDepUrlHead(self):
        if self.isDepUrlEmpty():
            print('url为空,不能再移除')
            MyLog.info('url为空,不能再移除')
            return
        self.departmentInfo.pop(0)

    def addDepUrlHundred(self,pageIndex):
        '''
        分页查询
        每次从数据库中查出200条记录中指向学院信息的url
        并将查询出来的url放在self.depUrl这个set中
        :param pageIndex: 页码，其中
        :return:
        '''

        # create procedure paging_procedure(@pageIndex int,@pageSize int)
        # as begin
        #     select top (select @pageSize) *     -- 这里注意一下，不能直接把变量放在这里，要用select
        #     -- row_number() over(order by column) 按指定列名排序并且重新连续编号
        #     from (select row_number() over(order by Aca_ID) as rownumber,Aca_ID,Dep_Url,* from AcademyInfo) temp_row
        #     where rownumber>(@pageIndex-1)*@pageSize;
        # end
        #
        # exec paging_procedure @pageIndex=2,@pageSize=20;

        mssql = MSSQL()
        sql = 'exec paging_procedure ' + '@pageIndex=' + str(pageIndex) + ',@pageSize='+str(self.MAXSIZE)
        # print(sql)
        res = mssql.ExecQuery(sql)#返回类型是tuple
        for re in res:
            self.departmentInfo.append(re)

    def getDepUrlHundred(self):
        if not self.isDepUrlEmpty():
            return self.departmentInfo

    def removeDepUrlHundred(self):
        if not self.isDepUrlEmpty():
            for i in range(SpiderMajor.MAXSIZE):
                self.removeDepUrlHead()

    def isDepUrlEmpty(self):
        isEmpty = False
        if not(len(self.departmentInfo)):
            isEmpty = True
        return isEmpty

    def index_page(self,acaId,schoolUrl):
        """
        抓取索引页
        """
        db = MAJORS_COLLECTION
        try:
            browser = spiderMajor.browser
            browser.get(schoolUrl)

            html = browser.page_source

            soup = BeautifulSoup(str(html), 'html.parser')
            tbodyRaw = soup.find('tbody')
            trs = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            for item in trs:

                dep = item.find_all('td')[1].get_text()
                rawDep_Specialty = item.find_all('td')[2].get_text()
                rawDep_Direction = item.find_all('td')[3].get_text()

                Dep_No = Dep_Name = Dep_Specialty=''

                if(len(dep)):
                    Dep_No = dep.lstrip('(').split(')',1)[0]
                    Dep_Name = dep.lstrip('(').split(')',1)[1]

                if(len(rawDep_Specialty)):
                    Dep_Specialty = rawDep_Specialty.split(')',1)[1]

                if(len(rawDep_Direction)):
                    Dep_Direction = rawDep_Direction.split(')',1)[1]

                AcceStu_Url = 'http://yz.chsi.com.cn/'+ item.find_all('td')[7].find('a').get('href')
                
                cur_sql_users_value ="('" + str(acaId) + "','" + str(Dep_No) + "','" + Dep_Name + "','"+ Dep_Specialty+  "','"+ Dep_Direction + "','"+ AcceStu_Url+ "')"
                cur_sql= "insert into " + db + "(Aca_ID,Dep_No,Dep_Name,Dep_Specialty,Dep_Direction,AcceStu_Url) values"  + cur_sql_users_value

                mssql = MSSQL()
                try:
                    MyLog.info('DepartmentInfo:')
                    mssql.ExecNonQuery(cur_sql)
                except Exception:
                    pass

        except TimeoutException:
            print("爬取专业信息失败")

    def spiderMajor(self):
        pageIndex = 1
        self.addDepUrlHundred(pageIndex)
        while(not self.isDepUrlEmpty()):
            for i in range(len(self.departmentInfo)):
                AcaId = self.getDepUrlHead()['AcaId']
                depUrl = self.getDepUrlHead()['depUrl']

                self.index_page(AcaId,depUrl)
                MyLog.info('AcaId:'+str(AcaId)+' depUrl:'+depUrl)
                self.removeDepUrlHead()
            pageIndex += 1
            self.addDepUrlHundred(pageIndex)

if __name__ == '__main__':
    spiderMajor = SpiderMajor()
    spiderMajor.spiderMajor()




