# iGEM Site Builder
The iGEM Site Builder is a utility package to aid in the process of building a site for the iGEM competition.

- [convert](#convert)
- [template](#template)
- [post-process](#post-process)
- [build-site](#build-site)
- [sync-site](#sync-site)

## convert
Converts a file from .doc, .docx, or .md to .html and outputs that as a string..

**Usage:**
```
usage:  convert [-h] input-file output-file

Converts a file from .doc, .docx, or .md to .html to .md.

positional arguments:
  input-file   The input path to the file that is being converted from .doc, .docx, or .md to .html and outputs that as a string.
  output-file  The output path to the file that is being converted from .doc, .docx, or .md to .html or .md and outputs that as a string.

optional arguments:
  -h, --help   show this help message and exit
```

## template
Here, using a Python package called [staticjinja](https://github.com/staticjinja/staticjinja).

**Usage:**
```
usage:  template [-h] output-path source-path

Templates a source site.

positional arguments:
  output-path  The path where the templated site will be output to.
  source-path  The path where the source site and its templates are.

optional arguments:
  -h, --help   show this help message and exit
```

The file directory structure is expected to be as follows:
```
_src
├── _assets
│   ├── css
│   ├── images  
│   ├── js
│   ├── webfonts 
│
├── _pages
│   ├── index.html.
│   ├── other_page.html
│   ├── ...
│
└── .template.html
```
With this structure, all files in the 'pages' directory are inserted into the template file '.template.html'. This is done to cutdown on the amount of re-used HTML. Additionally, everything in the 'assets' directory is simply copied to the output directory.

## post-process
Applies post processing to a site. Post processing includes the following:
- Converting local links to absolute. ('iGEM server does not support relative.')
- Sets non-iGEM links to open in a new browser.
- Minimize html and css files to speed up load time.
- Replaces with `<references id="1" />` with citations based on a process file.
- Replaces with `<bibliography />` with bibliographies based on reference tags on a page.

*Note: Post process does not expect the any specific file structure as it works on a file by file basis unlike [template-site](#template-site).*

**Usage:**
```
usage:  post-process [-h] site-path process-path

Applies post processing to a site.

positional arguments:
  site-path     The path of the site being modified.
  process-path  The path with the following process files: ".glossary.json", ".references.json", and ".external-link-whitelist.json"

optional arguments:
  -h, --help    show this help message and exit
```

## build-site
Build site combines the commands [template-site](#template-site) and [post-process](#post-process) for convenience.
*Note: template-site and post-process are still separate commands in case the site needs to be built without post-processing.*

**Usage:**
usage:  build [-h] output-path source-path

Builds a source site. This combines both templating and post processing

positional arguments:
  output-path  The path where the templated site will be output to.
  source-path  The path where the source site and its templates are.

optional arguments:
  -h, --help   show this help message and exit
```
_src
├── _assets
│   ├── css
│   ├── images  
│   ├── js
│   ├── webfonts 
│
├── _pages
│   ├── index.html.
│   ├── other_page.html
│   ├── ...
│
├── .template.html
├── .external-link-whitelist.json
├── .glossary.json
└── .references.json
```
With this structure, all files in the 'pages' directory are inserted into the template file '.template.html'. This is done to cutdown on the amount of re-used HTML. Additionally, everything in the 'assets' directory is simply copied to the output directory.

## sync-site
Syncs a source site with the a team's iGEM Wiki on the iGEM MediaWiki server.

**Usage:**
```
usage:  sync [-h] site-directory temp-directory team-name

Syncs a source site with the a team's iGEM Wiki on the iGEM MediaWiki server.

positional arguments:
  site-directory  The path to the directory that is being synced to the wiki.
  temp-directory  The path to a temporary directory. Used to sync the wiki.
  team-name       The iGEM team name.

optional arguments:
  -h, --help      show this help message and exit
```