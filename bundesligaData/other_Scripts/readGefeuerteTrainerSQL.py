# -*- coding: utf-8 -*-
'''
Created on 20.12.2020

@author: Luca_
'''

import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="Luca",
  password="****",
  database="trainerschnitt"
)

mycursor = mydb.cursor()

#Vergleiche Endplatzierungen von Mannschaften, die ihren Trainer feuerten, mit Mannschaften die es in der gleichen Situation nicht taten

_rang = 16;
_spielTag = 24;
_datum = "2009-07-01";

sql_select_Query = "select avg(gefeuert.rang), avg(gefeuert.finalerRang), avg(ungefeuert.rang), avg(ungefeuert.finalePlatzierung) from gefeuerteTrainer as gefeuert, saisontabellenohnegefeuertetrainerA as ungefeuert where (gefeuert.rang > "+str(_rang)+" and ungefeuert.rang > '"+str(_rang)+"') and (matchDay >= "+str(_spielTag)+" and spielTag >= "+str(_spielTag)+") and (gefeuert.datum >= '"+_datum+"' and ungefeuert.datum >= '"+_datum+"');"
mycursor.execute(sql_select_Query)
gefeuerteTrainer = mycursor.fetchall()
print("Total number of rows in saison is: ", mycursor.rowcount)

for row in gefeuerteTrainer:
    print("Durchschnittlicher Rang der Mannschaften, die ihren Trainer entlassen haben. Zum Entlassungszeitpunkt = ", row[0], )
    print("Durchschnittlicher finaler Rang dieser Mannschaften  = ", row[1], )
    print("Durchschnittlicher Rang der Mannschaften, die ihren Trainer nicht entlassen haben. Zum gleichen Zeitpunkt = ", row[2], )
    print("Durchschnittlicher finaler Rang dieser Mannschaften = ", row[3], )

print()


#Vergleiche Punkte Pro Spiel von Mannschaften, die ihren Trainer feuerten, mit Mannschaften die es in der gleichen Situation nicht taten

pps_saison = "2000/2001";
pps_datum = "2000-07-01";
pps_ersterSpielTag = 20;
pps_zweiterSpielTag = 34;
pps_rang = 16;

#gefeuerte Trainer
sql_select_Query = "select count(*), avg((B.punkte-A.punkte)/(B.spielTag-A.spielTag)) from allegefeuertentrainer as A, allesaisontabellen as B where A.club = B.club and A.saison = B.saison and A.rang >= "+str(pps_rang)+" and A.spielTag>="+str(pps_ersterSpielTag)+" and B.spielTag = "+str(pps_zweiterSpielTag)+" and A.datum >= '"+pps_datum+"';"
mycursor.execute(sql_select_Query)
gefeuerteTrainer = mycursor.fetchall()
print("Total number of rows in saison is: ", mycursor.rowcount)

for row in gefeuerteTrainer:
    print("Zähle Punkte von Mannschaften, die ihren Trainer zwischen Spieltag " +str(pps_ersterSpielTag)+ " und Spieltag " +str(pps_zweiterSpielTag)+ " gefeuert haben")
    print("Durchschnittliche Punkte Pro Spiel dieser Mannschaften innerhalb dieses Zeitraums  = ", row[1], )

print() 

#ungefeuerte Trainer
sql_select_Query = "select count(*), avg((B.punkte-A.punkte)/(B.spielTag-A.spielTag)) from saisontabellenohnegefeuertetrainera as A, saisontabellenohnegefeuertetrainerb as B where A.club = B.club and A.saison = B.saison and A.rang >= "+str(pps_rang)+" and A.spielTag>="+str(pps_ersterSpielTag)+" and B.spielTag = "+str(pps_zweiterSpielTag)+" and A.datum >= '"+pps_datum+"';"
mycursor.execute(sql_select_Query)
gefeuerteTrainer = mycursor.fetchall()
print("Total number of rows in saison is: ", mycursor.rowcount)

for row in gefeuerteTrainer:
    print("Zähle Punkte von Mannschaften, die ihren Trainer zwischen Spieltag " +str(pps_ersterSpielTag)+ " und Spieltag " +str(pps_zweiterSpielTag)+ " NICHT gefeuert haben")
    print("Durchschnittliche Punkte Pro Spiel dieser Mannschaften innerhalb dieses Zeitraums  = ", row[1], )
