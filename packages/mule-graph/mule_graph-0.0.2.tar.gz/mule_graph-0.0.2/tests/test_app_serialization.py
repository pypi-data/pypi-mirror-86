# dummy file for now
# the import problem was solved formm:
# https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
import os
import sys

test_module_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, test_module_path + "/../")

import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv

from mule_graph.serialization import search_app
from mule_graph.serialization.app_serlialization_in_memory import (
    search_app as search_in_memory,
)

load_dotenv()
import os
import zipfile
from io import BytesIO

APP_PATH = os.getenv("TEST_DATA")


def give_app_folder():
    return APP_PATH


def test_app_serialization():

    graph = search_app(give_app_folder())
    assert type(graph) != type(None)
    return True


# por cada elemento de la lista, debo
def unzip_object(obj, recursive: bool = True):
    """
    This functions takes a byte stream (file-like for those of you pythonistas) representation of a zip file and
    unzips the information within returning a dictionary containing the inner paths as keys and the string representation
    of the content as values. In case an element is another zip, you can specify for recursive unziping.
    Params:
        - obj: zipFile object. tip: if you have a string representation you can use -> zipfile.ZipFile(BytesIO(resp))
        - recursive: bool determines whether or not to continue the proces further than a 1st degree of depth.
    Returns:
        dictionary containing iner paths as keys and the string content as values.
    """
    decompressed_obj = {}
    name_list = obj.namelist()
    for elem in name_list:
        if not (elem[-1] in ["/"]) and not (
            elem.split(".")[-1] in ["jar", "zip", "class"]
        ):
            decompressed_obj[elem] = obj.read(elem)
        elif (
            recursive and len(elem.split(".")) > 1 and (elem.split(".")[-1] in ["zip"])
        ):
            content = zipfile.ZipFile(BytesIO(obj.read(elem)))
            decompressed_obj.update(unzip_object(content))
    return decompressed_obj


def test_in_memory():
    app = zipfile.ZipFile("/Users/sbassani/trash/app_data.zip")
    content = unzip_object(app)

    graph = search_in_memory(content, "app_data")
    assert type(graph) != type(None)
    return True


if __name__ == "__main__":

    pass
