# -- coding:utf-8 --

# !~/anaconda3/bin/python3



import pandas as pd

from collections import defaultdict

import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt



def dictify_ownership(dataframe):

    """

    convert data format from pd.DataFrame to dict

    :param dataframe:

    :return:

    {

        company1: {

            time1: {

                    name1:(ratio,type),

                    name2:(...),

                    ...

                    }

            time2: {...}

        }

        company2:

        {

            ...

        }

    }

    """

    data = defaultdict(dict)

    companies = set()



    for idx, row in dataframe.iterrows():

        company = row['company_name']

        companies.add(company)

        

        time = row['report_date']

        

        name = row['shareholder_name']

        ratio = row['invest_ratio']

        type_ = row['idtype']

        shareholder = (ratio,type_)

        

        if time not in data[company]:

            data[company][time] = dict()

            if name not in data[company][time]:

                data[company][time][name] = shareholder

        else:

            if name not in data[company][time]:

                data[company][time][name] = shareholder



    return data, companies



def ownershipRatio(data,companies):

    """

    ownership_Aratio: biggest shareholder ratio

    ownership_Bratio: the sum of (2nd,3rd,4th) shareholder ratio

    """

    ownership_Aratio = list()

    ownership_Bratio = list()

    time_latest = list()

    

    for company in companies:

        time = list()

        for key in data[company]:

            time.append(key)

            

        time_sorted = sorted(time,reverse=True)

        time_latest.append(time_sorted[0])

        

        ownership = list() 

        for value in data[company][time_sorted[0]].values():

            ownership.append(value)                

        

        # sort ownership

        ownership_sort = sorted(ownership, key=lambda owner: owner[0], reverse=True)

         # calculate ownership_Aratio

        ownership_Aratio.append(ownership_sort[0][0])

        

        # calculate ownership_Bratio

        if len(ownership_sort) > 3 :

            ownership_Bratio.append(ownership_sort[1][0] + ownership_sort[2][0] + ownership_sort[3][0])

        if 2 < len(ownership_sort) < 4 :

            ownership_Bratio.append(ownership_sort[1][0] + ownership_sort[2][0])

        if 1 <len(ownership_sort) < 3 :

            ownership_Bratio.append(ownership_sort[1][0])

    

    return ownership_Aratio,ownership_Bratio, time_latest





def ownership_AChange(data,companies):

    """

    count how many times did the biggest shareholder change

        1. change name

        2. change ratio(slight change included)

        

    haven't consider: 

        A 3.1 t1

        A 3.2 t2

        A 3.1 t3

        

        change: 1? 2?

    """

    change_ratio = list()

    change_name = list()

    change_A = list()

    

    for company in companies:

        ownership_ratio = set()

        ownership_name = set()

        ownership_A = set()

        for key in data[company]:

            ownership = list()

            for key,value in data[company][key].items():

                ownership_ = (key,value[0])

                ownership.append(ownership_)

            ownership_sort = sorted(ownership, key=lambda owner: owner[1], reverse=True)

            

            ownership_ratio.add(ownership_sort[0][1])

            ownership_name.add(ownership_sort[0][0])

            ownership_A.add(ownership_sort[0])

            

        change_ratio.append(len(ownership_ratio) - 1)

        change_name.append(len(ownership_name) - 1)

        change_A.append(len(ownership_A) - 1)

        

    return change_A, change_name, change_ratio



def drawSD (data):

    plt.hist(data,100)

    plt.xlabel('Biggest shareholder ratio')

    plt.ylabel('Frequency')

    plt.title('Ownership Structure B')

    plt.savefig("Ownership Structure B.png")

    print ("Finish ploting")





# =========================================================



# get shareholder structure

df = pd.read_excel('gdxx_sample.xlsx')

#df = pd.read_excel('gdxx.xlsx'sheetname=[0])

data, companies = dictify_ownership(df)

ownership_Aratio, ownership_Bratio, time_latest = ownershipRatio(data,companies)

change_A,_,_ = ownership_AChange(data,companies)



with open('ownership.txt','w') as f:

    f.write('company_name' + ',' + 'A' + ',' + 'B' +',' + 'changeA' + '\n')

    i = 0

    for cmp in companies:

        f.write(cmp + ',' +str(ownership_Aratio[i]) + ',' +str(ownership_Bratio[i]) + ',' + str(change_A[i])+'\n')

        i = i+1



drawSD(ownership_Bratio)

