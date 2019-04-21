# https://yz.chsi.com.cn/zsml/pages/getZy.jsp

import requests
import re

'''
从网页上获得专业领域列表
'''
class RequestXueke:

    def __init__(self):
        self.dm = []

    def spider(self,url,data):
        response = requests.post(url = url, data = data)
        return  response.text

    def spider_xueke(self,mlCode):
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        data = {'mldm':mlCode}
        response = self.spider(url,data)
        return response


    def spider_parse(self,response1):
        '''
            将获得的返回数据进行解析
            response1
        '''
        response = response1.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')

        for i in range(len(response)):
            self.dm.append(response[i])
        return self.dm

    def spider_writer(self, content,filename):

        with open(filename, 'w+') as fd:
            for chunk in content:
                fd.write(chunk)


    def spider_reader(self,filename):
        '''

        :param filename: 按文件名读取文件
        :return: 返回查询列表，这里是学科代码列表
        '''
        content = []
        f = open(filename)
        lines = f.readlines()
        for line in lines:
            content.append(line.replace('\n',''))
        return content

    def getXuekeListByMenlei(self, mlCode='zyxw',filename = 'xueke.txt'):
        '''
        按门类类别得到对应的专业领域，并且写入文件xueke.txt中
        :param mlCode:
        :return:
        '''
        response = self.spider_xueke(mlCode)  ###爬去专业领域的数据

        dmsList = self.spider_parse(response)  ###解析爬取好的数据

        ###将爬取好的数据写入txt文档
        dm_content = ''
        for dm in dmsList:
            strb = re.sub(r'(\w+):', "'\g<1>':", dm)
            dict_str = eval(strb)
            dm_content += dict_str['dm'] + '\n'
        self.spider_writer(dm_content,filename)

    def main(self):
        ###爬取学科的数据
        response = self.getXuekeListByMenlei()

        ###将txt文档中的数据读取出来
        filename = 'xueke.txt'
        line = self.spider_reader(filename)
        print('line',line)


if __name__ == '__main__':
    requestXueke = RequestXueke()
    requestXueke.main()