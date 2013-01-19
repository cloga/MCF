from __future__ import division
import random
import collections
def agg_dic(dic,key,value):
    if dic.has_key(key):
        dic[key]=[float(dic[key][0])+float(value[0]),float(dic[key][1])+float(value[1])]
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
    file=f.read()
lines=file.split('\n')[7:-3]
for line in lines:
    paths=line.split(',')[0].split(' > ')
##    print paths
    conversions=line.split(',')[1]
    values=line.split(',')[2][2:]
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
##print 'dic_f',dic_f
##print 'dic_l',dic_l
##print 'dic_ln',dic_ln
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
