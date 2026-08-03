# JavaSE综合测试卷 解析

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

**解析：**

即使将 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">this</font>` 转型为 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">A</font>`，实际对象仍然是 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">B</font>` 类型，所以调用的还是 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">B</font>` 的 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">print()</font>` 方法。只有使用 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">super</font>` 关键字才能显式调用父类方法。

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

**解析：**

- **只有 finally 中有 return 语句时**才会覆盖之前的返回值
- finally 中只是修改变量值，不会影响**已经暂存**的返回值拷贝

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

**解析：**

for each 迭代集合时不能使用集合的 remove 方法。

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

**解析：**
**CPU 缓存一致性**

- 每个线程可能在自己的 CPU 缓存中保存 flag 的副本
- 主线程修改 flag 后，可能只更新了自己 CPU 的缓存
- 子线程的 CPU 缓存中的旧值 true 没有被刷新

**JIT 编译器可能将循环优化为：****JIT 编译器是 Java 运行时将热点代码编译成本地机器码的即时编译器，用来提升程序执行速度。**

```java
if (flag) {
    while (true) {
        // 无限循环
    }
}
```

**解决方案：**使用 volatile 关键字

```java
private static volatile boolean flag = true;
```

**volatile 保证：**

- 可见性：一个线程的修改对其他线程立即可见
- 禁止指令重排序

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

**解析：**Integer 提供了整数型常量池 [-128~127]

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

**解析：**

- 因为 Lambda 表达式中的 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">this</font>` 指向的是创建 Lambda 的外部类实例，而不是方法内的局部变量。
- Lambda 没有自己的 this，它继承外部作用域的 this。

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

**解析：**已进行终止操作的的 stream 不能再用。

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

**解析：**

因为反射代码写在同一个类内部，所以可以访问本类的私有成员

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

**解析：**因为使用了@Inherited，所以@MyAnnotation 支持继承。

## 程序输出结果是？

```java
public class TryWithResourceTrap {
    static class Resource implements AutoCloseable {
        public void close() {
            System.out.print("close ");
            // 资源自动释放的close方法中出现异常会受到抑制。
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

**解析：** try-with-resources 会先执行 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">close()</font>` 方法，其中抛出的异常被抑制，只有 try 块中的原始异常被捕获。

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

**解析：**NaN 与任何值（包括自己）用 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">==</font>` 比较都返回 false，但 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Double.compare()</font>` 方法将两个 NaN 视为相等。

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

**解析：**静态初始化时第一次实例化因变量尚未赋值而输出 x=0,y=0，静态初始化完成后第二次实例化时变量已赋值故输出 x=5,y=5。

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

**解析：**lambda 表达式必须有上下文环境。

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

**解析：**** **泛型擦除后两个方法签名相同，构成方法重载冲突（方法重复了。）

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

**解析：**ThreadLocal 只能保存住当前线程中的数据。

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

**解析：**每一个枚举值都是对象。

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

**解析：**空参数调用可变参数方法，单参数优先匹配单参方法，多参数调用可变参数方法。

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

**解析：**Integer.MIN_VALUE 取负和绝对值运算时发生整数溢出，结果仍为 Integer.MIN_VALUE

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

**解析：**filter 条件不匹配返回空 Optional 所以输出 "world"，但 `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Optional.of(null)</font>` 直接抛空指针异常。

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

可参考：

