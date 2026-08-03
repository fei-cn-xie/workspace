# Java面向对象和数组测试 答案

**满分：100分 时间：3 个小时**

## 一、选择题（每题3分，共30分）

*每题可能有1个或多个正确答案，全部选对得3分，选对但不全得1分，有错选得0分。*

1. 以下关于Java数组的说法，正确的是（　AB　）
A. `int[] a = new int[0];` 是合法的，长度为0的数组
B. 二维数组中，每个一维数组的长度可以不同
C. 数组的`length`是一个方法，调用方式是`a.length()`
D. `int[] a = {1,2,3}; int[] b = a; b[1]=5;` 执行后`a[1]`是2
2. 阅读以下代码，输出结果是（　AB　）

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

1. 关于`static`代码块和构造方法的执行顺序，已知以下代码：( A )

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

1. 以下哪些情况下，`final`关键字修饰的变量值可以改变？（　BC　）
A. `final int x; x = 10;`（在构造方法中赋值）
B. `final int[] arr = {1,2}; arr[0] = 99;`
C. `final Student s = new Student(); s.setName("Tom");`
D. `final int y = 5; y = 6;`
2. 有一个`Person`类，子类`Student`。以下哪项会发生**错误**？（　BC　）
A. `Person p = new Student();`
B. `Student s = (Student) new Person();`
C. `Person p = new Person(); Student s = (Student) p;`
D. `Student s = new Student(); Person p = s;`
3. 关于`this`和`super`的说法，正确的有（　BC　）
A. `super()`和`this()`可以同时出现在同一个构造方法中
B. 在构造方法中，`super()`必须写在第一行
C. `this`可以引用当前对象的任意成员（包括私有成员）
D. 静态方法中可以使用`super`
4. 以下代码的输出结果是（　B　）

```java
int[] arr = new int[3];
int[][] matrix = new int[3][];
System.out.println(arr.length);
System.out.println(matrix.length);
System.out.println(matrix[0] == null);
```

A. 3 3 false B. 3 3 true C. 编译错误 D. 3 0 true

1. 下面关于方法重载（Overload）和方法重写（Override）的描述，正确的有（　C　）
A. 重载方法的返回类型必须不同
B. 重写方法可以抛出比父类更宽泛的异常
C. 重载发生在同一个类中，重写发生在继承关系中
D. `private`方法可以被重写
2. 以下代码输出正确的是（　B　）

```java
public class Test {
    public static void main(String[] args) {
        // int[] a = 0x1234;
        int[] a = {1, 2, 3};
        change(a);
        System.out.println(a[0] + "," + a[1] + "," + a[2]);
    }
    static void change(int[] arr) { // arr = 0x1234
        int[] b = {4, 5, 6};
        arr = b;
        arr[0] = 100;
    }
}
```

A. 100,5,6 B. 1,2,3 C. 4,5,6 D. 100,2,3

1. 以下关于`ArrayList`和数组的区别，正确的有（　ABC　）
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
        new Dog(); // null 子类构造
    }
}
```

**输出结果：** null 子类构造

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

    /*
    public void printAverage() {
        int sum = 0;
        for(int i=0; i<this.data.length; i++) {
            sum += this.data[i];
        }
        double avg = (double)sum / this.data.length;
        System.out.println("平均值为：" + avg);
    }
    */
    
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

1. `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">getMax()</font>` 方法在 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">data</font>` 为 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">null</font>` 时会抛出异常
2. `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">printAverage()</font>` 中同样存在 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">null</font>` 访问风险
3. `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">printAverage()</font>` 中整数除法导致平均值截断
4. `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">setData()</font>` 没有防御性拷贝（潜在逻辑问题）
5. `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">printAverage()</font>` 是静态方法，直接访问私有字段 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">am.data</font>`
6. 如果数组长度为 0，会出现被 0 除异常。最好判断一下。

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

```java
package com.jkweilai.array3;

import java.util.Arrays;
import java.util.Random;

public class ArrayTest {
    public static void main(String[] args) {
        // 随机生成一个长度为20的整数数组，元素范围[10, 99]（包含两端）
        Random r = new Random();
        int[] arr = new int[20];
        for (int i = 0; i < arr.length; i++) {
            int num = r.nextInt(90) + 10;
            arr[i] = num;
        }
        System.out.println(Arrays.toString(arr));
        // 调用方法，反转数组
        reverse(arr);
        System.out.println(Arrays.toString(arr));

        // 找出质数
        int[] primes = getPrimes(arr);
        System.out.println(Arrays.toString(primes));
    }

    // 编写方法 public static void reverse(int[] arr) 将数组原地反转（不使用新数组）
    public static void reverse(int[] arr){
        if(arr == null || arr.length == 0 || arr.length == 1) {
            return;
        }
        // 数组不为null，并且长度也不是0，也不是1.
        for (int i = 0; i < arr.length / 2; i++) {
            // 首尾交换位置
            // 首（arr[i]）
            // 尾（arr[arr.length - 1 - i]）
            int temp = arr[i];
            arr[i] = arr[arr.length - i - 1];
            arr[arr.length - i - 1] = temp;
        }
    }

    // 编写方法 public static int[] getPrimes(int[] arr) 返回一个新数组，包含原数组中所有的质数（素数），保持原顺序
    public static int[] getPrimes(int[] arr){
        // 从 arr 数组中获取质数
        int[] newArr = new int[arr.length];
        int index = 0;
        for (int i = 0; i < arr.length; i++) {
            if(isPrime(arr[i])){
                newArr[index++] = arr[i];
            }
        }
        // 返回新数组
        return Arrays.copyOf(newArr, index);
    }

    /**
     * 判断某个数字是否为质数。
     * @param num
     * @return
     */
    public static boolean isPrime(int num){
        if(num < 2){
            return false;
        }
        // 程序执行到此处说明 num 是 >= 2
        for (int i = 2; i <= num / 2; i++) {
            if(num % i == 0){
                return false;
            }
        }
        return true;
    }
}
```

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

