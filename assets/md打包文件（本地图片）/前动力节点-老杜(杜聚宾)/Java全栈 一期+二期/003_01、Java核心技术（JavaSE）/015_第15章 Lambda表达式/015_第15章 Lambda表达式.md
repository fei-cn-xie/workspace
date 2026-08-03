# 第15章 Lambda表达式

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/Bdv3beMI9oqe9txj6mdcxmiHn3c.jpeg)

# Lambda表达式的概述

## Lambda表达式的引入

Lambda表达式是JDK1.8的一个新特性，可以取代大部分的匿名内部类，以便写出更优雅的Java代码，尤其在集合的遍历和其他集合操作中，可以极大地优化代码结构。

在以前的学习中，想要实现对List集合的“降序”排序操作，就需要使用匿名内部类来实现，这样的代码非常的复杂和繁琐，代码如下：

```java
// 方式一：使用匿名内部类来实现
List<Integer> list = Arrays.asList(3, 6, 1, 7, 2, 5, 4);
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o2 - o1;
    }
});
System.out.println("排序后：" + list);
```

针对以上对List集合的的“降序”排序操作，除了使用匿名内部类来实现外，还可以使用Lambda表达式来实现，使用Lambda表达式的代码非常优雅，并且还非常的简洁，代码如下：

```java
// 方式二：使用Lambda表达式来实现
List<Integer> list = Arrays.asList(3, 6, 1, 7, 2, 5, 4);
Collections.sort(list, (o1, o2) -> o2 - o1);
System.out.println("排序后：" + list);
```

## 函数式编程思想的概述

Java自诞生以来一直以“一切皆对象”为核心理念，面向对象编程（OOP）是它的基本范式。然而，随着 Python、Scala 等语言的兴起和编程范式的多样化，Java 也在不断演进，从 JDK 1.8 开始支持函数式编程（OFP），引入了 Lambda 表达式等重要特性。

- **面向对象思想**：
做一件事，通常需要找到一个能够处理该事情的对象，调用其方法，从而完成任务。重点在于对象和行为的封装。
- **函数式编程思想**：
更关注执行的结果，而非具体由谁执行或如何执行。它强调将行为抽象为函数，并支持将函数作为参数传递或返回值使用，代码更简洁、灵活。

在函数式编程语言中，函数被视为“一等公民”——可以像普通变量一样被传递、赋值和操作。在 Java 中，Lambda 表达式本质上是函数式接口的一个具体实例，而不是一个独立的函数。因此，Lambda 表达式必须依附于函数式接口（即只有一个抽象方法的接口）存在。

**简单来说：在 JDK 1.8 及以后版本中，Lambda 表达式就是函数式接口的实例。只要一个接口是函数式接口，就可以使用 Lambda 表达式来实现它。**

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/IIYVbEceQoE95XxX3uTcxZcdnJh.jpeg)

## 如何去理解函数式接口

能够使用Lambda表达式的一个重要依据是必须有相应的函数式接口，所谓的函数式接口，指的就是“一个接口中有且只能有一个抽象方法”。也就是说，如果一个接口只有一个抽象方法，那么该接口就是一个函数式接口。

如果我们在接口上声明了 @FunctionalInterface 注解，那么编译器就会按照函数式接口的定义来要求该接口，也就是该接口中有且只能定义一个抽象方法，如果该接口中定义了多个或0个抽象方法，则程序编译时就会报错。

【示例】定义一个函数式接口

```java
@FunctionalInterface
public interface Flyable {
    // 在函数式接口中，我们有且只能定义一个抽象方法
    void showFly();
    // 但是，可以定义任意多个默认方法或静态方法
    default void show() {
        System.out.println("JDK1.8之后，接口还可以定义默认方法和静态方法");
    }
}
```

另外，从某种意义上来说，只要你保证你的接口中有且只有一个抽象方法，则接口中没有使用 @FunctionalInterface 注解来标注，那么该接口也依旧属于函数式接口。

在以下代码中，Flyable接口中没有使用@FunctionalInterface 注解，但是Flyable接口中只存在一个抽象方法，因此Flyable接口依旧属于函数式接口，那么使用Lambda表达式就可以表示Flyable 接口的实例，代码如下：

