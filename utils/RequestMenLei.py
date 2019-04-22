# https://yz.chsi.com.cn/zsml/pages/getMl.jsp

import requests
import  json

'''
从网上获取门类类别列表
'''
class RequestMenlei:

    def __init__(self):
        self.menleiCodes = []#元素为字符串
        self.menleiNames = []#元素为字符串

    def get_menleiCodes(self):
        return self.menleiCodes

    def get_menleiName(self):
        return self.menleiNames

    def get_menlei(self):
        '''
        将获得的返回数据进行解析分成门类代码列表和门类名称列表 格式[{"mc":"北京市","dm":"11"},{"mc":"天津市","dm":"12"},...] )
        并返回字典
        'zyxw'和'专业学位'需要另外添加
        :return:列表类型{"mc": "哲学","dm": "01"},{"mc": "经济学","dm": "02"},...]
        '''
        response = self.spider_menlei()
        result = response.replace('[', '').replace('\r', '').replace('\n', '').replace(']', '').replace('},','}.').split('.')

        menlei = []
        for i in range(len(result)):
            menlei.append(json.loads(result[i]))

        menlei.insert(0,{'mc': '专业学位', 'dm': 'zyxw'})

        return menlei

    def insertHead_menleiCode(self,menleiCode):
        self.menleiCodes.insert(0,menleiCode)

    def insertHead_menleiName(self,menleiName):
        self.menleiNames.insert(0,menleiName)

    def remove_menleiCode(self,menleiCode):
        '''
        移除门类类别代码
        :param menleiCode:门类类别
        :return:
        '''
        self.menleiCodes.remove(menleiCode)

    def remove_menleiName(self,menleiName):
        self.menleiNames.remove(menleiName)

    def ismenleiCodesEmpty(self):
        '''
        判断门类代码列表是否为空
        :return:
        '''
        menleiCodessEmpty = False
        if(len(self.menleiCodes)==0):
            menleiCodessEmpty = True

        return menleiCodessEmpty

    def spider_menlei(self):
        '''
        接口返回发送请求后的原始数据[
        :return: 字符串类型{"mc": "哲学","dm": "01"},{"mc": "经济学","dm": "02"},...]
        '''
        url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'

        response = requests.post(url=url)
        result = response.text
        return result

    def spider_parse(self):
        '''
            将获得的返回数据进行解析分成门类代码列表和门类名称列表
            分别存放在menleiCodes和menleiName中
            'zyxw'和'专业学位'需要另外添加
        '''
        #将传来的字符串转化成列表
        response = self.spider_menlei()
        result = response.replace('[','').replace('\r','').replace('\n','').replace(']','').replace('},','}.').split('.')

        for i in range(len(result)):
            self.menleiCodes.append(json.loads(result[i]).get('dm'))
            self.menleiNames.append(json.loads(result[i]).get('mc'))

        self.insertHead_menleiCode('zyxw')
        self.insertHead_menleiName('专业学位')

if __name__ == '__main__':
    requestMenlei = RequestMenlei()
    result=requestMenlei.spider_parse()

    # print(requestMenlei.get_menlei())

    print(requestMenlei.ismenleiCodesEmpty())

    print(requestMenlei.get_menleiCodes())

    print(requestMenlei.get_menleiName())

    requestMenlei.remove_menleiCode('01')
    print(requestMenlei.get_menleiCodes())

    requestMenlei.remove_menleiName('教育学')
    print(requestMenlei.get_menleiName())

