
                                                     #BHMA1:
#pairnei thn hmerominia thn simerini 
#kanei select apo thn basi thn hmeromhnia pou einai sthn bash apo tis metrikes tou kathe pinaka 
#elegxei an einai mia mera prin 
#an einai mia mera prin (prohgoumenh bardia):

                                                     #BHMA2
# Anathetei ta aitima px oxi random opws thn prwth fora ,estw oti ta anathetei se auton pou exei kaluteri metriki  ta kontinotera aitimata!
    #pws fantazomai oti tha ginei:
      # 1) 'Εστω ότι το κάνει μέσω συνολικής μετρικής !!!
                  # θα πρεπει να κανει σελεκτ για την καθε βαρδια του διανομεα την συνολικη μετρικη!
                  #να αποθηκευει τις μετρικες τοπικα!
                  #να σβηνει απο τον πινακα αιτηματα τα Id dianomea, time_aitimatos 
                  #γενικα να σβηνει καθε πίνακα από το database Και να κραταει εδω τοπικα μονο τις μεταβλητες που θελω να χρησιμοποιησω !!! Ισως θα πρέπει να το κανω στην αρχή 
                  
        # 2) Κάνω την ανάθεση των αιτημάτων στους διανομείς 
        # 3) βαθμολογω random τους διανομεις γι αυτες τις παραδοσεις 
        #  4) καλώ την metrics() 
        # 5) καλω το αρχειο buckets.py και τα αποθηκευω στην βάση  τις τωρινές μετρικές !!!!!!
        #το ξανακανει για την επόμενη μέρα !!!!!!!
import mysql.connector
import datetime
import script

mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="diplomatiki11"
    )


cursor = mydatabase.cursor()

#Παίρνω όλες τις τιμές, ταξιμομημένες με απο την μεγαλύτερη στην μικρότερη μετρική για κάθε κατηγορία
sql = "SELECT * FROM metrics ORDER BY metrics_rate DESC"
cursor.execute(sql)
metrics_results = cursor.fetchall()
mydatabase.commit()
sql = "SELECT * FROM metrics_costumer ORDER BY total_rate_costumer DESC"
cursor.execute(sql)
metrics_costumer_results = cursor.fetchall()
mydatabase.commit()
sql = "SELECT * FROM metrics_company ORDER BY total_rate_company DESC"
cursor.execute(sql)
metrics_company_results = cursor.fetchall()
mydatabase.commit()
sql = "SELECT * FROM metrics_store ORDER BY total_rate_store DESC"
cursor.execute(sql)
metrics_store_results = cursor.fetchall()
mydatabase.commit()
print(metrics_store_results)
#Ταξινομηση διανομέων με βάση κάθε κριτήριο 


#Συγκριση ημερομηνιων 

#Α: παίρνω ημερομηνίες

for row in metrics_results:
        shift= row[1]  #Aυτή που πήρα απο την βάση  
            
print(shift) #δουλευει


today = datetime.datetime.today().strftime('%Y-%m-%d')
yesterday =  datetime.date.today() - datetime.timedelta(days=1)
print(yesterday) #χθεσινη μερα 

#αν η χθεσινη == με αυτη του shift που πηρα προχωράω στην διαδικασία

#καθαριζω την βάση
if(shift==yesterday):
        #σβηνω απο τα αιτήματα που έχω στην βάση τους διανομείς και τις ώρες που τα ανέλλαβαν για να τα ξαναθέσω βάση μετρικών
        cursor = mydatabase.cursor()
        cursor.execute("DELETE id_aitimatos,id_distr,time_aitimatos,date_aitimatos,accepted  FROM Aitima")
        mydatabase.commit()
        
if(shift==yesterday):

        cursor = mydatabase.cursor()
        cursor.execute("DELETE * FROM Shift")
        mydatabase.commit()
        
#ασ μην κανω ακομα delete τα δεδομενα για τους πινακες metrics, metrics_store, metrics_costumer, metrics_comapny 
        
if(shift==yesterday):
        
        cursor = mydatabase.cursor()
        cursor.execute("DELETE * FROM Rating_From_Company")
        mydatabase.commit()

if(shift==yesterday):
        
        cursor = mydatabase.cursor()
        cursor.execute("DELETE * FROM Rating_From_Store")
        mydatabase.commit()
        
if(shift==yesterday):
       
        cursor = mydatabase.cursor()
        cursor.execute("DELETE * FROM Rating_From_Costumer")
        mydatabase.commit()

if(shift==yesterday):
        #δηλώνω ραντομ Shift για διανομείς
        script.Dilwsi_Shift()

        #Aνάθεση αιτημάτων με βάση τις μετρικές αντί για ραντομ 
        #δίνω στον διανομέα με την μεαλύτερη μετρική (έστω την συνολική) το πιο κοντινό αίτημα και περισσότερα αιτήματα

        mydatabase = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="123456789",
                        database="diplomatiki11"
                )

        cursor = mydatabase.cursor()



        # Παiρνω ολα τα αιτήματα ταξιμομημένα απο το μικρότερη προς την μεγαλυτερη απόσταση μεταξύ των locations
        sql_aitima = "SELECT COUNT(id_aitimatos) as count_aitimatwn,id_aitimatos FROM Aitima ORDER BY expected_difference_km"
        cursor.execute(sql_aitima)
        aitimata = [row[0] for row in cursor.fetchall()]     #ta3inomimena aitimata
        mydatabase.commit()
        
        #παίρνω τους διανομείς που δήλωσαν  βάρδια σήμερα,random

        sql_shift = "SELECT COUNT(ID_distributor_shift) as count_distributors,ID_distributor_shift FROM Shift WHERE date_shift = %s"
        val_shift = (today,)
        cursor.execute(sql_shift, val_shift)
        distributors = [row[0],row[1] for row in cursor.fetchall()]
        mydatabase.commit() 

        #γι αυτους τους διανομείς παίρνω τις μετρικές τις χθεσινές έστω απο τον Metrics την total_rate, ταξινομημένα απο την μεγαλύτερη τιμή στην μικρότερη
        for distributor in distributors:
               sql_total_rate = "SELECT total_rate FROM metrics WHERE distributor_id = %s ORDER BY total_rate DESC"
               val= (distributor,)
               cursor.execute(sql_total_rate, val) 
               mydatabase.commit()
               sort_distributors_onshift = [row[0],row[1] for row in cursor.fetchall()]
               mydatabase.commit() 
        
        
        #M aitimata, N dianomeis periptwseis
        #M>N
        
