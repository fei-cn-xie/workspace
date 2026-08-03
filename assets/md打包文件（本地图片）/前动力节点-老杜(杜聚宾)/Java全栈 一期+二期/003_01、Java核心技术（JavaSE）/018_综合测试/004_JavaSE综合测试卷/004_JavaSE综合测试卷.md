# JavaSE综合测试卷

**考试时间：3小时**
**总分：100分**

# 选择题（每题2分，共20题，共40分）

## 程序输出结果是？

```java
String s1 = "Hello";
String s2 = new String("Hello");
String s3 = "Hel" + "lo";
String s4 = "Hel";
String s5 = s4 + "lo";

System.out.println(s1 == s2);
System.out.println(s1 == s3);
System.out.println(s1 == s5);
System.out.println(s1.equals(s2));
```

输出结果正确的是：
A) false, false, true, true
B) false, true, false, true
C) true, false, true, false
D) false, true, true, true

## 程序输出结果是？

```java
class A {
    public void print() {
        System.out.println("A");
    }
}

class B extends A {
    public void print() {
        System.out.println("B");
    }
    
    public void test() {
        super.print();
        ((A) this).print();
    }
}

public class Main {
    public static void main(String[] args) {
        new B().test();
    }
}
```

输出结果：
A) A, A
B) A, B
C) B, B
D) B, A

## 程序的输出结果是？

```java
public class ExceptionTest {
    public static String test() {
        try {
            System.out.println("try");
            throw new RuntimeException();
        } catch (Exception e) {
            System.out.println("catch");
            return "return from catch";
        } finally {
            System.out.println("finally");
            return "return from finally";
        }
    }
    
    public static void main(String[] args) {
        System.out.println(test());
    }
}
```

输出结果：
A) try, catch, finally, return from catch
B) try, catch, finally, return from finally
C) try, catch, return from catch
D) 编译错误

## 这段代码会？

```java
List<Integer> list = new ArrayList<>();
list.add(1);
list.add(2);
list.add(3);
list.add(4);

for (Integer num : list) {
    if (num % 2 == 0) {
        list.remove(num);
    }
}
```

A) 正常执行，list变为[1, 3]
B) 抛出ConcurrentModificationException
C) 正常执行，list变为[1]
D) 无限循环

## 这段代码会？

```java
public class VisibilityTest {
    private static boolean flag = true;
    
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            while (flag) {
                // 空循环
            }
            System.out.println("Thread stopped");
        });
        
        thread.start();
        Thread.sleep(1000);
        flag = false;
        System.out.println("Main set flag to false");
    }
}
```

A) 1秒后正常停止
B) 可能永远不会停止
C) 立即停止
D) 抛出异常

## 输出结果是？

```java
public class BoxingTrap {
    public static void main(String[] args) {
        Integer a = 100;
        Integer b = 100;
        Integer c = 200;
        Integer d = 200;
        
        System.out.println(a == b);
        System.out.println(c == d);
        System.out.println(a.equals(b));
        System.out.println(c.equals(d));
    }
}
```

输出结果：
A) true, true, true, true
B) true, false, true, true
C) false, false, true, true
D) true, false, false, true

## 输出结果是？

```java
public class LambdaTrap {
    private String value = "outer";
    
    public void test() {
        String value = "inner";
        Runnable r = () -> System.out.println(this.value);
        r.run();
    }
    
    public static void main(String[] args) {
        new LambdaTrap().test();
    }
}
```

输出结果：
A) inner
B) outer
C) null
D) 编译错误

## 这段代码会？

```java
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream = list.stream();

stream.forEach(System.out::print);
stream.forEach(System.out::print);
```

A) 输出"abcabc"
B) 抛出IllegalStateException
C) 输出"abc"
D) 编译错误

## 这段代码会？

