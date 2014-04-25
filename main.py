import requests

form_data = "orderBy=Cost&anSide=Corp&filterText=&fTS=fulltext&filterUnique=Any&anarchFB=Anarch&criminalFB=Criminal&haas-bioroidFB=Haas-Bioroid&jintekiFB=Jinteki&nbnFB=NBN&shaperFB=Shaper&theweylandconsortiumFB=The%20Weyland%20Consortium&neutralFB=Neutral&filterType=Agenda&filterSet=0&operatorCost=e&filterCost=Any&operatorLoyalty=e&filterLoyalty=Any&operatorStr=e&filterStr=Any&operatorMU=e&filterMU=Any&operatorAP=e&filterAP=3&fSet=&fPage=cardsearch&md5check=7c0d024567ed8ff0d2ef3231f3d80de7"

url = "http://www.cardgamedb.com/forums/index.php?s=0ad95973a7f6f2d27d44d8d011089d6b&app=ccs&module=ajax&section=andeckbuilder&do=search"

headers = {
    "Host": "www.cardgamedb.com",
    "Connection": "keep-alive",
    "Content-Length": "483",
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "X-Prototype-Version": "1.7",
    "Origin": "http://www.cardgamedb.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://www.cardgamedb.com/index.php/netrunner/android-netrunner-card-search",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Cookie": "member_id=25479; coppa=0; rteStatus=rte; pass_hash=3c1c06b573ccc111387ee2f81b7d4352; session_id=0ad95973a7f6f2d27d44d8d011089d6b",
}
"""POST /forums/index.php?s=0ad95973a7f6f2d27d44d8d011089d6b&app=ccs&module=ajax&section=andeckbuilder&do=search HTTP/1.1
"""

r = requests.post(url, data=form_data, headers=headers)

print r.text
