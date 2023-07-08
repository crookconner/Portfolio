#%%
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns
#%%
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics
#from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
#%%
dwellings_ml = pd.read_csv('https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_ml/dwellings_ml.csv')
dwellings_ml
#%%
##GRAND QUESTION 1
"""
Create 2-3 charts that evaluate potential relationships between the home variables and before1980.

Finding Correlation between all the variables adn before1980

Dropping some of the variables that are not helpful: before1980, abstrprd
"""
variable_correlations = dwellings_ml.corr(method = 'pearson').before1980.sort_values()

variable_correlations.drop([
  'before1980',
  'abstrprd',
  'yrbuilt'], inplace = True)

variable_correlations = pd.DataFrame(variable_correlations.reset_index())

#%%
# Make the chart
correlation_chart_one = (alt
  .Chart(variable_correlations)
  .mark_bar()
  .encode(
    x = alt.X(
      'before1980',
      axis = alt.Axis(title = 'Correlation')),
    y = alt.Y(
      'index:N',
      axis = alt.Axis(title = 'Variables'),
      sort = None),
    color=alt.condition(
        alt.datum.before1980 > 0,
        alt.value("blue"), 
        alt.value("red") 
    )
  )
  .properties(
    title = 'Relationships Between Home Variables and before1980'
  )
  )

correlation_chart_one.save('predict_chart_one.png')
#%%
# Create second chart
correlation_chart_two = (alt.Chart(variable_correlations)
.mark_circle()
.encode(
  x = alt.X('before1980',
    axis = alt.Axis(title = "Correlation")),
  y = alt.Y('index:N',
    axis = alt.Axis(title = "Variables"), sort = None),
  color = alt.condition(
    alt.datum.before1980 > 0,
    alt.value("blue"),
    alt.value("red")
  )
))

zero = (alt.Chart(variable_correlations)
  .mark_rule()
  .encode(
    x = alt.X("mean(before1980):Q"),
    color = alt.value('green')
  )
  .properties(
    title={
      "text" : ["Relationship Between Variables and before1980"],
      "subtitle" : ["Green Line Represents the Mean"],
      "color": "black",
      "subtitleColor": "green"
    }
  ))

predict_chart_two = correlation_chart_two + zero

predict_chart_two.save('predict_chart_two.png')
#%%
##GRAND QUESTION 2
"""
Can you build a classification model (before or after 1980) that has at least 90% accuracy 
for the state of Colorado to use (explain your model choice and which models you tried)?
"""

#Seperate the data into features and targets
features = dwellings_ml.drop(dwellings_ml.filter(regex = 'before1980|abstrprd|yrbuilt|parcel').columns, axis = 1)
target = dwellings_ml.filter(regex = "before1980")
feature_train, feature_test, target_train, target_test = train_test_split(features, target, test_size = .30)

#%%
# Use the RandomForestclassifier
classifier = RandomForestClassifier()
classifier.fit(feature_train, target_train)
#%%
# Predict using classifier
targets_predicted = classifier.predict(feature_test)

#%%
## GRAND QUESTION 3
features_importance = pd.DataFrame(
    {'feature': feature_train.columns, 
    'importance': classifier.feature_importances_}).sort_values('importance', ascending = False)

feature_chart = (alt.Chart(features_importance.query('importance > .007'))
    .encode(
        alt.X('importance', title = "Importance Value"),
        alt.Y('feature', title = "Feature" ,sort = '-x'))
    .mark_bar()
    .properties(
      title = "Features by Level of Importance"
    ))

feature_chart.save('feature_chart.png')
#%%
## GRAND QUESTION 4
#Test Accuracy
accuracy_score(target_test, targets_predicted)
#%%
# Print classification report and show roc_curve

# 1 = True positive and 0 = True Negative
print(metrics.classification_report(targets_predicted, target_test))

metrics.plot_roc_curve(classifier, feature_test, target_test)
#%%
print(features_importance
    .head(20)
    .to_markdown(index = False))
#%%


#%%
