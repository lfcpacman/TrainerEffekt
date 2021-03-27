# -*- coding: utf-8 -*-
'''
Created on 21.12.2020

@author: Luca_
'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS
import mysql.connector

def durchTeamNamenVonGesuchtenTeamsIterieren(zeilenNummer,saison):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(1)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            try:
                clubName = platzierung.find('img')['alt']
                team_name = clubNamenUmwandeln(clubName)
                print(team_name)
                oldTrainer = entlassenerTrainer(zeilenNummer)
                oldPlacement = platzierungZumEntlassungsZeitpunkt(zeilenNummer)
                datum = entlassungsDatum(zeilenNummer)
                amtsZeit = tageImAmt(zeilenNummer)
                newTrainer = neuerTrainer(zeilenNummer)
                spiel_Tag = spielTag(zeilenNummer)
                newPlacement = platzierungZumTrainerEnde(zeilenNummer)
                pps = ppsDesNeuenTrainers(zeilenNummer)
                saison_ = saison
                print("")
                sql = "INSERT INTO gefeuerteTrainer (club, matchDay, coach, rang, aktuelleSaison, datum, daysInCharge, successor, finalerRang, ppS) VALUES ('" + team_name + "'," + spiel_Tag + ",'" + oldTrainer + "', " + oldPlacement + ", '" + saison_ + "' , '"+datum+"', " + amtsZeit + ", '" + newTrainer + "', " + newPlacement + ", " + pps + ");"  
                mycursor.execute(sql)
                print(mycursor.rowcount, "record inserted.")
                mydb.commit()
                durchTeamNamenVonGesuchtenTeamsIterieren(zeilenNummer+1,saison)
            except:
                durchTeamNamenVonGesuchtenTeamsIterieren(zeilenNummer+1,saison)
    else:
        print("---------------------------------------------------------------------------------------")

def clubNamenUmwandeln(clubName):
    if(clubName=="Bayern Munich"):
        clubName = "Bayern München"
    if(clubName=="TSV 1860 Munich"):
        clubName = "1860 München"
    if (clubName=="1.FC Nuremberg"):
        clubName = "1. FC Nürnberg"
    if (clubName=="SG Dynamo Dresden"):
        clubName = "1. FC Dynamo Dresden"
    if (clubName=="1.FC Kaiserslautern"):
        clubName = "1. FC Kaiserslautern"
    if (clubName=="1.FC Saarbrücken"):
        clubName = "1. FC Saarbrücken"
    if (clubName=="1.FSV Mainz 05"):
        clubName = "1. FSV Mainz 05"
    if (clubName=="Borussia Mönchengladbach"):
        clubName = "Bor. Mönchengladbach"
    if (clubName=="FC Energie Cottbus"):
        clubName = "Energie Cottbus"
    if (clubName=="SC Fortuna Köln"):
        clubName = "Fortuna Köln"
    if (clubName=="FC Hansa Rostock"):
        clubName = "Hansa Rostock"
    if (clubName=="SV Tasmania Berlin"):
        clubName = "SC Tasmania 1900 Berlin"
    if (clubName=="TSG 1899 Hoffenheim"):
        clubName = "TSG Hoffenheim"
    if (clubName=="SV Werder Bremen"):
        clubName = "Werder Bremen"
    if (clubName=="Wuppertaler SV Borussia"):
        clubName = "Wuppertaler SV"    
    if (clubName=="SV Waldhof Mannheim"):
        clubName = "Waldhof Mannheim"   
    return clubName
        
        
def entlassenerTrainer(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(2)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            trainer = platzierung.find('img')['alt']
            print("Entlassener Trainer: " + trainer)
            return trainer
    else:
        print("Ende")
        return None
    
def spielTag(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child("+str(zeilenNummer)+") > td:nth-child(3)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            matchDay = platzierung.get_text()
            print("spieltag: " + matchDay)
            return matchDay
    else:
        print("Ende")
        return None

def platzierungZumEntlassungsZeitpunkt(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(4)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            print("Trainer gefeuert auf Platz: " + platzierung.get_text())
            return platzierung.get_text()
    else:
        print("Ende")
        return None

def entlassungsDatum(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(7)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            datum = datumFuerSqlUmwandeln(platzierung.get_text())
            print("Entlassungs Datum: " + datum)
            return datum
    else:
        print("Ende")
        return None

def tageImAmt(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(8)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            amtsZeit = platzierung.get_text()
            print("Tage im Amt: " + amtsZeit)
            return amtsZeit
    else:
        print("Ende")
        return None

def neuerTrainer(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(9)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            trainer = platzierung.find('img')['alt']
            print("Neuer Trainer: " + trainer)
            return trainer
    else:
        print("Ende")
        return None
        

def platzierungZumTrainerEnde(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(10)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            print("Neuer Trainer endete auf Platz " + platzierung.get_text())
            return platzierung.get_text()
    else:
        print("Ende")
        return None

def datumFuerSqlUmwandeln(datum):
    
    monat = datum.strip()[:3]
    monate=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(len(monate)):
        if(monat==monate[i]):
            monat=str(i+1)
                
    jahr = datum.strip()[6:].split(" ",maxsplit=1)[1]
    tag = datum.strip()[4:].split(",", maxsplit=1)[0]
    endgueltigesDatum = jahr + "-" + monat + "-" + tag
    return endgueltigesDatum        

def ppsDesNeuenTrainers(zeilenNummer):
    platzierungsBehaelter = soup.select("#yw1 > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td:nth-child(11)")
    if(platzierungsBehaelter):
        for platzierung in platzierungsBehaelter:
            print("Neuer Trainer endete mit Punkteschnitt " + platzierung.get_text())
            return platzierung.get_text()
    else:
        print("Ende")
        return None

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="Luca",
    password="anomalisa1",
    database="trainerschnitt"
)
mycursor = mydb.cursor()



for jahr in range(1963,2021): #1963 einschliesslich, 2021 ausschliesslich
    url = "https://www.transfermarkt.com/bundesliga/trainerwechsel/wettbewerb/L1/saison_id/%d/plus/1" % (jahr)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BS(html,features="html.parser")
    print(url)
    saison =  str(jahr) + "/" + str(jahr+1)
    print(saison)
    x = 2
    print("")
    durchTeamNamenVonGesuchtenTeamsIterieren(x,saison)
    



    
    
    
    
    
    
    
    
    