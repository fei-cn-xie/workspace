
class TestOr(object):
    """
    让`a | b | c`的代码得到一个自定义的类对象(类似列表即[a,b,c]) 
    """
    def __init__(self, *args):
        self.arr : list = []
        for arg in args:
            self.arr.append(arg)
    
    def __str__(self):
        return f"TestOr({self.arr})"

    def __or__(self, other):
        return TestOr(*self.arr, other)
    
    def run(self):
        print(*self.arr)

# *号代表打包或者拆包一个元组或list

a = TestOr("a")
my_chain = a | "b" | "c"

print(my_chain)

my_chain.run()