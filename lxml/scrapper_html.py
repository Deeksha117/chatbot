import requests
from lxml import html

parent=''
seedurls = ['http://www.holidayiq.com/destinations/']
#seedurls = ['http://www.holidayiq.com/states/karnataka/']
crawl_seq = [["states"],["destinations"],['How-To-Reach','Sightseeing']]
#crawl_seq = [['How-To-Reach','Sightseeing']]

def html_links(urls,i):
   f =  open(str(i),"a+")
   pageurls = []
   for url in urls:
   	print "url",url
	if(url[-1]!="/"):
		continue
	#creating lxml tree from response body
	response = requests.get(url)
	tree = html.fromstring(response.text)
	#Finding all anchor tags in response
	#print tree.xpath('//div//a/@href')[100:-70]
	for link in tree.xpath('//div//a/@href')[100:-70]:
		#print link
		if not link.startswith('http'):
			link = url+link
		#print link.split('/')[-3]
		for seq in crawl_seq[i]:
			#print "matching",link,seq
			#if (link.find(seq,25)>-1):
			lst = link.split('/')
			if lst[3].find(seq)>-1 and (len(lst[-1])==0 or i==2):
				print link
				#f.write(link)
				#f.write("\n")
				pageurls.append(link)
				break
			
   #print pageurls
   #f.close()
   return set(pageurls)


#storing response
print seedurls
i = 0
while(1):
	f =  open(str(i),"a+")
	temp = html_links(seedurls,i)
	seedurls = temp
	print seedurls
	for url in seedurls:
		f.write(str(url))
		f.write("\n")
	i = i+1
	f.close()
	if i==3:
		break	
f.close()
