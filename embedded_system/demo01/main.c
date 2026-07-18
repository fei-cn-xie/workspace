#include <reg52.h>
#include <intrins.h>

// P2.5 (0x20), P2.6 (0x40), P2.7 (0x80)
// Keil C51不是标准C语言，它是针对8051单片机设计的C语言扩展。
// 注意，这里的 ^ 不是“平方”或“异或”！在Keil C51的sbit语法中，
// ^ 是“位选取”符号。P2^5 的意思就是：从P2这个端口（一个字节）里，选出第5号引脚（也就是第6个引脚，因为从0开始）。
// sbit led1 = P2^5; 
// sbit led2 = P2^6;
// sbit led3 = P2^7;

typedef unsigned char UCHAR;

void Delay1000ms()		//@11.0592MHz
{
	unsigned char i, j, k;

	_nop_();
	i = 8;
	j = 1;
	k = 243;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}

void Delay300ms()		//@11.0592MHz
{
	unsigned char i, j, k;

	_nop_();
	i = 3;
	j = 26;
	k = 223;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}

void Delay50ms()		//@11.0592MHz
{
	unsigned char i, j;

	i = 90;
	j = 163;
	do
	{
		while (--j);
	} while (--i);
}

void Delay100ms()		//@11.0592MHz
{
	unsigned char i, j;

	i = 180;
	j = 73;
	do
	{
		while (--j);
	} while (--i);
}

void main()
{
		UCHAR mask;
		int i;
    while(1)
    {
			for (i = 0; i < 3; i++){
				mask = 0x20 << i; // 0x20 P5, 0x40 P6, 0x80 P7
	
				P2 = P2 & ~mask; // 亮
				Delay100ms();
				P2 = P2 | mask; // 灭
				Delay100ms();
			}
    }
}