```java
package com.jkweilai.cart;

public class Product {
    private int id;
    private String name;
    // 单价
    private double price;

    public Product() {
    }

    public Product(int id, String name, double price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "【" + this.id + "】" + this.name + "，价格：" + this.price;
    }

    /**
     * 比较两个商品是否是同一个商品。只要id和name都一样，表示同一个商品。
     * @param obj
     * @return
     */
    @Override
    public boolean equals(Object obj){
        if(obj == null) return false;
        if(obj instanceof Product p){
            return this.id == p.id && this.name.equals(p.name);
        }
        return false;
    }
}
```

```java
package com.jkweilai.cart;

public class CartItem {
    private Product product;
    private int quantity;

    public CartItem() {
    }

    public CartItem(Product product, int quantity) {
        this.product = product;
        this.quantity = quantity;
    }

    public Product getProduct() {
        return product;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    /**
     * 小计，这个商品的总价。
     * @return
     */
    public double getTotalPrice(){
        return product.getPrice() * quantity;
    }

    @Override
    public String toString() {
        return this.getProduct().getName() + " x " + this.getQuantity() + " = " + this.getTotalPrice();
    }
}
```

```java
package com.jkweilai.cart;

public class ShoppingCart {
    private CartItem[] items;
    private int itemCount; // 商品的种类数。不是商品的总数。

    // 创建一个空的购物车。
    public ShoppingCart() {
        items = new CartItem[10];
        this.itemCount = 0;
    }

    // setter and getter
    public CartItem[] getItems() {
        return items;
    }

    public void setItems(CartItem[] items) {
        this.items = items;
    }

    public int getItemCount() {
        return itemCount;
    }

    public void setItemCount(int itemCount) {
        this.itemCount = itemCount;
    }

    /**
     * 添加商品到购物车
     * @param p
     * @param quantity
     */
    public void addProduct(Product p, int quantity){
        if(p == null || quantity <= 0) {
            System.out.println("因商品数量非法，无法添加商品到购物车");
            return;
        }
        // 先看看购物车中是否存在这个商品。
        int index = hasProduct(p);
        if(index == -1){
            if(itemCount == 10){
                System.out.println("购物车已满，添加商品失败");
            }else{
                // 购物车没满
                //items[itemCount] = new CartItem(p, quantity);
                //itemCount++;
                items[itemCount++] = new CartItem(p, quantity);
            }
        }else{
            // 购物车中已经存在这个商品了。
            CartItem cartItem = items[index];
            cartItem.setQuantity(cartItem.getQuantity() + quantity);
        }
    }

    /**
     * 判断购物车中是否存在该商品。
     * @param p 商品
     * @return 大于等于0则表示该商品存在，如果是-1表示该商品不存在。
     */
    private int hasProduct(Product p){
        for (int i = 0; i < items.length; i++) {
            if(items[i] == null){
                return -1;
            }
            if(items[i].getProduct().equals(p)){
                return i;
            }
        }
        return -1;
    }

    private int hasProduct(int productId){
        for (int i = 0; i < items.length; i++) {
            if(items[i] == null){
                return -1;
            }
            if(items[i].getProduct().getId() == productId){
                return i;
            }
        }
        return -1;
    }

    /**
     * 计算购物车总价。
     * @return
     */
    public double getTotal(){
        double total = 0.0;
        for (int i = 0; i < itemCount; i++) {
            total += items[i].getTotalPrice();
        }
        return total;
    }

    /**
     * 打印购物车信息
     * 打印购物车所有商品明细（每行一个CartItem的格式，如“商品名称 x 数量 = 小计”）
     */
    public void printCart(){
        System.out.println("购物车商品列表如下：");
        for (int i = 0; i < itemCount; i++) {
            System.out.println(items[i]);
        }
        System.out.println("总价：" + this.getTotal());
    }

    /**
     * 根据商品id删除购物车项（删除后数组前移）
     * @param productId
     */
    public void removeProduct(int productId){
        // index 正好是要删除的CartItem对象的下标。
        int index = hasProduct(productId);
        if(index == -1) {
            System.out.println("该商品不存在，删除失败");
            return;
        }
        // 这个商品一定是存在的。删除这个CartItem。 items[items.length - 1] = null
        System.arraycopy(items, index + 1, items, index, items.length - index - 1);
        items[--itemCount] = null;
    }
}
```

