import tabula as tb
import pandas as pd
import numpy as np
import sys
import os
import warnings
warnings.filterwarnings('ignore')
from functools import reduce
import time
import datetime
msg= ""
previous_adl= ""
audit_file = 'Z:/Ajay/python_errors/Audit_file.txt'

#adl_excel_out_name="Z:\Ajay\Performer_Framework\Python\Output\ADL_excel_output.xls"
#Inputfile=(r"Z:\Ajay\Performer_Framework\Python\Input\Downloaded_ADL_Report.pdf")

In=sys.argv[1]
Intermediate=sys.argv[2]
Out=sys.argv[3]
Inputfile=In
adl_excel_out_name=Out

##In=r"Z:\Ajay\Performer_Framework\Python\Input\Bkup\ADL_N410667_07012022_ND.pdf"
##Intermediate=r"Z:\Ajay\Performer_Framework\Python\Intermediate\test.csv"
##Out=r"Z:\Ajay\Performer_Framework\Python\output\test.xls"
##Inputfile=In
##adl_excel_out_name=Out

##In=r"C:/Python310/bin/ADL5July/ADL_N410667_07012022_ND.pdf"
##Intermediate=r"C:/Python310/bin/ADL5July/test.csv"
##Out=r"C:/Python310/bin/ADL5July/ADL_N410667_07012022_ND_Adl_output.xls"
##Inputfile=In
##adl_excel_out_name=Out


writer = pd.ExcelWriter(adl_excel_out_name)
sorted_df=score_df=pd.DataFrame(columns=['ADL','Score'])

def process_coma_df(df):    
        df_coma=df.loc[df['adl'].str.contains(",", case=False,na=False)]
        coma_ind=df_coma.index[0]
        df_len=len(df)
        cols=['self','support','frequency']
        start_ind=coma_ind-1
        end_index=coma_ind
        start_range=coma_ind + 1
        end_range=min(coma_ind+5,df_len)
        prev_adl_df=df[coma_ind-1:coma_ind]
        prev_adl=prev_adl_df.tail(1)['adl'].tolist()[0]
        
        for i in range(start_range,end_range):
            next_coma_df=df[i:i+1]
            next_coma_adl=next_coma_df.tail(1)['adl'].tolist()[0]
            #print(next_coma_adl)            
            if next_coma_adl in list_of_adls:
                break
            end_index=i
        test_df=df[start_ind:end_index+1]
        test_df=test_df.replace(prev_adl, "0,0,0", regex=True)
        test_df=test_df.replace(np.nan, "0,0,0", regex=True)
        for col in test_df.columns:
            test_df[col]=test_df[col].str.split(',')

        somelist=test_df.values.tolist()
        single_list = reduce(lambda x,y: x+y, somelist)
        test_df=pd.DataFrame(single_list)
        test_df.columns=cols
        test_df  = test_df.replace('','1',regex = True)
        test_df['self'] = test_df['self'].fillna(1)
        test_df['support'] = test_df['support'].fillna(1)
        test_df['frequency'] = test_df['frequency'].fillna(1)
        test_df  = test_df.replace({'NA','RX','RR','NR','BB','S','T'},'0',regex = True)
        test_df=test_df[test_df['frequency'].astype(int)!=0] # remove 0 frequency records - Nan was converted in to [0,0,0] so remove these records.
        test_df.reset_index(drop=True,inplace=True)
        return (prev_adl,test_df,start_ind, end_index+1)


