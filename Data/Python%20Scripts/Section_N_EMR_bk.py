import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
import time
import datetime
import warnings
import sys
import time
import datetime
warnings.filterwarnings('ignore')
msg= ""
audit_file = 'Z:/Ajay/python_errors/Audit_file.txt'

##url=r"C:\Users\admin\Downloads\PointClickCare_ Report Output.html"
##url=r"C:\Users\admin\Downloads\N412445_Emar_ARD0712 Report Output.html"
#url=r"C:\Users\admin\Downloads\Sheila_Mathews_ARD_0712_Emar_ Report Output.html"
##url=r"C:\Users\admin\Downloads\Melling_N411970_ARD0712_Emar_ Report Output.html"
##url=r"C:\Users\admin\Downloads\Melling_1_Emar_Report.html"
##url=r"C:\Users\admin\Downloads\AlveyDonald_Blank_eMAR.html"
##url=r"C:\Users\admin\Downloads\EMPTY_eMAR.html"
##url=r"C:\Users\admin\Downloads\EMR_N413382_08072022_NP.html"

##Inputfile=r"Z:\Ajay\Performer_Framework\Python\Input\Sheila_Mathews_ARD_0712_Emar_ Report Output.html"
##Intermediate=r"Z:\Ajay\Performer_Framework\Python\Intermediate\EMAR_Report.xls"
##Outputfile=r"Z:\Ajay\Performer_Framework\Python\Output\EMAR_Report_out.xls"
##Medicationfile=r"Z:\Ajay\Performer_Framework\Python\Input\Med_N413432.xlsx"

##Inputfile=url
##Intermediate="Medication_Report.xlsx"
##Outputfile=r"C:\Python310\bin\Medication_count.xlsx"
####Medicationfile="MED_N410667_07012022_ND.xls"
##Medicationfile="medications.xlsx"

Inputfile=sys.argv[1]
Intermediate=sys.argv[2]
Outputfile=sys.argv[3]
Medicationfile=sys.argv[4]


def get_medication_day_count(df,keyword):
    #print(keyword)
    count_list=[]
    #df1=df.loc[df['Order Summary'].str.contains(keyword, case=False)]
    df['indexes']= df["Order Summary"].str.find(keyword, 0)
    df1=df[df['indexes']==0]
    #print(df1)
    df1=df1.groupby(by='Adm_Dt').count()
    count=len(df1)
    date_list=df1.index.to_list()
    count_list=[keyword,count,date_list]   
    
    return count_list

def get_injections_day_count(df,injections):
    count_list=[]
    dfx  = pd.DataFrame(columns = df.columns)
    #df1=df.loc[df['Order Summary'].str.contains(keyword, case=False)]
    for injection in injections:
        df['indexes']= df["Order Summary"].str.find(injection, 0)
        df1=df[df['indexes']==0]
        dfx=dfx.append(df1)
        
    #print(df1)
    dfx=dfx.groupby(by='Adm_Dt').count()
    count=len(dfx)
    date_list=dfx.index.to_list()
    count_list=["All Injections",count,date_list]    
    return count_list


try:
    medications_file=pd.read_excel(Medicationfile)
    injections=medications_file[medications_file['Type']=="Inj"]['eMAR_Medication'].tolist()
    medications=pd.read_excel(Medicationfile)['eMAR_Medication'].tolist()
    f = open(Inputfile, encoding="utf8")
    #f = open(Inputfile)
    soup = BeautifulSoup(f)
except Exception as msg:
    errormsg = "Reading Medication file Error - " + str(msg)
    print(errormsg)
    df=pd.DataFrame()
    df.to_excel(Outputfile,index=False)
    f=open(audit_file, 'a+')
    text = "File Error - " + Inputfile + " time - " + str(datetime.datetime.now())
    f.write("\n")
    f.write(text)
    f.close()
    exit(0) ## change this in production

##medications=['ANTIDEPRESSANT','LORazepam Intensol Concentrate 2 MG/ML (LORazepam)', 'LORazepam Intensol Oral Concentrate 2 MG/ML (Lorazepam)', 'oxyCODONE HCl Tablet 5 MG', 'Morphine Sulfate (Concentrate) Solution 20 MG/ML']



#ignorelist=['Facility #:','SouthPointe Healthcare Center','Facility Code:','Date:','Medication Admin Audit Report','User:','Time:','Resident:','Page']
ignorelist=[]
count=0
outerlist=[]
break_out_flag = False
innerlist=[]
chartcodelist=[]
for tr in soup.find_all("tr"):
    if len(tr) > 1:
        for td in tr.find_all("td"):
            break_out_flag = False
            #innerlist=[]
            if not td.text.isspace() and len(td) > 1:
                for ignore in ignorelist:
                    if td.text.find(ignore) > 0:
                        #print(ignore)
                        count=count+1
                        break_out_flag = True
                        break
                if break_out_flag :
                    break
                #print(len(td))
                #print(td.text)
                #print(len(td.text))
                innerlist.append(td.text.strip())
                #print("length of inerlist - " + str(len( innerlist)))

        if len(innerlist)==5: # or 5 if Chart Code is not mentioned
            outerlist.append(innerlist)

        if len(innerlist)==1 and len(innerlist[0]) <= 2: # Chart code is of 1 or 2 length length for number 0-0 or 10 or NC
            chartcodelist.append(innerlist)
            
    #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    innerlist=[]
headers=["Order Summary","Schedule Date","Administration Time","Doc'd Time","Doc'd By"]#,"Chart Code"]
df = pd.DataFrame(outerlist, columns=headers)
df[['Adm_Dt','Adm_Tm']]='' # Initialize
if len(df) > 0 :
    df = df.drop(0) # drop first text row
    df[['Adm_Dt','Adm_Tm']]=df["Administration Time"].str.split(' ',expand=True)

dfchart = pd.DataFrame(chartcodelist, columns=['Chart Code'])

#define empty dataframe
df_final=pd.DataFrame(columns=["Order Summary","Schedule Date","Administration Time","Doc'd Time","Doc'd By","Chart Code"])
if len(outerlist) == len(chartcodelist) :
    df_final=df.join(dfchart)

df_final=df_final[df_final['Chart Code']=='0']
df_final.to_excel(Intermediate)

#df_final1=pd.read_excel(Intermediate)
Final_medication_counts=[]

inj_count_list = get_injections_day_count(df_final,injections)
Final_medication_counts.append(inj_count_list)

for medication in medications:
    count_list = get_medication_day_count(df_final,medication)
    Final_medication_counts.append(count_list)

df_medication_counts = pd.DataFrame(Final_medication_counts, columns=['Medication','Days Count','Comments'])
df_medication_counts.to_excel(Outputfile,sheet_name='Medication Counts',index=False)
