import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

#database_path = '/Users/karol/Downloads/LaLiga Dashboard/Team and Goalie Database'
db = sqlite3.connect("Team and Goalie Database")
# Connect to the SQLite database
#connection = sqlite3.connect(database_path)

col1, col2= st.columns(2)
with col1:
    st.image("LaLiga.png", width=150)
with col2:
    st.header('Team and Goalie Stats')
    st.write('An overview of the stats for the 2023-2024 season')
    st.write('By Will Adams, Andrew Cyhaniuk, Karol Kusmierczuk, & William Smith')



#st.subheader('Top LaLiga Players')
#tab1, tab2, tab3, tab4 = st.tabs(["Modric", "Lewandowski", "Griezmann", "Bellingham"])
#with tab1:
#    
#   
#with tab2:
#    
#with tab3:
#    st.header("Antoine Griezmann")
#    st.image("Antoine_Griezmann.jpg", width=200)
#with tab4:
#    st.header("Jude Bellingham")
#    st.image("Jude_Bellingham.jpg", width=200)


#Question per tab
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Attacking Third", "Attacking Efficiency", "Corners", "Passing v Big Opportunities",
      "Dominating Possession", "League Defensive Metrics", "Safe Hands", "Dirtiest Teams"])

with tab1: #Attacking Third
    col1, col2= st.columns(2)
    with col1:
        st.header("What is the relationship between possession in the attacking third and successful scoring attempts for teams?")
    with col2:
        st.image("Antoine_Griezmann.jpg", width=200)
        st.subheader("Antoine Griezmann")
    query_8 = "SELECT team, wins, possession_won_final_3rd_per_match, goals,  NTILE(4) OVER (ORDER BY wins DESC) AS win_quartile FROM team_data"
    df8 = pd.read_sql_query(query_8, db)
    #st.dataframe(df8)

    basic_scatter_fig = px.scatter(df8, x="possession_won_final_3rd_per_match", y="goals", color = 'win_quartile', 
                                   hover_data=['team'], trendline="ols")

    st.subheader("Possession in the Attacking Third and Successful Scoring Attempts") 
    basic_scatter_fig.update_layout(xaxis_title= "Possessions in the Attacking Third per Match", 
                                    yaxis_title= "Goals Scored", legend_title=dict(text="New Legend Title"))
    st.plotly_chart(basic_scatter_fig)

    st.write('''The scatter plot exploring the relationship between possession in the attacking third and successful scoring attempts, with an R-squared value of 0.12, suggests only a weak correlation between the two metrics. 
             This indicates that while some teams may convert possession in the attacking third into successful scoring attempts, it is not a consistent pattern across all teams. 
             Teams with high possession but lower scoring attempts may face challenges in creating clear opportunities or finishing them effectively. 
             The weak correlation highlights that simply dominating possession in advanced areas does not guarantee offensive efficiency, emphasizing the importance of quality over quantity in attacking play.''')

