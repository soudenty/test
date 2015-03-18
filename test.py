import re
import urllib
import urllib2
from urllib2 import Request, urlopen, URLError
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
import MySQLdb
import tw_get_freport

ifrs_dic = {}
ifrs_bsci_title_dic = {}
ifrs_bsci_dic = {}
ifrs_scf_dic = {}





print "loading ifrs labels..."

tree = ET.parse('lab_ifrs-zh-tw_2010-04-30.xml')
root = tree.getroot()
#print ET.dump(tree1)

for child in root.iter('{http://www.xbrl.org/2003/linkbase}label'):
    try:
        if(child.get('{http://www.w3.org/XML/1998/namespace}lang') == 'zh-tw'):
           #print "Tag: "
           #print child.tag
           #print child.get('id').split('_')[1]
           #print child.text.encode('utf-8')
           ifrs_dic[child.get('id').split('_')[1]] = child.text.encode('utf-8')
    except Exception as e:
      print e

print "finished!!"



print "loading bsci-ci labels..."

tree = ET.parse('tifrs-bsci-ci-2014-03-31-label.xml')
root = tree.getroot()

# create a dictionary that stores mapping from title label to bsci-ci label
for child in root.iter('{http://www.xbrl.org/2003/linkbase}loc'):
    try:
            ifrs_bsci_title_dic[child.get('{http://www.w3.org/1999/xlink}title')] = \
                child.get('{http://www.w3.org/1999/xlink}href').split('#')[1].split('_')[1]
    except Exception as e:
        print e
                   
for child in root.iter('{http://www.xbrl.org/2003/linkbase}label'):
    try:
        if(child.get('{http://www.w3.org/XML/1998/namespace}lang') == 'zh-tw'):
           #print "Tag: "
           #print child.get('id').split('_')[1]
           #print child.text.encode('utf-8')
           #print child.attrib
           #print "Search: "
           #print child.get('id').split('_')[1]
           
           #tt = root.findall(
           #      ".//{http://www.xbrl.org/2003/linkbase}loc[@{http://www.w3.org/1999/xlink}title='"
           #      + child.get('id').split('_')[1] + "']"
           #      )[0].get('{http://www.w3.org/1999/xlink}href').split('#')[1].split('_')[1]
        
           #ifrs_bsci_dic[child.get('id').split('_')[1]] = child.text.encode('utf-8')
           tt = ifrs_bsci_title_dic[child.get('id').split('_')[1]]
           ifrs_bsci_dic[tt] = child.text.encode('utf-8')
    except Exception as e:
        print e

print "finished!!"


print "loading scf..."

tree = ET.parse('tifrs-scf-2014-03-31-label.xml')
root = tree.getroot()

for child in root.iter('{http://www.xbrl.org/2003/linkbase}label'):
    try:
        if(child.get('{http://www.w3.org/XML/1998/namespace}lang') == 'zh-tw'):
            ifrs_scf_dic[child.get('id').split('_')[1]] = child.text.encode('utf-8')
    except Exception as e:
        print e

print "finished!!"



"""
for key, value in ifrs_scf_dic.items():
     print "( " + key + ", " + value + " )"
"""

"""
#text = 'http://xbrl.iasb.org/taxonomy/2010-04-30/ifrs'
#text ='http://www.xbrl.org/tifrs/bsci/ci/2013-03-31'
#text = 'http://www.xbrl.org/tifrs/scf/ci/2013-03-31'
if(re.search('.*/ifrs' ,text)):
    match = re.search('.*/ifrs' ,text)
    print match.group()
        elif(re.search('.*/bsci/ci/.*', text)):
match =re.match('.*/bsci/ci/.*', text)
    print match.group()
        elif(re.search('/scf/[^ci]+', text)):
match = re.search('/scf/[^ci]+', text)
    print match.group()
        elif(re.search('/scf/ci/', text)):
match = re.search('/scf/ci/', text)
    print match.group()
        elif(re.search('/ar/', text)):
match = re.search('/ar/', text)
    print match.group()
        elif(re.search('/es/[^cr]+', text)):
match = re.search('/es/[^cr]+', text)
    print match.group()
        elif(re.search('/es/cr', text)):
match = re.search('/es/cr', text)
    print match.group()
        elif(re.search('/notes/[^ci]+', text)):
match = re.search('/notes/[^ci]+', text)
    print match.group()
        elif(re.search('/notes/ci/', text)):
match = re.search('/notes/ci/', text)
    print match.group()
        else:
print "does not match"
"""



print "\n\n"





try:
   
 selected_symbol = 6207;
 selected_year = 2013;
 selected_quarter = 1;
 
 if(selected_quarter == 1):
   search_string = str(selected_year) + "0331"
 elif(selected_quarter ==2):
   search_string = str(selected_year) + "0630"
 elif(selected_quarter ==3):
   search_string = str(selected_year) + "0930"
 else:
   search_string = str(selected_year) + "1231"
 
 url = 'http://mops.twse.com.tw/server-java/FileDownLoad'
 values = {
          'step' : '9',
          'functionName': 't164sb01',
          'report_id': 'C',
          'co_id' :  selected_symbol,
          'year': selected_year,
          'season': selected_quarter

 }

 headers = { 'Content-Type' :'application/x-www-form-urlencoded',
             'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

 data = urllib.urlencode(values)
 print data
 #data = data.encode('utf-8') # data should be bytes
 req = urllib2.Request(url, data, headers)
 response = urllib2.urlopen(req)
 the_page = response.read()


 root = ET.fromstring(the_page)

 tag = ""
 pp = []
 ch_name = ""
 equity_count = 0
 pnl_b_tqx_count = 0
 target_table = "TW_BalanceSheet"