```java
package com.jkweilai.cart;

public class Test {
    public static void main(String[] args) {
        // 创建商品对象
        Product p1 = new Product(1, "苹果手机", 1.0);
        Product p2 = new Product(2, "华为手机", 10.0);
        Product p3 = new Product(3, "小米手机", 5.0);

        // 向购物车中添加商品
        ShoppingCart cart = new ShoppingCart();
        cart.addProduct(p1, 10);
        cart.addProduct(p1, 10);
        cart.addProduct(p2, 3);
        cart.addProduct(p3, 2);

        // 打印购物车信息
        cart.printCart();

        // 删除小米手机
        //cart.removeProduct(3);
        cart.removeProduct(2);

        cart.printCart();
    }
}
```

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

```java
package com.jkweilai.studentsort;

public class Student {
    private String name;
    private int chinese;
    private int math;
    private int english;

    public Student() {
    }

    public Student(String name, int chinese, int math, int english) {
        this.name = name;
        this.chinese = chinese;
        this.math = math;
        this.english = english;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getChinese() {
        return chinese;
    }

    public void setChinese(int chinese) {
        this.chinese = chinese;
    }

    public int getMath() {
        return math;
    }

    public void setMath(int math) {
        this.math = math;
    }

    public int getEnglish() {
        return english;
    }

    public void setEnglish(int english) {
        this.english = english;
    }

    /**
     * 获取学生的总成绩
     * @return
     */
    public int getTotalScore(){
        return this.chinese + this.math + this.english;
    }

    /**
     * 这个方法是专门用来比较学生大小。
     * Student s1 = new ...;
     * Student s2 = new ...;
     * s1.compareTo(s2);
     * @param student
     * @return
     */
    public int compareTo(Student student) { // 10 - 10 = 0   10 - 9 = 1   9 - 10 = -1
        // 外部程序中比较的是 s1 和 s2的大小关系。
        // 在程序内部比较的是 this 和 student的大小关系。
        // s1总成绩和s2总成绩是相等的，则返回0
        // s1总成绩大于s2总成绩，返回大于0的数字
        // s1总成绩小于s2总成绩，返回小于0的数字
        return this.getTotalScore() - student.getTotalScore();
    }
}
```

```java
package com.jkweilai.studentsort;

import java.util.Arrays;

/**
 * 自定义的数组工具类。
 */
public class ArrayUtil {
    // 构造方法私有化
    private ArrayUtil(){}

    /**
     * 使用冒泡排序按总分从高到低对学生数组进行原地排序。
     * @param students
     */
    public static void sortByTotal(Student[] students){
        // 冒泡排序怎么写？
        /*int[] arr = {10, 20, 30, 50, 40, 9, 7};
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if(arr[j] < arr[j + 1]){
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        System.out.println(Arrays.toString(arr));*/

        for (int i = 0; i < students.length - 1; i++) {
            for (int j = 0; j < students.length - i - 1; j++) {
                if(students[j].compareTo(students[j + 1]) < 0){
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }

                /*if(students[j].compareTo(students[j + 1]) > 0){
                    Student temp = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = temp;
                }*/
            }
        }
    }

    /**
     * 返回一个新数组，包含同时满足语文≥minChinese 且总分≥minTotal的学生（保持原顺序）
     * @param students 需要过滤的学生数组
     * @param minChinese 语文最低成绩
     * @param minTotal 最低总分
     * @return
     */
    public static Student[] filterByCondition(Student[] students, int minChinese, int minTotal){
        if(students == null || students.length == 0){
            return null;
        }
        Student[] newStudents = new Student[students.length];
        int index = 0;
        // 对学生数组进行遍历，取出每个学生对象，判断学生对象是否满足条件。
        for(Student student : students){
            if(student.getChinese() >= minChinese && student.getTotalScore() >= minTotal){
                newStudents[index++] = student;
            }
        }
        if(index == newStudents.length){
            // 不需要拷贝
            return newStudents;
        }
        return Arrays.copyOf(newStudents, index);
    }

}
```

```java
package com.jkweilai.studentsort;

public class Test {
    public static void main(String[] args) {
        //ArrayUtil.sortByTotal(null);

        // 创建学生对象
        Student s1 = new Student("张三", 90, 60, 90);
        Student s2 = new Student("李四", 60, 80, 92);
        Student s3 = new Student("王五", 50, 90, 93);
        Student s4 = new Student("赵六", 88, 95, 100);
        Student s5 = new Student("周八", 99, 100, 60);

        Student[] students = {s1, s2, s3, s4, s5};

        // 排序
        ArrayUtil.sortByTotal(students);

        // 输出
        for(Student s: students) {
            System.out.println("姓名：" + s.getName() + "，总分：" + s.getTotalScore());
        }

        Student[] newStudents = ArrayUtil.filterByCondition(students, 100, 200);
        System.out.println(newStudents.length);
    }
}
```