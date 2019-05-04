# https://yz.chsi.com.cn/zsml/pages/getZy.jsp

import requests
import json

'''
从网页上获得专业领域列表
'''
class RequestLingyu:

    def __init__(self):
        self.lingyuCodes = []#元素为字符串
        self.lingyuNames = []#元素为字符串

    def get_lingyuCodes(self):
        return self.lingyuCodes

    def get_lingyuNames(self):
        return self.lingyuNames

    def get_lingyu(self,lingyu):
        '''
        将获得的返回数据进行解析分成学科代码列表和学科名称列表并返回字典
        :return:列表类型{"mc": "哲学","dm": "01"},{"mc": "经济学","dm": "02"},...]
        '''
        response = self.spider_lingyu(lingyu)
        result = response.replace('[', '').replace('\r', '').replace('\n', '').replace(']', '').replace('},','}.').split('.')

        lingyu = []
        for i in range(len(result)):
            lingyu.append(json.loads(result[i]))

        return lingyu

    def remove_lingyuCodeHead(self):
        '''
        移除专业领域代码
        :param lingyuCode:专业领域代码
        :return:
        '''
        self.lingyuCodes.pop(0)

    def remove_lingyuName(self,lingyuName):
        self.lingyuNames.remove(lingyuName)

    def isLingyuCodesEmpty(self):
        lingyuCodesEmpty = False
        if(len(self.lingyuCodes)==0):
            lingyuCodesEmpty = True

        return lingyuCodesEmpty

    def spider_lingyu(self,menlei):
        '''
        接口返回发送请求后的原始数据,专业领域的数据获取依赖于门类类别的选择
        :param :menlei门类类别的选择
        :return:lingyu: 字符串类型，格式[{"mc":"金融","dm":"0251"},{"mc":"应用统计",...]
        '''
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        data = {'mldm':menlei}

        response = requests.post(url=url,data=data)
        lingyu = response.text
        return lingyu

    def spider_parse(self,menlei):
        '''
            专业领域的数据获取依赖于门类类别的选择
            将获得的返回数据进行解析分成专业领域代码列表和专业领域名称列表
            分别存放在lingyuCodes和lingyuNames中
            :param menlei: 门类类别代码,字符串格式
            :return:
        '''
        #将传来的字符串转化成列表
        response = self.spider_lingyu(menlei)
        result = response.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')

        for i in range(len(result)):
            self.lingyuCodes.append(json.loads(result[i]).get('dm'))
            self.lingyuNames.append(json.loads(result[i]).get('mc'))

if __name__ == '__main__':
    requestLingyu = RequestLingyu()

    requestLingyu.spider_parse('07')

    print(requestLingyu.isLingyuCodesEmpty())

    print(requestLingyu.get_lingyu('07'))
    print(requestLingyu.get_lingyuCodes())
    print(requestLingyu.get_lingyuNames())

    requestLingyu.remove_lingyuCodeHead()
    print(requestLingyu.isLingyuCodesEmpty())
    print(requestLingyu.get_lingyuCodes())

    requestLingyu.remove_lingyuName('物理学')
    print(requestLingyu.get_lingyuNames())

