#include <iostream>
using namespace std;
template <class T>
int getArrayLen(T& array)      //return the lenght of array
{ 
 return (sizeof(array) / sizeof(array[0]));
}

int max_profit(int *price,int n){
	if (n==1)
		return 0;
  //Positive traversal£¬opt[i] repersent the max profit in day of price[0...i] by once transactions.
  int   *opt=new int[n];
  int ans=0;
  opt[0] = 0;
  int low = price[0];
  int curAns = 0;
  for(int i = 1; i<n; i++){
      if(price[i] < low) low = price[i];
      else if(curAns < price[i] - low) curAns = price[i] - low;
      opt[i] = curAns;
  }

  //Reverse traversal, optReverse[i] repersent the max profit in day of price[i...n] by once transactions.
  int   *optReverse=new int[n];
  optReverse[n - 1] = 0;
  curAns = 0;
  int high = price[n - 1];
  for(int i=n-2; i>=0; i--){
      if(price[i] > high) high = price[i];
      else if(curAns < high - price[i]) curAns = high - price[i];
      optReverse[i] = curAns;
  }

  //combine the max profit in price[0...i] and price[i...n], and find the max profit by twice transactions.
  for(int i=0; i<n; i++){
      int tmp = opt[i] + optReverse[i];
      if(ans < tmp) ans = tmp;
  }
  return ans;

}
int main(){

int price[]={5,2,1,4,3,1,2,9};
int n=getArrayLen(price);
cout<<"The Maximum profit is "<<max_profit(price,n)<<"."<<"\n";
return 0;
}