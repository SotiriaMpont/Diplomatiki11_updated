import mysql.connector
import script
import mysql.connector
import datetime
import random
import osmium
import requests
import os
import json
import osmnx.distance as distance
import osmnx as ox
import networkx as nx
from random import uniform
import pandas as pd
import numpy as np


                                                     #ΜΕΤΡΙΚΗ ΤΟΥ COSTUMER 
                                                     #βημα 1: κανονικοποίηση των rating_costumer
mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
cursor = mydatabase.cursor()

#selectarw gia na ftiaxw to DataFrame
        
cursor.execute("SELECT * FROM metrics_costumer")

results_metrics_costumer= cursor.fetchall()

#print(results_metrics_costumer)

metrics_costumer_dataframe = pd.DataFrame(results_metrics_costumer, columns=[desc[0] for desc in cursor.description])


# Close the cursor and connection
cursor.close()
mydatabase.close()

# Print the DataFrame
#print(metrics_costumer_dataframe)
metrics_costumer_dataframe.fillna(0, inplace=True) 

#criterion1
metrics_costumer_dataframe['percentile_criterion1'] = metrics_costumer_dataframe['criterion1'].rank(pct=True)
#criterion2
metrics_costumer_dataframe['percentile_criterion2'] =metrics_costumer_dataframe['criterion2'].rank(pct=True)
#criterion3
metrics_costumer_dataframe['percentile_criterion3'] = metrics_costumer_dataframe['criterion3'].rank(pct=True)

num_buckets = 10
bucket_labels = [num_buckets] + list(reversed(range(1, num_buckets))) 

metrics_costumer_dataframe['bucket_percentile_criterion1'] = pd.cut(metrics_costumer_dataframe['percentile_criterion1'], bins=num_buckets, labels=range(1, num_buckets+1))
metrics_costumer_dataframe['bucket_percentile_criterion2'] = pd.cut(metrics_costumer_dataframe['percentile_criterion2'], bins=num_buckets, labels=range(1, num_buckets+1))
metrics_costumer_dataframe['bucket_percentile_criterion3'] = pd.cut(metrics_costumer_dataframe['percentile_criterion3'], bins=num_buckets, labels=range(1, num_buckets+1))

metrics_costumer_dataframe['bucket_percentile_criterion1'] = metrics_costumer_dataframe['bucket_percentile_criterion1'].astype(int)
metrics_costumer_dataframe['bucket_percentile_criterion2'] =metrics_costumer_dataframe['bucket_percentile_criterion2'].astype(int)
metrics_costumer_dataframe['bucket_percentile_criterion3'] = metrics_costumer_dataframe['bucket_percentile_criterion3'].astype(int)

#print(metrics_costumer_dataframe)
#realistika apotelesmata,proxwrame!!!!!!!

#BHMA2: υπολογίζω μετρική για costumer kai insert metrics_costumer
criterion1_weight=2
criterion2_weight=2
criterion3_weight=2

for index, row in metrics_costumer_dataframe.iterrows():   
  total_cost_costumer = 0
  total_cost_costumer += row['bucket_percentile_criterion1'] * criterion1_weight
  total_cost_costumer += row['bucket_percentile_criterion2'] * criterion2_weight
  total_cost_costumer += row['bucket_percentile_criterion3'] * criterion3_weight
  
  #print(total_cost_costumer)    # bgazei noumero twra an einai realistiko den 3erw 
    
  mydatabase = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="diplomatiki11"
  )

    
  cursor = mydatabase.cursor()
   
      
  update_total_cost_metrics = 'UPDATE metrics_costumer SET total_rate_costumer=%s ,criterion1_b=%s,criterion2_b=%s,criterion3_b=%s WHERE distributor_id=%s AND shift=%s'
  values_metriki = (total_cost_costumer,row['bucket_percentile_criterion1'],row['bucket_percentile_criterion2'],row['bucket_percentile_criterion3'], row['distributor_id'], row['shift'])
  cursor.execute(update_total_cost_metrics, values_metriki)
  mydatabase.commit()
  

  
  
#Μετρική για τo rating απο το store

#βημα1: κανονικοποίηση των βαθμολογιών  του store

                                                     #βημα 1: κανονικοποίηση των rating_costumer
mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
cursor = mydatabase.cursor()

#selectarw gia na ftiaxw to DataFrame
        
cursor.execute("SELECT * FROM metrics_store")

results_metrics_store= cursor.fetchall()
#ok
#print(results_metrics_store)

metrics_store_dataframe = pd.DataFrame(results_metrics_store, columns=[desc[0] for desc in cursor.description])


# Close the cursor and connection
cursor.close()
mydatabase.close()

# Print the DataFrame
#print(metrics_store_dataframe)
metrics_store_dataframe.fillna(0, inplace=True) 

metrics_store_dataframe['percentile_Rating_Stores'] = metrics_store_dataframe['Rating_stores'].rank(pct=True)

num_buckets = 10
bucket_labels = [num_buckets] + list(reversed(range(1, num_buckets)))

