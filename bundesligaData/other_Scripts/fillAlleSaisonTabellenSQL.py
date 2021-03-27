# -*- coding: utf-8 -*-
'''
Created on 21.12.2020

@author: Luca_
'''

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS
import mysql.connector


def erhaltePlatzierung(zeilenNummer):
    rang = zeilenNummer-1
    return rang


def erhalteClubNamen(zeilenNummer):
    zuDurchsuchendesElement = soup.select("#\\31  > div > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td.kick__table--ranking__teamname.kick__table--ranking__index.kick__t__a__l.kick__respt-m-o-4.kick__respt-m-w-120.kick__t__a__l > a > span.kick__table--show-desktop")
    if(zuDurchsuchendesElement):
        for gesuchterWert in zuDurchsuchendesElement:
            try:
                clubName = gesuchterWert.get_text().strip().split("(",maxsplit=1)[0]
                clubName = clubName.replace("*","")
                if (clubName[len(clubName)-1]==" "):
                    clubName = clubName[:len(clubName)-1]
                return clubName
            except:
                print("Error")
    else:
        print("durchPlatzierungenIterieren DEBUG ENDE")
        return None

def erhalteSiege(zeilenNummer):
    zuDurchsuchendesElement = soup.select("#\\31  > div > table > tbody > tr:nth-child("+str(zeilenNummer)+") > td:nth-child(6) > span.kick__table--show-desktop")
    if(zuDurchsuchendesElement):
            for gesuchterWert in zuDurchsuchendesElement:
                try:
                    siege = gesuchterWert.get_text().strip()
                    return siege
                except:
                    print("Error")
    else:
        print("durchPlatzierungenIterieren DEBUG ENDE")
        return None 
    
def erhalteUnentschieden(zeilenNummer):
    zuDurchsuchendesElement = soup.select("#\\31  > div > table > tbody > tr:nth-child("+str(zeilenNummer)+") > td.kick__table--ranking__number.kick__respt-m-w-60.kick__table--show-desktop")
    if(zuDurchsuchendesElement):
            for gesuchterWert in zuDurchsuchendesElement:
                try:
                    unentschieden = gesuchterWert.get_text().strip()
                    return unentschieden
                except:
                    print("Error")
    else:
        print("durchPlatzierungenIterieren DEBUG ENDE")
        return None     
    
def erhaltePunkte(zeilenNummer,jahresZahl):
    if(jahresZahl >= 1995):
        zuDurchsuchendesElement = soup.select("#\\31  > div > table > tbody > tr:nth-child(" + str(zeilenNummer) + ") > td.kick__table--ranking__master.kick__respt-m-o-5")
        if(zuDurchsuchendesElement):
            for gesuchterWert in zuDurchsuchendesElement:
                try:
                    punkte = gesuchterWert.get_text().strip()
                    return punkte
                except:
                    print("Error")
        else:
            print("durchPlatzierungenIterieren DEBUG ENDE")
            return -1 #für spiele vor 1995, als noch 2 punkte system war
    else:
        punkte = (int(erhalteSiege(zeilenNummer))*3) + (int(erhalteUnentschieden(zeilenNummer)*1))
        return punkte


def durchTabellenPlaetzeIterieren(anzahlTabellenPlaetze):
    for betrachteteZeile in range(2,anzahlTabellenPlaetze+2):
        erhaltePlatzierung(betrachteteZeile)
        erhalteClubNamen(betrachteteZeile)
        erhaltePunkte(betrachteteZeile)
        print("")

def erhalteSpieltag(spielTag):
    return spielTag

def erhalteSpieltagsDatum(spielTag,jahr):
        zuDurchsuchendesElement = soup.select("#kick__header > div > div.kick__head-breadcrumb__items > div > span:nth-child(2) > div > select > option:nth-child(" + str(spielTag) + ")")
        if(zuDurchsuchendesElement):
            for gesuchterWert in zuDurchsuchendesElement:
                try:
                    datumsAnfang = gesuchterWert.get_text().strip().split("(",maxsplit=1)[1]
                    datumTagUndMonat = datumsAnfang.strip().split(" ",maxsplit=1)[0]
                    zuUntersuchenderMonatSchritt_1 = datumTagUndMonat.strip().split(".",maxsplit=1)[1]
                    zuUntersuchenderMonat = zuUntersuchenderMonatSchritt_1.split(".",maxsplit=1)[0]
                    zuUntersuchenderTag = datumTagUndMonat.strip().split(".",maxsplit=1)[0]
                    if(int(zuUntersuchenderMonat)>=7):
                        jahresZahl = jahr
                    else:
                        jahresZahl = jahr+1
                    
                    datum = str(jahresZahl)+"-"+zuUntersuchenderMonat+"-"+zuUntersuchenderTag   #datumTagUndMonat+str(jahresZahl)
                    return datum
                except:
                    print("Error")
        else:
            print("durchPlatzierungenIterieren DEBUG ENDE")
            return None



mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="Luca",
    password="****",
    database="trainerschnitt"
)
mycursor = mydb.cursor()


ersteSaison = 1963
letzteSaison = 2021
for jahr in range(ersteSaison,letzteSaison): #1963 einschliesslich, 2021 ausschliesslich
    saisonEnde = str(jahr+1).strip()[2:]
    unvollstaendigeURL = "https://www.kicker.de/bundesliga/tabelle/" + str(jahr) + "-" + str(saisonEnde) 
    momentaneSaison =  str(jahr) + "/" + str(jahr+1)
    print("")
    spieltagRangeEnde = 35
    tabellenRangeEnde = 20
    if(jahr==1963 or jahr==1964):
        spieltagRangeEnde = 31
        tabellenRangeEnde = 18
    if (jahr==1991):
        spieltagRangeEnde=39
        tabellenRangeEnde = 22
    for spielTag in range(1,spieltagRangeEnde): #1 einschliesslich, 35 ausschliesslich
        url = unvollstaendigeURL + "/" + str(spielTag)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BS(html,features="html.parser")
        print (url)
        for tabellenPlatz in range(2,tabellenRangeEnde):
            spiel_Tag = erhalteSpieltag(spielTag)
            datum_ = erhalteSpieltagsDatum(spielTag,jahr)
            platzierung_ = erhaltePlatzierung(tabellenPlatz)
            club_Name = erhalteClubNamen(tabellenPlatz)
            punkte_ = erhaltePunkte(tabellenPlatz,jahr)
            
            print("Club Name: " + club_Name)
            print("Datum: " + datum_)
            print("Spieltag: " + str(spiel_Tag))
            print("Platzierung: " + str(platzierung_))
            print("Punkte: " + str(punkte_))

            print("")
            sql = "INSERT INTO alleSaisonTabellen (club, rang, saison, datum, spielTag, punkte) VALUES ('" + club_Name + "', " + str(platzierung_) + ",'"+str(momentaneSaison)+"', '"+datum_+"', " + str(spiel_Tag) + ", " + str(punkte_) + ");"  
            mycursor.execute(sql)
            print(mycursor.rowcount, "record inserted.")
            mydb.commit()



    
    


    