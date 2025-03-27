// program for systematic investment plan calculator
#include<iostream.h>
#include<conio.h>
#include<math.h>

class investment
{
  public:
  int minvestment;
  float annualinterestrate;
  int tenure;

  void getinvestmentdetails()
  {
    cout<<"enter sip amount\n";
    cin>>minvestment;
    cout<<"enter annual interest interest rate\n";
    cin>>annualinterestrate;
    cout<<"enter the tenure (years)\n";
    cin>>tenure;

  }
};
class SIPcalculator: public investment
{
  public:
  void calculatefuturevalue()
  {
    float monthlyrate=annualinterestrate/(12*100);

    int totalmonths= tenure*12;

    float futurevalue=minvestment*((pow(1+monthlyrate,totalmonths)-1)/
	  monthlyrate)*(1+monthlyrate);

   cout<<"future value of sip = Rs. "<<futurevalue;

  }
};
void main()
{
  SIPcalculator obj;
  clrscr();
  obj.getinvestmentdetails();
  obj.calculatefuturevalue();
  getch();
}