```java
/**
 * 没有使用@FunctionalInterface标注的接口
 */
public interface Flyable {
    void showFly();
}
/**
 * 测试类
 */
public class Test01 {
    public static void main(String[] args) {
        // 使用lambda表示来表示Flyable接口的实例
        Flyable flyable = () -> {
            System.out.println("小鸟自由自在的飞翔");
        };
        // 调用Flyable接口的实例的showFly()方法
        flyable.showFly();
    }
}
```

## Lambda和匿名内部类

1. **适用类型不同**
  1. 匿名内部类：适用于任意类型的接口、抽象类或具体类。具体类？对的，即使你不是接口也不是抽象类，是一个具体类。通过匿名内部类也是可以重写方法的。比如：User user = new User(){}; 通过这种方式继承具体类，来重写方法，子类是一个没有名字的类。
  2. Lambda表达式：仅适用于接口。
2. **使用条件不同**
  1. 当接口中有且仅有一个抽象方法（函数式接口）时，可以使用Lambda表达式，也可以使用匿名内部类。
  2. 当接口中有多个抽象方法时，只能使用匿名内部类，不能使用Lambda表达式。
3. **实现机制不同**
  1. 匿名内部类：编译后会生成一个单独的.class字节码文件。
  2. Lambda表达式：编译后不会生成单独的.class文件，而是在运行时动态生成。

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/CSiobFXlXoeXr5xP7YGcg5RTn6d.jpeg)

# Lambda表达式的使用

## Lambda表达式的语法

Lambda 表达式本质上是一个匿名函数。在传统的方法定义中，我们需要声明返回值类型、方法名、形参列表和方法体等部分，而 Lambda 表达式则只关注最核心的**形参列表**和**方法体**。

在 Java 中，Lambda 表达式的语法为：

```plaintext
(形参列表) -> { 方法体 }
```

其中 `->` 是 Lambda 操作符（也称箭头操作符），"形参列表"对应接口中抽象方法的参数列表，"方法体"则是该抽象方法的具体实现。

下面通过一个具体的例子，展示如何从匿名内部类演化为 Lambda 表达式：

**原始匿名内部类写法：**

```java
List<Integer> list = Arrays.asList(3, 6, 1, 7, 2, 5, 4);
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o2 - o1;  // 核心逻辑：降序排序
    }
});
System.out.println("排序后：" + list);
```

在这个匿名内部类中，大部分代码都是固定的模板代码，只有 `compare` 方法的参数列表 `(Integer o1, Integer o2)` 和方法体 `return o2 - o1;` 是实际完成排序功能的核心代码。

**转换为 Lambda 表达式：**

```java
List<Integer> list = Arrays.asList(3, 6, 1, 7, 2, 5, 4);
Collections.sort(list, (Integer o1, Integer o2) -> {
    return o2 - o1;
});
System.out.println("排序后：" + list);
```

在 Lambda 表达式中：

- `(Integer o1, Integer o2)` 对应抽象方法的形参列表
- `return o2 - o1;` 对应方法体的具体实现

Lambda 表达式的价值在于它摒弃了冗余的语法模板，只保留最核心的业务逻辑，让代码更加简洁清晰，体现了函数式编程的优雅与高效。

## Lambda 表达式的上下文环境

**关键点**：在使用 Lambda 表达式时，编译器需要根据**上下文环境**来推断它实现的是哪个接口。没有这个上下文，Lambda 表达式将因类型不明而无法使用。

```java
public class Test {
    public static void main(String[] args) {
        Flyable f = () -> { System.out.println("fly...."); };
        f.fly();
    }
}

interface Flyable {
    void fly();
}
```

Lambda 表达式 `() -> { System.out.println("fly...."); }` 能够被正确编译，是因为它被直接赋值给了 `Flyable` 类型的变量 `f`。这个赋值操作提供了关键的**上下文环境**，让编译器可以明确推断出该 Lambda 表达式即为 `Flyable` 接口的实例。如果没有这个上下文，编译器将无法理解 Lambda 表达式的类型归属。

## Lambda表达式的使用

### Lambda表达式的基本使用

接下来，我们以自定义的函数式接口为例，先从匿名对象的实现过程，慢慢演变为Lambda表达式的实现过程。

#### 无返回值函数式接口

情况一：无返回值无参数

