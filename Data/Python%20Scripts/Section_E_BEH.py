import tabula as tb
import pandas as pd
import numpy as np
from functools import reduce
import sys
import os
import warnings
import time
import datetime
warnings.filterwarnings('ignore')
msg= ""
audit_file = 'Z:/Ajay/python_errors/Audit_file.txt'


def write_output(df):
    writer = pd.ExcelWriter(adl_excel_out_name)
    df.to_excel(writer,index=False,sheet_name='Behaviors_Observed_Count')
    writer.save()
    writer.close()

def get_data(df,shift):
    
    single_list_s=[]
    try:
        dfx, dfs = [x for _, x in df.groupby(df.iloc[:,0] == shift)]
        dfs=dfs.replace(np.nan,'blank')
        for col in dfs.columns:
            dfs[col]=dfs[col].str.split('(')
        list_s=dfs.values.tolist()
        single_list_s=reduce(lambda x,y: x+y, list_s)
        single_list_s = [item[0] for item in single_list_s]
        single_list_s = [x for x in single_list_s if x!= 'blank']
        
    except Exception as e:
        print(e)

    return single_list_s        

def main():
    msg= ""
    #tb.convert_into(inputfile, Intermediate, output_format="csv", pages='all')

    try:
        tb.convert_into(inputfile, Intermediate, output_format="csv", pages='all')
        df=pd.read_csv(Intermediate,skip_blank_lines=True,header=None)
    except pd.errors.EmptyDataError as msg:
        writer = pd.ExcelWriter(adl_excel_out_name)
        df=pd.DataFrame(columns=['Behaviors Observed','MDS_Item_Set_Count'])
        df.loc[len(df)]=["No_Behaviors_Observed",'']
        print(msg)
        write_output(df)
        f=open(audit_file, 'a+')
        text = "File Error - " + inputfile + " time - " + str(datetime.datetime.now())
        f.write("\n")
        f.write(text)
        f.close()        
        exit(0)
        
##    #df=df.fillna(" ")
##    df1, dfd = [x for _, x in df.groupby(df.iloc[:,0] == "D")]
##    df1, dfe = [x for _, x in df.groupby(df.iloc[:,0] == "E")]
##    df1, dfn = [x for _, x in df.groupby(df.iloc[:,0] == "N")]
##    df1, dfall = [x for _, x in df.groupby(df.iloc[:,0] == "ALL")]
##    df1, dfshift = [x for _, x in df.groupby(df.iloc[:,0].isin(['Shift',np.nan]))]
##    dfshift=dfshift.fillna("")
##    dfshift=dfshift.drop_duplicates()
##
##    dfd=dfd.replace(np.nan,'blank')
##    dfe=dfe.replace(np.nan,'blank')
##    dfn=dfn.replace(np.nan,'blank')
##
##
##    for col in dfd.columns:
##        dfd[col]=dfd[col].str.split('(')
##
##    for col in dfe.columns:
##        dfe[col]=dfe[col].str.split('(')
##
##    for col in dfn.columns:
##        dfn[col]=dfn[col].str.split('(')
##
##
##
##    list_d=dfd.values.tolist()
##    single_list_d=reduce(lambda x,y: x+y, list_d)
##
##
##    list_e=dfe.values.tolist()
##    single_list_e=reduce(lambda x,y: x+y, list_e)
##
##
##    list_n=dfn.values.tolist()
##    single_list_n=reduce(lambda x,y: x+y, list_n)
##
##    single_list_d = [item[0] for item in single_list_d]
##    single_list_e = [item[0] for item in single_list_e]
##    single_list_n = [item[0] for item in single_list_n]
##
##    #single_list_d = [x for x in single_list_d if pd.isnull(x) == False]
##    single_list_d = [x for x in single_list_d if x!= 'blank']
##    single_list_e = [x for x in single_list_e if x!= 'blank']
##    single_list_n = [x for x in single_list_n if x!= 'blank']



    cols=['Shift1','NoBehaviorsObserved','PhysicalBehaviorsDirectedAtOthers','GrabbingOthers','HittingOthers','KickingOthers','PushingOthers','PhysicallyAggressiveTowardsOthers',
          'ScratchingOthers','VerbalBehaviorsDirectedAtOthers','AccusingofOthers','CursingatOthers','ExpressFrustration/AngeratOthers','ScreamingatOthers','ThreateningOthers',
          'Shift2','SociallyInappropriateBehaviors','DisruptiveSounds','DisrobinginPublic','EnteringOtherResidentRoom/PersonalSpace','PublicSexualActs','RepetitiveMotions','Rummaging',
          'Spitting','Throwing/SmearingFood','Throwing/SmearingBodilyWaste','OtherBehaviorsNotDirectedAtOthers','Agitated','Anxious,Restless','Delusions','Shift3','Elopement,ExitSeeking',
          'Hallucinations','HittingSelf','Hoarding','Insomnia,NotSleeping','NeglectingSelfCare','Pacing','Panic','Picking AtSelf','RefusingCare','Sad,Tearful','ScratchingSelf',
          'ScreamingNotAtOthers','SelfInjury','Shift4','Wandering','Withdrawn/Isolating']


    behav_df=pd.DataFrame(columns=cols)
    
    shifts=['D','E','N']
    single_list=[]
    for shift in shifts:
        single_list = get_data(df,shift)
        print(shift)
        print(len(single_list))
        if (len(single_list)) > 0:
            behav_df.loc[len(behav_df)] = single_list
            
