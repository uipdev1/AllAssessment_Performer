import tabula as tb
import pandas as pd
import numpy as np
from functools import reduce
import os
import warnings
import time
import datetime
import sys
warnings.filterwarnings('ignore')
msg= ""
audit_file = 'Z:/Ajay/python_errors/Audit_file.txt'

##resident="Timothy Henslee"
##
##resident="Margaret Cheatham"
##resident="Joan_Resto_Less_Mins"

##resident="Robert_Resto_RR_values"
##resident="Restorative look back report example 2[228]"
##resident="Restorative look back report example[227]"

##adl_excel_out_name=resident+'_RESTO_output.xls'
##Inputfile=(r"C:/Users/admin/Downloads/" + resident +".pdf")
##Intermediate="pdf_output.csv"

In=sys.argv[1]
Intermediate=sys.argv[2]
Out=sys.argv[3]
Inputfile=In
adl_excel_out_name=Out


list_of_adls=['Passive ROM','Assistance with Splint or','Brace','Active ROM','Amputation/Prosthesis Care','Bed Mobility','Communication'
              ,'Dressing/Grooming','Eating/Swallowing','Transfers','Walking','Toileting']


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
        adl_df.columns=['mins','steps']
        adl_df=adl_df.drop(['steps'],axis=1)
    else:
        adl_df.columns=['mins']


    adl_df=adl_df[adl_df['mins'].astype(int)!=0]
    days=adl_df[adl_df['mins'].astype(int)>=15].count()[0]
    return ( adl, days)

#list_of_adls=['Toilet Use', 'Transferring', 'Eating', 'Walk in room', 'Dressing', 'Locomotion on Unit', 'Bed Mobility', 'Bathing', 'Locomotion off Unit', 'Personal Hygiene', 'Walk in corridor']
list_of_adls=['Passive ROM','Passive ROM','Assistance with Splint or','Brace','Active ROM','Amputation/Prosthesis Care','Bed Mobility','Communication'
              ,'Dressing/Grooming','Eating/Swallowing','Transfers','Walking','Toileting']


#table =tb.read_pdf(Inputfile,pages='all')
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

try:
    col2=df.columns[2]
    col3=df.columns[3]
    cols=['adl','day1','day2','day3','day4','day5','day6','day7']
    #cols=['adl','day1','day2','day3','day4','day5','day6','day7','day11','day22','day33','day44','day55','day66','day77']
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
         #print(i + " "+ str(ind))
         count=count+1
     except Exception as msg:
         errormsg=msg
         #print(msg)


if count==0:
    msg = "There are no ADL data in the Inputfile"
    errormsg=msg
    df=pd.DataFrame()
    df.to_excel(adl_excel_out_name,index=False)
    print(msg)

else:
    print("Total ADLs to process - " + str(count))
##    try:
##        ind=df.index[df['adl']=='Bath as Necessary'].to_list()[0]
##        df=df[0:ind]
##
##    except Exception as msg:
##        print(msg)

    df=df.replace('RX','0',regex=True)
    df=df.replace('RR','0',regex=True)
    df=df.replace('NA','0',regex=True)
    df=df.replace('NR','0',regex=True)
    
    
    #below col2 and col3 statement should be after abnove 'Bath as Necessary' statement        
    df=df[df['day2']!=col2]
    df=df[df['day3']!=col3] # extra check    

##    df=df.set_index('adl')
    df=df.dropna(how='all',axis=1)
    df=df.dropna(how='all',axis=0)
    substrings=[":","/20"]
    #substring=":" # remove all time rows
    for substring in substrings:
        df=df[df.apply(lambda row: ~row.astype(str).str.contains(substring, case=False).any(), axis=1)]

    df['adl']=df['adl'].ffill(axis = 0)

    
    df = df.set_index('adl')
    df=df.dropna(how='all',axis=0)

    df = df.replace(np.nan, "0,0", regex=True)
    for col in df.columns:
        df[col]=df[col].str.split(',')

    for col in df.columns:
        df[col]=df[col].apply(lambda x:x[0])
    
    df=df.replace(np.nan,0)
    df=df.astype(int) # very important statement ..if removed.it will concatement the numbers in the groupby sum clause
    df=df.groupby('adl').sum()

    unique_adl_list=df.index.drop_duplicates().to_list()

    writer = pd.ExcelWriter(adl_excel_out_name)
    score_df=pd.DataFrame(columns=['Restorative Programs','Days'])
    for adl in unique_adl_list:
        print(adl)
        
        final_score=get_adl_df(adl)
        final_score=list(final_score)
        print(final_score)
        f=pd.DataFrame([(final_score)],columns=['Restorative Programs','Days'])
        score_df=score_df.append(f,ignore_index=True)

    score_df.to_excel(writer,index=False,sheet_name='RESTO_PGM_Count')
    writer.save()
    writer.close()
    
   


