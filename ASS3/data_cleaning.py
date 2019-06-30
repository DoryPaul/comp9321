import pandas as pd

def load_file(data_path):
    df = pd.read_csv(data_path,names=['age','sex','chest pain type','resting blood pressure','serum cholestoral','fasting blood sugar',
                                      'resting electrocardiographic results','maximum heart rate','exercise induced angina',
                                      'oldpeak','the slope of ST','number of major vessels','thal','target'])
    df.replace('?',99,inplace=True)
    df['target'].replace([2,3,4],1,inplace=True)
    df.to_csv('clean_data.csv',header=0)
    #df.groupby('age')['sex'].plot(kind='bar', legend=True, figsize=(20, 5))

def data_uniform(data_path):
    df1 = pd.read_csv(data_path,index_col=0,names=['age','sex','chest pain type','resting blood pressure','serum cholestoral','fasting blood sugar',
                                      'resting electrocardiographic results','maximum heart rate','exercise induced angina',
                                      'oldpeak','the slope of ST','number of major vessels','thal','target'])
    keys = df1.keys()
    temp = pd.DataFrame()
    for i in range(len(keys)):
        if df1.keys()[i] != 'target':
            temp[df1.keys()[i]] = ((df1[df1.keys()[i]]-min(df1[df1.keys()[i]]))/(max(df1[df1.keys()[i]])-min(df1[df1.keys()[i]])))
        else:
            temp[df1.keys()[i]] = df1[df1.keys()[i]]
    return temp
load_file('processed.csv')