metrics_store_dataframe['bucket_percentile_Rating_Stores'] = pd.cut(metrics_store_dataframe['percentile_Rating_Stores'], bins=num_buckets, labels=range(1, num_buckets+1))

metrics_store_dataframe['bucket_percentile_Rating_Stores'] = metrics_store_dataframe['bucket_percentile_Rating_Stores'].astype(int)

#print an douleiei

#kanei print , swsta apotelesmata opws fainetai 
#print(metrics_store_dataframe)


#Bημα2: βρισκω μετρικη για κάθε κριτική διανομέα από το κατάστημα με βάση το rating, insert metrics_store
rating_store_weight=2 

for index, row in metrics_store_dataframe.iterrows():   
  total_cost_store = 0
  total_cost_store+= row['bucket_percentile_Rating_Stores'] * rating_store_weight
 
  
  #print(total_cost_store)    # bgazei noumero twra an einai realistiko den 3erw 
    
  mydatabase = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="diplomatiki11"
  )

    
  cursor = mydatabase.cursor()
   
   #pernaei swsta tis times   
  update_total_cost_metrics = 'UPDATE metrics_store SET total_rate_store=%s , Rating_Stores_b=%s WHERE distributor_id=%s AND shift=%s'
  values_metriki = (total_cost_store,row['bucket_percentile_Rating_Stores'], row['distributor_id'], row['shift'])
  cursor.execute(update_total_cost_metrics, values_metriki)
  mydatabase.commit()
  

  
                                      #Υπολογισμός μετρικής για το Company
                                    
#Βημα1: κανονικοποίηση 


                                                     
mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
cursor = mydatabase.cursor()

#selectarw gia na ftiaxw to DataFrame
        
cursor.execute("SELECT * FROM metrics_company")

results_metrics_company= cursor.fetchall()
#ok
#print(results_metrics_store)

metrics_company_dataframe = pd.DataFrame(results_metrics_company, columns=[desc[0] for desc in cursor.description])


# Close the cursor and connection
cursor.close()
mydatabase.close()

# Print the DataFrame
#print(metrics_company_dataframe)
metrics_company_dataframe.fillna(0, inplace=True) 

metrics_company_dataframe['percentile_Rate_Company'] = metrics_company_dataframe['Rate_Company'].rank(pct=True)

num_buckets = 10
bucket_labels = [num_buckets] + list(reversed(range(1, num_buckets)))

metrics_company_dataframe['bucket_percentile_Rate_Company'] = pd.cut(metrics_company_dataframe['percentile_Rate_Company'], bins=num_buckets, labels=range(1, num_buckets+1))

metrics_company_dataframe['bucket_percentile_Rate_Company'] = metrics_company_dataframe['bucket_percentile_Rate_Company'].astype(int)


#print(metrics_company_dataframe)


#Bημα2: βρισκω μετρικη για κάθε κριτική διανομέα από την εταιρεία με βάση το rating, insert metrics_company 
rating_company_weight=2 

for index, row in metrics_company_dataframe.iterrows():   
  total_cost_company = 0
  total_cost_company+= row['bucket_percentile_Rate_Company'] * rating_company_weight
 
  
  #print(total_cost_company )    
    
  mydatabase = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="diplomatiki11"
  )

    
  cursor = mydatabase.cursor()
   
   #pernaei swsta tis times   
  update_total_cost_metrics = 'UPDATE metrics_company SET total_rate_company=%s , Rate_Company_b=%s WHERE distributor_id=%s AND shift=%s'
  values_metriki = (total_cost_company,row['bucket_percentile_Rate_Company'], row['distributor_id'], row['shift'])
  cursor.execute(update_total_cost_metrics, values_metriki)
  mydatabase.commit()
  
                   #metriki gia to overhead, sinepeia stin enarxi/lixi , average_distance (dld twn xaraktiristikwn twn dianomewn pou xw  sto metrics)

#ΒΗΜΑ1 : κανονικοποιηση



mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
cursor = mydatabase.cursor()

#selectarw gia na ftiaxw to DataFrame
        
cursor.execute("SELECT * FROM metrics")
        
#fetch apotelesmata kai ftiaxnw DataFrame 
results_metrics = cursor.fetchall()

metrics_dataframe = pd.DataFrame(results_metrics, columns=[desc[0] for desc in cursor.description])


# Close the cursor and connection
cursor.close()
mydatabase.close()

# Print the DataFrame
#print(metrics_dataframe)

metrics_dataframe.fillna(0, inplace=True) # mpas kai glitwsw to error
# ftiaxnw stili sto dataframe percentile_rank_avg_dist kai kanei rank me basi to average_distance_k tou metrics (lowest rank 1, highest 10)
metrics_dataframe['percentile_rank_avg_dist'] = metrics_dataframe['average_distance_k'].rank(pct=True)
#overhead
metrics_dataframe['percentile_overhead'] = metrics_dataframe['overhead_real'].rank(pct=True)
#sunepeia exarxi 
metrics_dataframe['percentile_supenepeia_enarxi'] = metrics_dataframe['sunepeia_enarxi'].rank(pct=True)
#sunepeia lixi
metrics_dataframe['percentile_sunepeia_lixi'] = metrics_dataframe['sunepeia_lixi'].rank(pct=True)