with tab2: #Attacking efficiency
    col1, col2= st.columns(2)
    with col1:
        st.header("Which teams exhibit the highest attacking efficiency, scoring the most goals relative to their expected goals?")
    with col2:
        st.image("Robert_Lewandowski.jpg", width=200)
        st.subheader("Robert Lewandowski")
    query_4 = '''SELECT team, goals, expected_goals_scored, goals_per_match, big_chances, big_chances_missed,
     CASE 
        WHEN (goals/expected_goals_scored) >1 THEN 'Over'
        WHEN (goals/expected_goals_scored) =1 THEN 'Expected'
        ELSE 'Under'
    END AS attacking_efficiency_grouping
       FROM team_data'''
    df4 = pd.read_sql_query(query_4, db)
    #st.dataframe(df4)

    st.subheader('Goals Scored vs Expected Goals (xG)')
    st.write('Filter on legend')
    fig = px.bar(df4.sort_values(by='goals', ascending=False), x='team', y=['goals', 'expected_goals_scored'], barmode='group')
    fig.update_layout(xaxis_tickangle=-45, xaxis_title= "Team", yaxis_title= "Goals Scored/Expected", legend_title_text='Legend')
    new_names = {"goals": "Goals Scored", "expected_goals_scored": "Expected Goals"}
    for trace in fig.data:
        if trace.name in new_names:
            trace.name = new_names[trace.name]
    st.plotly_chart(fig)

    df4['expected_goals_per_match'] = df4['expected_goals_scored']/38
    st.subheader('Goals per Match vs Expected Goals per Match')
    fig = px.scatter(df4, x='expected_goals_per_match', y='goals_per_match', hover_data=['team'])
    fig.update_layout(xaxis_title= "Expected Goals per Match", yaxis_title= "Goals per Match")
    st.plotly_chart(fig)

    st.subheader('Attacking Efficiency by Team')
    st.write('Shows a ratio of whether a team scored more or less than their expected goals for the season.')
    st.write('Filter on legend')
    df4['attacking_efficiency'] = df4['goals'] / df4['expected_goals_scored']
    #st.dataframe(df4)
    fig = px.bar(df4.sort_values(by='attacking_efficiency', ascending=False), x='team', 
                 y='attacking_efficiency', color='attacking_efficiency_grouping')
    fig.update_layout(xaxis_tickangle=-45, xaxis_title= "Team", yaxis_title= "Attacking Efficiency", legend_title_text='Legend')
    st.plotly_chart(fig)

    st.subheader('Big Chances Missed by Team')
    fig = px.bar(df4.sort_values(by='big_chances_missed', ascending=False), x='team', y='big_chances_missed')
    fig.update_layout(xaxis_tickangle=-45, xaxis_title= "Team", yaxis_title= "Big Chances Missed")
    st.plotly_chart(fig)

    st.write('''These charts offer insights into how well teams perform relative to their expected performance. 
             The bar chart comparing goals to expected goals shows that 10 out of 20 teams over delivered on expected goals, while the other 10 under delivered, suggesting a balance of teams performing better or worse than anticipated. 
             The scatter plot highlights the relationship between actual and expected goal-scoring, helping to identify teams that are either efficient or lucky in converting opportunities. ''')

with tab3: #Corners
    col1, col2= st.columns(2)
    with col1:
        st.header('''How do the number of corners taken correlate with the success rate of crosses and the amount of goals scored across different teams?''')
    with col2:
        st.image("Luka_Modric.jpg", width=200)
        st.subheader("Luka Modric")
    query_1 = "SELECT team, goals, corners_taken, cross_success_percent FROM team_data"
    df1 = pd.read_sql_query(query_1, db)
    #st.dataframe(df1)

    fig = px.histogram(df1, x="corners_taken")
    fig.update_layout(xaxis_title= "Corners Taken", yaxis_title= "Amount of Teams")
    st.plotly_chart(fig)

    basic_scatter_fig = px.scatter(df1, x='corners_taken', y='cross_success_percent', hover_data=['team'], trendline="ols")
    st.subheader("Corners Taken vs Cross Success Percentage") 
    basic_scatter_fig.update_layout(xaxis_title= "Corners Taken", yaxis_title= "Percent of Successful Crosses")
    st.plotly_chart(basic_scatter_fig)

    basic_scatter_fig = px.scatter(df1, x='corners_taken', y='goals', hover_data=['team'], trendline="ols")
    st.subheader("Corners Taken vs Goals Scored") 
    basic_scatter_fig.update_layout(xaxis_title= "Corners Taken", yaxis_title= "Goals Scored")
    st.plotly_chart(basic_scatter_fig)

    st.write('''
             The first chart displays a histogram showing that there is normal distribution of the amount of corners team took and that most teams fell within the average range for the number of corners taken. 
             This suggests that corner-taking behavior is fairly consistent across teams, with few outliers. 
             When examining the first scatterplot,which compares corners taken to successful crosses, the trend line and an R-squared value of 0.02 indicate that there is virtually no 
             correlation between the number of corners a team takes and their success rate with crosses.
             The second scatterplot shows a better relationship when comparing corners taken to overall goals scored. 
             With an R-squared value of 0.21, there is a weak correlation between the two varibales. 
             While corners may have some influence on goal-scoring, it is not a strong predictor, and teams should focus on a broader set of strategies for improving performance.
             ''')