##    behav_df.loc[len(behav_df)] = single_list_d
##    behav_df.loc[len(behav_df)] = single_list_e
##    behav_df.loc[len(behav_df)] = single_list_n

    behav_df=behav_df.drop(['Shift1','Shift2','Shift3','Shift4'],axis=1)
    #behav_df = behav_df.set_index('Shift1')


    behav_df = behav_df.astype(int)

    no_behav_df=behav_df['NoBehaviorsObserved']
    physical_df=behav_df[['GrabbingOthers','HittingOthers','KickingOthers','PushingOthers','PhysicallyAggressiveTowardsOthers','ScratchingOthers']]
    verbal_df=behav_df[['AccusingofOthers','CursingatOthers','ExpressFrustration/AngeratOthers','ScreamingatOthers','ThreateningOthers']]
    social_df=behav_df[['DisruptiveSounds','DisrobinginPublic','EnteringOtherResidentRoom/PersonalSpace','PublicSexualActs','RepetitiveMotions','Rummaging','Spitting','Throwing/SmearingFood','Throwing/SmearingBodilyWaste']]
    other_behav_df=behav_df[['Agitated','Anxious,Restless','Delusions','Elopement,ExitSeeking','Hallucinations','HittingSelf','Hoarding','Insomnia,NotSleeping','NeglectingSelfCare','Pacing','Panic','Picking AtSelf','RefusingCare','Sad,Tearful','ScratchingSelf',
          'ScreamingNotAtOthers','SelfInjury','Wandering','Withdrawn/Isolating']]
    hallucinations_df=behav_df[['Hallucinations']]
    delusions_df=behav_df[['Delusions']]
    wandering_df=behav_df[['Wandering']]

    #
    #verbal_df.max(axis=1)
    physical_cnt=physical_df.max(axis=1).max()
    verbal_cnt=verbal_df.max(axis=1).max()
    social_cnt=social_df.max(axis=1).max()
    other_behav_cnt=other_behav_df.max(axis=1).max()
    hallucinations_cnt=hallucinations_df.max(axis=1).max()
    delusions_cnt=delusions_df.max(axis=1).max()
    wandering_cnt=wandering_df.max(axis=1).max()


    print("Physical_Behaviors_Directed_AtOthers_cnt = " + str(physical_cnt))
    print("Verbal_Behaviors-Directed_AtOthers_cnt = " + str(verbal_cnt))
    print("Socially_Inappropriate_Behaviors_cnt = " + str(social_cnt))
    print("Other_Behaviors_NotDirected_AtOthers_cnt = " + str(other_behav_cnt))
    print("Hallucinations_cnt = " + str(hallucinations_cnt))
    print("Delusions_cnt = " + str(delusions_cnt))
    print("Wandering_cnt = " + str(wandering_cnt))


    writer = pd.ExcelWriter(adl_excel_out_name)
    final_behave_df=pd.DataFrame(columns=['Behaviors Observed','MDS_Item_Set_Count'])
    final_behave_df.loc[len(final_behave_df)]=["Physical_Behaviors_Directed_AtOthers_cnt",physical_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Verbal_Behaviors-Directed_AtOthers_cnt",verbal_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Socially_Inappropriate_Behaviors_cnt",social_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Other_Behaviors_NotDirected_AtOthers_cnt",other_behav_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Hallucinations_cnt",hallucinations_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Delusions_cnt",delusions_cnt]
    final_behave_df.loc[len(final_behave_df)]=["Wandering_cnt",wandering_cnt]

    final_behave_df.to_excel(writer,index=False,sheet_name='Behaviors_Observed_Count')
    writer.save()
    writer.close()


if __name__ == "__main__":

    In=sys.argv[1]
    Intermediate=sys.argv[2]
    Out=sys.argv[3]
    inputfile=In
    adl_excel_out_name=Out

##    In=r"C:/Python310/bin/ADL5July/BEH_3716493_10032022_ND.pdf"
##    #In=r"C:/Python310/bin/ADL5July/BEH_I711406_10032022_NQ.pdf"
##    Intermediate=r"C:/Python310/bin/ADL5July/test.csv"
##    Out=r"C:/Python310/bin/ADL5July/BEH_out.xls"
##    Inputfile=In
##    adl_excel_out_name=Out


##    In="Z:\Ajay\Performer_Framework\Python\Input\ArmstrongbehaviorReport.pdf"
##    Intermediate="Z:\Ajay\Performer_Framework\Python\Intermediate\ArmstrongbehaviorReport.csv"
##    Out="Z:\Ajay\Performer_Framework\Python\output\ArmstrongbehaviorReport.xls"
##    inputfile=In
##    adl_excel_out_name=Out

##    import argparse
##    parser = argparse.ArgumentParser(description='Personal information')
##    parser.add_argument('--inputfile', dest='inputfile', type=str, help='Resident input pdf file')
##    parser.add_argument('--outputfile', dest='outputfile', type=str, help='Resident output XLS file')
##    #parser.add_argument('--OutFilepath', dest='outfile', type=str, help='Surname of the candidate')
##
##    args = parser.parse_args()

    ##print("argument " + args.resident)
    
##    resident="Timothy Henslee"

##    resident="behaviorReport_Alvarado_Summary"
    #resident="behaviorReport_Alvarado"
    #resident="ArmstrongbehaviorReport"
    inputfile = In
    outputfile = Out		
    #resident=args.resident
    adl_excel_out_name=outputfile #+'_Behavior_output.xls'
    #inputfile="Z:\Ajay\Performer_Framework\Python\Python Scripts\""+resident+".pdf"
    #inputfile=(r"Z:/Ajay/Performer_Framework/Python/Python Scripts/" + resident +".pdf")
    main()

