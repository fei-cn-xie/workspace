
# region

# endregion

names = ['zs','ls','ww']
cities = ['bj','sh','NY']
a = 10

print(iter(names))
print(iter(cities))


it = iter(names)

print(it.__next__())
print(next(it))
print(next(it))
# print(next(it))

print("="*30)
it1 = iter(names)
it2 = iter(it1)
print(it1)
print(it2)
print(iter(names))

for_it = iter(names)
print("= start 2 iterator")
for item in for_it:
    print(item)

for item in for_it:
    print(item)
print("= end 2 iterator")

iter1 = iter(names)
print(iter1.__next__())



# ========================================
print("="*20 + "手写迭代器" + "="*20)


class Person:

    def __init__(self, name, age, gender) -> None:
        self.name = name
        self.age = age
        self.gender = gender


    def __iter__(self):
        return PersonIterator(self)

from typing import Any
class PersonIterator:

    def __init__(self, obj:Person) -> None:
        self.person = obj
        self.point = 0

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if self.point >= len(self.person.__dict__.keys()):
            raise StopIteration
        self.point += 1
        return list(self.person.__dict__.keys())[self.point -1]



p1:Person = Person('zs', 10, 'man')

# print(p1.__dict__)
# print(p1.__dict__.keys())
p1 = iter(p1)
print(next(iter(p1)))
print(next(iter(p1)))
print(next(iter(p1)))
# print(next(iter(p1)))

