import pandas as pd
import requests
import matplotlib.pyplot as plt

# First Dataset

event=pd.read_csv('events.csv')
event=event.iloc[:-2746101]
event=event.drop(columns='transactionid')
event=event.dropna()

# Second Dataset

items=pd.read_csv('item1.csv')
items=items.iloc[:-10989999]

# Both Datasets are combined on itemid

combine = pd.merge(event,items,on='itemid', how='inner')

# User Interaction Analysis

combine.drop(columns=['timestamp_x'],inplace=True)
combine.rename(columns={'timestamp_y':'timestamp'},inplace=True)
combine['timestamp']=pd.to_datetime(combine['timestamp'])
combine.set_index('timestamp',inplace=True)
combine.sort_index(inplace=True)
event_overtime=combine.resample('H').size()
plt.figure(figsize=(7,5))
plt.plot(event_overtime.index,event_overtime.values,marker='o',linestyle='-')
plt.title("Events on the Day")
plt.xlabel("Hours of the Day")
plt.ylabel("Number of events")
min_date, max_date = event_overtime.index.min(), event_overtime.index.max()
if min_date == max_date:
    plt.xlim(min_date - pd.Timedelta(days=1), min_date + pd.Timedelta(days=1))
else:
    plt.xlim(min_date - pd.Timedelta(hours=1), max_date + pd.Timedelta(hours=1))
plt.grid(True)
plt.show()

# Item Analysis

most_viewed=combine[combine['event']=='view']['itemid'].value_counts().head(10)
print(most_viewed)
add_to_cart=combine[combine['event']=='addtocart']['itemid'].value_counts().head(10)
print(add_to_cart)
transaction=combine[combine['event']=='transaction']['itemid'].value_counts().head()
print(transaction)

# User Behaviour Analysis

unique_user=combine['visitorid'].nunique()
print(f"unique user: {unique_user}")
user_activity=combine['visitorid'].value_counts().describe()
print(user_activity)

# Segmentation - Segment user based on their behaviour

# Segments

viewers=combine[combine['event']=='view']['visitorid'].unique()
carters=combine[combine['event']=='addtocart']['visitorid'].unique()
transients=combine[combine['event']=='transaction']['visitorid'].unique()

# Segment Analysis

segment={
    "viewers": len(viewers),
    "carters": len(carters),
    "transients": len(transients)
}
print(segment)

# Trend Analysis

viewing=combine[combine['event']=='view'].resample('H').size()
plt.figure(figsize=(7,5))
plt.plot(viewing.index,viewing.values,marker='o',linestyle='-')
plt.title("Views of the Day")
plt.xlabel("Hours of the Day")
plt.ylabel("Number of views")
min_date, max_date = viewing.index.min(), viewing.index.max()
if min_date == max_date:
    plt.xlim(min_date - pd.Timedelta(days=1), min_date + pd.Timedelta(days=1))
else:
    plt.xlim(min_date - pd.Timedelta(hours=1), max_date + pd.Timedelta(hours=1))
plt.grid(True)
plt.show()
carting=combine[combine['event']=='addtocart'].resample('H').size()
plt.figure(figsize=(7,5))
plt.plot(carting.index,carting.values,marker='o',linestyle='-')
plt.title("Add to Cart of the Day")
plt.xlabel("Hours of the Day")
plt.ylabel("Number of Addition to Cart")
min_date,max_date=carting.index.min(),carting.index.max()
if min_date==max_date:
    plt.xlim(min_date-pd.Timedelta(days=1),min_date+pd.Timedelta(days=1))
else:
    plt.xlim(min_date-pd.Timedelta(hours=1),max_date+pd.Timedelta(hours=1))
plt.grid(True)
plt.show()
transacting=combine[combine['event']=='transaction'].resample('H').size()
plt.figure(figsize=(7,5))
plt.plot(transacting.index,transacting.values,marker='o',linestyle='-')
plt.title("Transaction of the Day")
plt.xlabel("Hours of the Day")
plt.ylabel("Number of Transaction")
min_date,max_date=transacting.index.min(),transacting.index.max()
if min_date==max_date:
    plt.xlim(min_date-pd.Timedelta(days=1),min_date+pd.Timedelta(days=1))
else:
    plt.xlim(min_date-pd.Timedelta(hours=1),max_date+pd.Timedelta(hours=1))
plt.grid(True)
plt.show()
event_count=combine['event'].value_counts()
event_count.plot(kind='bar',title='Event Count')
plt.show()
most_viewed.plot(kind='bar',title='Most Viewed Dresses')
plt.show()
combine['visitorid'].value_counts().plot(kind='hist',title='User Activity Distribution')
plt.show()

# Result Generation

views=combine[combine['event']=='view']
v1=views['itemid'].value_counts().idxmax()
v1_count=views['itemid'].value_counts().max()
print(v1_count)
carts=combine[combine['event']=='addtocart']
c1=carts['itemid'].value_counts().idxmax()
c1_count=carts['itemid'].value_counts().max()
print(c1_count)
transact=combine[combine['event']=='transaction']
t1=transact['itemid'].value_counts().idxmax()
t1_count=transact['itemid'].value_counts().max()
print(t1_count)
result=max(v1_count,c1_count,t1_count)

#result finalization

if result==v1_count:
    x=v1
    print(f'Outfit of The Day is: {v1}')
    print("This was the most viewed dress of yesterday")
elif result==c1_count:
    x=c1
    print(f'Outfit of The Day is: {c1}')
    print("This dress was added to cart by most of the people yesterday")
else:
    x=t1
    print(f'Outfit of The Day is: {t1}')
    print("This was the most bought dress of yesterday")

# Sending content to server

analysis_result={
    'most_browsed_dress':str(x)
}
response=requests.post('http://localhost:5000/upload-analysis',json=analysis_result)
if response.status_code==200:
    print("Analysis result uploaded sucessfully")
else:
    print("failed to upload analysis result")

