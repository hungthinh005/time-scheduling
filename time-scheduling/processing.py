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
    st.markdown("<h1 style='text-align: center; color: white;'>Time Scheduling Engine</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader('')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    else:
        df = [['Data Mining', 1, 35, 4, 'Nguyen Thi Thanh Sang'],
            ['AOD', 2, 35, 4, 'Nguyen Thi Thanh Sang'],
            ['Functional Programming', 0, 90, 3, 'Dao Tran Hoang Chau'],
            ['Operating Systems', 0, 90, 3, 'Tran Manh Ha']]
        room_columns = ['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV']
        df = pd.DataFrame(df, columns=room_columns)
    
    df1 = df[['TenMH', 'ToTH', 'TongSoSV', 'SoTiet', 'TenDayDuNV']]
    df1 = df1.rename(columns={'TenMH': 'Course_Name', 'ToTH': 'Group_Lab', 'TongSoSV': 'Size_Course', 'SoTiet': 'Duration', 'TenDayDuNV': 'Prof_Name'})
    df1['Lab'] = df1['Group_Lab']
    # df1['Lab'] = df1['Lab'].astype(str)
    for index, row in df1.iterrows():
        if row['Lab'] == 1 or row['Lab'] == 2 or row['Lab'] == 3 or row['Lab'] == 4:
            df1.at[index, 'Lab'] = 'True'
        else:
            df1.at[index, 'Lab'] = 'False'
    df1['Lab'] = df1['Lab'].astype(bool)
    


    ## create default room
    room_default = [['A1.309', 90, 0],
                    ['L107', 40, 0],
                    ['LA1.605', 35, 1],
                    ['La1.607', 35, 1]
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
    
    col1, col2, col3 = st.columns([5.5,2,4])
    with col1:
        df1['Group_id'] = np.arange(1, len(df1) + 1)   
        list_course = []
        index_count_course_id = 0
        list_prof = []     
        index_count_prof_id = 0
        for index1, row1 in df1.iterrows():
            if row1['Course_Name'] not in list_course:
                df1.at[index1, 'Course_id'] = index_count_course_id + 1
                index_count_course_id += 1
                list_course.append(row1['Course_Name'])
            else:
                df1.at[index1, 'Course_id'] = index_count_course_id

            if row1['Prof_Name'] not in list_prof:
                df1.at[index1, 'Prof_id'] = index_count_prof_id + 1
                index_count_prof_id += 1
                list_prof.append(row1['Prof_Name'])
            else:
                df1.at[index1, 'Prof_id'] = index_count_prof_id
        df2 = st.experimental_data_editor(df1, num_rows="dynamic")
        

    with col2:
        df_room = st.experimental_data_editor(df_room, num_rows="dynamic")
        df_room['Size_Room'] = df_room['Size_Room'].astype(int)

        
    with col3:
        with st.expander("Descriptions for Data Input"):    
            st.write("- Must Include: Course Name, Lab Group, Size of Course, Duration (Period of Course), Professor Name.")
            st.write("- In the case of the course with 4 periods, 1 room can only accommodate 12 classes at most. Be careful when modifying the info on rooms")
    

    st.write(df2)
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
