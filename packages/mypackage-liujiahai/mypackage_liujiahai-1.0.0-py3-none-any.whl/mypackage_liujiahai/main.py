# -*- coding: utf-8 -*-


class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        return '姓名: {}, 年龄：{}.'.format(self.name, self.age)


if __name__ == '__main__':
    s = Student('刘家海', 29)
    result = s.show_info()
    print(result)