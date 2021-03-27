# TrainerEffekt
Tracking and calculating the effect(pertaining to final placement and points per game) that managerial firings during the saison had on football clubs

## tldr:

downloading the *** folder and compiling the "readFromExcel.py" within will launch a window application which calculates the effectiveness of managerial firings in 
the bundesliga. The User can specify the date, as well as a range of matchdays and table placings he wants to examine. the programm will than find all the teams
which fired their manager in the specified timeframe (pulling the needed information from excel sheets which i implemented beforehand. for more details see below) and calculate 
their average final placings, as well as their points per game. it then does the same for teams who did not fire their manager in similar situations.


## THE CORE IDEA

When looking at the effect that a managerial firing can have on the performance of a football club, all sources i could find only looked at how the football club itself performed before and after the "sacking" of said manager. I felt that, in order to have a more informed understanding of the so called phenomenon "Trainer Effekt" (at least thats what its called in german), one would also have to look at football clubs which did NOT fire their managers, even though they were in similar situations as the ones that did. So thats what this code does.


## HOW EVERYTHING IS CALCULATED

I have stored every league table entry from every bundesliga season in both excel sheets and sql tables. The code is using the excel sheets, as i find them easier to share with strangers. 

after launching the *** script, a tk window pops up and the user can specify some input parameters. For example,  the user could look at managerial firings that happened from 2010 onwards, and only wanted to count them if they occured from matchdays 20-23 and which where placing fifteenth or worse.
What the script then does is look through the excel sheet which holds all the information on fired managers for every entry which matches the given parameters.
It then counts the total number of fired managers, and stores the placing, season, points, club and the matchday of the firing in an array. Next, using this data it looks at how each stored club finished its given saison, and compares the total number of points from all those clubs with the total number of points they ended the season with (it does the same for the clubs respective placings)

the calculation being done at this point is a simple: 

Points per game:
total number of points at the end of the season - total number of points at moment of firing / number of firings

as well as:

Average Placing:
total league table placings at the end of the season - total league table placings at moment of firing / number of firings

Next, using the values we stored in the array, the script goes through an excel sheet which has every league table entry from every bundesliga season EXCEPT from clubs which fired their manager that season, and finds clubs that where in similar situations during different season. For example, if a manager was fired on matchday 20 while his team was placing fifteenth in 2011, we would store all clubs that were placing fifteenth on matchday 20 in different seasons, so long as those clubs did not also fire their manager at some point during the season.
From here on out its the same procedure as above: count every entry we find and calculate the average point per game as well as average placings.
...

## WHAT EACH SCRIPT DOES

All the actual calculations, as well as the creation of the user interface happen in the readFromExcel.py script. i wrote other scripts to scrap all the info i need from the websites transfermarkt.de and kicker.de. 

fillGefeuerteTrainerSQL.py pulls all the info from managerial firings from the website transfermarkt.de and puts it into a mySQL table. for the script to work properly, the user has to have a working mySQL server and specify the server details within the script

fillAlleSaisontabellenSQL.py does the same, except it straight up takes EVERY entry from from every bundesliga season from kicker.de

Left joining the two sql tables, i then manually created a SQL table which consists of ONLY entrys where the manager was not fired.

readGefeuerteTrainerSQL.py is more of a prove of concept, i abandoned the script as i chose to continue working with excel as opposed to reading the data from sql(again, because its much easier to share with other people this way). its main purpose right now is to prove that i have a decent understanding of SQL queries as well
