#coding:utf-8
import os
import jieba

def ff(dd):
    return dd[1]

def array2dic(arr):
    segdict={}
    for seg in arr:
        if len(seg)<2:
            continue
        if seg in segdict:
            segdict[seg]+=1
        else:
            segdict[seg]=1
    return segdict

novels=['douyuDanmu673327.txt']
freq=[]
for novel in novels:
    maotext=open(novel).read()
    seglist=jieba.cut(maotext)
    segdict=array2dic(seglist)

    c=1
    segsort=sorted(segdict.items(),key=ff,reverse=True)
    for item in segsort:
        #print(item[0]+'  '+str(item[1]))
        freq.append(item[0])
        if c==1500:
            break
        c+=1

freqdict=array2dic(freq)
freqsort=sorted(freqdict.items(),key=ff,reverse=True)
k=1
f=open('filter3.txt','w+')
for item in freqsort:
    if item[1]>3:
        f.write(item[0]+"  ")
    if k%5==0:
        f.write("\n")
    k+=1
f.close()
print('ok')