import os
from staticjinja import Site
from pathlib import Path
import minify_html

def build(outpath, searchpath):
    site = Site.make_site(
        searchpath=searchpath,
        outpath=outpath,
        contexts=[(".*\.html", _page_context)],
        rules=[(".*\.html", _page_render)],
        staticpaths=["assets"]
    )
    site.render()

    _minimize(outpath)


def _page_context(template):
    ## Reads the content of a page and places it into the body context.
    page_content = Path(template.filename).read_text()
    return {"body": page_content}


def _page_render(site, template, **kwargs):
    # # i.e. site/pages/Team.html > temp/Team.html
    out = os.path.join(site.outpath, os.path.basename(template.name))
    site.get_template(".base.html").stream(**kwargs).dump(str(out), encoding="utf-8")


def _minimize(outpath):
    path = outpath

    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file or '.css' in file:
                files.append(os.path.join(r, file))

    for f in files:
        print(f'Minimizing {f}')
        minified = minify_html.minify(open(f).read(), minify_js=True, minify_css=True)
        textfile = open(f, 'w')
        textfile.write(minified)
        textfile.close()

if __name__ == '__main__':
    build('temp\\build', 'site')