num_buckets = 10
bucket_labels = [num_buckets] + list(reversed(range(1, num_buckets)))

metrics_dataframe['bucket_avg_dist'] = pd.cut(metrics_dataframe['percentile_rank_avg_dist'], bins=num_buckets, labels=range(1, num_buckets+1))
#bucket overhead
metrics_dataframe['bucket_overhead'] = pd.cut(metrics_dataframe['percentile_overhead'], bins=num_buckets, labels=range(1, num_buckets+1))
#sunepeia_enarxi
metrics_dataframe['bucket_sunepeia_enarxi'] = pd.cut(metrics_dataframe['percentile_supenepeia_enarxi'], bins=num_buckets, labels=range(1, num_buckets+1))
#sunepeia_lixi
metrics_dataframe['bucket_sunepeia_lixi'] = pd.cut(metrics_dataframe['percentile_sunepeia_lixi'], bins=num_buckets, labels=range(1, num_buckets+1))

metrics_dataframe['bucket_overhead'] = metrics_dataframe['bucket_overhead'].astype(int)
metrics_dataframe['bucket_avg_dist'] = metrics_dataframe['bucket_avg_dist'].astype(int)
metrics_dataframe['bucket_sunepeia_enarxi'] = metrics_dataframe['bucket_sunepeia_enarxi'].astype(int)
metrics_dataframe['bucket_sunepeia_lixi'] = metrics_dataframe['bucket_sunepeia_lixi'].astype(int)

#print(metrics_dataframe)

#βημα2: υπολογιζω rate_metrics και update metrics table 
avg_dist_weight = 2
overhead_weight = 2
startwork_diff_weight = 2
endwork_diff_weight = 2

for index, row in metrics_dataframe.iterrows():   
    total_cost_metrics = 0
    total_cost_metrics += row['bucket_avg_dist'] * avg_dist_weight
    total_cost_metrics += row['bucket_overhead'] * overhead_weight
    total_cost_metrics += row['bucket_sunepeia_enarxi'] * startwork_diff_weight
    total_cost_metrics += row['bucket_sunepeia_lixi'] * endwork_diff_weight
   
    
    #print(total_cost_metrics)    # bgazei noumero twra an einai realistiko den 3erw 
    
    mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
    cursor = mydatabase.cursor()
   
    update_query = "UPDATE metrics SET metrics_rate=%s, overhead = %s ,difference_time_startshift_accepted=%s,difference_time_endshift_accepted=%s,  average_distance=%s WHERE distributor_id = %s AND shift = %s"
    values = (total_cost_metrics,row['bucket_overhead'],row['bucket_sunepeia_enarxi'],row['bucket_sunepeia_lixi'],row['bucket_avg_dist'], row['distributor_id'], row['shift'])
    cursor.execute(update_query, values)

# commit the changes and close the connection
mydatabase.commit()
mydatabase.close()

      
 # Yπολογισμος total_rate= cost_costumer+cost_metrics+ cost_company+ cost_store
   
#Βημα1: Φτιάχνω ένα dataframe απο τα 4 που'χω (παίρνει μονο τα colums ΠΟΥ ΘΕΛΩ απο τα dataframes που έχουν κοινά distributor_id, shift )

# merge the metrics_customer and metrics_store dataframes on distributor_id and shift columns
merged_df = pd.merge(metrics_costumer_dataframe, metrics_store_dataframe, on=['distributor_id', 'shift'])

# merge the merged_df with the metrics_driver dataframes on distributor_id and shift columns
merged_df = pd.merge(merged_df, metrics_dataframe, on=['distributor_id', 'shift'])

# merge the merged_df with the metrics_vehicle dataframes on distributor_id and shift columns
merged_df = pd.merge(merged_df, metrics_company_dataframe, on=['distributor_id', 'shift'])

# select the desired columns from merged_df and group by distributor and shift
grouped_df = merged_df[['distributor_id', 'shift', 'total_rate_costumer', 'total_rate_store', 'total_rate_company', 'metrics_rate']].groupby(['distributor_id', 'shift']).sum()

# add a new column 'total' by summing up the other columns
grouped_df['total'] = grouped_df.sum(axis=1)

# reset index and display the result
dataframe5 = grouped_df.reset_index()
print(dataframe5)

#Exw ton pinaka total (pou exei thn sunoliki metriki )

for index, row in dataframe5.iterrows():   

   
    mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="diplomatiki11"
  )

    
    cursor = mydatabase.cursor()
   
    update_query = "UPDATE metrics SET total_rate=%s WHERE distributor_id = %s AND shift = %s"
    values = (row['total'],row['distributor_id'], row['shift'])
    cursor.execute(update_query, values)

# commit the changes and close the connection
mydatabase.commit()
mydatabase.close()

