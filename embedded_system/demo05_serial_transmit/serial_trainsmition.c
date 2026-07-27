#include <reg52.h>

#define TIMS_10_MS (65536 - 9216) 

// 配置定时器
void Timer1() {
	TH1 = TIMS_10_MS
	TL1 = TIMS_10_MS >> 8;
}

void SendMsg() interrupt 3
{

}


void main()
{
	
	TMOD = 0x10; // 使用定时器1的模式1： 16位全用
	TR1 = 1; // 使用定时器1的计数功能
	
	// 使能定时器0的中断.  is in IE of SFR, and it's bit addressable
	ET0 = 1;
	// 使能总中断控制器
	EA = 1;
	
	// 8位UART, 波特率可变 ；每秒信号变化的次数（符号/秒）在串口通信（你图中的 USB-TTL）场景下，你可以直接把它理解为“每秒传输的位数（bit/s，即 bps
	SM0 = 0;
	SM1 = 1;
	
	Timer1(); // 开机后10ms后触发定时器中断
}