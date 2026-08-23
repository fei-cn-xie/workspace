class Person:
    pass

# c1就是一个类对象
c1 = Person
c2 = type("Person1", (), {'age': 25})  # 创建一个类对象
print(c2().__class__)  # (<class 'object'>,)