```java
// 情况一：无返回值无参数
interface NoParameterNoReturn {
    void test();
}

public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        NoParameterNoReturn obj1 = new NoParameterNoReturn() {
            @Override
            public void test() {
                System.out.println("无参无返回值");
            }
        };
        obj1.test();

        // 方式二：使用Lambda表达式来实现
        NoParameterNoReturn obj2 = () -> {
            System.out.println("无参无返回值");
        };
        obj2.test();
    }
}
```

情况二：无返回值一个参数

```java
// 情况二：无返回值一个参数
interface OneParameterNoReturn {
    void test(int num);
}

public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        OneParameterNoReturn obj1 = new OneParameterNoReturn() {
            @Override
            public void test(int num) {
                System.out.println("无返回值一个参数 --> " + num);
            }
        };
        obj1.test(10);

        // 方式二：使用Lambda表达式来实现
        OneParameterNoReturn obj2 = (int num) -> {
            System.out.println("无返回值一个参数 --> " + num);
        };
        obj2.test(20);
    }
}
```

情况三：无返回值多个参数

```java
// 情况三：无返回值多个参数
interface MoreParameterNoReturn {
    void test(String str1, String str2);
}
public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        MoreParameterNoReturn obj1 = new MoreParameterNoReturn() {
            @Override
            public void test(String str1, String str2) {
                System.out.println(str1 + " : " + str2);
            }
        };
        obj1.test("hello", "world");

        // 方式二：使用Lambda表达式来实现
        MoreParameterNoReturn obj2 = (String str1, String str2) -> {
            System.out.println(str1 + " : " + str2);
        };
        obj2.test("你好", "世界");
    }
}
```

#### 有返回值函数接口

情况一：有返回值无参数

```java
// 情况一：有返回值无参数
interface NoParameterHasReturn {
    int test();
}

public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        NoParameterHasReturn obj1 = new NoParameterHasReturn() {
            @Override
            public int test() {
                return 520;
            }
        };
        System.out.println(obj1.test()); // 输出：520

        // 方式二：使用Lambda表达式来实现
        NoParameterHasReturn obj2 = () -> {
            return 1314;
        };
        System.out.println(obj2.test()); // 输出：1314
    }
}
```

情况二：有返回值一个参数

```java
// 情况二：有返回值一个参数
interface OneParameterHasReturn {
    String test(double num);
}

public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        OneParameterHasReturn obj1 = new OneParameterHasReturn() {
            @Override
            public String test(double num) {
                return "传入的小数为：" + num;
            }
        };
        System.out.println(obj1.test(520.0));

        // 方式二：使用Lambda表达式来实现
        OneParameterHasReturn obj2 = (double num) -> {
            return "传入的小数为：" + num;
        };
        System.out.println(obj2.test(1314.0));
    }
}
```

情况三：有返回值多个参数

