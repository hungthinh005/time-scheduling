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


def main(file_name):
    start_time = int(round(time.time() * 1000))

    configuration = Configuration()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)
    alg = NsgaII(configuration)
    # alg = Hgasso(configuration)
    alg.run()
    html_result = HtmlOutput.getResult(alg.result)

    # temp_file_path = tempfile.gettempdir() + file_name.replace(".json", ".html")
    # writer = codecs.open(temp_file_path, "w", "utf-8")

    st.markdown(html_result, unsafe_allow_html=True)
    # writer.write(html_result)
    # writer.close()

    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    st.write("\nCompleted in {} secs.\n".format(seconds))
        # os.startfile(temp_file_path)

# if __name__ == "__main__":
#     file_name = "/GaSchedule3.json"
#     if len(sys.argv) > 1:
#         file_name = sys.argv[1]

#     try:
#         main(file_name)
#     except:
#         traceback.print_exc()
