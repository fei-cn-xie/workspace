#include <reg52.h>

#define TIMS_10_MS (65536 - 9216) 
#define TIMS_100_MS (65536 - 92160)  // 溢出

sbit led1 = P2^7;

void Timer_10ms(){
	// rest_TL0_TL1
	// 10ms = 65536 - 9216
	// TL0 = 0x00 // 低八位
	// TH0 = 0xDC // 高八位
	// 对TL预装载值，当值超过16位标识范围，TF0被置1，触发CPU中断后TF0置0
	TL0 = TIMS_10_MS;
	TH0 = TIMS_10_MS >> 8;
}
void Timer_100ms(){
	// rest_TL0_TL1
	// 对TL预装载值，当值超过16位标识范围，TF0被置1，触发CPU中断后TF0置0
	TL0 = TIMS_100_MS;
	TH0 = TIMS_100_MS >> 8;
}
int count = 0;

void timer0_Interrupt() interrupt 1
{
	count++;
	
	if(count == 100) {
		led1 = ~led1;
		count = 0;
	}
	Timer_10ms();

}



void main()
{
	// 设置TMOD 定时器模式寄存器
	// 设置定时器模式为模式1，M1 = 0(位0x01), M0 = 1(位0x02); TL0, TH0全用（定时器/计数器0）
	// 设置 TR0(TOCN 位0x10) 【可位寻址的】 并且 TMOD【不可位寻址的】的 INT0 或GATE(0x08)为0 - （定时器/计数器0）
	TR0 = 1;
	TMOD = 0x01; 
	

	
	// 使能定时器0的中断.  is in IE of SFR, and it's bit addressable
	ET0 = 1;
	// 使能总中断控制器
	EA = 1;
	Timer_10ms();
	
	while(1) {
	}
	
}