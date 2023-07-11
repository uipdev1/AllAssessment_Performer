import tabula as tb
import pandas as pd
import numpy as np
import sys
import os
import warnings
import time
import datetime
from camelot import read_pdf
warnings.filterwarnings('ignore')
msg= ""
audit_file = 'Z:/Ajay/python_errors/Audit_file.txt'

#resident="Scott SOB V2"
#resident="Allen Crow"
#resident="Stephen SOB V2"
#resident="Rick SOB V2"
#resident="Hunter SOB V2"
#resident="Ronald SOB V2"
#outfile_location="Z:\Ajay\Performer_Framework\Python\Output\SOB_excel_output.xls" # pad with Resident Name
#csv_pdf_file = "Z:/Python/SOB/CSV/pdf_output.csv" # pad with Resident Name
#file=(r"Z:\Ajay\Performer_Framework\Python\Input\Downloaded_SOB_Report.pdf")

In=sys.argv[1]
Intermediate=sys.argv[2]
Out=sys.argv[3]
file=In
outfile_location=Out
csv_pdf_file=Intermediate

##outfile_location="C:/Python310/bin\ADL5July/SOB/SOB_excel_output.xls" # pad with Resident Name
##csv_pdf_file = "C:/Python310/bin/ADL5July/SOB_pdf_output.csv" # pad with Resident Name
##file=(r"C:\Python310\bin\ADL5July\SOB\SOB_N412987_09282022_NQ.pdf")

##outfile_location="Z:\Ajay\Performer_Framework\Python\Output\SOB_excel_output.xls" # pad with Resident Name
##csv_pdf_file = "Z:/Python/SOB/CSV/pdf_output.csv" # pad with Resident Name
##file=(r"Z:\RPA\Python\Input\SOB_N412987_09282022_NQ.pdf")


list_of_adls=['Shortness of Breath V2']


#table =tb.read_pdf(file,pages='all')
#tb.convert_into(file, csv_pdf_file, output_format="csv", pages='1')

try:
    tables = read_pdf(file, pages = '1')
    df=tables[0].df
except Exception as msg:
    errormsg = "Reading CSV Error - " + str(msg)
    print(errormsg)
    df=pd.DataFrame()
    df.to_excel(outfile_location,index=False)
    f=open(audit_file, 'a+')
    text = "File Error - " + file + " time - " + str(datetime.datetime.now())
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
    #date_list=df.columns[0:8].values.tolist()
    date_list=df[0:1].values.tolist().pop(0)
##    col2=df.columns[2]
##    col3=df.columns[3]
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
    msg = "There are no ADL data in the file"
    errormsg=msg
    df=pd.DataFrame()
    df.to_excel(outfile_location,index=False)
    print(msg)

else:
    print("Total ADLs to process - " + str(count))
        
##    df=df[df['day2']!=col2]
##    df=df[df['day3']!=col3] # extra check    


    df=df.dropna(how='all',axis=1)
    df=df.dropna(how='all',axis=0)
    substring=":" # remove all time rows
    df=df[df.apply(lambda row: ~row.astype(str).str.contains(substring, case=False).any(), axis=1)]
    df['adl']=df['adl'].ffill(axis = 0)

    # Check the combination  "Y, Y" or "Y,Y"
    y1=df.apply(lambda row: row.astype(str).str.contains("Y, Y").any(), axis=0).to_list() # axis 0 = days
    y2=df.apply(lambda row: row.astype(str).str.contains("Y,Y").any(), axis=0).to_list()
##    y1=[False, False, False, False, False, False, False, False]
##    y2=[False, False, False, False, False, False, False, False]
    y1_pos=[i for i, x in enumerate(y1) if x == True]
    y2_pos=[i for i, x in enumerate(y2) if x == True]
    final_pos=y1_pos+y2_pos

    c1=y1.count(True)
    c2=y2.count(True)

    dates=[]
    for i in final_pos:
        dates.append(date_list[i])

    print(dates)
    
    out_df=pd.DataFrame(columns=['Days_Count','Comments'],index=['Shortness of Breath'])
    out_df['Days_Count']=max(c1,c2)
    out_df['Comments']=" , ".join(dates)

    writer = pd.ExcelWriter(outfile_location)
    out_df.to_excel(writer,index=True,sheet_name='Shortness of Breath')
    writer.save()
    writer.close()          
