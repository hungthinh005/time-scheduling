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


@st.cache_data()
def main_filter(file_name):
    # start_time = int(round(time.time() * 1000))
    configuration_filter = Configuration()
    target_file_filter = str(pathlib.Path().absolute()) + file_name
    configuration_filter.parseFile(target_file_filter)
    alg_filter = NsgaII(configuration_filter)
    # alg = Hgasso(configuration)
    
    alg_filter.run()
    html_result_filter = HtmlOutput.getResult(alg_filter.result)
    # st.markdown(html_result, unsafe_allow_html=True)
    # seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    # st.write("\nCompleted in {} secs.\n".format(seconds))
    return html_result_filter

def main(file_name):
    start_time = int(round(time.time() * 1000))
    configuration = Configuration()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)
    alg = NsgaII(configuration)
    # alg = Hgasso(configuration)
    
    alg.run()
    html_result = HtmlOutput.getResult(alg.result)
    # st.markdown(html_result, unsafe_allow_html=True)
    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    st.write("\nCompleted in {} secs.\n".format(seconds))
    return html_result

    # temp_file_path = tempfile.gettempdir() + file_name.replace(".json", ".html")
    # writer = codecs.open(temp_file_path, "w", "utf-8")

    # writer.write(html_result)
    # writer.close()


