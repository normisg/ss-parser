import time
import threading
from parser_main import run_parser
from config import PARSE_INTERVAL_MINUTES

def main():
    while True:
        print("Running parser...")
        run_parser()
        print(f"Sleeping for {PARSE_INTERVAL_MINUTES} minutes...")
        time.sleep(PARSE_INTERVAL_MINUTES * 60)

def run_api():
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)

def run_all():
    parser_thread = threading.Thread(target=main, daemon=True)
    api_thread = threading.Thread(target=run_api, daemon=True)
    parser_thread.start()
    api_thread.start()
    parser_thread.join()
    api_thread.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api()
    else:
        run_all()