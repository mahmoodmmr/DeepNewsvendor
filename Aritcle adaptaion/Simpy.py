#!/ usr / bin / env python
# coding : utf -8
# <h1 align =’ center ’> College " Snack " Demand Generation </h1 >
## Simulated Demands for " daily Ice Cream " snack at a hypothetical " university " with __N_students__ students .

get_ipython (). run_line_magic (’matplotlib ’, ’inline ’)

import matplotlib . pyplot as plt
import numpy as np
import pandas as pd
from numpy . random import choice , rand , uniform
import tqdm . notebook as tqdm

# __Scenario :__ A campus of $N$ students , where each student
# 1. Takes 15 hours of classes ( = 5 courses at 3 hours each )
# 2. Obtains lunch either from the " commons " or from one of a number of local food trucks
# 3. Often gets something "on the fly" from an ice cream or coffee vendor

ScheduleTimes = {( ’M’,’W’,’F’):[8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16] , 
    # Military time
    (’T’,’R’) :[8 ,9.5 ,11 ,12.5 ,14 ,15.5] }
    # classes are 1.5 hours on TR

MWF = [8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16]
TR = [8 ,9.5 ,11 ,12.5 ,14 ,15.5]
_demand = 500 # Assuming No Features
RANDOM_SEED = 42
SIM_TIME = 300 # minutes per day
SIM_START = 10. # hours
SIM_END = 15. # hours
N_students = 10 _000
nclasses = 5 # number of courses each student takes
pTR = 2/3 # probability of scheduling a course on a Tuesday or
Thursday

