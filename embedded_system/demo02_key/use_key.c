#include <reg52.h>
sbit led1 = P2^7;

void delay_ms(unsigned int xms)
{
	unsigned int i, j;
	for(i=xms; i >0; i--)
	{
		for(j=124;j>0;j--)
		{}
	}
}

void main() {
	
	while(1) {
		if ( ((0x80) & P3) == 0 ) {
			delay_ms(100);
			if( ((0x80) & P3) != 0 ){
				led1 = ~led1;
			}
			
		}
	}
}