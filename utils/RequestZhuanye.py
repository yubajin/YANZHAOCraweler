# https://yz.chsi.com.cn/zsml/code/zy.do

import requests
import re

'''
从网页上获得专业名称列表
'''
class RequestZhuanye:

    def __init__(self):
        self.zhuanyeNames = []

    def get_zhuanyeNames(self):
        return self.zhuanyeNames

    def remove_zhuanyeName(self,zhuanyeName):
        self.zhuanyeNames.remove(zhuanyeName)

    def isZhuanyeNameEmpty(self):
        zhuanyeNameEmpty = False
        if (len(self.zhuanyeNames) == 0):
            zhuanyeNameEmpty = True

        return zhuanyeNameEmpty

    def spider_zhuanyeNames(self,zhuanyelinyu):
        '''
        接口返回发送请求后的原始数据,专业名称的数据获取依赖于专业领域(学科类别)的选择
        :param zhuanyelinyu:专业领域(学科类别)的选择
        :return:zhuanyeNames:字符串类型，格式["比较教育学","成人教育学","初等教育学",...]类型
        '''
        url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        data = {"q":zhuanyelinyu}
        response = requests.post(url=url, data=data)
        zhuanyeNames = response.text
        return zhuanyeNames

    def spider_parse(self,zhuanyelinyu):
        '''
            专业名称处的数据获取依赖于专业领域的选择
            将获得的返回数据进行解析成list列表,格式["比较教育学","成人教育学","初等教育学",...]类型
            zhuanyelinyu:是一个字符串
            return:返回一个专业名称的list列表
        '''
        response = self.spider_zhuanyeNames(zhuanyelinyu)
        zhuanyeNames = response.replace('[', '').replace('"', '').replace(']', '').split( ',')

        for i in range(len(zhuanyeNames)):
            self.zhuanyeNames.append(zhuanyeNames[i])

if __name__ == '__main__':
    requestZhuanye = RequestZhuanye()
    requestZhuanye.spider_parse('0351')
    print(requestZhuanye.isZhuanyeNameEmpty())

    print(requestZhuanye.get_zhuanyeNames())

    requestZhuanye.remove_zhuanyeName("法律（法学）")
    print(requestZhuanye.get_zhuanyeNames())

    requestZhuanye.remove_zhuanyeName("法律（非法学）")
    print(requestZhuanye.isZhuanyeNameEmpty())