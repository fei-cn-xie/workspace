a = [1,2,3,4,5]
print(*a)

b = {"key1": "value1", "key2": "value2"}
print({**b})

class Person:
    pass

# with Person() as p:
#     print(p)

def test():
    return 100

with test() as num:
    print(num)