from bs4 import BeautifulSoup
import requests
import datetime
from xfl_schedule_email import EmailSystem


# using datetime, the date in text month and number day are created
month = datetime.datetime.now()
formatted_m = month.strftime("%B")
day = datetime.datetime.now().day

# joins month and date into one string to be passed as a variable to be used at end of program to append only games being played
# today
combined_time = f"{formatted_m} {day}"

#Constants
URL = requests.get("https://www.xfl.com/schedule/", timeout=60)
TEAMS = ['<sup>Vegas Vipers</sup>', '<sup>Arlington Renegades</sup>', '<sup>Orlando Guardians</sup>', '<sup>Houston Roughnecks</sup>', '<sup>St. Louis Battlehawks</sup>', '<sup>San Antonio Brahmas</sup>',
         '<sup>Seattle Sea Dragons</sup>', '<sup>D.C. Defenders</sup>']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Create BeautifulSoup HTML file  and Hone in on all tags containing 'sup'
SOUP = BeautifulSoup(URL.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
SCHEDULES = SOUP.find_all('sup')


# For loop to remove tags from each side of list item in SCHEDULES before appending it to a new list called CLEANED_SCHEDULE
CLEANED_SCHEDULE = []
for schedule in SCHEDULES:
    if str(schedule) in TEAMS:
        strip_1 = str(schedule).split("<sup>")[1]
        strip_2 = str(strip_1).split("</sup>")[0]

        CLEANED_SCHEDULE.append(strip_2)

# For loop that goes into CLEANED SCHEDULE, locates each team and the opposing team for each game, temporarily assigns
# those teams to first_team and second_team variables and then a flag assigns which team gets placed in the new text variable
# that text variable is formatted with a vs. with each team and amended to the games list, the first and second team variables are
# then cleared
games = []
flag = 0
first_team = ''
second_team = ''
for team in CLEANED_SCHEDULE:
    if flag == 0:
        first_team += team
        flag = 1
    elif flag == 1:
        second_team += team
        games.append(f"{first_team} vs. {second_team}")
        first_team = ''
        second_team = ''
        flag = 0

# This pulls the dates from the SCHEDULES list, cleans the data, then adds it to the Dates list
Dates = []
for schedule in SCHEDULES:
    schedule_conv = str(schedule)
    if "February" in schedule_conv or "January" in schedule_conv or "March" in schedule_conv or "April" in schedule_conv or "May" in schedule_conv:
        split_1 = schedule_conv.split("<sup><strong>")[1]
        split_2 = split_1.split("</strong></sup>")[0]
        Dates.append(split_2)

# This pulls the times from the SCHEDULES list, cleans the data, then adds it to the Times list
Times = []
for schedule in SCHEDULES:
    schedule_conv = str(schedule)
    if "ET" in schedule_conv:
        split_1 = schedule_conv.split("<sup>")[1]
        split_2 = split_1.split("</sup>")[0]
        Times.append(split_2)

# Using the lenth of the Dates list, using the positions in each corresponding list, it merges all information
# such as Teams, Dates, and Times together and appends them to the combined_games list, if the list of any list is longer than
# another (such as championship games with tenative dates) then it simply passes and moves on
current_index = 0
combined_games = []
for i in Dates:
    try:
        game = games[current_index]
        time = Times[current_index]
        combined_games.append(f'{game}: {i} at {time}')
        current_index +=1
    except IndexError:
        pass

# Games being played only today will be checked and added to list sendable_games
sendable_content = []
for games in combined_games:
    if combined_time in games:
        sendable_content.append(games)

# if length of sendable games is greater than 0 it will send corresponding text with game information
# else it simply passes
if len(sendable_content) > 0:
    sender = EmailSystem(message=sendable_content, games=str(len(sendable_content)))
    print("Email or text successfully sent to recipients")
else:
    print("No XFL games are being played today!")
