
import pandas as pd
import numpy as np
import re
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    a = []
    GDP = pd.read_excel('gdplev.xls',skiprows=5)
    GDP = GDP.drop(['Unnamed: 3','Unnamed: 7'],axis=1)
    GDP = GDP.drop([0,1],axis=0)
    GDP = GDP[['Unnamed: 4','GDP in billions of current dollars.1']]
    GDP.columns = ['quarter', 'gdp']
    GDP = GDP[212:]
    for i in range(len(GDP)-4):
        if ((GDP.iloc[i][1] > GDP.iloc[i+1][1]) & (GDP.iloc[i+2][1] < GDP.iloc[i+1][1])):
            a.append(GDP.iloc[i][0])
    return a[0]
get_recession_start()

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    stat = []
    stat1 = []
    temp = []
    reg = []
    c = []
    f = open('university_towns.txt')
    for x in f:
        if 'edit' in x:
            stat1.append(x)
        stat = stat1
    for x in stat:
        x = x.replace('\n','')
        temp.append(x)
    stat = temp
    flag = False
    for val in range(len(stat1)):
        temp = []
        stat1.append('%')
        f = open('university_towns.txt')
        for lin in f:
            if stat1[val+1] == lin:
                flag = False
            if flag:
                temp.append(lin)
            if stat1[val] == lin:
                flag = True
        reg.append(temp)
        stat1.pop()    
    reg.pop()
    c.append(lin)
    reg.append(c)
    temp = []
    for i in stat:
        i = i.replace('[edit]','')
        temp.append(i)
    stat = temp
    regions = []
    for i in reg:
        temp = []
        for j in i:
            j = j.split(' (')[0]
            j = j.replace('\n','')
            temp.append(j)
        regions.append(temp)
    state = []
    for val,i in enumerate(reg):
        for val1,l in enumerate(stat):
            for j in range(len(i)):
                if val == val1:
                    state.append(l)
    region = []
    for i in regions:
        for j in i:
            region.append(j)
    data = pd.DataFrame(region, state)           
    data['State'] = data.index
    data = data.set_index('State')
    data['RegionName'] = data[0]
    del data[0]
    data = data.reset_index()
    return data

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    a = 0
    GDP = pd.read_excel('gdplev.xls',skiprows=5)
    GDP = GDP.drop(['Unnamed: 3','Unnamed: 7'],axis=1)
    GDP = GDP.drop([0,1],axis=0)
    GDP = GDP[['Unnamed: 4','GDP in billions of current dollars.1']]
    GDP.columns = ['quarter', 'gdp']
    GDP = GDP[212:]
    for i in range(len(GDP)-4):
        if ((GDP.iloc[i+1][1] < GDP.iloc[i][1]) & (GDP.iloc[i+1][1] > GDP.iloc[i+2][1]) & (GDP.iloc[i+2][1] < GDP.iloc[i+3][1]) & (GDP.iloc[i+3][1] < GDP.iloc[i+4][1])):
            a = GDP.iloc[i+4][0]
    return a
get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    a = []
    b = 0
    GDP = pd.read_excel('gdplev.xls',skiprows=5)
    GDP = GDP.drop(['Unnamed: 3','Unnamed: 7'],axis=1)
    GDP = GDP.drop([0,1],axis=0)
    GDP = GDP[['Unnamed: 4','GDP in billions of current dollars.1']]
    GDP.columns = ['quarter', 'gdp']
    GDP = GDP[212:]
    for i in range(len(GDP)-4):
        if ((GDP.iloc[i+1][1] < GDP.iloc[i][1]) & (GDP.iloc[i+1][1] > GDP.iloc[i+2][1]) & (GDP.iloc[i+2][1] < GDP.iloc[i+3][1]) & (GDP.iloc[i+3][1] < GDP.iloc[i+4][1])):
            a.append(min([GDP.iloc[i+4][1],GDP.iloc[i][1],GDP.iloc[i+2][1],GDP.iloc[i+1][1],GDP.iloc[i+3][1]]))
            b = GDP['quarter'][GDP['gdp'] == a].tolist()
    return b[0]

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    house = pd.read_csv('City_Zhvi_AllHomes.csv')
    house = house.drop(['Metro','CountyName', 'SizeRank','RegionID'],axis = 1)
    a = house.columns[2:47].tolist()
    house.drop(a, axis = 1, inplace = True)
    house.replace({'State':states},inplace=True)
    years = [n for n in range(2000,2016)] 
    house.set_index(['State','RegionName'],inplace=True)
    house = house.groupby(pd.PeriodIndex(house.columns, freq='q'), axis=1).mean()
    for col in house.columns:
        col1 = col
        col1 = col1.strftime('%Fq%q')
        if col1[4] == 'q':
            house.rename(columns={col:col1}, inplace = True)
    return house
    


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    all_towns = convert_housing_data_to_quarters()
    univer = get_list_of_university_towns()
    start = get_recession_start()
    for val,a in enumerate(all_towns.columns):
        if a == start:
            pos = val-1
    start1 = all_towns.columns[pos]
    bottom = get_recession_bottom()
    all_towns = all_towns[[start1,bottom]]
    all_towns['ratio'] = (all_towns[start1]) - (all_towns[bottom])
    univer['uni'] = True
    all_towns = all_towns.reset_index()
    univers = pd.merge(all_towns, univer,how='inner', on=['State','RegionName'])
    all_towns = pd.merge(univers,all_towns,how='outer',on = [start1,bottom,'State','RegionName','ratio'])
    all_towns = all_towns.fillna(False)
    uni = all_towns[all_towns['uni'] == True]
    non = all_towns[all_towns['uni'] == False]
    s,p = ttest_ind(uni['ratio'],non['ratio'],nan_policy="omit")
    different = False
    if p < 0.01:
        different = True
    else:
        different = False
    meanu = uni['ratio'].mean()
    meann = non['ratio'].mean()
    if meanu > meann:
        better = "non-university town"
    elif meanu < meann:
        better = "university town"
    return (different,p,better)


