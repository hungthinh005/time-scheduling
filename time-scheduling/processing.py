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
        df = [['Data Mining', 1, 90, 4, 1, "Nguyen Thi Thanh Sang", 1]
                  ,['AOD', 2, 90, 4, 1, "Nguyen Thi Thanh Sang", 1]]
        room_columns = ['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'MaNV', 'TenDayDuNV', 'Lab']
        df = pd.DataFrame(df, columns=room_columns)
    
    df = pd.DataFrame(df)
    df1 = df[['TenMH', 'ToTH', 'TongSoSV', 'SoTiet','MaNV', 'TenDayDuNV']]
    df1 = df1.rename(columns={'TenMH': 'course_name', 'ToTH': 'ToTH_Lab', 'TongSoSV': 'size', 'SoTiet': 'duration', 'MaNV': 'prof_id', 'TenDayDuNV': 'prof_name'})
    
    # df1['Lab'] = df1['ToTH'].fillna(0)
    df1['Lab'] = df1['ToTH_Lab'].astype(str)
    df1['prof_id'] = df1['prof_id'].astype(int)
    # df1['course_id'] = df1['course_id'].astype(int)

    for index, row in df1.iterrows():
        if row['Lab'] == '1.0' or row['Lab'] == '2.0' or row['Lab'] == '3.0' or row['Lab'] == '4.0':
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


    
    col1, col2, col3 = st.columns([5,2,4.5])
    with col1:
        df1 = st.experimental_data_editor(df1, num_rows="dynamic")
        list_course = []
        index_count = 0
        for index, row in df1.iterrows():
            if row['course_name'] not in list_course:
                df1.at[index, 'course_id'] = index_count + 1
                index_count += 1
                list_course.append(row['course_name'])
            else:
                df1.at[index, 'course_id'] = index_count
        df1.reset_index(inplace=True)
        df1 = df1.rename(columns={'index': 'group_id'})
        df1['group_id'] = np.arange(1, len(df) + 1)

    with col2:
        st.experimental_data_editor(df_room, num_rows="dynamic")

    with col3:
        with st.expander("Instructions"):    
            st.write("fwfwf")

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
        main(file_name)
    except:
        traceback.print_exc()
