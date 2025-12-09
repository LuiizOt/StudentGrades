import pandas as pd
import streamlit as st
import plotly.express as px
'''
# Student Academic Performance Analysis
***
'''
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

# side navigation bar
page = st.sidebar.radio("Menu", ["Main Page", "Grade Comparsion"])

# main page
if page == "Main Page":
    st.write('This application provides an analysis of students\' academic performance based on various parameters such as attendance, internal test scores, assignment scores, daily study hours, and final exam marks. The dataset used in this analysis is sourced from [Kaggle](https://www.kaggle.com/datasets/sonalshinde123/student-academic-performance-dataset?resource=download).')
    #dataframe button and display
    sd_button = st.button('Show Dataframe')
    if sd_button:
        st.dataframe(st2, height=600)
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
                        color_discrete_sequence=['light blue'],
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
                        color_discrete_sequence=['light blue', 'orange'],
                        width=1000)
    # updating legend position - inside plot area
    fig3.update_layout(legend= {'x':0.95,
                                'y':0.95,
                                'xanchor':'right',
                                'yanchor':'top',
                                'bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig3)