```java
// 情况三：有返回值多个参数
interface MoreParameterHasReturn {
    String test(int num1, int num2);
}
public class Test01 {
    public static void main(String[] args) {
        // 方式一：使用匿名内部类来实现
        MoreParameterHasReturn obj1 = new MoreParameterHasReturn() {
            @Override
            public String test(int num1, int num2) {
                return "运算的结果为：" + (num1 + num2);
            }
        };
        System.out.println(obj1.test(10, 20));

        // 方式二：使用Lambda表达式来实现
        MoreParameterHasReturn obj2 = (int num1, int num2) -> {
            return "运算的结果为：" + (num1 + num2);
        };
        System.out.println(obj2.test(20, 30));
    }
}
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/RJIAbz2enoG2ifx3ZWtc4U4hnHc.jpeg)

### Lambda表达式的语法精简

在以上代码中，虽然Lambda表达式的语法已经很简洁了，但是Lambda表达式的语法格式还可以更加的精简，从而写出更加优雅的代码，但是相应的代码可读性也会变差。

在以下的应用场景中，我们就可以对Lambda表达式的语法进行精简，场景如下：

1. 形参类型可以省略，如果需要省略，则每个形参的类型都要省略。
2. 如果形参列表中只存在一个形参，那么形参类型和小括号都可以省略。
3. 如果方法体当中只有一行语句，那么方法体的大括号也可以省略。
4. 如果方法体中只有一条return语句，那么大括号可以省略，且必须去掉return关键字。

接下来，我们就对以下的Lambda表达式代码进行精简，从而写出更加优雅的代码。

```java
public class Test01 {
    public static void main(String[] args) {
        // (1)形参类型可以省略，如果需要省略，每个形参的类型都要省略。
        // 没有精简的Lambda表达式代码
        MoreParameterNoReturn obj1 = (String str1, String str2) -> {
            System.out.println(str1 + " : " + str2);
        };
        obj1.test("hello", "world");
        // 精简之后的Lambda表达式代码
        MoreParameterNoReturn obj2 = (str1, str2) -> {
            System.out.println(str1 + " : " + str2);
        };
        obj2.test("你好", "世界");

        // (2)如果形参列表中只有一个形参，那么形参类型和小括号都可以省略。
        // 没有精简的Lambda表达式代码
        OneParameterHasReturn obj3 = (double num) -> {
            return "传入的小数为：" + num;
        };
        System.out.println(obj3.test(520.0));
        // 精简之后的Lambda表达式代码
        OneParameterHasReturn obj4 = num -> {
            return "传入的小数为：" + num;
        };
        System.out.println(obj4.test(1314.0));

        // (3)如果方法体当中只有一行代码，那么方法体的大括号也可以省略。
        // 没有精简的Lambda表达式代码
        NoParameterNoReturn obj5 = () -> {
            System.out.println("无参无返回值");
        };
        obj5.test();
        // 精简之后的Lambda表达式代码
        NoParameterNoReturn obj6 = () -> System.out.println("无参无返回值");
        obj6.test();

        // (4)方法体中只有一条return语句，则大括号可以省略，且必须去掉return关键字
        // 没有精简的Lambda表达式代码
        MoreParameterHasReturn obj7 = (int a, int b) -> {
            return "运算的结果为：" + (a + b);
        };
        System.out.println(obj7.test(10, 20));
        // 精简之后的Lambda表达式代码
        MoreParameterHasReturn obj8 = (a, b) -> "运算的结果为：" + (a + b);
        System.out.println(obj8.test(20, 30));
    }
}
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/VohFbJ97To0LQXxQVrvc1yNyn8e.jpeg)

## 四个基本的函数式接口

| **名字** | **接口名** | **对应的抽象方法** |
| --- | --- | --- |
| 消费型接口 | Consumer | void accept(T t); |
| 生产型接口 | Supplier | T get(); |
| 转换型接口 | Function<T, R> | R apply(T t); |
| 判断型接口 | Predicate | boolean test(T t); |

以上的函数式接口都在java.util.function包中，通常函数接口出现的地方都可以使用Lambda表达式，所以不必记忆函数接口的名字，这些函数式接口及子接口在后续学习中很常用。

# Lambda表达式的方法引用

## 方法引用的概述

当我们使用 Lambda 表达式时，如果方法体中的内容**仅仅是调用一个已存在的方法（并且函数式接口中方法的返回值和方法的参数 与 内部调用方法的返回值和方法的参数相同时）**，而没有其他任何逻辑操作，这种情况下就可以使用**方法引用**来进一步简化代码。

方法引用可以看作是 Lambda 表达式的一种更简洁的替代形式。

**示例说明**

**Lambda 表达式写法：**

```java
Function<Double, Long> function = (Double x) -> {
    return Math.round(x);  // 方法体只是单纯地调用 Math.round() 方法
};
```

**使用方法引用简化：**

```java
Function<Double, Long> function = Math::round;
```

**关键理解**

在刚才的例子中：

- Lambda 表达式 `(Double x) -> { return Math.round(x); }` 的方法体除了调用 `Math.round()` 外没有其他任何操作
- 这种"单纯转发调用"的场景，正是方法引用的典型适用场景
- 使用 `Math::round` 方法引用，代码变得更加简洁直观

方法引用的本质是**让编译器知道：这里需要执行的操作，与某个已存在的方法完全一致**。

方法引用可以看作是Lambda表达式的一种更简洁的语法糖。

本质上，方法引用就是Lambda表达式，同样是函数式接口的一个实例。

它通过直接使用已有的方法名来指向一个方法，从而避免重复编写Lambda表达式的方法体。

在Java中，方法引用主要分为以下四种核心情况：