class CollegeStudent ( object ):
""" A template for the features relevant to buying either
ice cream or
hot chocolate for a student at a university with $N$
students """
def __init__ (self , p_NoFeatures = _demand / N_students ):
’’’ Construct the Features that motivate a student to
buy either icecream or hot chocolate ’’’
## Initialize
self . p_MWF = p_NoFeatures / (1- pTR )
self . p_TR = p_NoFeatures / pTR
## Build Schedule
MWF = [8. ,9. ,10. ,11. ,12. ,13. ,14. ,15. ,16.]
TR = [8. ,9.5 ,11. ,12.5 ,14. ,15.5]
self . sched = {’MWF ’:[] , ’TR ’:[]}
for i in range ( nclasses ):
if( rand () < pTR and len ( self . sched [’TR ’]) < 5 ):
## Force at least one MWF course -- if all
courses are TR ,
## then no times on MWTRF that student goes to
vendor
crse = choice (TR)
self . sched [’TR ’]. append ( crse )
TR. remove ( crse )
else :
crse = choice (MWF )
self . sched [’MWF ’]. append ( crse )
MWF . remove ( crse )
if( len ( self . sched [’MWF ’]) > 0 ): self . sched [’MWF ’].
sort ()
if( len ( self . sched [’TR ’] ) > 0 ): self . sched [’TR ’ ].
sort ()
## pairs start time and menu choice
self . FoodOps = dict () # At most 1 per day
for day in [’M’,’T’,’W’,’R’,’F’]:
self . FoodOps [day ] = []
daydur = (’MWF ’ ,1.0) if day in [’M’,’W’,’F’] else
(’TR ’ ,1.5)
ndurs = len ( self . sched [ daydur [0]])
if( ndurs == 0): continue
## Food Ops between 10 a.m. and 3 p.m.
if( self . sched [ daydur [0]][0] > SIM_START ):
self . FoodOps [day ]. append ( ( SIM_START , self .
sched [ daydur [0]][0] ) )
for i in range ( ndurs ):
start_time = max (10 , self . sched [ daydur [0]][ i] +
daydur [1])
if( i+1 < ndurs ):
63end_time = min( SIM_END , self . sched [ daydur
[0]][ i +1])
else :
end_time = SIM_END
if( start_time < end_time ):
self . FoodOps [day ]. append ( ( start_time ,
end_time ) )
def GetSnackTime (self ,day):
## Negative if no snack time available that day
if( len ( self . FoodOps [day ]) > 0):
snackperiod = self . FoodOps [ day ][ choice ( range ( len(
self . FoodOps [day ])))]
return np. round ( uniform (* snackperiod ) ,4)
else :
return -1
def BuyIceCream (self , day , FeatureScales = None , ignore =
False ): # does student buy ice cream at time t
""" Student Decides to buy ice cream or not:
returns Number_purchased """
if( day in [’T’,’R’] ):
p = self . p_TR
else :
p = self . p_MWF
odds = p/(1 -p) ## Features increase or decrease the
odds
if( len ( self . FoodOps [day ]) == 0):
return 0 ## Nothing purchased this day
if( not ignore ): # Ignore all features other than
what day it is
## Features Scale Proportionally
WinLen = 0
for per in self . FoodOps [day ]:
WinLen += 60*( per [1] - per [0]) ## in minutes
odds = odds * WinLen / SIM_TIME ## restricted
opporunity decreases the odds
if(np. iterable ( FeatureScales ) ):
for scaler in FeatureScales :
odds *= scaler # scalers are positive (
not zero )
p = odds /( odds + 1) # tranform back to a probability
if( rand () < p):
return 1 # buys one ice cream
else :
return 0
def __repr__ ( self ):
return self . sched . __repr__ () + ’\n’ + self . FoodOps .
__repr__ ()
64# create an instance
# Fred = CollegeStudent ()
# Fred . GetSnackTime (’M ’)
# Fred . BuyIceCream (’M ’)
# Weather data for a semester
DailyData = pd. read_csv (’ETSU2020 -2021 AcademicYear .csv ’,
index_col =0)
DailyData . head (100)
columns = DailyData . columns
WkDays = [’M’,’T’,’W’,’R’,’F’]*100
DailyData [’Day ’] = WkDays [: len( DailyData )]
DailyDf = DailyData [[ ’Day ’,’Maximum Temperature ’, ’Minimum
Temperature ’, ’Wind Chill ’, ’Heat Index ’, ’ Precipitation ’,
’Wind Speed ’, ’Cloud Cover ’, ’Relative Humidity ’]]
DailyDf . head ()
# fill up missing data
DailyDf [’Wind Chill ’]. fillna ( DailyDf [’Heat Index ’], inplace =
True )
DailyDf [’Wind Chill ’]. fillna ( DailyData . Temperature , inplace =
True )
DailyDf . columns = [’Day ’,’Tmax ’,’Tmin ’,’FeelsLike ’,’HeatIndex ’
,’ Precipitation ’,’WindSpeed ’,
’CloudCover ’,’ RelativeHumidity ’]
DailyDf . drop (’HeatIndex ’,axis =1, inplace = True )
DailyDf
DailyDf . head ()
# temperature model
Tmin = 60
Tmax = 80
Am = ( Tmax - Tmin )/2
Mn = ( Tmax + Tmin )/2
= np.pi /(60*12) #t in minutes
Temp = lambda t: Mn+Am*np.cos ( *(t -17*60) )
tran = np. linspace (0 ,24 ,1000)
plt. plot (tran , Temp (60* tran ))
= np.pi /(60*12) # time in minutes
# temp at any given time
def TempAtTime (t, tempran ):
Tmin , Tmax = tempran
Am = ( Tmax - Tmin )/2
Mn = ( Tmax + Tmin )/2
return Mn+Am*np.cos ( *(t -17*60) ) #max at 5 p.m. (so min
at 5 a.m.)
IC_ran = (40 ,110)
# HC_ran = (70 , -20)
65# temp to odds
def TempToScaler (temp , ran , = 0.1 ):
p = ( temp - ran [0]) /( ran [1] - ran [0])
return 1+ *np. tanh (p -0.5)
TempToScaler (100 , IC_ran )
# In[ ]:
# features to odds
def PrecipToScaler_IC (precip , = 0.1) :
return np. exp(- * precip )
def PrecipToScaler_HC (precip , = 0.1) :
return np. exp( * precip )
def WindSpeedToScaler_IC ( windspeed , = 0.01) :
return np. exp(- * windspeed )
def CloudCoverToScaler_IC (CC , = 0.1 ):
p = 1-CC /100
return 1+ *np. tanh (p -0.5)
def CloudCoverToScaler_HC (CC , = 0.1) :
p = CC /100
return 1+ *np. tanh (p -0.5)
def RelativeHumidityToScaler (RH , = 0.1) :
p = RH /100
return 1+ *np. tanh (p -0.5)
## Generate Demands -- Single Instance of Schedules
CollegeStudents = [ CollegeStudent () for __ in range ( N_students
)]
WeekDays = [’M’,’T’,’W’,’R’,’F’]
FeaturesAndDemands = DailyDf . copy ()
FeaturesAndDemands [’Demand ’] = np. zeros (len( DailyDf ))
pd. DataFrame ( columns = [ ’Day ’,’Tmax ’,’Tmin ’,’FeelsLike ’,’
Precipitation ’,’WindSpeed ’,
’CloudCover ’,’
RelativeHumidity
’, ’Demand ’
],
index = DailyDf . index )
fdmax = np. zeros (6)
fdmin = 1e10*np. ones (6)
for idx , row in tqdm . tqdm ( DailyDf . iterrows () , total = DailyDf .
shape [0]) :
FeatureScalars = np. array (
[ PrecipToScaler_IC (row. Precipitation )
,
WindSpeedToScaler_IC (row . WindSpeed ),
CloudCoverToScaler_IC ( row. CloudCover
),
RelativeHumidityToScaler (row .
RelativeHumidity ),
TempToScaler (row . FeelsLike , IC_ran ),
661.0 ] ) # for Max , Min temp scaling
Tmax = row . Tmax
Tmin = row . Tmin
n_purchases = 0
for student in CollegeStudents :
snackTemp = TempAtTime ( student . GetSnackTime (row.Day),
(Tmin , Tmax ))
FeatureScalars [ -1] = TempToScaler ( snackTemp , IC_ran )
n_purchases += student . BuyIceCream ( row.Day ,
FeatureScales = FeatureScalars )
FeaturesAndDemands .loc[idx ,’Demand ’] = n_purchases
fdmax = np. maximum ( FeatureScalars , fdmax )
fdmin = np. minimum ( FeatureScalars , fdmin )
FeaturesAndDemands . head (15)
fdmin , fdmax
FeatureScalars
FeaturesAndDemands . tail (20)
## Multiple Instances of Schedules to create Demands
FeaturesAndDemands = DailyDf . copy ()
for i in tqdm . trange (100) :
CollegeStudents = [ CollegeStudent () for __ in range (
N_students )]
FeaturesAndDemands [’Demand %s’%i] = np. zeros (len( DailyDf ))
pd. DataFrame ( columns = [ ’Day ’,’Tmax ’,’Tmin ’,’FeelsLike ’,
’ Precipitation ’,’WindSpeed ’,
’CloudCover
’,’
RelativeHumidity
’, ’
Demand ’
],
index = DailyDf . index )
fdmax = FeatureScalars
fdmin = FeatureScalars
for idx , row in tqdm . tqdm ( DailyDf . iterrows () , total =
DailyDf . shape [0] , leave = False ):
FeatureScalars = np. array (
[ PrecipToScaler_IC (row.
Precipitation ),
WindSpeedToScaler_IC (row .
WindSpeed ),
CloudCoverToScaler_IC ( row.
CloudCover ),
RelativeHumidityToScaler (row.
RelativeHumidity ),
TempToScaler (row . FeelsLike ,
IC_ran ),
1.0 ] ) # for Max , Min temp
scaling
Tmax = row . Tmax
Tmin = row . Tmin
n_purchases = 0
67for student in CollegeStudents :
snackTemp = TempAtTime ( student . GetSnackTime (row.
Day), (Tmin , Tmax ))
FeatureScalars [ -1] = TempToScaler ( snackTemp ,
IC_ran )
n_purchases += student . BuyIceCream ( row.Day ,
FeatureScales = FeatureScalars )
FeaturesAndDemands .loc[idx ,’Demand %s’%i] = n_purchases
fdmax = np. maximum ( FeatureScalars , fdmax )
fdmin = np. minimum ( FeatureScalars , fdmin )
## This Will Take Approximately 3(100) = 300 minutes (5 hours )
FeaturesAndDemands . head (10)
one_hot = pd. get_dummies ( FeaturesAndDemands [’Day ’])
FeaturesAndDemands = FeaturesAndDemands . drop (’Day ’ , axis = 1)
FeaturesAndDemands = FeaturesAndDemands . join ( one_hot )
FeaturesAndDemands . head (10)
cols = list ( FeaturesAndDemands . columns . values )