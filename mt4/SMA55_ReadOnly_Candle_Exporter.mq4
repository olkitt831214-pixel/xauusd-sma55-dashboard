// SMA55_ReadOnly_Candle_Exporter.mq4
// Attach to Trade Nation XAUUSD.. D1. NEVER sends orders.
#property strict
input int ExportEverySeconds=60;
input int HistoryBars=4000;
input string ExportFilename="sma55_mt4_daily.csv";
int OnInit(){EventSetTimer(MathMax(10,ExportEverySeconds));Export();Print("SMA55 read-only candle export started");return(INIT_SUCCEEDED);}
void OnDeinit(const int reason){EventKillTimer();}
void OnTimer(){Export();}
void OnTick(){} // no trading logic
void Export(){
 if(Period()!=PERIOD_D1 || StringFind(Symbol(),"XAU")<0){Print("SMA55 exporter: attach to XAUUSD daily chart");return;}
 int count=iBars(Symbol(),PERIOD_D1);if(count<2)return;
 int file=FileOpen(ExportFilename,FILE_CSV|FILE_WRITE|FILE_COMMON,',');
 if(file==INVALID_HANDLE){Print("SMA55 exporter: FileOpen failed ",GetLastError());return;}
 FileWrite(file,"date","open","high","low","close","complete","source");
 int n=MathMin(count-1,HistoryBars);
 for(int i=n;i>=0;i--){
  datetime t=iTime(Symbol(),PERIOD_D1,i);
  if(t<=0)continue;
  FileWrite(file,TimeToString(t,TIME_DATE),DoubleToString(iOpen(Symbol(),PERIOD_D1,i),Digits),
    DoubleToString(iHigh(Symbol(),PERIOD_D1,i),Digits),DoubleToString(iLow(Symbol(),PERIOD_D1,i),Digits),
    DoubleToString(iClose(Symbol(),PERIOD_D1,i),Digits),i==0?"0":"1","MT4");
 }
 FileClose(file);
}
