# https://yz.chsi.com.cn/zsml/pages/getMl.jsp

import requests
import re
import  json

'''
从网上获取门类类别列表
'''
class RequestMenlei:

    def __init__(self):
        self.dm = []

    def spider_menlei(self):
        '''

        :return: 返回接口的数据
        '''
        url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'

        response = requests.post(url=url)
        result = response.text
        return result


    def spider_parse(self,response1):
        '''
            将获得的返回数据进行解析成列表格式
            response1
        '''
        #将传来的字符串转化成列表
        response = response1.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')

        for i in range(len(response)):
            self.dm.append(json.loads(response[i]).get('dm') + ',' + json.loads(response[i]).get('mc'))
        return self.dm

    def spider_writer(self, content,filename='menlei.txt'):

        with open(filename, 'w+',encoding='utf-8') as fd:
            fd.writelines('zyxw,专业学位')
            fd.write('\n')
            for chunk in content:
                fd.writelines(chunk)
                fd.write('\n')


    def spider_reader(self,filename):
        '''

        :param filename: 按文件名读取文件
        :return: 返回查询列表，这里是字典(包含门类代码和门类名称)的列表
        '''
        content = []
        f = open(filename,encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            dm_mc = line.replace('\n','').split(',')
            dm = dm_mc[0]#门类代码
            mc = dm_mc[1]#门类名称
            dm_mcDict = {}
            dm_mcDict['dm'] = dm
            dm_mcDict['mc'] = mc
            content.append(dm_mcDict)

        return content

    def getXuekeListByMenlei(self,filename = 'menlei.txt'):
        '''
        得到对应的门类领域，并且写入文件xueke.txt中
        :return:返回查询列表，这里是字典(包含门类代码和门类名称)的列表
        '''
        response = self.spider_menlei()  ###爬去门类领域的数据

        dmsList = self.spider_parse(response)  ###解析爬取好的数据

        self.spider_writer(dmsList, filename)  ###将爬取好的数据写入txt文档

        ###将xueke.txt文档中的数据读取出来
        result = self.spider_reader(filename)
        return  result

if __name__ == '__main__':
    requestMenlei = RequestMenlei()
    result=requestMenlei.getXuekeListByMenlei()

    print('result:', result)