# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author :  Huny
# @Email : hy54688010@qq.com
# @File : app.py
# @Project: 第22课时作业
import itertools

class TestCase():
    def __init__(self):
        self.case_list = input('输入所有测试对象,并用空格分开：')
        self.step = input('输入执行的动作：')
        self.value_list = input('输入所有测试结果,并用空格分开：')
        print('测试用例集合》》》')
        self.str1 = self.case_list.split(' ')
        self.str2 = self.value_list.split(' ')
    def get_case(self):
        '''输出笛卡尔用例集合'''
        count = 0
        sum = itertools.product(self.str1, self.str2)
        for i in sum:
            count += 1
            yongli = str(self.step).join(i)
            print(f'{count}.{yongli}')
        
if __name__ == '__main__':
    Y = TestCase()
    Y.get_case()
