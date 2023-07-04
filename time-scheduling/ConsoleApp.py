import pathlib
import time
from model.Configuration import Configuration
from algorithm.NsgaII import NsgaII
import streamlit as st

from HtmlOutput import HtmlOutput


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

