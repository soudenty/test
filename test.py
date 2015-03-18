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


 print 'Balance Sheet --------------------'


 db = MySQLdb.connect("114.34.172.50","sedifer","1qaz@WSX","Finance", 3306)
 cursor = db.cursor()
 #sql = "update TW_BalanceSheet set title_ch = 'ASD' where stkNo = 1 and year =1 and quarter = 1 and title_en = 'aaa'"
 #sql = "INSERT INTO TW_BalanceSheet (stkNo, year, quarter, title_en, title_ch, value) VALUES (9910, 2014, 3, 'aaa', 'bbb', 12.12)"
 #sql = "call TW_AddFStatementValue('TW_BalanceSheet', 'CashAndCashEquivalents', 'abc', 1828755.000000, 9910, 2014, 3)"

 if(root.tag == 'PRE'):
     print "Cannot download the file"


 for child in root:
     try:
       
       if(child.attrib.has_key('decimals')):
           
          if(not re.search(search_string, child.get('contextRef'))):
               continue
          if(re.search('Member', child.get('contextRef'))):
               break
          
          """
          if(tag == child.tag.split("}")[1]):
               continue
          """
       
          tag = child.tag.split("}")[1]
          if(tag == "Year" or tag == "Quarter" or tag == "ReportType" or
             tag == "ReportCategory" or tag == "Market" or tag == "IndustrySector"):
               continue
     
          print child.get('contextRef')
     
          """
          if(tag == "Equity"):   # This is only Equity. If the second Equity appears, we just leave
             equity_count += 1
             if(re.search('Member', child.get('contextRef'))):
                print child.get('contextRef')
                break
             #if(equity_count > 1):
                #print child.get('contextRef')
                #break
          """
          
          #print "Tag: "
          pp = child.tag.split("}")
          pp[0] = pp[0][1:]
          #print pp

          """
          if(pp[1] == 'OperatingRevenue'):
             target_table = "TW_IncomeStatement"
              print "Income Statement --------------------"

          if(pp[1] == 'ProfitLossBeforeTax'):
             pnl_b_tqx_count += 1

          if(pnl_b_tqx_count == 2 and pp[1] == 'ProfitLossBeforeTax'):
             target_table = "TW_CashFlowStatement"
             print "Cash Flow Statement --------------------"
          """

          """
          if(pp[0] == 'http://xbrl.iasb.org/taxonomy/2010-04-30/ifrs'):
             print ifrs_dic[pp[1]]
          elif(pp[0] == 'http://www.xbrl.org/tifrs/bsci/ci/2013-03-31'):
             print ifrs_bsci_dic[pp[1]]
          elif(pp[0] == 'http://www.xbrl.org/tifrs/scf/2013-03-31'):
             print ifrs_scf_dic[pp[1]]
          else:
             print "cannot find corresponding IFRS table"
          """
          
          if(re.search('.*/ifrs' ,pp[0])):
             ch_name = ifrs_dic[pp[1]]
             print ch_name
          elif(re.search('.*/bsci/ci/.*', pp[0])):
             ch_name = ifrs_bsci_dic[pp[1]]
             print ch_name
          elif(re.search('/scf/[^ci]+', pp[0])):
             ch_name = ifrs_scf_dic[pp[1]]
             print ch_name
          else:
             ch_name = ""
             print "cannot find corresponding IFRS table"

          
          
          #print " ---"
          #print child.attrib
          value = float(child.text) * 10 ** int(child.attrib['decimals'])
          print value
          
          if(ch_name != ""):
           sql = "call TW_AddFStatementValue('%s', '%s', '%s', %f, %d, %d, %d)" % \
                   ('TW_FinancialReport', pp[1], ch_name, value, selected_symbol, selected_year, selected_quarter)
           #print sql
           cursor = db.cursor()
           cursor.execute(sql)
           cursor.close()
     except Exception as e :
       print e



except URLError as e:
 if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
 elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
 else:
        print 'everything is fine'

db.commit()
db.close()

