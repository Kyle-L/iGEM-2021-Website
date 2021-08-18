import argparse
from bs4 import BeautifulSoup
import htmlmin
import json
import os
from pathlib import Path
from staticjinja import Site
import re


def _page_context(template):
    ## Reads the content of a page and places it into the body context.
    page_content = Path(template.filename).read_text()
    return {"body": page_content}


def _page_render(site, template, **kwargs):
    # # i.e. site/pages/Team.html > temp/Team.html
    out = os.path.join(site.outpath, os.path.basename(template.name))
    site.get_template(".base.html").stream(**kwargs).dump(str(out), encoding="utf-8")


def _minimize(html):
    """Minimizes the html for a page to save memory.

    Args:
        html (str): A single page's html as a string.

    Returns:
        str: The modified page html.
    """    
    return htmlmin.minify(html, remove_empty_space=False, remove_comments=True)

def _replace_local_links_with_absolute(html, src_link="https://2021.igem.org/Team:MiamiU_OH"):
    """
    Replaces all local or relative links with absolute links. This is done because of the iGEM
    team format does not support relative links.

    Args:
        html (str): A single page's html as a string.
        src_link (str, optional): The absolute url used to prefix onto relative links. Defaults to "https://2021.igem.org/Team:MiamiU_OH".

    Returns:
        str: The modified page html.
    """

    # A regex pattern recognize if a link starts for / to determine local links.
    pattern = "(^\/.*$)"

    soup = BeautifulSoup(html, features="lxml")

    for a in soup.findAll('a'):
        if a.has_attr('href') and (re.match(pattern , a['href']) or not a['href']):
            a['href'] = a['href'].replace(a['href'], src_link + a['href'])

    return str(soup)
    

def _set_link_target(html, open_external_links_in_new_tab = True, open_internal_links_in_new_tab = False):
    """Takes all a tags and sets whether external links to open in a new tab and whether internal links to open in the same tab.

    Args:
        html (str): A single page's html as a string.
        open_external_links_in_new_tab (bool, optional): Determines whether external links open in a new tab. Defaults to True.
        open_internal_links_in_new_tab (bool, optional): Determines whether internal links open in a new tab. Defaults to False.

    Returns:
        str: The modified page html.
    """    

    # A regex pattern to recognize external links.
    pattern = "^(?:[a-z]+:)?\/\/"

    soup = BeautifulSoup(html, features="lxml")

    for a in soup.findAll('a'):
        if a.has_attr('href') and re.match(pattern , a['href']):
            # TODO: Decide on whether to use old or new code.

            # Old code
            a['target'] = "#blank"

            # New code
            # span = soup.new_tag('span')
            # span['title'] = f'<a href="{a["href"]}" target="#blank">This will open on an external site in a new tab!</a>'
            # span['class'] = ['note', 'tooltip', 'link'] + a.get('class', [])
            # span.contents = a.contents

            # a.replace_with(span)
        else:
            del a['target']
            
    return str(soup)


def _load_glossary(file_path):
    """Given a filepath loads a glossary and de-normalizes it to speed up build time.

    Args:
        file_path (str): The file path of a glossary in the form:
        {
            '[term name]': '[definition]'
        }

    Returns:
        dict: The glossary in the form:
        {
            '[lower case term name]': {
                'name': '[the name with capitalization]',
                'definition': [definition]
        }
    """    
    dict = {}

    with open(file_path) as json_file:
        data = json.load(json_file)

        for key in data.keys():
            dict[key.lower()] = {
                'name': key,
                'definition': data[key]
            }
    
    return dict


def _add_tooltips_for_terms(html, glossary):
    """Adds tooltips to a particular page adding a tooltip span to words from the glossary.

    Args:
        html (str): A single page's html as a string.
        glossary (dict): The glossary in the form:
        {
            '[lower case term name]': {
                'name': '[the name with capitalization]',
                'definition': [definition]
        }
    """
    soup = BeautifulSoup(html, features="lxml")

    keys = "|".join(glossary.keys())

    paragraphs = soup.find_all(text = re.compile(keys, re.IGNORECASE))
    for paragraph in paragraphs:
        replaced_text = paragraph
        found_keys =  set(re.compile(keys, re.IGNORECASE).findall(str(paragraph)))
        for key in found_keys:
            title = f'<i>{glossary[key.lower()]["name"]}</i> - {glossary[key.lower()]["definition"]}'
            replaced_text = replaced_text.replace(key, f'<span class="note tooltip" title="{title}">{key}</span>')
        paragraph.replace_with(replaced_text)

    return str(soup)


def build(build_path, src_path):
    """
    Builds a site using the staticjinja templating engine.
    Also performs quality of life operations for iGEM including:
        - Converting local links to absolute. ('iGEM server does not support local.')
        - Sets non-local links to open in a new browser.
        - Minimize html and css files to speed up load time.

    Args:
        build_path (str): The output directory of the built wiki.
        src (str): The source wiki that is being built.
    """

    # Builds the site with staticjinja.
    site = Site.make_site(
        searchpath=src_path,
        outpath=build_path,
        contexts=[(".*\.html", _page_context)],
        rules=[(".*\.html", _page_render)],
        staticpaths=["assets"]
    )
    site.render()
    
    # With the site built, performs quality of life modifications.
    files = []
    for r, d, f in os.walk(build_path):
        for file in f:
            if '.html' in file or '.css' in file:
                files.append(os.path.join(r, file))

    glossary = _load_glossary(os.path.join(src_path, '.glossary.json'))

    for f in files:
        print('===================================')
        print(f'Processing {f}')
        html = open(f).read()

        if '.html' in f:
            print(f'Setting link targets for {f}')
            html = _set_link_target(html)

            print(f'Replacing local links with absolute for {f}')
            html = _replace_local_links_with_absolute(html)

            print(f'Adding glossary terms for {f}')
            html = _add_tooltips_for_terms(html, glossary)

        print(f'Minimizing {f}')
        html = _minimize(html)

        textfile = open(f, 'w')
        textfile.write(html)
        textfile.close()


if __name__ == '__main__':
    """
    If run as a main file (i.e., `python ./build.py`), Builds the local wiki

    positional arguments:
        build-path    The output path of the built wiki.
        src-path      The source path wiki that is being built.

    """

    parser = argparse.ArgumentParser(description='Builds the local wiki.')

    parser.add_argument('Build',
                        metavar='build-path',
                        type=str,
                        help='The output path of the built wiki.')

    parser.add_argument('Site',
                        metavar='src-path',
                        type=str,
                        help='The source wiki that is being built.')

    args = parser.parse_args()

    build_path = args.Build
    src = args.Site

    build(build_path, src)