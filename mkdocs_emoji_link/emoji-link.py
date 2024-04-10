#this is a script to add emojis after every URI reference
#it works as following:
#   For page references:
#       It takes the name of the page, in the mkdocs.yml goes to extra: -> emoji -> <page name>
#   For email references:
#       takes the email, in the mkdocs.yml goes to extra: -> social -> <email>
# to exclude something from getting linked, place a ./ infront of the page name

#https://mkdocs-dupe-test.readthedocs.io/en/latest/user-guide/plugins/

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

class EmojiLink(BasePlugin):
    config_scheme = ()
    #function is triggered when markdown page is loaded, the markdown variable is the raw markdown text
    def on_page_markdown(self, markdown: str, page: Page, config: MkDocsConfig, files: Files):
        #the emoji variables are in config["extra"]["emoji"]
        text = markdown.split()
        for word in text:
            if word[0] == "[" and "http" not in word: #checks first character of the word to see a URI trigger, excludes external links
                if "mailto:" in word: #mailto reference, put mail icon next to
                    word = word.replace("]", f"{config["extra"]["emoji"]["email"]}]")
                else:#web page reference
                    tmp = word.split("(")[1]
                    tmp = tmp.split("/")[1]
                    tmp = tmp.replace(".md)")
                    if tmp in config["extra"]["emoji"]:
                        word = word.replace("]", f"{config["extra"]["emoji"][tmp]}]")

        return text.join() #combine the array back to an original markdown
    