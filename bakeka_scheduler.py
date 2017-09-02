import re
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
from bs4 import BeautifulSoup as BS
import subprocess
import time

if __name__ == "__main__":
    while True:
        subprocess.call("bakeka_parser.py", shell=True)
        subprocess.call("bakeka_mailer.py", shell=True)
        time.sleep(3600)
