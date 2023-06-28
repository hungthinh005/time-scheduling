import codecs
import pathlib
import os
import sys
import tempfile
import time
import traceback
from model.Configuration import Configuration
from algorithm.NsgaII import NsgaII
import streamlit as st
# from algorithm.GeneticAlgorithm import GeneticAlgorithm
# from algorithm.APNsgaIII import APNsgaIII
# from algorithm.NsgaIII import NsgaIII

# from algorithm.Ngra import Ngra
# from algorithm.Amga2 import Amga2
# from algorithm.Hgasso import Hgasso
from HtmlOutput import HtmlOutput
from bs4 import BeautifulSoup

def main(file_name):
    start_time = int(round(time.time() * 1000))

    configuration = Configuration()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)
    alg = NsgaII(configuration)
    # alg = Hgasso(configuration)
    alg.run()
    html_result = HtmlOutput.getResult(alg.result)
    st.markdown(html_result, unsafe_allow_html=True)
    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    st.write("\nCompleted in {} secs.\n".format(seconds))
    return html_result
    # temp_file_path = tempfile.gettempdir() + file_name.replace(".json", ".html")
    # writer = codecs.open(temp_file_path, "w", "utf-8")

# def get_filter(html_result, list_filter):
#     # Parse the HTML
#     soup = BeautifulSoup(html_result, 'html.parser')
#     # Find all div elements with id starting with 'room_'
#     div_elements = soup.find_all('div', id=lambda x: x and x.startswith('room_'))

#     filtered_html = ''
#     # Filter and display the schedule for specific rooms
#     for div in div_elements:
#         room_id = div['id'].replace('room_', '')  # Extract the room ID from the div's id attribute
#         if room_id in list_filter:
#             filtered_html += str(div)
#     # st.markdown(filtered_html, unsafe_allow_html=True)
#     st.write(filtered_html)
#     return filtered_html
    # writer.write(html_result)
    # writer.close()


