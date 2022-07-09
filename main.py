#main.py
"""
GitHub Action Code to update README file with provided images randomly.
"""

import os
import re
import sys
import base64
import requests
import random
from typing import List
from github import Github, GithubException



####################################################################

STARTS_WITH = "<!--STARTS_HERE_QUOTE_README-->"
ENDS_WITH = "<!--ENDS_HERE_QUOTE_README-->"
REPL_PATTERN = f"{STARTS_WITH}[\\s\\S]+{ENDS_WITH}"

REPOSITORY = os.getenv("INPUT_REPOSITORY")
GHTOKEN = os.getenv("INPUT_GH_TOKEN")
COMMIT_MSG = os.getenv("INPUT_COMMIT_MESSAGE")
OPTION = os.getenv("INPUT_OPTION")

QUOTES_PATH = "/quotes/quotes.txt"



def get_quotes() -> List[str]:
    """
    Get quotes from quotes/quotes.txt, return a list.
    """
    global QUOTES_PATH
    quotes = []
    with open(QUOTES_PATH, "r") as file:
        quotes.extend(file.readlines())
    random.shuffle(quotes)
    return quotes




def get_option_list(OPTION):
    """
    Utility to get text list for corresponding given option.
    """
    text_list = []
    if OPTION == 'quote':
        text_list.extend(get_quotes())
    elif OPTION == 'funfact':
        text_list.extend(get_funfacts())
    elif OPTION == 'both':
        text_list.extend(get_quotes())
        text_list.extend(get_funfacts())
        random.shuffle(text_list)
    return text_list


def get_quote_funfact(text_list: List[str]) -> str:
    """
    Utility to get random text from given list.
    """
    return random.choice(text_list)


def get_text_to_display() -> str:
    """
    Get text to display on readme, depending on option.
    """
    global OPTION
    text_list = get_option_list(OPTION)
    text_to_display = get_quote_funfact(text_list)
    text_to_display = re.sub('[\n]', '', text_to_display)
    text_to_display = re.sub('[\xa0]', ' ', text_to_display)
    text_to_display = f"<i>❝{text_to_display}❞</i>"
    return text_to_display


def decode_readme(data: str) -> str:
    """
    Decode the contents of old readme.
    """
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')



# def generate_new_readme(readme: str, image_tag: str) -> str:
#     '''Generate a new Readme.md'''
#     update_readme_with = f"{START_COMMENT}\n{image_tag}\n{END_COMMENT}"
# "
#     return re.sub(IMAGE_REPL, update_readme_with, readme)

def generate_new_readme2(readme: str, i_tag: str) -> str:
    """
    Generate a new Readme.
    """
    update_readme_with = f"{STARTS_WITH}\n{i_tag}\n{ENDS_WITH}"
    return re.sub(REPL_PATTERN, update_readme_with, readme)



if __name__ == "__main__":
    g = Github(GHTOKEN)
    try:
        readme_repo = g.get_repo(REPO)
        img_repo = g.get_repo(IMG_REPO)
    except GithubException:
        print("Authentication Error. Try saving a GitHub Token in your Repo Secrets or Use the GitHub Actions Token, which is automatically used by the action.")
        sys.exit(1)
#     image_tag = get_image_tag(img_repo)
    text_to_display = get_text_to_display()
    readme_obj = readme_repo.get_readme()
    readme_content = readme_obj.content
    readme_content_decoded = decode_readme(readme_content)
#     new_readme = generate_new_readme(readme=readme_content_decoded, image_tag=image_tag)
    new_readme = generate_new_readme2(readme=readme_content_decoded,i_tag=text_to_display)
    if readme_content_decoded != new_readme:
        readme_repo.update_file(path=readme_obj.path, message=COMMIT_MSG,
                             content=new_readme, sha=readme_obj.sha)
        print("Success")
    else:
        print("No change")
