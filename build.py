import argparse
from bs4 import BeautifulSoup
import htmlmin
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
    return htmlmin.minify(html, remove_empty_space=False, remove_comments=True)


def _replace_local_links_with_absolute(html, src_link="https://2021.igem.org/Team:MiamiU_OH"):
    # A regex pattern recognize if a link starts for / to determine local links.
    pattern = "(^\/.*$)"

    soup = BeautifulSoup(html, features="lxml")

    for a in soup.findAll('a'):
        if 'href' in a and (re.match(pattern , a['href']) or not a['href']):
            a['href'] = a['href'].replace(a['href'], src_link + a['href'])

    return str(soup)
    

def _set_link_target(html, open_external_links_in_new_tab = True, open_internal_links_in_new_tab = False):
    # A regex pattern to recognize external links.
    pattern = "^(?:[a-z]+:)?\/\/"

    soup = BeautifulSoup(html, features="lxml")

    for a in soup.findAll('a'):
        if 'href' in a and re.match(pattern , a['href']):
            a['target'] = "#blank"
        else:
            del a['target']
            
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

    for f in files:
        html = open(f).read()

        if '.html' in f:
            print(f'Setting link targets for {f}')
            html = _set_link_target(html)

            print(f'Replacing local links with absolute for {f}')
            html = _replace_local_links_with_absolute(html)

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