```java
public class ReflectionTrap {
    private String secret = "confidential";
    
    public static void main(String[] args) throws Exception {
        ReflectionTrap obj = new ReflectionTrap();
        Field field = ReflectionTrap.class.getDeclaredField("secret");
        
        field.set(obj, "hacked");
        System.out.println(obj.secret);
    }
}
```

A) confidential
B) hacked
C) 抛出IllegalAccessException
D) 编译错误

## 这段代码的输出结果是？

```java
@Inherited
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@interface MyAnnotation {
    String value();
}

@MyAnnotation("parent")
class Parent {}

class Child extends Parent {}

public class AnnotationTrap {
    public static void main(String[] args) {
        System.out.println(Child.class.isAnnotationPresent(MyAnnotation.class));
    }
}
```

A) false
B) true
C) 抛出异常
D) 编译错误

## 程序输出结果是？

```java
public class TryWithResourceTrap {
    static class Resource implements AutoCloseable {
        public void close() {
            System.out.print("close ");
            throw new RuntimeException("from close");
        }
    }
    
    public static void main(String[] args) {
        try (Resource r = new Resource()) {
            throw new RuntimeException("from try");
        } catch (Exception e) {
            System.out.print(e.getMessage());
        }
    }
}
```

A) from try
B) close from try
C) from close
D) close from close

## 这段代码会？

```java
public class DoubleNaN {
    public static void main(String[] args) {
        double d1 = 0.0 / 0.0;
        double d2 = 0.0 / 0.0;
        
        System.out.println(d1 == d2);
        System.out.println(Double.compare(d1, d2) == 0);
    }
}
```

A) false, false
B) false, true
C) true, false
D) true, true

## 程序输出结果是？

```java
public class StaticInitialization {
    private static StaticInitialization instance = new StaticInitialization();
    private static int x = 5;
    private int y = x;
    
    public StaticInitialization() {
        System.out.println("x=" + x + ", y=" + y);
    }
    
    public static void main(String[] args) {
        new StaticInitialization();
    }
}
```

A) x=5, y=5 两次
B) x=0, y=0 然后 x=5, y=5
C) x=0, y=0 两次
D) x=5, y=0 然后 x=5, y=5

## 这段代码会？

```java
public class MethodReference {
    public static void main(String[] args) {
        List<String> list = Arrays.asList("a", "b", "c");
        list.forEach(System.out::println);
        
        // 下面这行会怎样？
        MethodReference::nonStaticMethod;
    }
    
    public void nonStaticMethod(String s) {
        System.out.println(s);
    }
}
```

A) 正常输出abc
B) 编译错误
C) 运行时报错
D) 输出abc然后编译错误

## 程序输出结果是？

```java
public class GenericErasure {
    public void method(List<String> list) {
        System.out.println("String");
    }
    
    public void method(List<Integer> list) {
        System.out.println("Integer");
    }
    
    public static void main(String[] args) {
        new GenericErasure().method(new ArrayList<>());
    }
}
```

A) String
B) 编译错误
C) Integer
D) 运行时报错

## 这段代码会？

```java
public class ThreadLocalTrap {
    private static ThreadLocal<Integer> threadLocal = new ThreadLocal<>();
    
    public static void main(String[] args) {
        threadLocal.set(1);
        
        Thread thread = new Thread(() -> {
            System.out.println(threadLocal.get());
        });
        
        thread.start();
    }
}
```

A) 输出1
B) 输出null
C) 编译错误
D) 运行时报错

## 程序输出结果是？

```java
public class EnumTrap {
    enum Color {
        RED, GREEN;
        
        Color() {
            System.out.print(name() + " ");
        }
    }
    
    public static void main(String[] args) {
        System.out.print("Start ");
        Color color = Color.RED;
        System.out.print("End");
    }
}
```

A) Start RED End
B) Start RED GREEN End
C) RED GREEN Start End
D) Start End

## 这段代码会？

```java
public class VarArgsTrap {
    public static void method(int... nums) {
        System.out.println("varargs");
    }
    
    public static void method(int num) {
        System.out.println("single");
    }
    
    public static void main(String[] args) {
        method();
        method(1);
        method(1, 2);
    }
}
```

