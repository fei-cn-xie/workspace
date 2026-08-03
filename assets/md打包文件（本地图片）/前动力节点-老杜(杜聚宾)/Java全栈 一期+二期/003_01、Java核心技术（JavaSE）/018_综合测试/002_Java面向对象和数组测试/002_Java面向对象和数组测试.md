# Java面向对象和数组测试

**满分：100分 时间：3 个小时**

## 一、选择题（每题3分，共30分）

*每题可能有1个或多个正确答案，全部选对得3分，选对但不全得1分，有错选得0分。*

1. 以下关于Java数组的说法，正确的是（　　）
A. `int[] a = new int[0];` 是合法的，长度为0的数组
B. 二维数组中，每个一维数组的长度可以不同
C. 数组的`length`是一个方法，调用方式是`a.length()`
D. `int[] a = {1,2,3}; int[] b = a; b[1]=5;` 执行后`a[1]`是2
2. 阅读以下代码，输出结果是（　　）

```java
class A {
    public void print() { System.out.print("A"); }
}
class B extends A {
    public void print() { System.out.print("B"); }
    public void onlyB() { System.out.print("OnlyB"); }
}
public class Test {
    public static void main(String[] args) {
        A obj = new B();
        obj.print();
        // obj.onlyB();  // 语句1
        ((B)obj).onlyB(); // 语句2
    }
}
```

A. 编译错误在语句1 B. 输出 `BOnlyB` C. 运行时异常 D. 输出 `AOnlyB`

1. 关于`static`代码块和构造方法的执行顺序，已知以下代码：

```java
class Parent {
    static { System.out.print("Parent静态 "); }
    { System.out.print("Parent构造块 "); }
    Parent() { System.out.print("Parent构造 "); }
}
class Child extends Parent {
    static { System.out.print("Child静态 "); }
    { System.out.print("Child构造块 "); }
    Child() { System.out.print("Child构造 "); }
}
// 执行 new Child(); 输出顺序是？
```

A. Parent静态 → Child静态 → Parent构造块 → Parent构造 → Child构造块 → Child构造
B. Parent构造块 → Parent构造 → Child构造块 → Child构造 → Parent静态 → Child静态
C. Parent静态 → Parent构造块 → Parent构造 → Child静态 → Child构造块 → Child构造
D. Child静态→Parent静态 → Parent构造块 → Parent构造 → Child构造块 → Child构造

1. 以下哪些情况下，`final`关键字修饰的变量值可以改变？（　　）
A. `final int x; x = 10;`（在构造方法中赋值）
B. `final int[] arr = {1,2}; arr[0] = 99;`
C. `final Student s = new Student(); s.setName("Tom");`
D. `final int y = 5; y = 6;`
2. 有一个`Person`类，子类`Student`。以下哪项会发生**错误**？（　　）
A. `Person p = new Student();`
B. `Student s = (Student) new Person();`
C. `Person p = new Person(); Student s = (Student) p;`
D. `Student s = new Student(); Person p = s;`
3. 关于`this`和`super`的说法，正确的有（　　）
A. `super()`和`this()`可以同时出现在同一个构造方法中
B. 在构造方法中，`super()`必须写在第一行
C. `this`可以引用当前对象的任意成员（包括私有成员）
D. 静态方法中可以使用`super`
4. 以下代码的输出结果是（　　）

```java
int[] arr = new int[3];
int[][] matrix = new int[3][];
System.out.println(arr.length);
System.out.println(matrix.length);
System.out.println(matrix[0] == null);
```

A. 3 3 false B. 3 3 true C. 编译错误 D. 3 0 true

1. 下面关于方法重载（Overload）和方法重写（Override）的描述，正确的有（　　）
A. 重载方法的返回类型必须不同
B. 重写方法可以抛出比父类更宽泛的异常
C. 重载发生在同一个类中，重写发生在继承关系中
D. `private`方法可以被重写
2. 以下代码输出正确的是（　　）

```java
public class Test {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        change(a);
        System.out.println(a[0] + "," + a[1] + "," + a[2]);
    }
    static void change(int[] arr) {
        int[] b = {4, 5, 6};
        arr = b;
        arr[0] = 100;
    }
}
```

A. 100,5,6 B. 1,2,3 C. 4,5,6 D. 100,2,3

1. 以下关于`ArrayList`和数组的区别，正确的有（　　）
A. 数组可以存储基本数据类型，`ArrayList`只能存储引用类型
B. 数组的长度一旦确定不可变，`ArrayList`可以动态扩容
C. 访问数组元素使用`[]`，访问`ArrayList`元素使用`get()`方法
D. 数组的性能通常优于`ArrayList`

