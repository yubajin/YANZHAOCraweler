# http://yz.chsi.com.cn/zsml/pages/getSs.jsp

import requests
import json

'''
从网页上获得省份列表，存在类属性self.sf中
'''
class RequestShengfen:

    def __init__(self):
        self.sfNames = []#元素为字符串
        self.sfCodes = []#元素为字符串

    def get_sfCodes(self):
        return self.sfCodes

    def get_sfNames(self):
        return self.sfNames

    def get_sf(self):
        '''
        将获得的返回数据进行解析成由字典组成的列表 格式[{"mc":"北京市","dm":"11"},{"mc":"天津市","dm":"12"},...] )
        并返回字典
        :return:返回字典列表
        '''
        response = self.spider_shengfen()
        resp = response.replace('[', '').replace('\r', '').replace('\n', '').replace(']', '').replace('},', '}.').split('.')

        sf = []
        for i in range(len(resp)):
            dm_mc = resp[i]
            dm_mcDict = json.loads(dm_mc)
            sf.append(dm_mcDict)
        return sf

    def remove_sfCode(self,sfCode):
        '''
        移除省份代码
        :param sfCode:省份代码，参数为字符串类型
        :return:
        '''
        self.sfCodes.remove(sfCode)

    def remove_sfName(self,sfName):
        '''
        移除省份代码
        '''
        self.sfNames.remove(sfName)

    def isSfCodesEmpty(self):
        sfCodesEmpty = False
        if(len(self.sfCodes)==0):
            sfCodesEmpty = True

        return sfCodesEmpty

    def spider(self,url,data):

        response = requests.post(url = url, data = data)
        return  response.text

    def spider_shengfen(self):
        '''
        将向接口发送请求返回的原始数据返回
        :return: 字符串[{"mc":"北京市","dm":"11"},{"mc":"天津市","dm":"12"},...] 格式
        '''
        url = 'http://yz.chsi.com.cn/zsml/pages/getSs.jsp'
        data = ''
        response = self.spider(url,data)
        return response

    def spider_parse(self):
        '''
            将获得的返回数据进行解析
            将解析的结果(由字典组成的列表 格式[{"mc":"北京市","dm":"11"},{"mc":"天津市","dm":"12"},...] )
            进一步将字典中的省份名称存放在类属性sfNames列表中
            字典中的省份代码存放在类属性sfCodes列表中
        '''
        response = self.spider_shengfen()
        resp = response.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')

        for i in range(len(resp)):
            dm_mc = resp[i]
            dm_mcDict = json.loads(dm_mc)
            self.sfNames.append(dm_mcDict['mc'])
            self.sfCodes.append(dm_mcDict['dm'])

if __name__ == '__main__':
    requestShengfen = RequestShengfen()

    print('省份代码和名称以字典形式输出:')
    print(requestShengfen.get_sf())

    requestShengfen.spider_parse()
    print('判断省份代码列表是否为空:'+str(requestShengfen.isSfCodesEmpty()))
    print('纯输出省份代码:')
    print(requestShengfen.get_sfCodes())
    print('纯输出省份名称:')
    print(requestShengfen.get_sfNames())

    requestShengfen.remove_sfCode('11')
    print('省份代码移除操作后:')
    print(requestShengfen.get_sfCodes())

    requestShengfen.remove_sfName('天津市')
    print('省份名称移除操作后:')
    print(requestShengfen.get_sfNames())