import argparse
import os
from pathlib import Path
from staticjinja import Site


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


def template(build_path, src_path):
    """
    Templates a site using the staticjinja templating engine.

    Args:
        build_path (str): The output directory of the templated site.
        src (str): The source site that is being templated.
    """

    print(console_colors.HEADER + f'Templating site.' + console_colors.OKBLUE)

    try:
        # Builds the site with staticjinja.
        site = Site.make_site(
            searchpath=os.path.abspath(src_path),
            outpath=os.path.abspath(build_path),
            contexts=[(".*\.html", _page_context)],
            rules=[(".*\.html", _page_render)],
            staticpaths=["assets"],
            encoding='utf8'
        )
        site.render()
    except:
        print(console_colors.WARNING + f'Something went wrong templating the site!!!' + console_colors.ENDC)

    print(console_colors.OKGREEN + f'Templating done!' + console_colors.ENDC)


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
    site.get_template('.template.html').stream(**kwargs).dump(str(out), encoding="utf-8")