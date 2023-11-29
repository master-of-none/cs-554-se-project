# image-text-translation <br>

# Description

A program capable of translating text in images from various languages into English, with the potential to extend the project to include handwritten text translation. <br>

# Language

We are choosing python as our primary programming language, since it has rich library support and API integration is not much complicated and all the team members are comfortable in python.

# Prerequisites for Google Vision API

Follow the steps in the below link for creating the required credentials file
https://cloud.google.com/python/docs/reference/vision/latest

Once the credential file is downloaded, store it in the project directory and name it 'google-cloud-vision-credentials.json'

# Requirements

Install the requirements from the file `requirements.txt` in the folder **docs** using `pip` tool

### Note

For the language packs, we must install each language seperately.
For example: To install French language pack use the pip to install (Spacy must be installed before this).<br>
`python -m spacy download fr_core_news_sm`
