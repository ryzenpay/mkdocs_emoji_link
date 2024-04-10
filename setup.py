from setuptools import setup, find_packages

setup(
    name="mkdocs_emoji_link",
    version="0.1",
    description="A MKDocs plugin to place emojis next to URI notation",
    url="https://github.com/ryzenpay/mkdocs_emoji_link",
    author="payryzen",
    python_requires=">=3.6",
    install_requires=["mkdocs>=1.0.4"],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins":[
            "include_emoji_link = mkdocs_emoji_link.emoji_link:EmojiLink"
        ]
    },
)
# <name of plugin> = <folder><file>:<function>