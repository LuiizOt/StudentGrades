import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
'''
# Student Academic Performance Analysis
***
'''

def calculate_overall(row):
    it1_percentage = (row['internal_test1'] / 40) * 100
    it2_percentage = (row['internal_test2'] / 40) * 100
    assignment_percentage = (row['assignment_score'] / 10) * 100
    final_exam_score = row['final_exam_marks']
    overall = (0.20 * it1_percentage) + (0.20 * it2_percentage) + (0.10 * assignment_percentage) + (0.50 * final_exam_score)
    return overall


# loading dataset
students_data = pd.read_csv('./data/Final_Marks_Data.csv')
st2 = pd.read_csv('./data/Final_Marks_Data.csv') #used for dataframe display

# changing column names for better readability
new_columns = [{'Student_ID':'student_id',
                'Attendance (%)': 'attendance',
                'Internal Test 1 (out of 40)':'internal_test1',
                'Internal Test 2 (out of 40)':'internal_test2',
                'Assignment Score (out of 10)':'assignment_score',
                'Daily Study Hours':'daily_study_hours',
                'Final Exam Marks (out of 100)':'final_exam_marks'}]
students_data.rename(columns=new_columns[0], inplace=True)

# calculating overall marks
students_data['overall'] = students_data.apply(calculate_overall, axis=1)

# creating jitter column for study hours scatter plot, value between -0.05 and +0.05, just to make things better visible
students_data['jitter'] = np.random.uniform(-0.05, 0.05, size=len(students_data))
students_data['study_hours_jitter'] = students_data['daily_study_hours'] + students_data['jitter']
students_data.drop(columns=['jitter'], inplace=True)
ticks = sorted(students_data['daily_study_hours'].unique())

# gathering information regarding overall pass/fail
fail_final_exam = 0
fail_attendance = 0
fail_overall = 0
for idx, row in students_data.iterrows():
    if (row['final_exam_marks'] >= 50) and (row['attendance'] >= 75) and (row['overall'] >= 60):
        students_data.loc[idx, 'status'] = 'Passed'
    else:
        students_data.loc[idx, 'status'] = 'Failed'
    if (row['final_exam_marks'] < 50):
        fail_final_exam += 1
    if (row['attendance'] < 75):  
        fail_attendance += 1
    if (row['overall'] < 60):
        fail_overall += 1

# side navigation bar
page = st.sidebar.radio("Menu", ["Main Page", "Grade Comparsion","Grades Stastistics"])

# main page
if page == "Main Page":
    st.write('This application provides an analysis of students\' academic performance based on various parameters such as attendance, internal test scores, assignment scores, daily study hours, and final exam marks. The dataset used in this analysis is sourced from [Kaggle](https://www.kaggle.com/datasets/sonalshinde123/student-academic-performance-dataset?resource=download).')
    st.write('Dataset credits to [Sonal Shinde](https://github.com/sonalshinde24).')
    st.write('[My GitHub Page](https://github.com/LuiizOt/)')
    #dataframe button and display
    sd_button = st.button('Show Dataframe')
    if sd_button:
        st.dataframe(students_data, height=600)
        sd_button = st.button('Hide Dataframe')

