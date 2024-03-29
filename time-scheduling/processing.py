import pandas as pd
import numpy as np
import json
import streamlit as st
from ConsoleApp import main
# from ConsoleApp import main_filter

# from ConsoleApp import get_filter
import sys
import hashlib
import json
import ast
import traceback
import hashlib
from PIL import Image
from itertools import chain
from bs4 import BeautifulSoup
# from session_state import SessionState



def load_file(df2, df_room):
    
    list_course = []
    index_count_course_id = 0
    list_prof = []     
    index_count_prof_id = 0
    for index1, row1 in df2.iterrows():
        if row1['Course_Name'] not in list_course:
            df2.at[index1, 'Course_id'] = index_count_course_id + 1
            index_count_course_id += 1
            list_course.append(row1['Course_Name'])
        else:
            df2.at[index1, 'Course_id'] = index_count_course_id

        if row1['Prof_Name'] not in list_prof:
            df2.at[index1, 'Prof_id'] = index_count_prof_id + 1
            index_count_prof_id += 1
            list_prof.append(row1['Prof_Name'])
        else:
            df2.at[index1, 'Prof_id'] = index_count_prof_id
            
    # create list of dictionaries representing each object in the JSON file
    objects = []
    for index, row in df2.iterrows():       
        if row['Prof_id'] != '':
            # create professor object
            prof = {
                "prof": {
                    "id": row['Prof_id'],
                    "name": row['Prof_Name']
                }
            }
            if prof not in objects:
                objects.append(prof)
        if row['Course_id'] != '':
            # create course object
            course = {
                "course": {
                    "id": row['Course_id'],
                    "name": row['Course_Name']
                }
            }
            if course not in objects:
                objects.append(course)
        if row['Group_id'] != '':
            # create group object
            group = {
                "group": {
                    "id": row['Group_id'],
                    "size": row['Size_Course']
                }
            }
            # if group not in objects:
            objects.append(group)
        if row['Prof_id'] != '' and row['Course_id'] != '':
            # create class object
            class_ = {
                "class": {
                    "professor": row['Prof_id'],
                    "course": row['Course_id'],
                    "duration": row['Duration'],
                    "group": row['Group_id'],
                    "lab": row['Lab']
                }
            }
            if class_ not in objects:
                objects.append(class_)
            
    for index, row in df_room.iterrows():
        if row['Room'] != '':
            # create room object
            room = {
                "room": {
                    "name": row['Room'],
                    "lab": row['Lab'],
                    "size": row['Size_Room']
                }
            }
            objects.append(room)    
            
    # create JSON object with list of objects
    json_data = json.dumps(objects, sort_keys=False)
    # write JSON object to file
    with open('GaSchedule1.json', 'w') as f:
        f.write(json_data) 
    file_name = "/GaSchedule1.json"
    return file_name




def for_stu():
    df_stu = pd.read_csv("time-scheduling/data_stu.csv")
    df_ctdt = pd.read_csv("time-scheduling/ctdt_ds.csv")

    df_ctdt = df_ctdt[['MaMH', 'Course Name', 'Sem', 'Expect Year', 'Credits', 'Elective']]

    df_stu = df_stu[['MaSV', 'NHHK', 'HK', 'MaMH', 'TenMH', 'SoTinChi', 'DiemHP']]
    df_stu = df_stu.dropna()
    df_stu['NHHK'] = df_stu['NHHK'].astype(str).str[:-1]
    input = st.text_input("Type Student ID", value="")

                
    

    col1, col2, col3 = st.columns(3)
    with col1:
        if input:

            # Convert 'DiemHP' column to numeric type, ignoring non-numeric values
            df_stu['DiemHP'] = pd.to_numeric(df_stu['DiemHP'], errors='coerce')

            list_subject_have_done = df_stu.loc[(df_stu['MaSV'].str.lower() == input.lower()) & (df_stu['DiemHP'].gt(50))]
            list_subject_have_done[''] = np.arange(1, len(list_subject_have_done) + 1) 
            list_subject_have_done = list_subject_have_done.reindex(columns=['', 'MaMH', 'TenMH','HK', 'NHHK', 'SoTinChi'])
            list_subject_have_done = list_subject_have_done.rename(columns={'NHHK': 'Actual Year', 'HK': 'Sem', 'TenMH': 'Course Name', 'SoTinChi': 'Credits'})           
            
            with st.expander("List of subjects have done"):  
                st.dataframe(list_subject_have_done.set_index(''))
    with col2:
        if input:
            list_subject_havent_done_yet = df_ctdt[~df_ctdt['MaMH'].isin(list_subject_have_done['MaMH'])]
            list_subject_havent_done_yet['Expect Year'] = list_subject_havent_done_yet['Expect Year'].astype(str)
            list_subject_havent_done_yet['Elective'] = list_subject_havent_done_yet['Elective'].astype(bool)
            list_subject_havent_done_yet[''] = np.arange(1, len(list_subject_havent_done_yet) + 1) 
            list_subject_havent_done_yet = list_subject_havent_done_yet.reindex(columns=['', 'MaMH', 'Course Name', 'Credits', 'Elective', 'Expect Year', 'Sem'])
            
            with st.expander("List of subjects haven't done yet"):  
                st.dataframe(list_subject_havent_done_yet.set_index(''))  

    with col3:
        if input:
            df_unique = df2[df2['Group_Lab'] == 1.0]
            df_unique = df_unique[['MaMH', 'Course_Name', 'Prof_Name', 'Duration', 'Group_Lab', 'Size_Course']]
            list_recommend_subjects = df_unique[df_unique['MaMH'].isin(list_subject_havent_done_yet['MaMH'])]
            list_recommend_subjects[''] = np.arange(1, len(list_recommend_subjects) + 1) 
            list_recommend_subjects = list_recommend_subjects.reindex(columns=['', 'MaMH', 'Course_Name', 'Prof_Name', 'Duration', 'Group_Lab', 'Size_Course'])
            with st.expander("List of recommend subjects in this semester"):    
                st.dataframe(list_recommend_subjects.set_index(''))  