1. **引用静态方法** (`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Class::staticMethod</font>`)
2. **引用特定对象的实例方法** (`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">instance::instanceMethod</font>`)
3. **引用任意类型（特定类）的实例方法** (`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Class::instanceMethod</font>`)
4. **引用构造方法** (`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Class::new</font>`)

另外，还有一种特殊的语法用于数组，常被单独列出：

1. **数组引用** (`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Type[]::new</font>`)

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/HtRTbj6jioxujJxgL1WciydHn8d.jpeg)

## 实例方法引用

语法：对象 :: 实例方法

特点：在Lambda表达式的方法体中，通过“对象”来调用指定的某个“实例方法”。

要求：函数式接口中抽象方法的返回值类型和形参列表与内部通过对象调用某个实例方法的返回值类型和形参列表保持一致。

【示例】实例化Consumer接口的实现类对象，并在重写的accept()方法中输出形参的值

```java
// 方式一：使用匿名内部类来实现
Consumer<String> consumer1 = new Consumer<String>() {
    @Override
    public void accept(String str) {
        System.out.println(str);
    }
};
consumer1.accept("hello world");

// 方式二：使用Lambda表达式来实现
Consumer<String> consumer2 = str -> System.out.println(str);
consumer2.accept("hello world");

// 方式三：使用方法引用来实现
Consumer<String> consumer3 = System.out :: println;
consumer3.accept("hello world");
```

【示例】实例化Supplier接口的实现类对象，并在重写方法中返回Teacher对象的姓名

```java
Teacher teacher = new Teacher("jack", 18);
// 方式一：使用匿名内部类来实现
Supplier<String> supplier1 = new Supplier<String>() {
    @Override
    public String get() {
        return teacher.getName();
    }
};
System.out.println(supplier1.get());

// 方式二：使用Lambda表达式来实现
Supplier<String> supplier2 = () -> teacher.getName();
System.out.println(supplier2.get());

// 方式三：使用方法引用来实现
Supplier<String> supplier3 = teacher :: getName;
System.out.println(supplier3.get());
```

## 静态方法引用

语法：类 :: 静态方法

特点：在Lambda表达式的方法体中，通过“类名”来调用指定的某个“静态方法”。

要求：函数式接口中抽象方法的返回值类型和形参列表与内部通过类名调用某个静态方法的返回值类型和形参列表保持一致。

【示例】使用Comparator比较器，来判断两个整数的大小

```java
// 方式一：使用匿名内部类来实现
Comparator<Integer> comparator1 = new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return Integer.compare(o1, o2);
    }
};
System.out.println(comparator1.compare(10, 20));

// 方式二：使用Lambda表达式来实现
Comparator<Integer> comparator2 = (o1, o2) -> Integer.compare(o1, o2);
System.out.println(comparator2.compare(10, 20));

// 方式三：使用方法引用来实现
Comparator<Integer> comparator3 = Integer :: compare;
System.out.println(comparator3.compare(10, 20));
```

【示例】实例化Function接口的实现类对象，并在重写的方法中返回小数取整的结果

```java
// 方式一：使用匿名内部类来实现
Function<Double, Long> function1 = new Function<Double, Long>() {
    @Override
    public Long apply(Double aDouble) {
        return Math.round(aDouble);
    }
};
System.out.println(function1.apply(3.14));

// 方式二：使用Lambda表达式来实现
Function<Double, Long> function2 = aDouble -> Math.round(aDouble);
System.out.println(function2.apply(3.14));

// 方式三：使用方法引用来实现
Function<Double, Long> function3 = Math :: round;
System.out.println(function3.apply(3.14));
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/WUC3bcT9YoTSjfxW52kczqfEncg.jpeg)

## 特殊方法引用

语法：类名 :: 实例方法

特点：在Lambda表达式的方法体中，通过方法的第一个形参来调用指定的某个“实例方法”。

要求：把函数式接口中抽象方法的第一个形参作为方法的调用者对象，并且从第二个形参开始（或无参）对应到该被调用实例方法的参数列表中，并且返回值类型保持一致。

【示例】使用Comparator比较器，来判断两个小数的大小

```java
// 方式一：使用匿名内部类来实现
Comparator<Double> comparator1 = new Comparator<Double>() {
    @Override
    public int compare(Double o1, Double o2) {
        return o1.compareTo(o2);
    }
};
System.out.println(comparator1.compare(10.0, 20.0));