# grade comparison page
elif page == "Grade Comparsion":
    st.write('This section allows you to visualize the distribution of marks obtained by students in Internal Test 1 and compare it to the marks obtained in the Internal Test 2.')
    st.write('### Distribution of Marks:')
    #plotting marks distribution for both tests
    fig1 = px.histogram(students_data,
                        x='internal_test1',
                        nbins=40,
                        title='Marks Distribution Histogram (Internal Test 1)',
                        labels={'internal_test1':'Marks Obtained'},
                        color_discrete_sequence=['lightblue'],
                        width=1000)
    st.plotly_chart(fig1)

    fig2 = px.histogram(students_data,
                        x='internal_test2',
                        nbins=40,
                        title='Marks Distribution Histogram (Internal Test 2)',
                        labels={'internal_test2':'Marks Obtained'},
                        color_discrete_sequence=['orange'],
                        width=1000)
    st.plotly_chart(fig2)

    # plotting comparison histogram
    st.write('### Comparison of Internal Test 1 and Internal Test 2 Marks:')
    
    # making a new dataframe for comparison
    grade_comparsion = pd.melt(students_data, value_vars=['internal_test1', 'internal_test2'])
    grade_comparsion.replace({'internal_test1':'Internal Test 1', 'internal_test2':'Internal Test 2'}, inplace=True)

    # comparison histogram
    fig3 = px.histogram(grade_comparsion,
                        opacity=0.7,
                        x='value',
                        labels={'value':'Marks Obtained',
                                'variable':'Exams',
                                'internal_test2':'Internal Test 2'},
                        title='Comparison of Internal Test 1 and Internal Test 2 Marks',
                        color='variable',
                        nbins=40,
                        barmode='overlay',
                        color_discrete_sequence=['lightblue', 'orange'],
                        width=1000)
    
    # updating legend position - inside plot area
    fig3.update_layout(legend= {'x':0.95,
                                'y':0.95,
                                'xanchor':'right',
                                'yanchor':'top',
                                'bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig3)

# grades statistics page
elif page == "Grades Stastistics":
    st.write('This section provides a detailed statistical analysis of the students\' grades, including measures such as mean, median and standard deviation for each row.')
    st.write('### Statistical Summary of Grades:')

    # displaying statistical summary
    summary = st2.describe()
    summary = summary.drop(['count','25%','75%'])
    summary = summary.T
    summary_columns = [{'mean':'Mean', 'std':'Std Dev', 'min':'Min', 'max':'Max','50%':'Median'}]
    summary.rename(columns=summary_columns[0], inplace=True)    
    st.dataframe(summary)

    # plotting approval bar chart
    st.write('### Distribution of Marks:')
    st.write('This bar chart shows the number of students who passed and failed based on a passing criteria shown below:')
    st.write('- Passing Criteria:')
    st.markdown('<div style="text-align:center"> - Final Exam Marks ≥ 50</div><div style="text-align:center"> - Attendance ≥ 75%</div><div style="text-align:center">Overall ≥ 60% </div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center">Overall Formula:</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center"><i>Overall = 0.20*IT1% + 0.20*IT2% + 0.10*Assign% + 0.50*Final%</i></div>', unsafe_allow_html=True)
    st.write('- Students meeting the criteria are considered "Passed", while those who do not are considered "Failed".') 
    st.write()

    # generating bar chart
    fig4 = px.bar(x=['Passed','Failed'],
                  y=[len(students_data[students_data['status']=='Passed']),
                     len(students_data[students_data['status']=='Failed'])],
                  color=['Passed','Failed'],
                  labels={'x':'Status', 'y':'Number of Students','color':'Status'},
                  title='Number of Students Passed vs Failed',
                  color_discrete_sequence=['lightblue','red'])
    st.plotly_chart(fig4)

    # displaying failure reasons
    st.write('### Failure Reasons:')
    st.write(f'- Number of students who failed due to Final Exam Marks < 50: {fail_final_exam}')
    st.write(f'- Number of students who failed due to Attendance < 75%: {fail_attendance}')
    st.write(f'- Number of students who failed due to Overall < 60%: {fail_overall}')
    st.write('###### Note: A student can fail for multiple reasons, so the sum of failure reasons may exceed the total number of failed students.')

    #scatter plot for daily study hours vs overall marks
    st.write('### Daily Study Hours vs Overall Score:')
    fig5 = px.scatter(students_data,
                      x='study_hours_jitter',
                      y='overall',
                      color='status',
                      opacity=0.7,
                      title='Daily Study Hours vs Overall Marks',
                      labels={'study_hours_jitter':'Daily Study Hours', 'overall':'Overall Score'},
                      color_discrete_sequence=['lightblue','red'],
                      trendline='ols')
    st.plotly_chart(fig5)
    fig5.update_xaxes(tickvals=ticks)
    