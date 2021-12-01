#!/usr/bin/env python

def findall_content(xml_string, tag):
    pattern = r"<(?:\w+:)?%(tag)s(?:[^>]*)>(.*)</(?:\w+:)?%(tag)s" % {"tag": tag}
    return re.findall(pattern, xml_string, re.DOTALL)


def create_directory_if_not_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def check_dir(dir_language):
    create_directory_if_not_exists("translated")

    file_directory = "translated/" + "values-" + dir_language

    return os.path.exists(file_directory)


def create_directories(dir_language):
    create_directory_if_not_exists("translated")

    file_directory = "translated/" + "values-" + dir_language

    create_directory_if_not_exists(file_directory)
    return file_directory


supported_languages = {  # as defined here: http://msdn.microsoft.com/en-us/library/hh456380.aspx
    'ar': ' Arabic',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh-CHS': 'Chinese (Simplified)',
    'zh-CHT': 'Chinese (Traditional)',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'el': 'Greek',
    'ht': 'Haitian Creole',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mww': 'Hmong Daw',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese',
}
default_output_languages = supported_languages.keys()
token = ""
key = ""
region = "westus2"


def update_token():
    global token, key, region
    headers = {'Ocp-Apim-Subscription-Key': key, 'Ocp-Apim-Subscription-Region': region}
    r = requests.post(
        "https://apicognitive.cognitiveservices.azure.com/sts/v1.0/issueToken"
        , headers=headers)
    data = r.content
    token = data.decode("utf-8")


def translate(to_translate, to_language="auto", language="auto"):
    global token
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(token)}
    r = requests.post(
        "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=%s" % (to_language)
        , json=[{"Text": "" + str(to_translate) + ""}], headers=headers)
    data = r.json()
    if ("error" in data):
        return data["error"]["code"]
    return data[0]["translations"][0]["text"].replace("'", "\'")


#
# MAIN PROGRAM
#

# import libraries
import html
import requests
import os
import xml.etree.ElementTree as ET
import sys
from io import BytesIO
import re

# read argument vector
INPUTLANGUAGE = "en"
INFILE = "./strings.xml"

languages_to_translate = default_output_languages

if INFILE is None:
    INFILE = "strings.xml"

# create outfile name by appending the language code to the infile name
name, ext = os.path.splitext(INFILE)

for language_name in languages_to_translate:
    language_to_translate = language_name.strip()

    if (check_dir(language_to_translate)): # if exits dir stop and next lang 
        continue
    translated_file_directory = create_directories(language_to_translate)
    print(" -> " + language_to_translate + " =========================")

    # read xml structure
    tree = ET.parse(INFILE)
    root = tree.getroot()
    update_token() # Token refresh
    # cycle through elements 
    for i in range(len(root)):
        isTranslatable = root[i].get('translatable')
        print((str(i) + " ========================="))
        if (isTranslatable == 'false'):
            print("Not translatable")
        if (root[i].tag == 'string') & (isTranslatable != 'false'):
            # ~ totranslate="".join(findall_content(str(ET.tostring(root[i])),"string"))
            totranslate = root[i].text
            if (totranslate != None):
                print(totranslate + "-->", end='')
                translate_get = translate(totranslate, language_to_translate, INPUTLANGUAGE)
                if (translate_get == 400036 or translate_get == 401000):
                    break
                root[i].text = translate_get
                print(root[i].text)
        if (root[i].tag == 'string-array'):
            print("Entering string array...")
            for j in range(len(root[i])):

                isTranslatable = root[i][j].get('translatable')
                print((str(i) + " " + str(j) + " ========================="))
                if (isTranslatable == 'false'):
                    print("Not translatable")
                if (root[i][j].tag == 'item') & (isTranslatable != 'false'):
                    # ~ totranslate="".join(findall_content(str(ET.tostring(root[i][j])),"item"))
                    totranslate = root[i][j].text
                    if (totranslate != None):
                        print(totranslate + "-->", end='')
                        translate_get = translate(totranslate, language_to_translate, INPUTLANGUAGE)
                        if (translate_get == 400036 or translate_get == 401000):
                            break
                        root[i][j].text = translate_get
                        print(root[i][j].text)

    # write new xml file
    translated_file = translated_file_directory + "/strings.xml"
    tree.write(translated_file, encoding='utf-8')