with tab4: #Passing v big opportunities 
    #query
    col1, col2= st.columns(2)
    with col1:
        st.header("Do teams with more efficient passing get more big opportunities? How do those big opportunities impact game outcomes? ")
    with col2:
        st.image("Pedri.jpg", width=200)
        st.subheader("Pedri")
    query_3 = "SELECT team, big_chances, pass_success_percent, successful_long_balls_percent, wins FROM team_data"
    df3 = pd.read_sql_query(query_3, db)
    #st.dataframe(df3)

    #scatterplots
    passing = st.radio("Passing:", ["Percent of Successful Passes","Percent of Successful Long Balls"])
    if passing == "Percent of Successful Passes":
        basic_scatter_fig = px.scatter(df3, x="big_chances", y="pass_success_percent", hover_data=['team'], trendline="ols")
        st.subheader("Successful Passes Percentage vs Big Opportunities") 
        basic_scatter_fig.update_layout(xaxis_title= "Big Opportunities", yaxis_title= "Successful Passes Percentage")
        st.plotly_chart(basic_scatter_fig)
    else:
        basic_scatter_fig = px.scatter(df3, x="big_chances", y="successful_long_balls_percent", hover_data=['team'], trendline="ols")
        st.subheader("Successful Long Ball Percentage vs Big Opportunities") 
        basic_scatter_fig.update_layout(xaxis_title= "Big Opportunities", yaxis_title= "Successful Long Ball Percentage")
        st.plotly_chart(basic_scatter_fig)

    #opportunity = st.radio("Opportunity:", ["Big Opportunities","Percent of Successful Long Balls"])
    #if opportunity == "Big Opportunities":
    basic_scatter_fig = px.scatter(df3, x="wins", y="big_chances", hover_data=['team'], trendline="ols")
    st.subheader("Big Opportunities vs Wins") 
    basic_scatter_fig.update_layout(xaxis_title= "Wins", yaxis_title= "Big Opportunities")
    st.plotly_chart(basic_scatter_fig)
    #else:
    #    basic_scatter_fig = px.scatter(df3, x="Wins", y="Shot Conversion Rate", hover_data=['team'], trendline="ols")
    #    st.subheader("Shot Conversion Rate vs Wins") 
    #    basic_scatter_fig.update_layout(xaxis_title= "Big Opportunities", yaxis_title= "Successful Long Ball Percentage")
    #    st.plotly_chart(basic_scatter_fig)

    st.write('''Analyzing passing success, long balls, and big opportunities reveals strong correlations with team performance. 
             The scatter plot between passing success and big opportunities shows a moderate positive correlation with an R-squared value of 0.48, suggesting that teams with higher passing accuracy are more likely to create big opportunities. 
             This indicates that efficient passing plays a role in setting up high-quality scoring chances. 
             The scatter plot between successful long balls and big opportunities shows a stronger positive correlation with an R-squared value of 0.67, highlighting that teams with more successful long balls tend to create more big opportunities, which could suggest that long passes are a key tactic in creating high-impact scoring chances. 
             The scatter plot between big opportunities and wins shows a very strong positive correlation with an R-squared value of 0.70, indicating that teams who create more big opportunities are more likely to win, reinforcing the importance of generating high-quality chances for success.
             Overall, four teams stood out from the rest of the league with much higher statistics in this analysis: Barcelona, Real Madrid, Atletico Madrid, and Girona. 
             ''')