```java
package test;

import java.io.*;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class MultiThreadFileDownloader {
    // 可配置参数
    private static final int TOTAL_SIZE = 1234;    // 文件总大小（非200倍数）
    private static final int THREAD_COUNT = 5;     // 线程数量
    private static final String FINAL_FILE = "final_file.dat";

    private final DownloadRange[] ranges;
    private final ExecutorService executor;

    public MultiThreadFileDownloader() {
        this.ranges = calculateRanges();
        this.executor = Executors.newFixedThreadPool(THREAD_COUNT);
    }

    public static void main(String[] args) {
        MultiThreadFileDownloader downloader = new MultiThreadFileDownloader();
        downloader.startDownload();
    }

    // 计算每个线程的下载范围
    private DownloadRange[] calculateRanges() {
        DownloadRange[] ranges = new DownloadRange[THREAD_COUNT];
        int chunkSize = TOTAL_SIZE / THREAD_COUNT;
        int remainder = TOTAL_SIZE % THREAD_COUNT;

        int start = 0;
        for (int i = 0; i < THREAD_COUNT; i++) {
            int end = start + chunkSize;
            // 将余数分配给最后一个线程
            if (i == THREAD_COUNT - 1) {
                end += remainder;
            }
            ranges[i] = new DownloadRange(i, start, end);
            start = end;
        }

        // 打印范围信息
        System.out.println("文件总大小: " + TOTAL_SIZE + "字节, 线程数: " + THREAD_COUNT);
        for (DownloadRange range : ranges) {
            System.out.printf("线程%d 下载范围: %d - %d (大小: %d)%n",
                    range.threadId, range.start, range.end, range.getSize());
        }
        System.out.println();

        return ranges;
    }

    // 开始下载
    public void startDownload() {
        try {
            // 提交所有下载任务到线程池
            for (int i = 0; i < THREAD_COUNT; i++) {
                final int threadId = i;
                executor.submit(() -> downloadChunk(threadId));
            }

            // 关闭线程池，不再接受新任务
            executor.shutdown();

            // 等待所有任务完成，设置超时时间
            boolean allCompleted = executor.awaitTermination(1, TimeUnit.MINUTES);

            if (allCompleted) {
                System.out.println("下载完成，开始文件合并...");
                mergeFiles();
                verifyResult();
                cleanup();
                System.out.println("所有操作完成!");
            } else {
                System.err.println("下载超时，强制关闭线程池");
                executor.shutdownNow();
            }

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("下载被中断");
            executor.shutdownNow();
        } catch (IOException e) {
            System.err.println("文件操作错误: " + e.getMessage());
            executor.shutdownNow();
        }
    }

    // 下载文件块（模拟下载）
    private void downloadChunk(int threadId) {
        DownloadRange range = ranges[threadId];
        String tempFileName = getTempFileName(threadId);

        try (RandomAccessFile file = new RandomAccessFile(tempFileName, "rw")) {
            // 模拟下载过程 - 生成随机数据
            Random random = new Random(threadId); // 使用线程ID作为种子保证可重现
            byte[] buffer = new byte[1024];
            int bytesWritten = 0;
            int chunkSize = range.getSize();

            while (bytesWritten < chunkSize) {
                int bytesToWrite = Math.min(buffer.length, chunkSize - bytesWritten);
                random.nextBytes(buffer);
                file.write(buffer, 0, bytesToWrite);
                bytesWritten += bytesToWrite;
            }

            System.out.printf("线程%d 下载完成: %s (大小: %d字节)%n",
                    threadId, tempFileName, new File(tempFileName).length());

        } catch (IOException e) {
            System.err.printf("线程%d 下载失败: %s%n", threadId, e.getMessage());
        }
    }

    // 合并临时文件
    private void mergeFiles() throws IOException {
        try (FileOutputStream finalFile = new FileOutputStream(FINAL_FILE)) {
            for (int i = 0; i < THREAD_COUNT; i++) {
                String tempFileName = getTempFileName(i);
                File tempFile = new File(tempFileName);

                if (!tempFile.exists()) {
                    System.err.println("临时文件不存在: " + tempFileName);
                    continue;
                }

                try (FileInputStream tempFileStream = new FileInputStream(tempFile)) {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = tempFileStream.read(buffer)) != -1) {
                        finalFile.write(buffer, 0, bytesRead);
                    }
                }
            }
        }
        System.out.println("临时文件合并完成: " + FINAL_FILE);
    }

    // 验证下载结果
    private void verifyResult() {
        File finalFile = new File(FINAL_FILE);
        if (!finalFile.exists()) {
            System.err.println("最终文件不存在");
            return;
        }

        long actualSize = finalFile.length();
        boolean success = actualSize == TOTAL_SIZE;
        System.out.printf("验证结果: 文件大小 %d/%d %s%n",
                actualSize, TOTAL_SIZE, success ? "✓" : "✗");

        if (!success) {
            System.err.println("文件大小不匹配！可能下载过程中出现错误。");
        }
    }

    // 清理临时文件
    private void cleanup() {
        System.out.println("清理临时文件...");
        int deletedCount = 0;

        for (int i = 0; i < THREAD_COUNT; i++) {
            File tempFile = new File(getTempFileName(i));
            if (tempFile.exists() && tempFile.delete()) {
                System.out.printf("删除临时文件: %s%n", tempFile.getName());
                deletedCount++;
            } else if (tempFile.exists()) {
                System.err.printf("无法删除临时文件: %s%n", tempFile.getName());
            }
        }

        System.out.printf("临时文件清理完成: 成功删除 %d/%d 个文件%n", deletedCount, THREAD_COUNT);
    }

    // 生成临时文件名
    private String getTempFileName(int threadId) {
        return "temp_part_" + threadId + ".dat";
    }

    // 下载范围内部类
    private static class DownloadRange {
        final int threadId;
        final int start;
        final int end;

        DownloadRange(int threadId, int start, int end) {
            this.threadId = threadId;
            this.start = start;
            this.end = end;
        }

        int getSize() {
            return end - start;
        }
    }

}
```