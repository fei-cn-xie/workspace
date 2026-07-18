> C语言51单片机STM32 HAL库入门到项目实战 单片机嵌入式入门必备教程
> 课程：https://www.bilibili.com/video/BV1C4421U7c2  
> 资料：https://x509p6c8to.feishu.cn/wiki/C5HHw0MqOii1d8kdziFcu1TlnJg  

## 基础
### Keil搭建51工程

根据芯片的类型选择创建启动代码文件  
`embedded_system\demo01\STARTUP.A51`
> `STARTUP.A51` 是 Keil C51 编译器为 51 单片机提供的一个启动代码文件。它是一个用 A51 汇编语言编写的源文件，在单片机上电或复位后，在用户程序的 main() 函数之前执行，其主要任务是为 C 语言程序的运行搭建好环境  
> `main.c`开发程序入口  
> `Objects\demo01.hex`通过main.c编译生成的，需要烧录到开发板的固件  


### 固件烧录

- 接线
  - 连接电源线
  - 连接数据线，查看COM口（如果没有驱动需要安装驱动）
- 烧录
  - 电脑安装烧录工具`STC-ISP`
  - 选择芯片型号`STC89C52RC/LE52RC` (FYI：STC89C52RC和STC89LE52RC两款芯片是完全兼容的)
  - 根据设备，选择COM口
  - 选择通过`main.c`编译好的`demo01.hex`烧录
- 运行