with tab5: #Dominating Possession
    #query
    col1, col2= st.columns(2)
    with col1:
        st.header("Which teams dominate possession, and how does possession correlate with match outcomes (wins, goals scored)?")
    with col2:
        st.image("Jude_Bellingham.jpg", width=200)
        st.subheader("Jude Bellingham")
    
    query_2 = "SELECT team, goals_per_match, possession_percent, goals_conceded_per_match, wins FROM team_data"
    df2 = pd.read_sql_query(query_2, db)
    #st.dataframe(df2)

    #scatterplots
    basic_scatter_fig = px.scatter(df2, x='goals_per_match', y='possession_percent', hover_data=['team'], trendline="ols")
    st.subheader("Average Team Percentage of Possession vs Average Goals Scored per Match") 
    basic_scatter_fig.update_layout(xaxis_title= "Average Goals Scored per Match", yaxis_title= "Average Percentage of Possession")
    st.plotly_chart(basic_scatter_fig)

    basic_scatter_fig = px.scatter(df2, x="goals_conceded_per_match", y="possession_percent", hover_data=['team'], trendline="ols")
    st.subheader("Average Team Percentage of Possession vs Average Goals Conceded per Match") 
    basic_scatter_fig.update_layout(xaxis_title= "Average Goals Conceded per Match", yaxis_title= "Average Percentage of Possession")
    st.plotly_chart(basic_scatter_fig)

    basic_scatter_fig = px.scatter(df2, x="wins", y="possession_percent", hover_data=['team'], trendline="ols")
    st.subheader("Average Team Percentage of Possession vs Team Wins") 
    basic_scatter_fig.update_layout(xaxis_title= "Wins", yaxis_title= "Average Percentage of Possession")
    st.plotly_chart(basic_scatter_fig)

    st.write('''The scatter plot between possession percentage and goals per match shows a moderate positive correlation with an R-squared value of 0.47, suggesting that teams with higher possession percentages tend to score more goals. 
            This indicates that dominating possession may contribute to offensive success. 
             On the other hand, the scatter plot between possession percentage and goals conceded per match presents a weaker negative correlation, with an R-squared value of 0.19, suggesting that teams with more possession are slightly less likely to concede goals. 
            This could imply that controlling the ball allows teams to limit the opponent's scoring opportunities. 
            Finally, the scatter plot between possession percentage and wins shows a moderate positive correlation with an R-squared value of 0.48, indicating that teams that dominate possession are more likely to win games. This reinforces the idea that possession is an important factor in a team's overall success.''')

