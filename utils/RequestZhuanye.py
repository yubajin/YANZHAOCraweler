# https://yz.chsi.com.cn/zsml/code/zy.do

import requests
import re

'''
从网页上获得专业名称列表
'''
class RequestZhuanye:

    def __init__(self):
        self.dm = []

    def spider(self,url,data):

        response = requests.post(url = url, data = data)
        return  response.text

    def spider_zhuanye(self,zhuanyelinyu):
        url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        data = {"q":zhuanyelinyu}
        response = self.spider(url,data)
        return response


    def spider_parse(self,response1):
        '''
            将获得的返回数据进行解析
            response1:是一个字符串
            return:返回一个list列表
        '''
        response = response1.replace('[', '').replace('"', '').replace(']', '').split( ',')

        for i in range(len(response)):
            self.dm.append(response[i])
        return self.dm

    def spider_writer(self, content,filename):
        '''

        :param content: 存在列表中的专业名称
        :return:
        '''

        with open(filename, 'w+',encoding='utf-8') as fd:
            for contentList in content:
                fd.writelines(contentList)
                fd.write('\n')


    def spider_reader(self,filename = 'zhuanye.txt'):
        '''

        :param filename: 按文件名读取文件
        :return: 返回查询列表，这里是专业代码列表
        '''
        content = []
        with open(filename,'r',encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                content.append(line.replace('\n',''))
        return content

    def getZhuanyeListByXueke(self,xuekeCode,filename = 'zhuanye.txt'):
        '''
        按学科代码得到对应的专业名称，并且写入文件zhuanye.txt中
        :param xuekeCode:
        :return:
        '''
        response = self.spider_zhuanye(xuekeCode)###爬去专业名称的数据

        dmsList = self.spider_parse(response) ###解析爬取好的数据

        self.spider_writer(dmsList,filename)###将爬取好的数据写入txt文档

    def main(self):

        self.getZhuanyeListByXueke('0101')
        ###将txt文档中的数据读取出来

        line = self.spider_reader()
        print('line:',line)


if __name__ == '__main__':
    requestZhuanye = RequestZhuanye()
    requestZhuanye.main()