// 方式二：使用Lambda表达式来实现
Comparator<Double> comparator2 = (o1, o2) -> o1.compareTo(o2);
System.out.println(comparator2.compare(10.0, 20.0));

// 方式三：使用方法引用来实现
Comparator<Double> comparator3 = Double :: compareTo;
System.out.println(comparator3.compare(10.0, 20.0));
```

需求：实例化Function接口的实现类对象，然后获得传入Teacher对象的姓名。

```java
// 方式一：使用匿名内部类来实现
Teacher teacher = new Teacher("jack", 18);
Function<Teacher, String> function1 = new Function<Teacher, String>() {
    @Override
    public String apply(Teacher teacher) {
        return teacher.getName();
    }
};
System.out.println(function1.apply(teacher));

// 方式二：使用Lambda表达式来实现
Function<Teacher, String> function2 = e -> e.getName();
System.out.println(function2.apply(teacher));

// 方式三：使用方法引用来实现
Function<Teacher, String > function3 = Teacher :: getName;
System.out.println(function3.apply(teacher));
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/LI8UbmMqmoNwSKx0iJAcJOM9n8e.jpeg)

## 构造方法引用

语法：类名 :: new

特点：在Lambda表达式的方法体中，返回指定“类名”来创建出来的对象。

要求：创建对象所调用构造方法形参列表和重写方法的形参列表保持一致，并且重写方法的返回值类型和创建对象的类型保持一致。

【示例】实例化Supplier接口的实现类对象，然后调用重写方法返回Teacher对象

```java
// 方式一：使用匿名内部类来实现
Supplier<Teacher> supplier1 = new Supplier<Teacher>() {
    @Override
    public Teacher get() {
        return new Teacher();
    }
};
System.out.println(supplier1.get());

// 方式二：使用Lambda表达式来实现
Supplier<Teacher> supplier2 = () -> new Teacher();
System.out.println(supplier2.get());

// 方式二：使用构造方法引用来实现
// 注意：根据重写方法的形参列表，那么此处调用了Teacher类的无参构造方法
Supplier<Teacher> supplier3 = Teacher :: new;
System.out.println(supplier3.get());
```

【示例】实例化Function接口的实现类对象，然后调用重写方法返回Teacher对象

```java
// 方式一：使用匿名内部类来实现
Function<String, Teacher> function1 = new Function<String, Teacher>() {
    @Override
    public Teacher apply(String name) {
        return new Teacher(name);
    }
};
System.out.println(function1.apply("jack"));

// 方式二：使用Lambda表达式来实现
Function<String, Teacher> function2 = name -> new Teacher(name);
System.out.println(function2.apply("jack"));

// 方式二：使用构造方法引用来实现
// 注意：根据重写方法的形参列表，那么此处调用了Teacher类name参数的构造方法
Function<String, Teacher> function3 = Teacher :: new;
System.out.println(function3.apply("jack"));
```

## 数组引用

语法：数组类型 :: new

特点：在Lambda表达式的方法体中，创建并返回指定类型的“数组”。

要求：重写的方法有且只有一个整数型的参数，并且该参数就是用于设置数组的空间长度，并且重写方法的返回值类型和创建数组的类型保持一致。

【示例】实例化Function接口的实现类对象，并在重写方法中返回指定长度的int类型数组

```java
// 方式一：使用匿名内部类来实
Function<Integer, int[]> function1 = new Function<Integer, int[]>() {
    @Override
    public int[] apply(Integer integer) {
        return new int[integer];
    }
};
System.out.println(Arrays.toString(function1.apply(10)));

// 方式二：使用Lambda表达式来实现
Function<Integer, int[]> function2 = num -> new int[num];
System.out.println(Arrays.toString(function2.apply(20)));

// 方式三：使用方法引用来实现
Function<Integer, int[]> function3 = int[] :: new;
System.out.println(Arrays.toString(function3.apply(30)));
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/KI6ObapDgoJJpLxptrrcLjWMnCe.jpeg)

# Lambda在集合当中的使用

为了能够让Lambda和Java的集合类集更好的一起使用，集合当中也新增了部分方法，以便与Lambda表达式对接，要用Lambda操作集合就一定要看懂源码。

## forEach()方法

在Collection集合和Map集合中，都提供了forEach()方法用于遍历集合。

在Collection集合中，提供的forEach()方法的形参为Consumer接口（消费型接口），通过该方法再配合Lambda表达式就可以遍历List和Set集合中的元素。

【示例】遍历List集合中的元素

```java
List<Integer> list = Arrays.asList(11, 22, 33, 44, 55);
// 方式一：使用匿名内部类来实现
list.forEach(new Consumer<Integer>() {
    /**
     * 获得遍历出来的元素
     * @param element 遍历出来的元素
     */
    @Override
    public void accept(Integer element) {
        System.out.println(element);
    }
});

