# android-localization-helper
A python script that helps you create strings.xml for all languages in different hierarchical folder (using microsoft translator Translation API cognitive services) 

# usage
strings.xml your file
Syntax

```
python3.7 translator.py
```

# Azure get Key

  - Create a resource
  - Search service input "cognitive services"
  - Create cognitive services
  - Go to Source
  - left panel Key and Endpoint
  - USE key1 or key 2 and Location/Region copy

# Change Veriable

```
key = ""  # azure key
region = "westus2" # azure key Location/Region
```

Output will be created in transalted/ folder with various langugaes folders.

Paste them in your res/ folder of Android Project.

# credits

Combined effort from below repositories + Some Add Ons 

https://github.com/Ra-Na/GTranslate-strings-xml

https://github.com/Swisyn/android-strings.xml-translator


# other useful commands

Extract only strings from strings.xml
cut -d ">" -f2 strings.xml | cut -d "<" -f1

Extract non translatable strings from strings.xml
cat strings.xml|grep -v "translatable" | cut -d ">" -f2  | cut -d "<" -f1


