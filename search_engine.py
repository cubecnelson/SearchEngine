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

def compute_ranks(graph):
	d=0.8
	numloops=10
	ranks={}
	npages=len(graph)
	for page in graph:
		ranks[page]=1.0/npages
	for i in range(0,numloops):
		newranks={}
		for page in graph:
			newrank=(1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank=newrank+d*ranks[node]/len(graph[node])
			newranks[page]=newrank
		ranks=newranks
	return ranks
	
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





def QuickSort(pages,ranks):
	if len(pages)>1:
		piv=ranks[pages[0]]
		i=1
		j=1
		for j in range(1,len(pages)):
			if ranks[pages[j]]>piv:
				pages[i],pages[j]=pages[j],pages[i]
				i+=1
		pages[i-1],pages[0]=pages[0],pages[i-1]
		QuickSort(pages[1:i],ranks)
		QuickSort(pages[i+1:len(pages)],ranks)

def Look_up_new(index,ranks,keyword):
	pages=Look_up(index,keyword)
	print '\nPrinting the results as is with page rank\n'
	for i in pages:
		print i+" --> "+str(ranks[i])
	QuickSort(pages,ranks)
	print "\nAfter Sorting the results by page rank\n"
	it=0
	for i in pages:
		it+=1
		print str(it)+'.\t'+i+'\n' 


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

ranks=compute_ranks(graph)
Look_up_new(index,ranks,search_term)
		