#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - [No-show appointments]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# In this project we will be analyzing Data associated with medical appointments we will use a 100k-appintments data to help us understand how the Different factors in the data set affects the probability of the patients to show in the scheduled appointments.
# 
# 
# ### Question(s) for Analysis
# One of the questions that we will go through is: how a specific Disease, Age Range, Gender or neighborhood would increase the probability of the patient to not to show up in the scheduled appointments.
# hence, we would predict if a patient will show up for their scheduled appointment or not.

# In[2]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# In[3]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.1')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# 
# 

# In[4]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')


# In[5]:


df.head(50)


# In[6]:


df.info()


# In[7]:


df.describe()


# In[8]:


df.duplicated().sum()


# In[9]:


df['PatientId'].nunique()


# In[10]:


df['PatientId'].duplicated().sum()


# In[11]:


df.duplicated(['PatientId','No-show']).sum()


# 
# ### Data Cleaning
# First step in Cleaning i searched for duplication and i found nun.
# Second i checked for duplication in Patient iD, ifound 62299 duplicate values, then i checked for duplication with the same No show status, i found 38710 so i dropped them
# Third , i dropped some columns that i see less important and might be distracting like (PatientId, AppointmentID ,ScheduledDay, AppointmentDay)
# Forth i found that there are more than 3k "0" values in Age columns which is non-sense and apparently it was mistakenly entered, so i replaced the "0" values with mean of the Age.
# Finally i corrected the name of the column: Hipertension and last cloumn "No-show" to "No_show" because the - is being treated as an operator.

# In[12]:


df.drop_duplicates(['PatientId','No-show'],inplace=True)


# In[13]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
df.drop(['PatientId','AppointmentID', 'ScheduledDay','AppointmentDay']
,axis=1, inplace=True)


# In[14]:


df.head()


# In[15]:


mean=df.Age.mean()
df['Age'] = df['Age'].replace([0,-1],mean)


# In[16]:


df=df.rename(columns = {'No-show' : 'No_show'})
df=df.rename(columns = {'Hipertension' : 'hypertension'})
df.head()


# In[17]:


showed = df.No_show == 'No'
didnt_show= df.No_show== "Yes"
df[showed].count(),df[didnt_show].count()


# In[18]:


df[showed].mean()


# In[19]:


df[didnt_show].mean()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. **Compute statistics** and **create visualizations** with the goal of addressing the research questions that you posed in the Introduction section. You should compute the relevant statistics throughout the analysis when an inference is made about the data. Note that at least two or more kinds of plots should be created as part of the exploration, and you must  compare and show trends in the varied visualizations. 
# 
# 
# 
# > **Tip**: - Investigate the stated question(s) from multiple angles. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables. You should explore at least three variables in relation to the primary question. This can be an exploratory relationship between three variables of interest, or looking at how two independent variables relate to a single dependent variable of interest. Lastly, you  should perform both single-variable (1d) and multiple-variable (2d) explorations.
# 
# 
# ### Research Question 1 (Does Age Affect The attendance!)

# In[20]:


df['Age'][showed].hist(color='blue',label='showed')
df['Age'][didnt_show].hist(color='red',label='didnt_show')
plt.legend();
plt.title('attendance to age relatioship')
plt.xlabel('Age')
plt.ylabel('No. of Patients');


# In[21]:



###the figure shows that people in the lower & mid age levels to the late 60's are more keen to tattend appointments.###


# ### Research Question 2  (Does chronic diseases affect attendance!)
# 

# In[22]:


df[showed].groupby('hypertension').mean()['Age'].plot(kind='bar',color='blue',label='showed')
df[didnt_show].groupby('hypertension').mean()['Age'].plot(kind='bar',color='red',label='didnt_show')
plt.legend();
plt.title('attendance to hypertension')
plt.xlabel('disease or no disease')
plt.ylabel('Age');


# In[23]:


df[showed].groupby('Diabetes').mean()['Age'].plot(kind='bar',color='blue',label='showed')
df[didnt_show].groupby('Diabetes').mean()['Age'].plot(kind='bar',color='red',label='didnt_show')
plt.legend();
plt.title('attendance to Diabetes')
plt.xlabel('disease or no disease')
plt.ylabel('Age');


# In[24]:


#there's a positive corolation between diseases and attendance but it's not that significant as the the disease it self isn't the main driver fot absense


# In[25]:


#testing if Gender Has impact on absense, conclusion is Gender does not affect absense as the percentatges between the show and no show cases are alomst identical 
df[showed].groupby('Gender')['No_show'].count(), df[didnt_show].groupby('Gender')['No_show'].count()


# In[29]:


#sms and it's correlation with attendance
df['SMS_received'][showed].hist(color='blue',label='showed')
df['SMS_received'][didnt_show].hist(color='red',label='didnt_show')
plt.legend();
plt.title('attendance to age relatioship')
plt.xlabel('SMS_received')
plt.ylabel('No. of Patients');


# In[24]:


#this figure shows that there is a negative correlation between receiving sms and attending the appointment


# In[68]:


df.Neighbourhood[showed].value_counts().plot.bar(figsize=[15,5],label='Showed', color='orange')
df.Neighbourhood[didnt_show].value_counts().plot.bar(figsize=[15,5],label='didnt_Show',color='black')
plt.legend();
plt.title('Neighbourhood to attendance')
plt.xlabel('Neighbourhood')
plt.ylabel('No. of Patients');


# In[ ]:


#neighbourhoods show to affect the attendance status


# In[60]:


#does sms affect the attendance differently according to neighbourhood?
df[showed].groupby('Neighbourhood').SMS_received.mean().plot.bar(figsize=[15,5],color='yellow')
df[didnt_show].groupby('Neighbourhood').SMS_received.mean().plot.bar(figsize=[15,5],color='black')
plt.legend();
plt.title('affect of SMS on the Different neighbouhoods')
plt.xlabel('Neighbourhood, SMS')
plt.ylabel('No. of Patients');


# In[48]:


#does sms affect the attendance differently according to neighbourhood?
df[showed].groupby('Neighbourhood').SMS_received.mean().hist();
df[didnt_show].groupby('Neighbourhood').SMS_received.mean().hist();
plt.legend();
plt.title('Neighbourhood, SMS to attendance')
plt.xlabel('Neighbourhood, SMS')
plt.ylabel('No. of Patients');


# In[79]:


#the figure shows different sms impact on neighbourhoods as we can see there are 2 neighbourhoods have a 100% attendance to sms 
#ratio which makes us question is the sms message unified or it differs from neighbourhood ro another/


# <a id='conclusions'></a>
# ## Conclusions
# 
# 1-Neighbouhood has a direct impact to attendance, as the number of specific neighbourhoods is greater than another neighbourhodos
# 
# 2-Age also has an impact as we saw from 0> to 8 are the most attended age range which means that parents are keen to attend the appointments with their children in the very first years of their lives
# 
# 3-the SMS impact on the attendance seems to be negative (only positive in two neighbourhoods) which indicates a needed action regarding the SMS campaign
# 

# In[80]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