A) varargs, varargs, varargs
B) varargs, single, varargs
C) 编译错误
D) 运行时报错

## 程序输出结果是？

```java
public class BitOperation {
    public static void main(String[] args) {
        int x = Integer.MIN_VALUE;
        System.out.println(x);
        System.out.println(-x);
        System.out.println(Math.abs(x));
    }
}
```

A) -2147483648, 2147483647, 2147483647
B) -2147483648, -2147483648, -2147483648
C) -2147483648, 2147483647, -2147483648
D) -2147483648, -2147483648, 2147483647

## 这段代码会？

```java
public class OptionalTrap {
    public static void main(String[] args) {
        Optional<String> optional = Optional.of("hello");
        optional = optional.filter(s -> s.startsWith("x"));
        
        System.out.println(optional.orElse("world"));
        
        // 下面这行会？
        Optional.of(null);
    }
}
```

A) 输出world然后输出null
B) 输出world然后抛出异常
C) 输出hello然后抛出异常
D) 编译错误

# 编程题（共60分）

## 自定义注解和反射应用（30分）

设计一个简单的ORM（对象关系映射）框架，要求：

1. 创建以下注解：
  - `@Table`：用于类，指定对应的数据库表名
  - `@Column`：用于字段，指定对应的列名和类型
  - `@Id`：用于主键字段
2. 创建一个`User`类，使用上述注解：

```java
@Table(name = "users")
public class User {
    @Id
    @Column(name = "id", type = "INTEGER")
    private Long id;
    
    @Column(name = "username", type = "VARCHAR")
    private String username;
    
    @Column(name = "email", type = "VARCHAR")
    private String email;
    
    // 构造方法、getter、setter
}
```

1. 创建一个`SQLGenerator`类，通过反射解析注解，生成对应的SQL语句：
  - `generateCreateTable(Class<?> clazz)`：生成建表SQL

```sql
# 建表语句示例
create table users(
  id INTEGER,
  username VARCHAR,
  email VARCHAR
);
```

```plaintext
- `generateInsert(Object obj)`：生成插入SQL
```

```sql
# 插入语句示例
inesrt into users(id, username, email) values(1, 'admin', 'admin@123.com');
```

```plaintext
- `generateSelectById(Class<?> clazz, Object id)`：根据ID查询的SQL
```

```sql
select id, username, email from users where id = 1;
```

1. 编写测试代码验证功能

## 多线程分段下载与文件合并系统（30 分）

设计并实现一个多线程文件下载系统，能够将大文件分成多个块进行并发下载，并在所有线程完成后将文件块合并成完整的文件。

**功能**

- 支持自定义文件总大小和线程数量
- 自动计算每个线程的下载范围，正确处理文件大小不是线程数整数倍的情况
- 每个线程将下载的数据保存为临时文件
- 所有线程完成后自动合并临时文件为最终文件

**技术实现要点**

- 线程范围的精确计算（包括余数处理）
- 临时文件的创建和管理
- 文件块的顺序合并
- 资源清理（删除临时文件）

**输出要求**

```plaintext
文件总大小: 1234字节, 线程数: 5
线程0 下载范围: 0 - 246 (大小: 246)
线程1 下载范围: 246 - 492 (大小: 246)
线程2 下载范围: 492 - 738 (大小: 246)
线程3 下载范围: 738 - 984 (大小: 246)

线程4 下载范围: 984 - 1234 (大小: 250) ← 最后一个线程处理余数
...
下载完成，开始文件合并...
临时文件合并完成: final_file.dat
验证结果: 文件大小 1234/1234 ✓
清理临时文件...
所有操作完成!
```

**输入参数**

```java
// 可配置参数
private static final int TOTAL_SIZE = 1234;    // 文件总大小（非200倍数）
private static final int THREAD_COUNT = 5;     // 线程数量
```