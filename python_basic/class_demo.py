class Animal:
    def __init__(self, name):
        self.name = name

    # 实例方法
    def speak(self):
        return f"实例，{self}"

    # 类方法
    @classmethod
    def classM(cls:type):
        """类方法必须在参数列表声明一个变量名"""
        return f"Class Method :\n name = {cls.__name__}\n type = {type(cls)} \n value = {cls}"


    # 静态方法
    @staticmethod
    def staticM():
        return "Static Method"

    # 类的普通方法，实例无法调用
    def normalM():
        return "Normal"

    # property 属性方法
    @property
    def prop(self):
        """只能使用 `实例名.prop调用` 才会正常返回"""
        return "属性值"




if __name__ == "__main__":
    print("class Method\n", Animal.classM())
    print("="*20)
    print(f"class Static: \n", Animal.staticM())
    print("="*20)
    print(f"class Normal: \n", Animal.normalM())

    a = Animal("cat")
    # a.normalM() # 无法调用
    a.staticM()

    print("="*20)
    print(a.prop)