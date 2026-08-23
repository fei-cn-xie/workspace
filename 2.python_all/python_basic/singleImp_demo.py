class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


s1 = Singleton()
s2 = Singleton()
print(s1)
print(s2)
print(s1 is s2)  # True

print(Singleton.__bases__)  # (<class 'object'>,)
print(object.__base__)  # (<class 'object'>,)

print("=" * 20)
print(Singleton.__class__)
print(object.__class__)
print(type.__class__)

print("=" * 20)

print(int.__base__)  # <class 'object'>
print(int.__class__)  # <class 'type'>


print("=" * 20)

def func():
    pass

print(func.__class__)  # <class 'function'>
print(func.__base__)  # AttributeError: 'function' object has no attribute '__bases__'

print("=" * 20)
