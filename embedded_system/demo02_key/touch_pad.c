#include <reg52.h>

sbit touch = P 4^3;
sbit led = P2^7;

void delay_ms(unsigned int xms)
{
	unsigned int i, j;
	for(i=xms; i >0; i--)
	{
		for(j=124;j>0;j--)
		{}
	}
}

int main()
{
	while(1)
	{
		if(touch == 0)
		{
			delay_ms(100);
			if(touch != 0)
			{
				led = ~led;
			}
		}
	}
	return 0;
}