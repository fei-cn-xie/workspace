> C语言51单片机STM32 HAL库入门到项目实战 单片机嵌入式入门必备教程
> https://www.bilibili.com/video/BV1C4421U7c2?spm_id_from=333.788.player.switch&vd_source=3e149ab79eab845696a34aa43635df76&p=39


## 基础
### Keil搭建51工程

根据芯片的类型选择创建启动代码文件  
`embedded_system\demo01\STARTUP.A51`
> STARTUP.A51 是 Keil C51 编译器为 51 单片机提供的一个启动代码文件。它是一个用 A51 汇编语言编写的源文件，在单片机上电或复位后，在用户程序的 main() 函数之前执行，其主要任务是为 C 语言程序的运行搭建好环境