def get_adl_df(adl):
    #print(adl)
    adl_df=df.loc[adl]
    adl_df=pd.DataFrame(adl_df) # if this statement is removed, it gives error for single index adl
    #print("length is " + str(len(adl_df)))
    somelist=adl_df.values.tolist()
    single_list = reduce(lambda x,y: x+y, somelist)
    adl_df=pd.DataFrame(single_list)
    if len(adl_df.columns) == 2 :
        # What if for a adl, for all 7 * 3 shifts data is available but in 2 dimentional..for eaxmple Eating - always 2 dimentions..so convert 2 dimensions to 3 dimentions with freq=1
        adl_df.columns=['self','support']
        adl_df['frequency']=1
    else:
        adl_df.columns=cols
    adl_df['self'] = adl_df['self'].fillna(1)
    adl_df['support'] = adl_df['support'].fillna(1)
    adl_df['frequency'] = adl_df['frequency'].fillna(1)
    adl_df['self']  = adl_df['self'].replace('','1',regex = True)
    adl_df['support']  = adl_df['support'].replace('','1',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('','1',regex = True)


    adl_df['self']  = adl_df['self'].replace('NA','8',regex = True)
    adl_df['self']  = adl_df['self'].replace('RX','8',regex = True)
    adl_df['self']  = adl_df['self'].replace('RR','8',regex = True)
    adl_df['self']  = adl_df['self'].replace('NR','8',regex = True)
    
    adl_df['self']  = adl_df['self'].replace('BB','1',regex = True)
    adl_df['self']  = adl_df['self'].replace('S','1',regex = True)
    adl_df['self']  = adl_df['self'].replace('T','1',regex = True)


    adl_df['support']  = adl_df['support'].replace('NA','8',regex = True)
    adl_df['support']  = adl_df['support'].replace('RX','8',regex = True)
    adl_df['support']  = adl_df['support'].replace('RR','8',regex = True)
    adl_df['support']  = adl_df['support'].replace('NR','8',regex = True)
    
    adl_df['support']  = adl_df['support'].replace('BB','1',regex = True)
    adl_df['support']  = adl_df['support'].replace('S','1',regex = True)
    adl_df['support']  = adl_df['support'].replace('T','1',regex = True)

    
    adl_df['frequency']  = adl_df['frequency'].replace('NA','0',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('RX','0',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('RR','0',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('NR','0',regex = True)
    
    adl_df['frequency']  = adl_df['frequency'].replace('BB','1',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('S','1',regex = True)
    adl_df['frequency']  = adl_df['frequency'].replace('T','1',regex = True)



    

    adl_df["frequency"] = np.where(adl_df["self"].astype(int) == 8, 0,adl_df["frequency"])
    adl_df["frequency"] = np.where(adl_df["support"].astype(int) == 8, 0,adl_df["frequency"])

    adl_df=adl_df[adl_df['frequency'].astype(int)!=0] # remove 0 frequency records - Nan was converted in to [0,0,0] so remove these records.
    adl_df.reset_index(drop=True,inplace=True)
    return adl_df

def cal_score(adl,adl_df):
    max_self=adl_df['self'].astype(int).max()
    min_self=adl_df['self'].astype(int).min()
    count_self=adl_df['self'].astype(int).count()
    sum_freq=adl_df['frequency'].astype(int).sum()
    
    count_self_0=len(adl_df[adl_df['self'].astype(int)==0])
    count_self_1=len(adl_df[adl_df['self'].astype(int)==1])
    count_self_2=len(adl_df[adl_df['self'].astype(int)==2])
    count_self_3=len(adl_df[adl_df['self'].astype(int)==3])
    count_self_4=len(adl_df[adl_df['self'].astype(int)==4])
    count_self_8=len(adl_df[adl_df['self'].astype(int)==8])
    all_self_0=all_self_1=all_self_2=all_self_3=all_self_4=all_self_8=False
    
    sum_freq_0=adl_df[adl_df['self'].astype(int)==0]['frequency'].astype(int).sum()
    sum_freq_1=adl_df[adl_df['self'].astype(int)==1]['frequency'].astype(int).sum()
    sum_freq_2=adl_df[adl_df['self'].astype(int)==2]['frequency'].astype(int).sum()
    sum_freq_3=adl_df[adl_df['self'].astype(int)==3]['frequency'].astype(int).sum()
    sum_freq_4=adl_df[adl_df['self'].astype(int)==4]['frequency'].astype(int).sum()
    
    max_support=adl_df['support'].astype(int).max()
    max_self=adl_df['self'].astype(int).max() ## required for Bathing
    #print("max_support - " + str(max_support))

    if adl_df.empty:
        max_self=np.nan_to_num(max_self).astype(int)
        if max_self==0:
            max_self = 8
        max_support=np.nan_to_num(max_support).astype(int) # for empty adl df .. selfscore will be 8 so the suppoert should be 8
        if max_support==0:
            max_support = 8
        


    if count_self_0==count_self:
        all_self_0=True
    if count_self_1==count_self:
        all_self_1=True
    if count_self_2==count_self:
        all_self_2=True
    if count_self_3==count_self:
        all_self_3=True
    if count_self_4==count_self:
        all_self_4=True
    if count_self_8==count_self:
        all_self_8=True
        
    mds_self_output=""
    
##If(OR(AND(count_self<=1,sum_freq<1),All_self_8="Yes"),"EIGHT",                # cond1
##
##If(AND(count_self<=2,sum_freq<3),"sEVEN",                                     # cond2
##
##If(All_self_0="Yes","ZERO",                                                   # cond3
##
##If(AND(OR(sum_freq_0>=3,sum_freq_1>=3), AND(sum_freq_2<3,sum_freq_3<3,sum_freq_4<3,(sum_freq_2+sum_freq_3+sum_freq_4)<3)),"ONE1",                                     # cond4
##
##If(OR(All_self_4="Yes",(count_self-count_self_8)=count_self_4),"fOUR",        # cond5
##
##If(OR(sum_freq_3>=3,(sum_freq_3)>=3),"THREE1",                                # cond6 # changed based on Heathers email on 8/5
##
##If(sum_freq_2>=3,"TWO1",                                                      # cond7
##
##If(sum_freq_1>=3,"ONE2",                                                      # cond8
##
##If((sum_freq_3+sum_freq_4)>=3,"THREE2",                                       # cond9
##
##If((sum_freq_3+sum_freq_4+sum_freq_2)>=3,"TWO2",                              # cond10
##
##ONE3))))))))))                                                                # cond11

    cond1=((count_self<=1 and sum_freq<1) or all_self_8)
    cond2=count_self<=2 and sum_freq<3
    cond3=all_self_0
    cond4=((sum_freq_0>=3 or sum_freq_1>=3) and (sum_freq_2<3 and sum_freq_3<3 and sum_freq_4<3 and (sum_freq_2+sum_freq_3+sum_freq_4)<3))
    cond5=(all_self_4 or (count_self-count_self_8)==count_self_4)
    #cond6=(sum_freq_3>=3 or(sum_freq_3+sum_freq_4)>=3)
    cond6=sum_freq_3>=3
    cond7=sum_freq_2>=3
    cond8=sum_freq_1>=3
    cond9=(sum_freq_3+sum_freq_4)>=3
    cond10=(sum_freq_3+sum_freq_4+sum_freq_2)>=3
    cond11= 1

    if cond1 :
        mds_self_output = 8
    else:
        if cond2 :
            mds_self_output = 7
        else:
            if cond3 :
                mds_self_output = 0
            else:
                if cond4 :
                    mds_self_output = 1
                else:
                    if cond5 :
                        mds_self_output = 4
                    else:
                        if cond6 :
                            mds_self_output = 3           
                        else:
                            if cond7 :
                                mds_self_output = 2
                            else:
                                if cond8 :
                                    mds_self_output = 1
                                else:
                                    if cond9 :
                                        mds_self_output = 3              
                                    else:
                                        if cond10 :
                                            mds_self_output = 2
                                        else:
                                            mds_self_output = 1          
    


    if adl=='Bathing':
        return ( max_self, max_support)
    else:
        return ( mds_self_output, max_support)


list_of_adls=['Toilet Use', 'Transferring', 'Eating', 'Walk in room', 'Dressing', 'Locomotion on Unit', 'Bed Mobility', 'Bathing', 'Locomotion off Unit', 'Personal Hygiene', 'Walk in corridor']
score_adl_order=['Bed Mobility','Transferring','Walk in room','Walk in corridor','Locomotion on Unit','Locomotion off Unit','Dressing','Eating','Toilet Use','Personal Hygiene','Bathing' ]



#table =tb.read_pdf(Inputfile,pages='all')

#tb.convert_into(Inputfile, Intermediate, output_format="csv", pages='1,2')
#tb.convert_into(Inputfile, Intermediate, output_format="csv", pages='all')


try:
    tb.convert_into(Inputfile, Intermediate, output_format="csv", pages='all')
    df=pd.read_csv(Intermediate)
except Exception as msg:
    errormsg = "Reading CSV Error - " + str(msg)
    print(errormsg)
    df=pd.DataFrame()
    df.to_excel(adl_excel_out_name,index=False)
    f=open(audit_file, 'a+')
    text = "File Error - " + Inputfile + " time - " + str(datetime.datetime.now())
    f.write("\n")
    f.write(text)
    f.close()
    exit(0) ## change this in production    
    

# get the column names for 2nd and 3rd column..Pdf contain the row with the date as
# column name like below
##
##      Unnamed: 0  1/25/2022  1/26/2022  1/27/2022  1/28/2022  1/29/2022  1/30/2022  1/31/2022
##16  Bed Mobility        NaN        NaN        NaN    3, 3, 3        NaN        NaN        NaN
##17           NaN        NaN        NaN        NaN      20:25        NaN        NaN        NaN
##18           NaN  1/25/2022  1/26/2022  1/27/2022  1/28/2022  1/29/2022  1/30/2022  1/31/2022
##19  Bed Mobility        NaN        NaN        NaN        NaN        NaN        NaN        NaN
##



try:
    col2=df.columns[2]
    col3=df.columns[3]
    cols=['adl','day1','day2','day3','day4','day5','day6','day7']
    df.columns=cols
except Exception as msg:
    cols=['adl']
    df.rename(columns={list(df)[0]:'adl'}, inplace=True)
    errormsg=msg
    print(msg)


count=0
for i in list_of_adls:
     try:
         ind=df.index[df['adl']==i].to_list()[0]
         print(i + " "+ str(ind))
         count=count+1
     except Exception as msg:
         errormsg=msg
         print(msg)


if count==0:
    msg = "There are no ADL data in the Inputfile"
    errormsg=msg
    df=pd.DataFrame()
    df.to_excel(adl_excel_out_name,index=False)
    print(msg)

else:
    print("Total ADLs to process - " + str(count))
    try:
        ind=df.index[df['adl']=='Bath as Necessary'].to_list()[0]
        df=df[0:ind]

    except Exception as msg:
        print(msg)
    #below col2 and col3 statement should be after abnove 'Bath as Necessary' statement        
    df=df[df['day2']!=col2]
    df=df[df['day3']!=col3] # extra check    


    df=df.dropna(how='all',axis=1)
    df=df.dropna(how='all',axis=0)
    substring=":" # remove all time rows
    df=df[df.apply(lambda row: ~row.astype(str).str.contains(substring, case=False).any(), axis=1)]
    df=df.reset_index(drop=True)
    df_4_coma_process=df.copy(deep=True) # this assignment should be after reset statment but before all other statements importantly ffill    

    df_coma=df_4_coma_process.loc[df_4_coma_process['adl'].str.contains(",", case=False,na=False)]
    if len(df_coma) > 0:
        #start_ind, end_index=get_coma_index_range(df_4_coma_process)
        coma_adl,coma_df,start_ind, end_index=process_coma_df(df_4_coma_process)
        coma_df["frequency"] = np.where(coma_df["self"].astype(int) == 8, 0,coma_df["frequency"])
        coma_df["frequency"] = np.where(coma_df["support"].astype(int) == 8, 0,coma_df["frequency"])
        coma_df=coma_df[coma_df['frequency'].astype(int)!=0]
        print(coma_adl)
        print(coma_df)
        coma_score=cal_score(coma_adl,coma_df)
        coma_score=list(coma_score)
        print(coma_score)
        f=pd.DataFrame([(coma_adl,coma_score)],columns=['ADL','Score'])
        coma_df=coma_df.astype(int)
        coma_df.to_excel(writer,index=False,sheet_name=coma_adl)
        score_df=score_df.append(f,ignore_index=True)
        # remove the comma related adl records from the original dataframe to to process other adls
        df=df.drop(df.index[start_ind:end_index])



    df['adl']=df['adl'].ffill(axis = 0) 

    df = df.replace(np.nan, "0,0,0", regex=True)
    df = df.set_index('adl')
    for col in df.columns:
        df[col]=df[col].str.split(',')


    #df['adl_flaten']=df.loc[:].values.tolist()

    unique_adl_list=df.index.drop_duplicates().to_list()

    #from functools import reduce
    ##somelist=eating.values.tolist()
    ##single_list = reduce(lambda x,y: x+y, somelist)
    cols=['self','support','frequency']

    #unique_adl_list=['Eating']
    #writer = pd.ExcelWriter(adl_excel_out_name)
    #score_df=pd.DataFrame(columns=['ADL','Score'])
    for adl in unique_adl_list:
        print(adl)
        adl_df=get_adl_df(adl)
        print(adl_df)
        final_score=cal_score(adl,adl_df)
        final_score=list(final_score)
        f=pd.DataFrame([(adl,final_score)],columns=['ADL','Score'])
        score_df=pd.concat([score_df,f],ignore_index=True)
        print(final_score)
        print("XXXXXXXXXXXXXXXXXXX")
        adl_df=adl_df.astype(int)
        adl_df.to_excel(writer,index=False,sheet_name=adl)

    for adl in score_adl_order:
        f=score_df[score_df['ADL']==adl]
        sorted_df=sorted_df.append(f,ignore_index=True)

    #score_df.to_excel(writer,index=False,sheet_name='ADL_Score')
    sorted_df.to_excel(writer,index=False,sheet_name='ADL_Score')
    writer.save()
    writer.close()    
