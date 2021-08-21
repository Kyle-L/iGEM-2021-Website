import argparse
from bs4 import BeautifulSoup
import htmlmin
import json
import os
from pathlib import Path
from staticjinja import Site
import re


process_links_whitelist = ['facebook.com', 'linkedin.com',
                           'twitter.com', 'instagram.com', 'igem.com', 'miamioh.edu', 'kylelierer.com', 'wangxlab.com']


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

    # Loads in a glossary and references to automatically add them to the site easily.
    glossary = _load_glossary(os.path.join(src_path, '.glossary.json'))
    references = _load_references(os.path.join(src_path, '.references.json'))

    # With the site built, performs quality of life modifications.
    for r, d, f in os.walk(build_path):
        for rel_file in f:
            if '.html' in rel_file or '.css' in rel_file:
                # Gets the absolute file path to make file processing cleaner.
                abs_file = os.path.join(r, rel_file)

                print(f'Processing {abs_file}')
                html = open(abs_file).read()
                page = iGEM_Page(html, glossary, references)

                if '.html' in abs_file:
                    #print(f'Adding references for {f}')
                    refer_results = page.insert_references_citations()
                    page.insert_bibliography_from_citations(refer_results)

                    #print(f'Adding glossary terms for {f}')
                    page.add_tooltips_for_terms()

                    #print(f'Setting link targets for {f}')
                    page.auto_set_link_targets(
                        tooltip_whitelist=process_links_whitelist)

                    #print(f'Replacing local links with absolute for {f}')
                    page.prefix_relative_links()

                #print(f'Minimizing {f}')
                page.minimize()

                textfile = open(abs_file, 'w')
                textfile.write(html)
                textfile.close()


def _page_context(template):
    """Reads the content of a page and places it into the body context.

    Args:
        template (str): The file path of the template file.

    Returns:
        str: The templated html page.
    """
    page_content = Path(template.filename).read_text()
    return {"body": page_content}


def _page_render(site, template, **kwargs):
    """i.e. site/pages/Team.html > temp/Team.html

    Args:
        site (any): The staticjinja site object.
        template (str): The file path of the template file.
    """
    out = os.path.join(site.outpath, os.path.basename(template.name))
    site.get_template(".base.html").stream(
        **kwargs).dump(str(out), encoding="utf-8")


def _load_references(file_path):
    """Given a filepath loads all references and converts it to a dict.

    Args:
        file_path (str): The file path of a glossary in the form:
        {
            '[reference id]': {
                'full': '[The full reference]',
                'doi_url': '[The url of the doi i.e., https://10....]',
                'title': '[The title of the reference, used for display]'
        }

    Returns:
        dict: The glossary in the form:
        {
            '[reference id]': {
                'full': '[The full reference]',
                'doi_url': '[The url of the doi i.e., https://10....]',
                'title': '[The title of the reference, used for display]'
        }
    """
    dict = {}
    with open(file_path) as json_file:
        dict = json.loads(json_file.read())

    return dict


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


