import pandas as pd
import numpy as np
import json
import streamlit as st
from ConsoleApp import main
import sys
import traceback

# with st.sidebar:
#     option = st.radio(
#     "Which option do you want to",
#     ('Upload File', 'Typing Data'))   
#     st.write('You selected ' + option)


##load file and processing data
def load_file():
    st.title('Time Scheduling Engine')

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    else:
        df = [['Data Mining', 1, 35, 4, "Nguyen Thi Thanh Sang"]
            ,['AOD', 2, 35, 4, "Nguyen Thi Thanh Sang"]
            ,['Functional Programming', 0, 90, 3, "Dao Tran Hoang Chau"]
            ,['Operating Systems', 0, 90, 3, "Tran Manh Ha"]]
        room_columns = ['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV']
        df = pd.DataFrame(df, columns=room_columns)
    
    df1 = df[['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV']]
    df1 = df1.rename(columns={'TenMH': 'course_name', 'ToTH': 'ToTH_Lab', 'TongSoSV': 'size', 'SoTiet': 'duration', 'TenDayDuNV': 'prof_name'})
    df1['Lab'] = df1['ToTH_Lab']
    # df1['Lab'] = df1['Lab'].astype(str)
    for index, row in df1.iterrows():
        if row['Lab'] == 1 or row['Lab'] == 2 or row['Lab'] == 3 or row['Lab'] == 4:
            df1.at[index, 'Lab'] = 'True'
        else:
            df1.at[index, 'Lab'] = ''
    df1['Lab'] = df1['Lab'].astype(bool)
    


    ## create default room
    room_default = [['A1.309', 90, 0],
                    ['L107', 40, 0],
                    ['A2.401', 40, 0],
                    ['LA1.605', 35, 1],
                    ['La1.606', 35, 1]
    ]
    room_columns = ['room', 'size', 'Lab']
    df_room = pd.DataFrame(room_default, columns=room_columns)
    df_room['Lab'] = df_room['Lab'].astype(str)
    for index, row in df_room.iterrows():
        if row['Lab'] == '1':
            df_room.at[index, 'Lab'] = 'True'
        else:
            df_room.at[index, 'Lab'] = ''
    df_room['Lab'] = df_room['Lab'].astype(bool)


    
    col1, col2, col3 = st.columns([5,2,4])
    with col1:
        df1 = st.experimental_data_editor(df1, num_rows="dynamic")
        df1['group_id'] = np.arange(1, len(df1) + 1)
        st.write(df1)
    with col2:
        df_room = st.experimental_data_editor(df_room, num_rows="dynamic")
        df_room['size'] = df_room['size'].astype(int)

    with col3:
        with st.expander("Instructions for Upload File Standard"):    
            st.write("- Including: Course Name, Lab Group, Size of Course, Period (Duration of Course), Professor Name")
    
    list_course = []
    index_count_course_id = 0
    list_prof = []
    index_count_prof_id = 0

    for index, row in df1.iterrows():
        if row['course_name'] not in list_course:
            df1.at[index, 'course_id'] = index_count_course_id + 1
            index_count_course_id += 1
            list_course.append(row['course_name'])
        else:
            df1.at[index, 'course_id'] = index_count_course_id

        if row['prof_name'] not in list_prof:
            df1.at[index, 'prof_id'] = index_count_prof_id + 1
            index_count_prof_id += 1
            list_prof.append(row['prof_name'])
        else:
            df1.at[index, 'prof_id'] = index_count_prof_id
    

    # create list of dictionaries representing each object in the JSON file
    objects = []
    for index, row in df1.iterrows():       
        if row['prof_id'] != '':
            # create professor object
            prof = {
                "prof": {
                    "id": row['prof_id'],
                    "name": row['prof_name']
                }
            }
            if prof not in objects:
                objects.append(prof)

        if row['course_id'] != '':
            # create course object
            course = {
                "course": {
                    "id": row['course_id'],
                    "name": row['course_name']
                }
            }
            if course not in objects:
                objects.append(course)

        if row['group_id'] != '':
            # create group object
            group = {
                "group": {
                    "id": row['group_id'],
                    "size": row['size']
                }
            }
            if group not in objects:
                objects.append(group)
                
        if row['prof_id'] != '' and row['course_id'] != '':
            # create class object
            class_ = {
                "class": {
                    "professor": row['prof_id'],
                    "course": row['course_id'],
                    "duration": row['duration'],
                    "group": row['group_id'],
                    "lab": row['Lab']
                }
            }
            if class_ not in objects:
                objects.append(class_)
            
    for index, row in df_room.iterrows():
        if row['room'] != '':
            # create room object
            room = {
                "room": {
                    "name": row['room'],
                    "lab": row['Lab'],
                    "size": row['size']
                }
            }
            objects.append(room)    
            
    # create JSON object with list of objects
    json_data = json.dumps(objects, sort_keys=False)

    # write JSON object to file
    with open('GaSchedule1.json', 'w') as f:
            f.write(json_data) 
        

st.set_page_config(layout="wide")
if __name__ == "__main__":
    load_file()
    file_name = "/GaSchedule1.json"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    try:
        if st.button('Generate'):    
            main(file_name)
    except:
        traceback.print_exc()