// 方式二：使用Lambda表达式来实现
list.forEach(element -> System.out.println(element));

// 方式三：使用方法引用来实现
list.forEach(System.out :: println);
```

【示例】遍历Set集合中的元素

```java
List<String> list = Arrays.asList("aa", "bb", "cc", "dd");
HashSet<String> hashSet = new HashSet<>(list);
// 方式一：使用匿名内部类来实现
hashSet.forEach(new Consumer<String>() {
    /**
     * 获得遍历出来的元素
     * @param element 遍历出来的元素
     */
    @Override
    public void accept(String element) {
        System.out.println(element);
    }
});
// 方式二：使用Lambda表达式来实现
hashSet.forEach(element -> System.out.println(element));

// 方式三：使用方法引用来实现
hashSet.forEach(System.out :: println);
```

在Map集合中，提供的forEach()方法的形参为BiConsumer接口，而BiConsumer接口属于两个参数的消费型接口，通过该方法再配合Lambda表达式就可以遍历Map集合中的元素。

【示例】遍历Map集合中的元素

```java
// 实例化Map集合并添加键值对
HashMap<String, String> map = new HashMap<>();
map.put("张三", "成都");
map.put("李四", "重庆");
map.put("王五", "西安");
// 方式一：使用匿名内部类来实现
map.forEach(new BiConsumer<String, String>() {
    /**
     * 获得遍历出来的key和value
     * @param key 键
     * @param value 值
     */
    @Override
    public void accept(String key, String value) {
        System.out.println("key：" + key + "，value：" + value);
    }
});
// 方式二：使用Lambda表达式来实现
map.forEach((k, v) -> System.out.println("key：" + k + "，value：" + v));
```

![65a44522-4f70-420a-85c7-80ba468b51a8.jpeg](images/XHoFbvYAvowLrkxN1PMcCC18nef.jpeg)

## removeIf()方法

在Collection集合中，提供的removeIf()方法的形参为Predicate接口（判断型接口），通过该方法再配合Lambda表达式就可以遍历List和Set集合中的元素。

【示例】删除List集合中的某个元素

```java
// 创建List集合并添加元素
List<String> list = new ArrayList<>(Arrays.asList("aa", "bb", "cc", "dd"));
// 方式一：使用匿名内部类来实现
list.removeIf(new Predicate<String>() {
    /**
     * 删除指定的某个元素
     * @param element 用于保存遍历出来的某个元素
     * @return 返回true，代表删除；返回false，代表不删除
     */
    @Override
    public boolean test(String element) {
        return "bb".equals(element);
    }
});
System.out.println(list); // 输出：[aa, cc, dd]

// 方式二：使用Lambda表达式来实现
list.removeIf("cc" :: equals);
System.out.println(list); // 输出：[aa, dd]
```

【示例】删除Set集合中的某个元素

```java

List<String> list = Arrays.asList("aa", "bb", "cc", "dd");
HashSet<String> hashSet = new HashSet<>(list);
// 方式一：使用匿名内部类来实现
hashSet.removeIf(new Predicate<String>() {
    /**
     * 删除指定的某个元素
     * @param element 用于保存遍历出来的某个元素
     * @return 返回true，代表删除；返回false，代表不删除
     */
    @Override
    public boolean test(String element) {
        return "bb".equals(element);
    }
});
System.out.println(hashSet); // 输出：[aa, cc, dd]

// 方式二：使用Lambda表达式来实现
hashSet.removeIf("cc" :: equals);
System.out.println(hashSet); // 输出：[aa, dd]
```