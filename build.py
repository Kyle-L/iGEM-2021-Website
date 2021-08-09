import argparse
import os
from staticjinja import Site
from pathlib import Path
import htmlmin


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
        minified = htmlmin.minify(open(f).read(), remove_empty_space=False, remove_comments=True)
        textfile = open(f, 'w')
        textfile.write(minified)
        textfile.close()


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
    

if __name__ == '__main__':
    """
    If run as a main file (i.e., `python ./build.py`), Builds the local wiki

    positional arguments:
        build-directory  The output directory of the built wiki.
        src              The source wiki that is being built.

    """

    parser = argparse.ArgumentParser(description='Builds the local wiki.')

    parser.add_argument('Build',
                        metavar='build-directory',
                        type=str,
                        help='The output directory of the built wiki.')

    parser.add_argument('Site',
                        metavar='src',
                        type=str,
                        help='The source wiki that is being built.')

    args = parser.parse_args()

    build_path = args.Build
    src = args.Site

    build(build_path, src)