#include <reg52.h>
sfr P4    = 0xe8;                   //for 89C5xRC/RD+ series and 90C5xRc/RD+, location at 0E8H
//sfr P4   = 0xc0;                  //for 90C5xAD series, location at 0C0H
sbit INT2 = P4^3;
sbit INT3 = P4^2;

sfr IPH = 0xB7;

sfr XICON = 0xc0;                   //for 89C5xRC/RD+ series and 90C5xRc/RD+, location at 0C0H
//sfr XICON = 0xe8;                 //for 90C5xAD series, location at 0E8H
sbit PX3  = XICON^7;
sbit EX3  = XICON^6;
sbit IE3  = XICON^5;
sbit IT3  = XICON^4;
sbit PX2  = XICON^3;
sbit EX2  = XICON^2;
sbit IE2  = XICON^1;
sbit IT2  = XICON^0;

sbit touch = P4^3;
sbit led = P2^7;
sbit led2 = P2^5;

void delay_ms(unsigned int xms)
{
	unsigned int i, j;
	for(i=xms; i >0; i--)
	{
		for(j=124;j>0;j--)
		{}
	}
}

// 外部中断INT0
void exit0() interrupt 0
{
	
}

// 外部中断INT2
void exit2() interrupt 6
{
	// 当按下按键灯切换
	led = ~led;
}

void main()
{
	IT0 = 1; // 运行中断0触发条件为下降沿
	EX0 = 1; // 使能中断INT0
	
	IT2 = 1; //设置中断触发条件为：下降沿
	EA = 1; // 允许所有中断经过；总中断使能
	EX2 = 2; // 允许中断2经过，EX2为IT2中断的允许控制器
	
	// 设置INT0中断的优先级为最低
	// PX0H = 0; // 这种无法编译通过，因为PXH是不可以·位寻址·的
	PX0 = 0;
	
	// 设置INT2中断优先级为最高
	// PX2H = 1; // 这种无法编译通过，因为PXH是不可以·位寻址·的
	PX2 = 1; 
	
	// IPH不可位寻址，所以只能通过IPH统一设置 PX0H和PX2H
	IPH = 0x40;
	while(1)
	{
		// P2.5一直闪烁，代表主程序在运行
		while(1) {
			delay_ms(300);
			led2 = ~led2;
		}
	}
}