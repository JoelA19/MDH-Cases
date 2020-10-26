import requests
import os
from tabulate import tabulate
url = "http://football-frenzy.s3-website.eu-north-1.amazonaws.com/api"

r = requests.get(url)
seasons = r.json()
seasons = seasons["seasons"]
teams= []
line = "-" *30
def errorproof():
  try:
    input("Press enter to continue")
  except KeyboardInterrupt:
    pass
def printseasons():
  os.system("clear")
  print("These are the available seasons:")
  print(line)
  for i in seasons:
      print(i)
  print(line)
  errorproof()

def chooseseason():
    print(line)
    print("which season would you like to view?")
    answer = input(">")
    if answer in seasons:
        yearurl = url + "/" + answer
        year = requests.get(yearurl).json()
        for i in year["teams"]:
            dictionary = {"team": i, "wins": 0 , "losses": 0, "draws": 0, "points": 0}
            teams.append(dictionary)
        for x in year["gamedays"]:
            dayurl = yearurl + "/" + x
            days = requests.get(dayurl).json()
            for a in days["games"]:
                if a["score"]["home"]["goals"] > a["score"]["away"]["goals"]:
                    for team in teams:
                        if team["team"] == a["score"]["home"]["team"]:
                            team["wins"] += 1
                            team["points"]+= 3
                        if team["team"] == a["score"]["away"]["team"]:
                            team["losses"] +=1
                if a["score"]["home"]["goals"] == a["score"]["away"]["goals"]:
                    for team in teams:
                        if team["team"] == a["score"]["away"]["team"]:
                            team["draws"] += 1
                            team["points"]+= 1
                        if team["team"] == a["score"]["home"]["team"]:
                            team["draws"] += 1
                            team["points"]+= 1
        print(line)
        print(" Team Name | Wins | Losses | Draws | Points |")
        print(line)
        def TakePoints(elem):
            return elem["points"]
        teams.sort(key=TakePoints, reverse=True)
        list = []
        for x in teams:
            templist =[x["team"], str(x["wins"]), str(x["losses"]), str(x["draws"]), str(x["points"])]
            list.append(templist)
        print(tabulate(list, headers=["Name", "Wins", "Losses", "Draws", "Points"]))
        print(line)
        errorproof()
    else:
        print("Thats not a valid season, try listing all the available seasons to see which ones you may view.")
        errorproof()
instructions = { 
    "List": printseasons,
    "View": chooseseason,
    "Exit": exit,
}

while True:
    os.system("clear")
    print(line)
    print("List  |  List avaible seasons")
    print("View  |  View table for season")
    print("Exit  |  Exit the program")
    function = input(">").title()
    try: 
        instructions[function]()
    except (KeyError, ValueError):
        print(line)
        print("Error: Invalid input, Try again")
        errorproof()