#include <reg52.h>
// Keil C51不是标准C语言，它是针对8051单片机设计的C语言扩展。
// 注意，这里的 ^ 不是“平方”或“异或”！在Keil C51的sbit语法中，
// ^ 是“位选取”符号。P2^5 的意思就是：从P2这个端口（一个字节）里，选出第5号引脚（也就是第6个引脚，因为从0开始）。
sbit led = P2^7;

//带参延时函数
void delay_ms(unsigned int xms)   //@12MHz
{
    unsigned int i, j;
    for(i=xms;i>0;i--)
    {
        for(j=124;j>0;j--)
        {}
    }
}

void main()
{
    while(1)
    {
			led = 0;
			delay_ms(500);
			led = 1;
			delay_ms(500);
    }
}