with tab6: #League Defensive Metrics
    col1, col2= st.columns(2)
    with col1:
        st.header("How do defensive metrics (clearances, interceptions, tackles won) vary among the league?")
    with col2:
        st.image("Araujo.jpg", width=200)
        st.subheader("Ronald Araujo")
    query_6 = '''SELECT team, total_clearances, clearances_per_match, total_interceptions, wins, 
    interceptions_per_match, tackle_success_percent, successful_tackles_per_match, rank_interceptions,  
    rank_effective_clearance, rank_successful_won_tackle FROM team_data'''
    df6 = pd.read_sql_query(query_6, db)
    #st.dataframe(df6)

    effective_clearance_summary = df6[['total_clearances', 'clearances_per_match']].describe().loc[['mean', 'min', 'max']]
    effective_clearance_summary = effective_clearance_summary.round(2).applymap(lambda x: f"{x:.2f}")
    effective_clearance_summary = effective_clearance_summary.rename(columns={
        'total_clearances': 'Total Clearances',
        'clearances_per_match': 'Clearances per Match'})
    st.subheader('Summary Statistics for Effective Clearances')
    st.table(effective_clearance_summary)

    interceptions_summary = df6[['total_interceptions', 'interceptions_per_match']].describe().loc[['mean', 'min', 'max']]
    interceptions_summary = interceptions_summary.round(2).applymap(lambda x: f"{x:.2f}")
    interceptions_summary = interceptions_summary.rename(columns={
        'total_interceptions': 'Total Interceptions',
        'interceptions_per_match': 'Interceptions per Match'})
    st.subheader('Summary Statistics for Interceptions')
    st.table(interceptions_summary)

    won_tackles_summary = df6[['tackle_success_percent', 'successful_tackles_per_match']].describe().loc[['mean', 'min', 'max']]
    won_tackles_summary = won_tackles_summary.round(2).applymap(lambda x: f"{x:.2f}")
    won_tackles_summary = won_tackles_summary.rename(columns={
        'tackle_success_percent': 'Tackle Success Percent',
        'successful_tackles_per_match': 'Successful Tackles per Match'})
    st.subheader('Summary Statistics for Won Tackles')
    st.table(won_tackles_summary)

    box_plot = px.box(df6, y='clearances_per_match', title='Distribution of Clearances per Match for the League') 
    box_plot.update_layout(yaxis_title= "Clearances per Match",)
    st.plotly_chart(box_plot)

    box_plot = px.box(df6, y='interceptions_per_match', title='Distribution of Interceptions per Match for the League') 
    box_plot.update_layout(yaxis_title= "Interceptions per Match",)
    st.plotly_chart(box_plot)

    box_plot = px.box(df6, y='successful_tackles_per_match', title='Distribution of Successful Tackles per Match for the League') 
    box_plot.update_layout(yaxis_title= "Successful Tackles per Match",)
    st.plotly_chart(box_plot)

    team_name = st.selectbox('Select a Team:', options = ['All'] + df6['team'].unique().tolist() )
    results6 = df6[['team', 'wins', 'rank_effective_clearance', 'clearances_per_match', 'rank_interceptions', 'interceptions_per_match', 'rank_successful_won_tackle', 'successful_tackles_per_match']]
    rename_dict = {
    'team': 'Team',
    'wins': 'Wins',
    'rank_effective_clearance': 'Effective Clearance Rank ',
    'clearances_per_match': 'Clearances per Match',
    'rank_interceptions': 'Interceptions Rank ',
    'interceptions_per_match': 'Interceptions per Match',
    'rank_successful_won_tackle': 'Successful Tackles Rank ',
    'successful_tackles_per_match': 'Successful Tackles per Match'}

    # Rename the columns
    results6 = results6.rename(columns=rename_dict)
    if team_name != 'All':
	    results6 = results6[results6['Team'] == team_name]
    
    st.dataframe(results6)