def get_filter(html, list_filter):
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all div elements with id starting with 'room_'
    div_elements = soup.find_all('div', id=lambda x: x and x.startswith('room_'))
    # Filter and display the schedule for specific rooms
    filtered = ""
    for div in div_elements:
        room_id = div['id'].replace('room_', '')  # Extract the room ID from the div's id attribute
        if room_id in list_filter:
            filtered += str(div)
    return filtered

def data_display():

    uploaded_file = st.file_uploader('')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    else:
        df = [['Data Mining', 1, 35, 4, 'Nguyen Thi Thanh Sang', 'IT132IU'],
            ['Analytics for Observational Data', 2, 35, 4, 'Nguyen Thi Thanh Sang', 'IT142IU'],
            ['Fundamentals of Programming', 0, 90, 3, 'Dao Tran Hoang Chau', 'IT149IU'],
            ['Object-Oriented Analysis and Design', 0, 90, 4, 'Ha Viet Uyen Synh', 'IT090IU']]
        room_columns = ['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV', 'MaMH']
        df = pd.DataFrame(df, columns=room_columns)

    df1 = df[['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV', 'MaMH']]
    df1 = df1.rename(columns={'TenMH': 'Course_Name', 'ToTH': 'Group_Lab', 'TongSoSV': 'Size_Course', 'SoTiet': 'Duration', 'TenDayDuNV': 'Prof_Name', 'MaMH': 'MaMH'})
    df1['Lab'] = df1['Group_Lab']
    # df1['Lab'] = df1['Lab'].astype(str)
    for index, row in df1.iterrows():
        if row['Lab'] == 1 or row['Lab'] == 2 or row['Lab'] == 3 or row['Lab'] == 4:
            df1.at[index, 'Lab'] = 'True'
        else:
            df1.at[index, 'Lab'] = ''
    df1['Lab'] = df1['Lab'].astype(bool)
    

    ## create default room
    room_default = [['A1.309', 90, 0],
                    ['L107', 90, 0],
                    ['LA1.605', 60, 1],
                    ['La1.607', 60, 1]
    ]
    room_columns = ['Room', 'Size_Room', 'Lab']
    df_room = pd.DataFrame(room_default, columns=room_columns)
    df_room['Lab'] = df_room['Lab'].astype(str)
    for index, row in df_room.iterrows():
        if row['Lab'] == '1':
            df_room.at[index, 'Lab'] = 'True'
        else:
            df_room.at[index, 'Lab'] = ''
    df_room['Lab'] = df_room['Lab'].astype(bool)


    col1, col2, col3, col4 = st.columns([0.5,7,2.4,0.5])

    with col2:
        df2 = st.experimental_data_editor(df1, num_rows="dynamic")
        df2['Size_Course'] = df2['Size_Course'].astype(int)
        df2['Duration'] = df2['Duration'].astype(int)
        df2['Group_id'] = np.arange(1, len(df2) + 1)
        df_prof_filter = df2['Prof_Name'].drop_duplicates().tolist()

    with col3:                          
        df_room = st.experimental_data_editor(df_room, num_rows="dynamic")
        df_room['Size_Room'] = df_room['Size_Room'].astype(int)
        filter = df_room['Room'].to_list()
        # df_room_filter = df_room[df_room['Room'].isin(list_filter)]   

    return df2, df_room, filter, df_prof_filter

st.set_page_config(layout="wide")
if __name__ == "__main__":

    st.markdown("<h1 style='text-align: center; color: white;'>Time Scheduling Engine</h1>", unsafe_allow_html=True)
    image = Image.open('time-scheduling/logo-vector-IU-01.png')
    st.sidebar.image(image, width=240)
    tab1, tab2 = st.tabs(["Schedule", "Student"])
    with tab1:
        df2, df_room, filter, df_prof_filter = data_display()
        file_name = load_file(df2, df_room)
        # html_result_filter = main_filter(file_name)
        html_result = main(file_name)
        if 'html_result' not in st.session_state:
            st.session_state.html_result = []
        list_room_filter = st.sidebar.multiselect('Room Filter', filter, filter)
        # list_prof_filter = st.sidebar.multiselect('Prof Filter', df_prof_filter, df_prof_filter)
        if st.button('Generate'):
            st.session_state.html_result = html_result
            st.markdown(st.session_state.html_result, unsafe_allow_html=True)
        if st.sidebar.button('Room Filter'): 
            filtered1 = get_filter(st.session_state.html_result, list_room_filter)
            st.markdown(filtered1, unsafe_allow_html=True)

        # if len(sys.argv) > 1:
        #     file_name = sys.argv[1]
        # try:
        #     if st.button('Generate'): 
        #         temp = session_state['html_result']
        #         filtered1 = get_filter(temp, list_filter)
        #         st.markdown(filtered1, unsafe_allow_html=True)  

        # except:
        #     traceback.print_exc()

    with tab2:         
        for_stu()
