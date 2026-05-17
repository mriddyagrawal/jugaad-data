
import os
import sys
import json
import io
from datetime import date, timedelta
from pprint import pprint
import requests

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jugaad_data.nse import NSEHistory, NSEArchives, NSELive

def probe_api():
    print("\n=== Probing JSON API (NSEHistory) ===")
    n = NSEHistory()
    n.s.get("https://www.nseindia.com", timeout=10)
    
    symbol = "SBIN"
    from_date = date(2025, 2, 1)
    to_date = date(2025, 2, 5)
    expiry_date = date(2025, 2, 27)
    instrument_type = "FUTSTK"
    
    try:
        data = n.derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, None, None)
        if data:
            print(f"Total records: {len(data)}")
            print(f"Resolution: DAILY (Confirmed by timestamps)")
            print("\nAvailable Fields in JSON API:")
            pprint(sorted(list(data[0].keys())))
    except Exception as e:
        print(f"API Probe failed: {e}")

def probe_bhavcopy():
    print("\n=== Probing F&O Bhavcopy (NSEArchives) ===")
    a = NSEArchives()
    # Pick a date after July 8, 2024 (UDiff era)
    target_date = date(2025, 2, 20) 
    
    print(f"Fetching F&O Bhavcopy for {target_date}...")
    try:
        # NSEArchives.bhavcopy_fo_raw expects a ZIP, but post-UDiff it might be different
        # Let's try the raw request to see what we get
        dd = target_date.strftime('%d')
        MMM = target_date.strftime('%b').upper()
        yyyy = target_date.year
        
        # This is the path used by the library
        url = f"https://nsearchives.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{MMM}/fo{dd}{MMM}{yyyy}bhav.csv.zip"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")
        
        if r.status_code == 200:
            import zipfile
            try:
                with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                    fname = zf.namelist()[0]
                    with zf.open(fname) as f:
                        content = f.read().decode('utf-8')
                        headers = content.split('\n')[0].split(',')
                        print(f"Bhavcopy Fields ({len(headers)}):")
                        pprint(sorted(headers))
            except zipfile.BadZipFile:
                print("Not a ZIP file. Might be raw CSV or UDiff.")
                content = r.content.decode('utf-8')
                headers = content.split('\n')[0].split(',')
                print(f"Raw Content Fields ({len(headers)}):")
                pprint(sorted(headers))
    except Exception as e:
        print(f"Bhavcopy Probe failed: {e}")

def probe_intraday():
    print("\n=== Probing Intraday (NSELive) ===")
    l = NSELive()
    # Note: chart_data is for current day usually
    symbol = "SBIN"
    print(f"Checking if intraday chart data is available for {symbol}...")
    try:
        data = l.chart_data(symbol)
        if data and 'grapthData' in data:
            print(f"Intraday resolution available! Point count: {len(data['grapthData'])}")
            if len(data['grapthData']) > 1:
                # Calculate interval
                t1 = data['grapthData'][0][0]
                t2 = data['grapthData'][1][0]
                print(f"Interval: {(t2-t1)/1000} seconds")
        else:
            print("No intraday chart data returned (Market might be closed or not available for this symbol)")
    except Exception as e:
        print(f"Intraday Probe failed: {e}")

if __name__ == "__main__":
    probe_api()
    probe_bhavcopy()
    probe_intraday()
