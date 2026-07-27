// #include <reg52.h>
// sfr P4   = 0xE8;
// sbit touch = P4^3;
// sbit led = P2^7;
// 
// void delay_ms(unsigned int xms)
// {
// 	unsigned int i, j;
// 	for(i=xms; i >0; i--)
// 	{
// 		for(j=124;j>0;j--)
// 		{}
// 	}
// }
// 
// void main()
// {
// 	while(1)
// 	{
// 		if(touch == 0)
// 		{
// 			delay_ms(100);
// 			if( touch != 0){
// 				led = ~led;
// 			}
// 		}
// 	}
// }