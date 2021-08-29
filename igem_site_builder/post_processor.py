import argparse
from bs4 import BeautifulSoup
import htmlmin
import json
import os
import re
from abc import ABC, abstractmethod


class console_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def apply_post_processes(build_path, process_path):
    """
    Applies post processing to a site. This includes:
    - Converting local links to absolute. ('iGEM server does not support local.')
    - Sets non-local links to open in a new browser.
    - Minimize html and css files to speed up load time.
    - Replaces with '<references id="1" /> with citations based on a process file.'
    - Replaces with '<bibliography /> with bibliographies based on reference tags on a page.'

    Args:
        build_path (str): The output directory of the built wiki.
        src (str): The source wiki that is being built.
    """
    process_links_whitelist = json.load(open(os.path.join(process_path, '.external-link-whitelist.json')))
    glossary = _load_glossary(os.path.join(process_path, '.glossary.json'))
    references = _load_references(os.path.join(process_path, '.references.json'))

    # With the site built, performs quality of life modifications.
    for r, d, f in os.walk(build_path):
        for file in f:

            process_file = None
            # try:
            if '.css' in file:
                print(console_colors.HEADER + f'Processing {file}' + console_colors.ENDC)
                process_file = iGEM_CSS(os.path.join(r, file))

                print(console_colors.OKBLUE + f'Minimizing...' + console_colors.ENDC)
                process_file.minimize()

                print(console_colors.OKGREEN + f'Done!' + console_colors.ENDC)
                process_file.save()

            if '.html' in file:
                print(console_colors.HEADER + f'Processing {file}' + console_colors.ENDC)
                process_file = iGEM_HTML(os.path.join(r, file))

                print(console_colors.OKBLUE + f'Adding references...' + console_colors.ENDC)
                process_file.insert_references(references)

                print(console_colors.OKBLUE + f'Setting link targets...' + console_colors.ENDC)
                process_file.set_page_link_targets_automatically(whitelist=process_links_whitelist)

                print(console_colors.OKBLUE + f'Adding glossary terms...' + console_colors.ENDC)
                process_file.add_tooltips_for_terms(glossary)

                print(console_colors.OKBLUE + f'Replacing local links with absolute...' + console_colors.ENDC)
                process_file.prefix_relative_links()

                print(console_colors.OKBLUE + f'Minimizing...' + console_colors.ENDC)
                process_file.minimize()

                print(console_colors.OKGREEN + f'Done!' + console_colors.ENDC)
                process_file.save()
            # except:
            #     print(console_colors.WARNING +
            #           f'Something went wrong processing {file}' + console_colors.ENDC)


