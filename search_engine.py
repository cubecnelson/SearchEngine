import urllib
max_limit=5
def get_page(url):
	try:
		f = urllib.urlopen(url)
		page = f.read()
		f.close()
		return page
	except:	
		return ""
	return ""

def union(a,b):
	for e in b:
		if e not in a:
			a.append(e)

def get_next_url(page):
	start_link=page.find("a href")
	if(start_link==-1):
		return None,0
	start_quote=page.find('"',start_link)
	end_quote=page.find('"',start_quote+1)
	url=page[start_quote+1:end_quote]
	return url,end_quote

def get_all_links(page):
	links=[]
	while(True):
		url,n=get_next_url(page)
		page=page[n:]
		if url:
			links.append(url)
		else:
			break
	return links
def Look_up(index,keyword):
	if keyword in index:
		return index[keyword]
	return []
def add_to_index(index,url,keyword):

	if keyword in index:
		if url not in index[keyword]:
			index[keyword].append(url)
		return
	index[keyword]=[url]
def add_page_to_index(index,url,content):
	for i in content.split():
		add_to_index(index,url,i)

	
def Crawl_web(seed):
	tocrawl=[seed]
	crawled=[]
	index={}
	graph={}#new graph
	global max_limit
	while tocrawl:
		p=tocrawl.pop()
		if p not in crawled:
			print p
			max_limit-=1
			print max_limit
			if max_limit<=0:
				break
			c=get_page(p)
			add_page_to_index(index,p,c)
			f=get_all_links(c)
			union(tocrawl,f)
			graph[p]=f
			crawled.append(p)
	return crawled,index,graph




#print index
print "Enter the seed page"
seed_page=raw_input()
print "Enter What you want to search"
search_term=raw_input()
try:
	print "Enter the depth you wanna go"
	max_limit=int(raw_input())
except:
	f=None
print '\nStarted crawling, presently at depth..'
crawled,index,graph=Crawl_web(seed_page)

		