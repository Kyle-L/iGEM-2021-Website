import os
from staticjinja import Site
from pathlib import Path

def page_context(template):
    ## Reads the content of a page and places it into the body context.
    page_content = Path(template.filename).read_text()
    return {"body": page_content}

def page_render(site, template, **kwargs):
    # # i.e. site/pages/Team.html > temp/Team.html
    out = os.path.join(site.outpath, os.path.basename(template.name))
    site.get_template(".base.html").stream(**kwargs).dump(str(out), encoding="utf-8")

def build():
    site = Site.make_site(
        searchpath="site",
        outpath="temp\\build",
        contexts=[(".*\.html", page_context)],
        rules=[(".*\.html", page_render)],
        staticpaths=["assets"]
    )
    site.render()

if __name__ == '__main__':
    answer = input("Are you sure you want to build the wiki (Y/N): ").lower() 
    if answer == "yes" or answer == "y": 
        build()