## 二、代码分析题（共20分）

**第1题（10分）**
阅读下面代码，写出运行结果，并简要说明原因。

```java
class Animal {
    String name = "Animal";
    public Animal() { 
        show(); 
    }
    public void show() { 
        System.out.println(name); 
    }
}
class Dog extends Animal {
    String name = "Dog";
    public Dog() {
        super();
        System.out.println("子类构造");
    }
    public void show() {
        System.out.println(name);
    }
}
public class Test {
    public static void main(String[] args) {
        new Dog();
    }
}
```

**输出结果：**

**第2题（10分）**
指出以下程序中存在的**所有错误**（编译期或逻辑错误），并给出改正方式。

```java
public class ArrayManager {
    private int[] data;
    
    public ArrayManager() {
        data = null;
    }
    
    public void setData(int[] arr) {
        data = arr;
    }
    
    public int getMax() {
        int max = data[0];
        for(int i=1; i<data.length; i++) {
            if(data[i] > max) max = data[i];
        }
        return max;
    }
    
    public static void printAverage(ArrayManager am) {
        int sum = 0;
        for(int i=0; i<am.data.length; i++) {
            sum += am.data[i];
        }
        double avg = sum / am.data.length;
        System.out.println("平均值为：" + avg);
    }
}
```

## 三、程序设计题（共50分）

### 第1题：数组算法 + 自定义排序（15分）

编写一个完整的Java程序，实现以下功能：

1. 随机生成一个长度为20的整数数组，元素范围[10, 99]（包含两端）
2. 编写方法 `public static void reverse(int[] arr)` 将数组**原地反转**（不使用新数组）
3. 编写方法 `public static int[] getPrimes(int[] arr)` 返回一个新数组，包含原数组中所有的**质数**（素数），保持原顺序
4. 在主方法中：
  - 生成随机数组并打印
  - 反转数组并打印
  - 提取质数数组并打印

**质数判断要求：** 写一个独立的 `isPrime(int n)` 方法，且对于小于2的数返回false。

### 第2题：面向对象综合设计——简单电商购物车（20分）

设计一个简化版的购物车系统，要求如下：

#### 类1：`Product`（商品）

- 私有属性：`id`(int)、`name`(String)、`price`(double)
- 构造方法、getter/setter
- 重写`toString()`方法，返回格式如：`"【1】华为手机，价格：2999.0"`

#### 类2：`CartItem`（购物车项）

- 私有属性：`product`(Product)、`quantity`(int)
- 提供构造方法
- 实例方法：`getTotalPrice()` 返回小计（单价×数量）
- 提供getter/setter

#### 类3：`ShoppingCart`（购物车）

- 私有属性：`items`(**CartItem数组**，不是ArrayList，固定最多10个商品)、`itemCount`(当前实际商品种类数)
- 构造方法：初始化数组长度为10，`itemCount=0`
- 实例方法：
  - `addProduct(Product p, int quantity)`：添加商品到购物车，**如果购物车中已有相同id的商品，则累加数量**，否则添加新商品（注意数组满时输出“购物车已满”）
  - `removeProduct(int productId)`：根据商品id删除购物车项（删除后数组前移）
  - `getTotal()`：返回购物车总金额
  - `printCart()`：打印购物车所有商品明细（每行一个CartItem的格式，如“商品名称 x 数量 = 小计”）

#### 测试要求（写在main中）：

1. 创建3~5个商品对象
2. 创建购物车，添加若干商品（包含重复添加同一商品的情况）
3. 删除其中一个商品
4. 打印购物车明细和总金额

**评分重点：**

- 封装性、数组的动态维护（添加、删除、查找）
- 重复商品合并逻辑
- 数组满时的处理

### 第3题：综合思维题 —— 对象数组排序（15分）

定义一个`Student`类，属性：`name`(String)、`chinese`(int)、`math`(int)、`english`(int)。

要求：

1. 编写一个方法 `public static void sortByTotal(Student[] students)`，使用**冒泡排序**按总分从高到低对学生数组进行**原地排序**。
2. 编写另一个方法 `public static Student[] filterByCondition(Student[] students, int minChinese, int minTotal)`，返回一个新数组，包含**同时满足**语文≥minChinese **且**总分≥minTotal的学生（保持原顺序）。
3. 在main中：
  - 创建一个包含至少5个学生的数组
  - 调用`sortByTotal`排序后打印（输出姓名+总分）
  - 调用`filterByCondition`筛选出语文≥80且总分≥240的学生，打印这些学生的信息

**注意：** 所有排序和筛选**不能使用**`Arrays.sort()`和`ArrayList`，必须手动实现。