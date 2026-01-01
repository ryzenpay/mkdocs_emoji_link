#this is a script to add emojis after every URI reference
#it works as following:
#   For page references:
#       It takes the name of the page, in the mkdocs.yml goes to extra: -> emoji -> <page name>
#   For email references:
#       takes the email, in the mkdocs.yml goes to extra: -> social -> <email>
#https://mkdocs-dupe-test.readthedocs.io/en/latest/user-guide/plugins/

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
from pathlib import Path
import yaml

import logging
logger = logging.getLogger(f"mkdocs.plugins.{__name__}")

blacklist = ["#", ".png", "!", ".jpg"]

#default emojis
EMAIL = ":e-mail:"
PHONE = ":material-phone:"
OUT_ARROW = ":octicons-arrow-up-right-16:" # external default
IN_ARROW = ":octicons-arrow-down-left-16:" # internal default
#TODO: blacklist options
# entire directories or individual files


class EmojiLink(BasePlugin):
    config_scheme = ()
    #function is triggered when markdown page is loaded, the markdown variable is the raw markdown text
    def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
        words = []
        for word in markdown.split(" "):
            if "](" in word and not any(entry in word for entry in blacklist):
                if ":" in word and "http" not in word:
                    logger.debug(f"Skipping `{word}` as it already contains an emoji")
                    words.append(word)
                    continue
                emoji = ""
                if "mailto:" in word:
                    emoji = EMAIL
                elif "tel:" in word:
                    emoji = PHONE
                elif "http" in word:
                    emoji = OUT_ARROW
                else:
                    rel_path = word.split("(")[1].split(")")[0]
                    if ".md" not in rel_path:
                        rel_path += "index.md" #if locating to directory, default to index.html
                    #ugly dont touch
                    path = (Path(page.file.abs_src_path).parent / rel_path).resolve().relative_to(Path(config["docs_dir"])).as_posix()
                    file = files.get_file_from_path(path=path)
                    if not file:
                        logger.error(f"Unable to find internal file/page for `{path}` referenced by word=`{word.strip()}` in page={page.file.abs_src_path}")
                        words.append(word)
                        continue

                    emoji = get_file_emoji(file=file)
                    if not emoji:
                        emoji = IN_ARROW
                        logger.warning(f"Unable to find emoji for {file.abs_src_path} referenced by {word.strip()} in {page.file.src_uri}")
                
                if emoji:
                    word = word.replace("]", f' {emoji}]')
                    logger.info(f"Emoji `{emoji}` set in `{page.file.src_uri}` for `{word.strip()}`")
            
            words.append(word)

        return " ".join(words)

    
def get_file_emoji(file: File) -> str:
    icon = ""
    if not file.page:
        logger.error(f"page {file.src_uri} was yet registered")
        return ""
    page = file.page
    # this is needed as pages which have not had on_markdown been ran yet
    if not page.meta:
        content = Path(file.abs_src_path).read_text()
        if not content.startswith("---"):
            logger.debug(f"page `{file.abs_src_path}` is missing metadata")
            return ""
        meta = yaml.safe_load(content.split("---", 2)[1])
        logger.debug(f"Metadata: {meta}")

        if "icon" in meta and meta["icon"]: #ensure key exists and value is not none
            icon = str(meta["icon"])

    elif "icon" in page.meta:
        icon = str(page.meta["icon"])
    
    if icon:
        return f":{icon.strip().replace('/', '-')}:"
    else:
        logger.debug(f"Page {file.abs_src_path} is missing icon")
        return ""