with tab7: #Safe hands
    col1, col2= st.columns(2)
    with col1:
        st.header("Which goalkeepers are the most reliable based on metrics such as save percentage, clean sheets, and goals prevented?")
    with col2:
        st.image("Oblak.jpg", width=200)
        st.subheader("Jan Oblak")
    query_5 = '''SELECT player, clean_sheets, rank_clean_sheets, total_goals_conceded, 
    total_saves, saves_per_90, goals_conceded_per_90, rank_saves_made, rank_goals_conceded FROM goalies
    WHERE goals_conceded_per_90 IS NOT ""
    AND total_saves IS NOT ""
    AND saves_per_90 IS NOT ""
    AND clean_sheets IS NOT ""
    AND rank_clean_sheets IS NOT ""
    AND rank_saves_made IS NOT ""
    AND rank_goals_conceded IS NOT ""
    AND total_goals_conceded IS NOT ""'''
    df5 = pd.read_sql_query(query_5, db)
    #st.dataframe(df5)

    selected_goalie = st.selectbox("Select a goalie:", df5['player'].unique().tolist())
    results5 = df5[ df5 ['player'] == selected_goalie]
    #st.write(results5)

    results5['saves_per_90'] = pd.to_numeric(results5['saves_per_90'], errors='coerce')
    results5['goals_conceded_per_90'] = pd.to_numeric(results5['goals_conceded_per_90'], errors='coerce')


    goalie_name = results5['player'].iloc[0] 
    clean_sheets = results5['clean_sheets'].iloc[0] 
    rank_clean_sheets = results5['rank_clean_sheets'].iloc[0]
    rank_saves_made = results5['rank_saves_made'].iloc[0]
    rank_goals_conceded = results5['rank_goals_conceded'].iloc[0]
    total_saves = results5['total_saves'].iloc[0]
    total_goals_conceded = results5['total_goals_conceded'].iloc[0]
    st.write(f'For the 2023-24 season, {goalie_name} was ranked:')
    st.write(f'#{rank_clean_sheets} for overall clean sheets with {clean_sheets} clean sheets')
    st.write(f"#{rank_saves_made} for saves made with a total of {total_saves}")
    st.write(f"#{rank_goals_conceded} for goals conceded with a total of {total_goals_conceded}")

    st.subheader('Average Goals Saved vs Average Goals Conceded')
    #values = [results5['Saves per 90'], results5 ['Goals Conceded per 90']]
    
    fig = px.bar(results5,  x='player', y=['saves_per_90', 'goals_conceded_per_90'], barmode='group')
    fig.update_layout(xaxis_title= "Goalie", yaxis_title= "Average Saves/Goals Conceeded per Match", 
                      legend_title_text='Legend', xaxis={'type': 'category'})
    new_names = {'saves_per_90': 'Saves', 'goals_conceded_per_90': 'Conceded'}
    for trace in fig.data:
        if trace.name in new_names:
            trace.name = new_names[trace.name]
    st.plotly_chart(fig)

with tab8: #Dirtiest teams
    col1, col2= st.columns(2)
    with col1:
        st.header("Which teams accumulate the most fouls and cards? How does this impact their performance and results over the season?")
    with col2:
        st.image("Ramos.jpg", width=200)
        st.subheader("Sergio Ramos")
    query_7 = "SELECT team, wins, draws, losses, red_cards, yellow_cards, fouls_per_match, penalties_conceded FROM team_data"
    df7 = pd.read_sql_query(query_7, db)
    #st.dataframe(df7)

    team_filter = st.selectbox('Select a team to view a breakdown of their season record:', options = ['All'] + df7['team'].unique().tolist(), key = 'team_filter')

    win_filter = st.slider('Select a minimum amount of wins:', min_value= int(df7['wins'].min()), max_value= int(df7['wins'].max()), value = int(df7['wins'].min()))
    results7 = df7[['team', 'wins', 'draws', 'losses', 'red_cards', 'yellow_cards', 'fouls_per_match', 'penalties_conceded']]
    if team_filter != 'All':
        results7 = results7[results7['team'] == team_filter]
    results7 = results7[results7['wins'] >= win_filter]
    rename_dict = {
    'team': 'Team',
    'wins': 'Wins', 'draws': 'Draws', 'losses': 'Losses',
    'red_cards': 'Red Cards',
    'yellow_cards': 'Yellow Cards',
    'fouls_per_match': 'Fouls per Match',
    'penalties_conceded': 'Penalties Conceded'}

    # Rename the columns
    results7 = results7.rename(columns=rename_dict)
    st.write('Filtered dataframe:')
    st.dataframe(results7)


    if team_filter != 'All':
        pie_data = {
        "Result": ['Wins', 'Draws', 'Losses'],
        "Count": [results7['Wins'].iloc[0] , results7['Draws'].iloc[0] , results7['Losses'].iloc[0] ]}
         #Create a pie chart
        fig = px.pie(pie_data,values="Count", names="Result", title=f"{team_filter}: Wins, Draws, and Losses",
        color_discrete_sequence=px.colors.qualitative.Set2) 
        st.plotly_chart(fig)




db.close()