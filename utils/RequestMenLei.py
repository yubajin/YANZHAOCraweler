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
            self.dm.append(json.loads(response[i]).get('dm'))
        return self.dm

    def spider_writer(self, content,filename='menlei.txt'):

        with open(filename, 'w+',encoding='utf-8') as fd:
            fd.writelines('zyxw')
            fd.write('\n')
            for chunk in content:
                fd.writelines(chunk)
                fd.write('\n')


    def spider_reader(self,filename):
        '''

        :param filename: 按文件名读取文件
        :return: 返回查询列表，这里是门类代码列表
        '''
        content = []
        f = open(filename)
        lines = f.readlines()
        for line in lines:
            content.append(line.replace('\n',''))
        return content

    def getXuekeListByMenlei(self,filename = 'menlei.txt'):
        '''
        得到对应的门类领域，并且写入文件xueke.txt中
        :return:
        '''
        response = self.spider_menlei()  ###爬去门类领域的数据

        dmsList = self.spider_parse(response)  ###解析爬取好的数据

        self.spider_writer(dmsList, filename)  ###将爬取好的数据写入txt文档

        ###将xueke.txt文档中的数据读取出来
        result = self.spider_reader(filename)
        print('result:', result)
        return  result

if __name__ == '__main__':
    requestMenlei = RequestMenlei()
    requestMenlei.getXuekeListByMenlei()