class iGEM_Page ():

    def __init__(self, html, glossary, references):
        self.soup_html = BeautifulSoup(html, features="lxml")
        self.glossary = glossary
        self.references = references

    def minimize(self):
        """Minimizes the html for a page to save memory.

        Args:
            html (str): A single page's html as a string.

        Returns:
            str: The modified page html.
        """
        return htmlmin.minify(str(self.soup_html), remove_empty_space=False, remove_comments=True)

    def prefix_relative_links(self, prefix="https://2021.igem.org/Team:MiamiU_OH"):
        """
        Replaces all local or relative links with absolute links. This is done because of the iGEM
        team format does not support relative links.

        Args:
            html (str): A single page's html as a string.
            prefix (str, optional): The absolute url used to prefix onto relative links. Defaults to "https://2021.igem.org/Team:MiamiU_OH".

        Returns:
            str: The modified page html.
        """

        # A regex pattern to recognize if a link starts for / or is empty.
        # This is used to determine if it is local or not.
        pattern = "(^\/.*$)"

        for a in self.soup_html.findAll('a'):
            if a.has_attr('href') and (re.match(pattern, a['href']) or not a['href']):
                a['href'] = a['href'].replace(a['href'], prefix + a['href'])

    def auto_set_link_targets(self, open_external_links_in_new_tab=True, open_internal_links_in_new_tab=False, tooltip_whitelist=[]):
        """Takes all a tags and sets whether external links to open in a new tab and whether internal links to open in the same tab.

        Args:
            html (str): A single page's html as a string.
            open_external_links_in_new_tab (bool, optional): Determines whether external links open in a new tab. Defaults to True.
            open_internal_links_in_new_tab (bool, optional): Determines whether internal links open in a new tab. Defaults to False.
            tooltip_whitelist: (str[], optional): Ignores adding a tooltip on hrefs that contain these strings. Defaults to [].

        Returns:
            str: The modified page html.
        """

        # A regex pattern to recognize external links.
        pattern = "^(?:[a-z]+:)?\/\/"

        for a in self.soup_html.findAll('a'):
            # Applies the regex pattern; since the above pattern matches links like 'https://websitename.com', it is true if it is an external link.
            if a.has_attr('href') and re.match(pattern, a['href']):
                # Add tooltips for non-whitelisted links so the user knows it is external.
                if not any(url in a['href'] for url in tooltip_whitelist):
                    span = self.soup_html.new_tag('span')
                    span['title'] = f'<a href="{a["href"]}" target="#blank">This will open on an external site in a new tab!</a>'
                    span['class'] = ['note', 'tooltip',
                                     'link'] + a.get('class', [])
                    span.contents = a.contents

                    a.replace_with(span)

                # Whitelisted urls are just set to blank; nothing fancy.
                else:
                    a['target'] = "#blank"

            # Removes the target for internal links- they probably don't have a target, but this verifies consistency.
            else:
                del a['target']

    def add_tooltips_for_terms(self):
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
        keys = "|".join(self.glossary.keys())

        paragraphs = self.soup_html.find_all(
            text=re.compile(keys, re.IGNORECASE))
        for paragraph in paragraphs:
            replaced_text = paragraph
            found_keys = set(re.compile(
                keys, re.IGNORECASE).findall(str(paragraph)))
            for key in found_keys:
                title = f'<i><b>{self.glossary[key.lower()]["name"]}</b></i> - {self.glossary[key.lower()]["definition"]}'
                replaced_text = replaced_text.replace(
                    key, f'<span class="note tooltip" title="{title}">{key}</span>')
            paragraph.replace_with(replaced_text)

    def insert_references_citations(self):
        page_reference_order = {}

        for ref in self.soup_html.findAll('reference'):
            if ref['identifier'] not in self.references:
                continue

            ref_id = ref['identifier']

            # Here, we use the page_reference_order to determine what references come in what order.
            # This aims to mock number based reference systems.
            if ref_id not in page_reference_order:
                page_reference_order[ref_id] = page_reference_order.get(
                    ref_id, len(page_reference_order) + 1)

            span = self.soup_html.new_tag('span')

            # The entire tooltip content is built here.
            # Adds the doi if one is present, if not, we don't want to include since the users can't go there.
            span['title'] = f'<b>{self.references[ref_id]["title"]}</b> '
            if 'doi_url' in self.references[ref_id] and self.references[ref_id]["doi_url"]:
                span['title'] += f'(<a href="{self.references[ref_id]["doi_url"]}" target="#blank">External DOI Link</a>)'

            # A break to create contrast from the rest of the tooltip content.
            span['title'] += f'<br />'

            # Adds the full reference, we want to include text breaking since some links words can't wrap on mobile.
            span['title'] += f'<span><i>{self.references[ref_id]["full"]}</i></span>'

            # Add space and jump to reference if a user wants to see all other references this is a nice shortcut.
            span['title'] += f'<br /><br />'
            span['title'] += f'(<a href="#references">Jump to all references</a>)'

            # Add all other classes so that it does not break intentional styling.
            span['class'] = ['note', 'tooltip', 'link'] + ref.get('class', [])
            span.string = f'({page_reference_order[ref["identifier"]]})'

            ref.replace_with(span)

        return page_reference_order

    def insert_bibliography_from_citations(self, page_reference_order):
        ordered_refs = dict((v, k) for k, v in page_reference_order.items())
        for bib in self.soup_html.findAll('bibliography'):
            div = self.soup_html.new_tag('div')
            div['class'] = bib.get('class', [])
            for index in ordered_refs.keys():
                p = self.soup_html.new_tag('p')
                p.string = f'{index}. {self.references[ordered_refs[index]]["full"]} (<a href="{self.references[ordered_refs[index]]["doi_url"]}" target="#blank">External DOI Link</a>)'
                div.append(p)
                div['id'] = 'references'

            bib.replace_with(div)


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