def _load_glossary(file_path):
    """Given a filepath loads a glossary and de-normalizes it to speed up apply_post_processes time.

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

    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)

        for key in data.keys():
            dict[key.lower()] = {
                'name': key,
                'definition': data[key]
            }

    return dict


def _load_references(file_path):
    """Given a filepath loads all references and converts it to a dict.

    Args:
        file_path (str): The file path of a glossary in the form:
        {
            '[reference id]': {
                'full': '[The full reference]',
                'url' (optional): '[The url of the doi i.e., https://10....]',
                'title': '[The title of the reference, used for display]'
        }

    Returns:
        dict: The glossary in the form:
        {
            '[reference id]': {
                'full': '[The full reference]',
                'url' (optional): '[The url of the doi i.e., https://10....]',
                'title': '[The title of the reference, used for display]'
        }
    """
    dict = {}
    with open(file_path, encoding='utf-8') as json_file:
        dict = json.loads(json_file.read())

    return dict


class iGEM_File(ABC):
    @abstractmethod
    def __init__(self, path):
        self._path = path

    @abstractmethod
    def minimize(self):
        """Minimizes html, css, and js to save memory.

        Args:
            content (str): An .html, .css, or .js file as a string.

        Returns:
            str: The modified page html.
        """
        pass

    @abstractmethod
    def save(self):
        pass


class iGEM_CSS(iGEM_File):
    def __init__(self, path):
        super().__init__(path)
        self._content = open(self._path).read()

    def minimize(self):
        self._content = htmlmin.minify(self._content)

    def save(self):
        textfile = open(self._path, 'w')
        textfile.write(self._content)
        textfile.close()


class iGEM_HTML(iGEM_File):
    def __init__(self, path):
        super().__init__(path)
        self._soup = BeautifulSoup(open(self._path, encoding='utf-8').read(), features='lxml')

    def minimize(self):
        self._soup = BeautifulSoup(htmlmin.minify(
            str(self._soup)), features='lxml')

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

        for a in self._soup.findAll('a'):
            if a.has_attr('href') and (re.match(pattern, a['href']) or not a['href']):
                a['href'] = a['href'].replace(a['href'], prefix + a['href'])

    def set_page_link_targets_automatically(self, open_external_links_in_new_tab=True, open_internal_links_in_new_tab=False, whitelist=[]):
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

        for a in self._soup.findAll('a'):
            if a.has_attr('href') and re.match(pattern, a['href']):
                if not any(url in a['href'] for url in whitelist):
                    a.name = 'span'
                    a['title'] = f'<a href="{a["href"]}" target="#blank">This will open on an external site in a new tab!</a>'
                    a['class'] = ['tooltip', 'link'] + a.get('class', [])
                else:
                    a['target'] = "#blank"

    def add_tooltips_for_terms(self, glossary):
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
        keys = "|".join(glossary.keys())

        paragraphs = self._soup.find_all(text=re.compile(keys, re.IGNORECASE))
        for paragraph in paragraphs:
            replaced_text = paragraph
            found_keys = set(re.compile(
                keys, re.IGNORECASE).findall(str(paragraph)))
                
            for key in found_keys:
                title = f'<i><b>{glossary[key.lower()]["name"]}</b></i> - {glossary[key.lower()]["definition"]}'
                replaced_text = replaced_text.replace(key, f'<span class="note tooltip" title="{title}">{key}</span>')

            paragraph.replace_with(BeautifulSoup(replaced_text, features="html.parser"))

    def insert_references(self, references):
        page_references = self._insert_reference_citations(references)
        self._insert_bibliography_from_citations(references, page_references)

    def _insert_reference_citations(self, references):
        page_reference_order = {}

        for ref in self._soup.findAll('reference'):
            if ref['identifier'] not in references:
                continue

            ref_id = ref['identifier']

            # Here, we use the page_reference_order to determine what references come in what order.
            # This aims to mock number based reference systems.
            if ref_id not in page_reference_order:
                page_reference_order[ref_id] = page_reference_order.get(ref_id, len(page_reference_order) + 1)

            span = self._soup.new_tag('span')

            # The entire tooltip content is built here.
            # Adds the doi if one is present, if not, we don't want to include since the users can't go there.
            span['title'] = f'<b>{references[ref_id]["title"]}</b> '
            if 'doi_url' in references[ref_id] and references[ref_id]["doi_url"]:
                span['title'] += f'<a href="{references[ref_id]["doi_url"]}" target="#blank">(External DOI Link)</a>'

            # A break to create contrast from the rest of the tooltip content.
            span['title'] += f'<br />'

            # Adds the full reference, we want to include text breaking since some links words can't wrap on mobile.
            span['title'] += f'<span><i>{references[ref_id]["full"]}</i></span>'

            # Add space and jump to reference if a user wants to see all other references this is a nice shortcut.
            span['title'] += f'<br /><br />'
            span['title'] += f'<a href="#references">(Jump to all references)</a>'

            # Add all other classes so that it does not break intentional styling.
            span['class'] = ['note', 'tooltip'] + ref.get('class', [])
            span.string = f'({page_reference_order[ref["identifier"]]})'

            ref.replace_with(span)

        return page_reference_order

    def _insert_bibliography_from_citations(self, references, page_reference_order):
        ordered_refs = dict((v, k) for k, v in page_reference_order.items())
        for bib in self._soup.findAll('bibliography'):
            div = self._soup.new_tag('div')
            div['class'] = bib.get('class', [])
            for index in ordered_refs.keys():
                a = self._soup.new_tag('a')
                p = self._soup.new_tag('p')
                div.append(p)

                reference = references[ordered_refs[index]]

                if 'url' in reference and reference["url"]:
                    a['href'] = reference["url"]
                    a['target'] = '#blank'
                    a.string = f'({reference["url"]})'

                p.string = f'{index} {reference["full"]} '

                p.append(a)

                div['id'] = 'references'
            bib.replace_with(div)

    def save(self):
        textfile = open(self._path, 'w', encoding='utf-8')
        textfile.write(str(self._soup))
        textfile.close()
