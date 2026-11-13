# XAU/USD SMA55 V1.1 Strategy Desk

A read-only, mobile-friendly daily chart dashboard. **No order execution, no broker credentials, and no external price feed.**

## Current state (v0.1)

- Blue: daily closing price; orange: SMA55; green: 94–100% band of the **previous 100 completed sessions' highest close**.
- Import CSVs with `date,open,high,low,close` or MT4/MT5-style headers.
- Select a source and the last **completed** daily candle date. MT4 replaces MT5 proxy data on matching dates.
- Stores imported data in **the browser's localStorage only**; export it regularly. Different devices do **not** share data yet.
- Shows historical eligible entry/exit markers for visual research. **Not a validated MT4-reconciled backtest**.
- No live price feed, scheduled collection, persistent server database, GitHub Pages deployment, or MT4 terminal connection yet.

## Open locally

Open `index.html` in a browser, or serve this repository as a static website.

## CSV import

The importer accepts tab-, comma-, or semicolon-separated files with columns date/open/high/low/close. Dates should be YYYY-MM-DD or YYYY.MM.DD. **Daily candles only**; don't import hourly files. Use the date field to exclude the current incomplete day. Validate the broker's daily session boundaries before using MT5 proxy data.

## Locked strategy (do not change without approval)

- Long-only, daily, one trade at a time.
- Signal T: completed daily close crosses above SMA55 from at/below, and **T−1** close is within 6% of the previous 100 completed trading days' highest close.
- Wait two full trading days; confirm at T+2 close still above SMA55.
- Eligible entry at T+3 open; exit at the next daily open after a completed close below SMA55.
- Historical economics model: 40% equity margin allocation, 5% margin requirement, 6.5% annual financing /360, $0.10 per-side spread; **not connected to broker execution**.

## Next phases

1. Validate indicator and entry/exit signals candle-by-candle against Trade Nation MT4 and historical MT5 proxy.
2. Add an authenticated MT4 read-only export and durable server-side daily candle storage, including provisional-candle handling and session-boundary validation.
3. Add automated ingestion via GitHub Actions or a secure endpoint; GitHub Actions alone cannot pull data directly from a user's local MT4 terminal.
4. Configure web hosting, with appropriate access control if the repository or data should remain private.

Do not commit broker account credentials, tokens, or private keys to this repository.
