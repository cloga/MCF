from __future__ import division
import random
import collections
import csv
def agg_dic(dic,key,value):
    if dic.has_key(key):
        dic[key]=[dic[key][0]+value[0],dic[key][1]+value[1]]
    else:
        dic[key]=value
def output_dic(dic):
    for k in dic.keys():
##        print k,dic[k][0],dic[k][1]
        f.write('%s,%s,%s\n' % (k,dic[k][0],dic[k][1]))
    f.write('\n\n\n')

dic_f={}##first touch
dic_l={}##last touch
dic_ln={}##linear
with open ('mcf.csv') as f:
    lines=f.read().split('\n')[7:-3]
for line in lines:
    paths=line.split(',')[0].split(' > ')
    if len(line.split('","'))>1:#value & conversion>1000
        conversions=float(','.join(line.split(',')[1:]).split('","')[0].replace('"','').replace(',',''))
        values=float(','.join(line.split(',')[1:]).split('","')[1].replace('"','').replace(',','')[2:])
    elif len(str(line.split(',')[1]).split('"'))>1:#conversions>1000
        conversions=float(''.join(line.split(',')[1:-1]).replace('"',''))
        values=float(''.join(line.split(',')[-1]).replace('"','')[2:])
    elif len(str(line.split(',')[-1]).split('"'))>1:#value>1000
        conversions=float(''.join(line.split('"')[0].split(',')[1:]).replace('"',''))
        values=float(''.join(line.split(',')[2:]).replace('"','')[2:])
    else:
        conversions=float(''.join(line.split(',')[1:-1]).replace('"',''))
        values=float(''.join(line.split(',')[-1]).replace('"','')[2:])
    if len(paths)==1:
        channel=paths
        cov=[conversions,values]
        agg_dic(dic_f,channel[0],cov)
        agg_dic(dic_l,channel[0],cov)
        agg_dic(dic_ln,channel[0],cov)
    else:
        ##first touch
        channel=paths[0]
        cov=[conversions,values]
        agg_dic(dic_f,channel,cov)
        ##last touch
        channel=paths[-1]
        agg_dic(dic_l,channel,cov)
        ##linear
        channels_list=collections.Counter(paths).most_common()
        for c in channels_list:
            weight=c[1]/len(paths)
            cov=[float(conversions)*weight,float(values)*weight]
            agg_dic(dic_ln,c[0],cov)
output='mcf_result_'+str(random.randrange(1, 100000))+'.csv'
with open (output,'w') as f:
    f.write('-----first touch------\n')
    f.write('channel,conversions,value\n')
    output_dic(dic_f)
    f.write('-----last touch------\n')
    f.write('channel,conversions,value\n')
    output_dic(dic_l)
    f.write('-----linear------\n')
    f.write('channel,conversions,value\n')
    output_dic(dic_ln)
print 'output',output
