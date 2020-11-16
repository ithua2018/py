#yield 生成器
# 1.与函数类似  但不同
#只能用循环去获取数据 或者next()
#没有实例yield函数  直接调用会停止
def yield_func():
    yield 1
    yield 2
    yield 3
    yield 4
    return 5


def func():
    return 10000

for i in yield_func():
    print(i)   #return 没有返回值
a=func()
print(a)
#没有实例yield函数  直接调用会停止
print(next(yield_func())) #1
print(next(yield_func())) #1
print(next(yield_func())) #1
print(next(yield_func())) #1
print(next(yield_func())) #1
#实例则不会
a = yield_func()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))

