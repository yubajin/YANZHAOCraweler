# http://yz.chsi.com.cn/zsml/pages/getSs.jsp

import requests
import re

'''
从网页上获得省份列表
'''
class RequestShengfen:

    def __init__(self):
        self.dm = []

    def spider(self,url,data):
        response = requests.post(url = url, data = data)
        return  response.text

    def spider_shengfen(self):
        url = 'http://yz.chsi.com.cn/zsml/pages/getSs.jsp'
        data = ''
        response = self.spider(url,data)
        return response


    def spider_parse(self,response1):
        '''
            将获得的返回数据进行解析
            response1
        '''
        response = response1.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')
        # print("response:",response)
        for i in range(len(response)):
            # print(response[i])
            self.dm.append(response[i])
        return self.dm

    def spider_writer(self, content):
        filename = 'shengfen.txt'
        with open(filename, 'w+') as fd:
            for chunk in content:
                fd.write(chunk)


    def spider_reader(self,filename):
        '''

        :param filename: 按文件名读取文件
        :return: 返回查询列表，这里是省份代码列表
        '''
        content = []
        f = open(filename)
        lines = f.readlines()
        for line in lines:
            content.append(line.replace('\n',''))
        return content

    def main(self):
        ###爬去省份的数据
        response = self.spider_shengfen()

        ###解析爬取好的数据
        dms = requestShengfen.spider_parse(response)

        ###将爬取好的数据写入txt文档
        dm_content = ''
        for dm in dms:
            strb = re.sub(r'(\w+):', "'\g<1>':", dm)
            dict_str = eval(strb)
            dm_content += dict_str['dm'] + '\n'
        self.spider_writer(dm_content)

        ###将txt文档中的数据读取出来
        filename = 'shengfen.txt'
        line = self.spider_reader(filename)
        print('line',line)


if __name__ == '__main__':
    requestShengfen = RequestShengfen()
    requestShengfen.main()