"""

==================

{

 '浙江信联股份有限公司': 

    {

    Timestamp('2005-06-30 00:00:00'): 

        {'上海声广投资有限公司': (19.0, '境内法人股'), 

         '中国建设银行浙江省信托投资公司': (0.25, '境内法人股'), 

         '杭州宏兴电子科技开发有限公司': (10.0, '境内法人股'), 

         '南京东渡房地产开发有限责任公司': (14.0, '境内法人股'), 

         '武汉汉讯经济发展有限公司': (3.53, '境内法人股'), 

         '武汉上行科技有限公司': (9.0, '境内法人股'), 

         '浙江省手工业合作社联合社': (5.56, '境内法人股'), 

         '上海迅宏科技有限公司': (3.0, '境内法人股'), 

         '北京华信电子企业集团': (4.7, '境内法人股')

         }, 

    Timestamp('2004-06-30 00:00:00'):

        {'武汉汉讯经济发展有限公司': (3.53, '境内法人股'), 

         '浙江省手工业合作社联合社': (5.56, '境内法人股'), 

         '中国人民建设银行浙江省信托投资公司': (0.25, '境内法人股'),

         '上海东渡房地产开发有限责任公司': (14.0, '境内法人股'), 

         '发达实业有限责任公司': (0.17, '境内法人股')

         }, 

    Timestamp('2004-12-31 00:00:00'):

        {'中国人民建设银行浙江省信托投资公司': (0.25, '境内法人股'), 

         '北京华信电子企业集团': (4.7, '境内法人股'),

         '上海声广投资有限公司': (19.0, '境内法人股'), 

         '南京市东渡房地产开发有限责任公司': (14.0, '境内法人股'), 

         '武汉汉讯经济发展有限公司': (3.53, '境内法人股'), 

         '武汉上行科技有限公司': (9.0, '境内法人股')

         }

    },

 '上海俊芮网络科技股份有限公司':

     {

     Timestamp('2016-09-06 00:00:00'):

         {'邵君俊': (35.7, '自然人持股'), 

          '韩卫国': (46.16, '自然人持股,三板流通A股'),

          '上海鋆汇企业管理中心（有限合伙）': (10.0, '境内法人股,三板流通A股'),

          '上海芮阳企业管理合伙企业（有限合伙）': (6.92, '境内法人股,三板流通A股'), 

          '上海思芮企业管理合伙企业（有限合伙）': (1.23, '境内法人股,三板流通A股')

          },

    Timestamp('2017-06-30 00:00:00'): 

        {'韩卫国': (44.81, '自然人持股,三板流通A股'), 

         '北京仙果广告股份有限公司': (2.91, '三板流通A股'), 

         '邵君俊': (34.66, '自然人持股,三板流通A股'), 

         '上海思芮企业管理合伙企业（有限合伙）': (1.19, '境内法人股,三板流通A股'), 

         '上海芮阳企业管理合伙企业（有限合伙）': (6.72, '境内法人股,三板流通A股'),

         '上海鋆汇企业管理中心（有限合伙）': (9.71, '境内法人股,三板流通A股')

         },

    Timestamp('2016-12-31 00:00:00'):

        {'上海芮阳企业管理合伙企业（有限合伙）': (6.92, '境内法人股,三板流通A股'),

         '上海思芮企业管理合伙企业（有限合伙）': (1.23, '境内法人股,三板流通A股'),

         '上海鋆汇企业管理中心（有限合伙）': (10.0, '境内法人股,三板流通A股'), 

         '黄建明': (0.005, '三板流通A股'), 

         '周丹': (0.005, '三板流通A股'), 

         '邵君俊': (35.7, '自然人持股'), 

         '北京仙果广告股份有限公司': (3.0, '三板流通A股'), 

         '韩卫国': (46.15, '自然人持股,三板流通A股')

         },

    Timestamp('2017-01-03 00:00:00'):

        {'黄建明': (0.05, '三板流通A股'),

         '周丹': (0.05, '三板流通A股'), 

         '上海鋆汇企业管理中心（有限合伙）': (9.71, '境内法人股,三板流通A股'),

         '邵君俊': (34.66, '自然人持股,三板流通A股'), 

         '上海思芮企业管理合伙企业（有限合伙）': (1.19, '境内法人股,三板流通A股'),

         '北京仙果广告股份有限公司': (2.91, '三板流通A股'),

         '韩卫国': (44.8, '自然人持股,三板流通A股'), 

         '上海芮阳企业管理合伙企业（有限合伙）': (6.72, '境内法人股,三板流通A股')

         },

    Timestamp('2016-09-14 00:00:00'): 

        {'邵君俊': (35.7, '自然人持股,三板流通A股'), 

         '韩卫国': (46.16, '自然人持股,三板流通A股'),

         '上海芮阳企业管理合伙企业（有限合伙）': (6.92, '境内法人股,三板流通A股'), 

         '上海鋆汇企业管理中心（有限合伙）': (10.0, '境内法人股,三板流通A股'), 

         '上海思芮企业管理合伙企业（有限合伙）': (1.23, '境内法人股,三板流通A股')

         }

    }

}

"""

