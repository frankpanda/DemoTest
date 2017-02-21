# _*_ coding=utf-8 _*_

__author__ = 'Huoyunren'

'''学习巩固类的demo'''


class Person(object):
    """
    the class is base class for Teacher class
    """
    acount = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        # 计数器，统计人数
        Person.acount += 1

    def say_hi(self):
        print "hi,i'm %s, my age is %s！" % (self.name, self.age)

    def get_count(self):
        print "当前人数：%s" % Person.acount


class Teacher(Person):
    """
    this  is children  class of Person class
    """

    def __init__(self, name, age, sex):
        # 老式的重写父类构造方法
        # Person.__init__(self, name, age)
        # 新式重写父类构造方法super()
        super(Teacher, self).__init__(name, age)
        self.sex = sex
        self.course = "math"

    def get_course(self):
        print "i teach %s!" % self.course

    def get_count(self):
        print "current count is：%s" % Person.acount

    def get_sex(self):
        print "my sex is:%s" % self.sex

    def get_teacher_info(self):
        super(Teacher, self).say_hi()  # 利用super函数调用父类的say_hi()方法
        self.get_sex()
        print "current count:", super(Teacher, self).acount
        # super是不能调用被子类重写了的父类方法的


class Rectangle(object):
    def __init__(self):
        self.width = 0
        self.height = 0

    def set_size(self, size):
        self.width, self.height = size

    def get_size(self):
        return self.width, self.height

    size = property(get_size, set_size, doc="test property!")


class TestProperty(object):
    """ the class for practice class's property"""

    def __init__(self):
        self.__val = 20

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, value):
        self.__val = value


class StaticAndCLS(object):
    count = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        StaticAndCLS.count += 1

    @staticmethod
    def static_md():
        print "this is static method!"
        try:
            print "count=", StaticAndCLS.count
            print "x=", self.x  # 静态方法不能访问域x,y
        except Exception, e:
            print e

    @classmethod
    def class_md(cls):
        print "this is class method!"
        try:
            print "count=", cls.count
            print "y=", self.y  # 类方法不能访问域x,y
        except Exception, e:
            print e

    def general_md(self):
        print "this is general method!"
        print "x=", self.x
        print "y=", self.y
        print "count=", self.count


class Fib(object):
    """ 迭代对象 """

    def __init__(self):
        self.a = 0
        self.b = 1

    def next(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

    def __iter__(self):
        return self


def fibs(num):
    """ use yield keyword """

    n, a, b = 0, 0, 1
    while n < num:
        yield b
        a, b = b, a + b
        n += 1


"""
panda = Person("panda",29)
panda.say_hi()

han = Person("han", 28)
han.say_hi()

han.get_acount()

"""

math_teacher = Teacher("frank_xiong", 29, "male")
math_teacher.say_hi()
math_teacher.get_count()
math_teacher.get_sex()

print "下面是通过super方法调用父类方法："
math_teacher.get_teacher_info()

print "####################class rectangle##################"

rectangle = Rectangle()
rectangle.size = (110, 150)
print "width and height is:", rectangle.size
print "width is:", rectangle.width

print "###################class TestProperty################"
test = TestProperty()
test.val = 255
print test.val

print "###################class StaticAndCLS################"
sc = StaticAndCLS(2, 3)
sc.static_md()
sc.class_md()
sc.general_md()
sc.count = 11
sc.static_md()
sc.class_md()
print sc.count

print "###################class Fib 迭代器###################"
fib = Fib()
for f in fib:
    if f < 10:
        print f
    else:
        break
s = "abc"
it = iter(s)

print "###################use yield in fibs method###################"
fib_yield = fibs(5)
print fib_yield.next()


def flatten(nested):
    try:
        for subs in nested:
            for element in flatten(subs):
                yield element
    except TypeError:
        yield nested


print list(flatten([[1, 2], [3, 4, [5, 6, 7]], 9]))


def use_yield(n):
    print "begin test..."
    i = 0
    num = 1

    while i < n:
        print "第%s次调用yield之前i=%s" % (num, i)
        yield i
        i += 1
        print "第%s次调用yield之后i=%s" % (num, i)
        num += 1

    print "end"


uy = use_yield(3)
print [x for x in uy]
