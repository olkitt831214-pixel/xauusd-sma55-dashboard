"""Read-only MT4 -> GitHub candle synchronizer.
Requires Python 3.10+. Environment variables:
GITHUB_TOKEN: fine-grained token scoped ONLY to this repository, Contents read/write.
MT4_COMMON_FILES: MetaTrader terminal common Files directory.
Never commit your token or credentials. No orders are placed.
"""
import base64, csv, io, json, os, pathlib, time, urllib.request, urllib.error
from datetime import datetime, timezone

REPO="olkitt831214-pixel/xauusd-sma55-dashboard"
API=f"https://api.github.com/repos/{REPO}/contents/data/daily.json"
TOKEN=os.environ.get("GITHUB_TOKEN","")
SOURCE=pathlib.Path(os.environ.get("MT4_COMMON_FILES",""))/"sma55_mt4_daily.csv"
INTERVAL=int(os.environ.get("SYNC_INTERVAL_SECONDS","300"))
def github(method="GET", payload=None):
    req=urllib.request.Request(API,method=method,headers={
      "Authorization":f"Bearer {TOKEN}","Accept":"application/vnd.github+json",
      "X-GitHub-Api-Version":"2022-11-28","User-Agent":"sma55-readonly-bridge",
      **({"Content-Type":"application/json"} if payload is not None else {})
    },data=json.dumps(payload).encode() if payload is not None else None)
    try:
        with urllib.request.urlopen(req,timeout=25) as response:return json.load(response)
    except urllib.error.HTTPError as e:
        if method=="GET" and e.code==404:return None
        raise
def read_mt4():
    rows=[]
    with SOURCE.open(newline="",encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            try:
                d=r["date"].replace(".","-")
                datetime.strptime(d,"%Y-%m-%d")
                x={k:float(r[k]) for k in ("open","high","low","close")}
                if not all(map(lambda v: v>0,x.values())):continue
                if x["high"]<max(x["open"],x["close"],x["low"]) or x["low"]>min(x.values()):continue
                rows.append({"date":d,**x,"source":"MT4","complete":r.get("complete")=="1"})
            except (KeyError,ValueError):continue
    return sorted(rows,key=lambda x:x["date"])
def sync():
    rows=read_mt4()
    if not rows:print("No MT4 candles available",flush=True);return
    remote=github()
    old=json.loads(base64.b64decode(remote["content"])) if remote else {"completed":[],"provisional":None}
    bydate={x["date"]:x for x in old.get("completed",[]) if x.get("source") in ("MT4","MT5_PROXY")}
    provisional=None
    for x in rows:
        if x["complete"]:bydate[x["date"]]=x
        else:provisional=x
    completed=sorted(bydate.values(),key=lambda x:x["date"])
    new={"schema":1,"symbol":"XAUUSD..","completed":completed,"provisional":provisional}
    if old.get("completed")==completed and old.get("provisional")==provisional:
        print("No changes",flush=True);return
    body={"message":"Update read-only MT4 daily candles","content":base64.b64encode((json.dumps(new,separators=(",",":"))+"\n").encode()).decode()}
    if remote:body["sha"]=remote["sha"]
    github("PUT",body)
    print(f"Synced {len(completed)} completed candles; provisional {bool(provisional)}",flush=True)
def main():
    if not TOKEN:raise SystemExit("Set GITHUB_TOKEN in your local environment; never put it in the repository")
    if not os.environ.get("MT4_COMMON_FILES"):raise SystemExit("Set MT4_COMMON_FILES to MetaTrader Common/Files folder")
    while True:
        try:sync()
        except (OSError,ValueError,urllib.error.URLError) as exc:print(f"Sync issue: {exc}",flush=True)
        time.sleep(max(60,INTERVAL))
if __name__=="__main__":main()
