__author__ = 'erenaslangiray'

import os
import clusters
import re

uncounted_words=['a','an','the','on','and','of','or','in','to','for','about']

def datacheck():
    all_data_list=os.listdir('Dataset')
    big_dict={}
    field_list=['teaser','coordinator']
    for data in all_data_list:
        data1=open("Dataset\\%s" % (data),'r+')
        data_text=data1.read().replace('\n',"")
        teaser=re.search('teaser>.*</teaser',data_text).group()[7:-8]
        coordinator=re.search('legalName>.*</legalName',data_text).group()[10:-11]
        if len (str(coordinator))>200:
            coordinator=re.search('.*</legalName',str(coordinator)[:200]).group()[:-11]
        big_dict.setdefault(data,{})
        big_dict[data]['teaser']=teaser
        big_dict[data]['coordinator']=coordinator
    data_write=open('data_clusters.txt','w+')
    word_list=[]
    writing_dict={}
    for data in big_dict:
        writing_dict.setdefault(data,{})
        word_count={}
        for field in field_list:
            line_words=big_dict[data][field].split()
            for word in line_words:
                if word not in word_list and re.match('\w+',word)!=None and word not in uncounted_words and len(word)>2 and re.match('\D+',word)!=None:
                    word_list.append(word.lower())
                if word not in word_count:
                    word_count[word.lower()]=1
                if word in word_count:
                    word_count[word.lower()]+=1
        writing_dict[data]=word_count
    data_write.write('Project-Name')
    for word in word_list:
        data_write.write('\t%s' % (word))
    for data in writing_dict:
        data_write.write('\n%s' % (data))
        for word in word_list:
            if word in writing_dict[data]:
                data_write.write('\t%s' % (writing_dict[data][word]))
            if word not in writing_dict[data]:
                data_write.write('\t0')

datacheck()
pointnames,coordinates,data=clusters.readfile('data_clusters.txt')
clust=clusters.hcluster(data)
clusters.printclust(clust,labels=pointnames,n=15)
clusters.drawdendrogram(clust,labels=pointnames,jpeg='hclusters.jpg')