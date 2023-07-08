#%%
import pandas as pd
import numpy as np
import altair as alt
import datadotworld as dw
#%%
# Testing
results = dw.query('byuidss/cse-250-baseball-database',
    'SELECT namefirst, namelast FROM People WHERE playerid = "stephga01"').dataframe
results
#%%
##GRAND QUESTION 1
# Pulls playerID, schoolID, salary, and the yearID/teamID associated with each salary
byui_baseball = dw.query('byuidss/cse-250-baseball-database',
    'SELECT p.playerID, c.schoolID, s.salary, s.yearID, s.teamID '
    'FROM People as p INNER JOIN CollegePlaying as c ON p.playerID = c.playerID '
    'INNER JOIN Salaries as s ON p.playerID = s.playerID '
    'INNER JOIN Schools as sc ON c.schoolID = sc.schoolID '
    'WHERE sc.name_full = "Brigham Young University-Idaho"').dataframe
byui_baseball
#%%
# Prints table
print(byui_baseball
    .head(30)
    .to_markdown(index=False))
#%%
# Create Line Chart
byui_baseball_chart = (alt.Chart(byui_baseball).mark_line()
    .encode(
        alt.X('yearID:O', title = "Year"),
        alt.Y('salary', title = "Salary"),
        color='playerID'
    )
    .properties(
        title={
            "text": ["BYUI Pro Baseball Salaries Over Time"]
        }
    ))
byui_baseball_chart.save('byui_baseball_chart.png')
#%%
## GRAND QUESTION 2
# Part 1 - Query playerID, yearID, and calculate the batting average for everyone who has at least one at bat. h/ab
batting_average_one = dw.query('byuidss/cse-250-baseball-database',
    'SELECT playerID, yearID, h/ab AS batting_average '
    'FROM Batting '
    'WHERE ab >= 1 '
    'ORDER BY batting_average DESC LIMIT 5').dataframe
#%%
#Print to a markdown table
print(batting_average_one
    .head(20)
    .to_markdown(index=False))
#%%
#part 2 - Same query as above but only include those who have at least 10 at bats.
batting_average_ten = dw.query('byuidss/cse-250-baseball-database',
    'SELECT playerID, yearID, h/ab AS batting_average '
    'FROM Batting '
    'WHERE ab >= 10 '
    'ORDER BY batting_average DESC LIMIT 5').dataframe
#%%
#Print above to markdown table
print(batting_average_ten
    .head(20)
    .to_markdown(index=False))
#%%
#Part 3 - Only include those who have at more than 100 at bats combined over their whole career
batting_average_hundred = dw.query('byuidss/cse-250-baseball-database',
    'SELECT playerID, yearID, h/ab AS batting_average '
    'FROM Batting '
    'WHERE ab > 100 '
    'GROUP BY playerID '
    'ORDER BY batting_average DESC LIMIT 5').dataframe
#%%
# Create Markdown table for above
print(batting_average_hundred
    .head(20)
    .to_markdown(index=False))
#%%
##GRAND QUESTION 3
#query from TeamFranchises and Team tables to find the average homeruns for BOS and ATL
compare_home_runs = dw.query('byuidss/cse-250-baseball-database',
    'SELECT tf.franchname ,t.franchid, t.yearid, SUM(t.hr) as Average_Homeruns '
    'FROM Teams as t INNER JOIN TeamsFranchises as tf '
    'ON t.franchid = tf.franchid '
    'WHERE (t.franchid = "BOS" OR t.franchid = "ATL") AND t.yearid > 1979 '
    'GROUP BY t.franchid, t.yearid').dataframe
#%%
#Create Chart for the above query
compare_chart = (alt.Chart(compare_home_runs).mark_line()
    .encode(
        alt.X('yearid:O', title = "Year"),
        alt.Y('Average_Homeruns', title = "Average Homeruns"),
        alt.Color('franchid', title = "Team Code")
    )
    .properties(
        title={
            "text": ["BOS and ATL Home Run Comparison"],
            "subtitle": ["Years 1980 - 2019"]
        }
    ))
#%%


