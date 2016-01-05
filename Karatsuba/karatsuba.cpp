#include <iostream>
#include <math.h>
using namespace std;

int size_base10(long num)
{
	int m=1;
	while(num/10!=0)
	{
		m++;
		num=num/10;
	}
	return m;
}
 
int pow10(int m)
{
	int pow10=1;
	for(int i=0;i<m;i++)
	{
		
		pow10=pow10*10;
	}
	return pow10;
}
long gethigh(long num, int m)
{
	long high=num/pow10(m);
	return high;
}

long getlow(long num, int m)
{
	long low=num%pow10(m);
	return low;
}

long karatsuba(long num1,long num2)
{
	if(num1<10||num2<10)
		return num1*num2;
	
	int m=max(size_base10(num1),size_base10(num2));
	int m2=m/2;
	long high1=gethigh(num1,m2);
	long high2=gethigh(num2,m2);
	long low1=getlow(num1,m2);
	long low2=getlow(num2,m2);
	long z0=karatsuba(low1,low2);
	long z1=karatsuba((low1+high1),(low2+high2));
	long z2=karatsuba(high1,high2);
	return z2*pow10(2*m2)+(z1-z2-z0)*pow10(m2)+z0;
}
int main()
{
cout<<karatsuba(12345,12345);
return 0;
}

