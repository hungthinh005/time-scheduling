import pandas as pd
import numpy as np
import json
import streamlit as st
from ConsoleApp import main
import sys
import traceback

with st.sidebar:
    option = st.radio(
    "Which option do you want to",
    ('Typing Data', 'Upload File'))   
    st.write('You selected ' + option)


##load file and processing data
def load_file():
    st.title('Time Scheduling Engine')

    if option == "Typing Data":
        key_disable = "disable"

        uploaded_file = st.file_uploader("Choose a file", disabled=key_disable)

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
    
    df = pd.DataFrame(df)
    df1 = df[['MaMH', 'TenMH', 'ToTH', 'TongSoSV', 'SoTiet','MaNV', 'TenDayDuNV']]
    df1 = df1.rename(columns={'MaMH': 'course_id', 'TenMH': 'course_name','ToTH': 'Lab', 'TongSoSV': 'size', 'SoTiet': 'duration', 'MaNV': 'prof_id', 'TenDayDuNV': 'prof_name' })
    df1['Lab'] = df1['Lab'].fillna(0)
    df1['Lab'] = df1['Lab'].astype(str)
    df1['prof_id'] = df1['prof_id'].astype(int)
    df1['course_id'] = df1['course_id'].astype(int)

    for index, row in df1.iterrows():
        if row['Lab'] == '1.0' or row['Lab'] == '2.0' or row['Lab'] == '3.0' or row['Lab'] == '4.0':
            df1.at[index, 'Lab'] = 'True'
        else:
            df1.at[index, 'Lab'] = ''
            
    df1['Lab'] = df1['Lab'].astype(bool)
    df1.reset_index(inplace=True)
    df1 = df1.rename(columns={'index': 'group_id'})
    df1['group_id'] = np.arange(1, len(df) + 1)


    ## create default room
    room_default = [['A1.309', 90, 0],
                    ['L107', 40, 0],
                    ['A2.401', 40, 0],
                    ['LA1.605', 35, 1],
                    ['La1.606', 35, 1]
    ]
    room_columns = ['room', 'size', 'Lab']
    df_room = pd.DataFrame(room_default, columns=room_columns)


    ##data input instead of data csv file
    data_input = [['Data Mining', True, 90, 4, 1, "Nguyen Thi Thanh Sang"]
                  ,['AOD', True, 90, 4, 1, "Nguyen Thi Thanh Sang"]]
    room_columns = ['course_name', 'Lab', 'size', 'duration', 'prof_id', 'prof_name']
    data_input = pd.DataFrame(data_input, columns=room_columns)




    df_room['Lab'] = df_room['Lab'].astype(str)
    for index, row in df_room.iterrows():
        if row['Lab'] == '1':
            df_room.at[index, 'Lab'] = 'True'
        else:
            df_room.at[index, 'Lab'] = ''
    df_room['Lab'] = df_room['Lab'].astype(bool)


    
    col1, col2 = st.columns(2)
    with col1:
        col1.write(df1[['course_name', 'Lab', 'size', 'duration', 'prof_id', 'prof_name']])

    with col2:
        with st.expander("Edit your data"):
            col3, col4 = st.columns([4,2])
            with col3:
                st.experimental_data_editor(data_input, num_rows="dynamic")
            with col4:
                st.experimental_data_editor(df_room, num_rows="dynamic")

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
        if option == "Typing Data":
            f.write(data_input)
        else:
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
