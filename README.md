![Logo animation](https://github.com/Kyle-L/iGEM-2021-Website/blob/main/src/assets/images/logo.gif?raw=true)
# Miami University's iGEM 2021 Team Website
![](https://img.shields.io/badge/-Website%20Under%20construction-orange)
![](https://img.shields.io/github/repo-size/Kyle-L/iGEM-2021-Website)

## Table of Contents
- [Overview](#overview)
- [Requirements](#reqs)
- [How to Download](#download)
- [How to Sync with Wiki (Remote)](#wikisync-setup)
- [How to Sync with Wiki (Local)](#wikisync-local-setup)
- [How to Edit Pages (Remote / Local)](#edit)
- [iGEM Wiki General Information](#igem)


<a name="overview"/></a>
## Overview
The website for [Miami University's](https://miamioh.edu/) Team Website for the [iGEM 2021 Competition](https://2021.igem.org/Main_Page).

*Important note: There are a lot of strange and slopply looking design decisions that were made (For instance, a CSS file to undo CSS / A lack of templating). These decisions were made to take into account how iGEM's MediaWiki server handles file uploads.*


<a name="reqs"/></a>
## Requirements
- [ ] [Git bash](https://git-scm.com/downloads)
- [ ] [Python (version >= 3.0.0)](https://www.python.org/)
- [ ] [Pip](https://pypi.org/project/pip/)
- [ ] [An iGEM account](igem.org)
- [ ] An IDE of your choice ([VSCode](https://code.visualstudio.com/) recommended)

<a name="download"/></a>
## How to Download and Setup the Site

1. Download the site.
```shell
$ git clone git@github.com:Kyle-L/iGEM-2021-Website.git
```
2. Install Pipenv using pip, install pip if you haven't already.
```shell
$ pip install pipenv
```

3. Setup a virtual environment with Pipenv.
```shell
$ python -m venv env
```

4. (on Windows) Start the virtual environment
```shell
$ ./env/Scripts/activate
```

4. (on Unix / Linux / MAC OS) Start the virtual environment
```shell
$ source env/bin/activate
```

5. Install the requirements
```shell
$ pip install -r requirements.txt
```
Now you are ready to start editing the site!


<a name="build"/></a>
## How to Build the Site (Local)
To cut down on down on code and make the site more maintainable, the Python package `staticjinja` has been setup to use as a templating engine. What does this mean? In the directory `iGEM-2021-Website/site`, the template layout of all the pages is definined in `.base.html`, however, the body of each page is defined in `iGEM-2021-Website/src/pages`. When the site is built, those bodies are inserted into the `.base.html` template layout. So, how do we build the site?

1. Navigate to the root directory
```shell
$ cd iGEM-2021-Website/
```
2. Call the build script.
```shell
$ python build.py 'temp/build' 'src'
```

You can now view the full website under `iGEM-2021-Website/temp/build`.


<a name="edit"/></a>
## How to Edit Pages (Remote / Local)
To edit pages on the wiki, navigate to [`iGEM-2021-Website/src/pages`](/src/pages). These are the html files which will be present when the site is built. For instance, if you create an html file called `test.html` and insert the following.
```html
<p>This is some placeholder text!</p>
```
When the site is built, that placeholder text will be placed into the layout defined in `.base.html`.


<a name="wikisync-setup"/></a>
## How Sync Site with Team Wiki (Remote)
This repository is setup to make use of GitHub Actions to sync the site on a push to the master branch.
On any push to the master branch, GitHub Actions will run the workflow in `.github/workflows/main.yaml` and sync the repository with the iGEM MediaWiki server.


<a name="wikisync-local-setup"/></a>
## How to Sync Site with Team Wiki (Local)
If you need to sync the site with you local wiki, you can use the following instructions.
*Note: This repository is setup to make use of GitHub Actions to sync the site on a push to the master branch. Thus, these instructions should only be used if needed.*

1. Check into the cloned repository's root.
```shell
$ cd iGEM-2021-Website/
```

2. Create the file `.env` at the root of `/iGEM-2021-Website` with following information. Replace `Your_username` and `Your_password` with your iGEM info.
```
IGEM_USERNAME=Your_username
IGEM_PASSWORD=Your_password
```

1. Run `python main.py`
```shell
$ python wikisync.py 'temp\\build' 'temp\\sync' 'MiamiU_OH'
```


<a name="helpful"/></a>
## Helpful
### HTML Converter
The file `html_converter.py` has been supplied to help convert files for web use by converting a `.docx`, `.doc`, or `.md` file to `.html`.

That can be run with the following command: 
```shell
$ python converter.py <some .docx path> <some .html path>
```


<a name="igem"/></a>
## iGEM Wiki General Information

### Deliverables / Requirements
Please be conscientious of the requirements for the wiki and the expected deliverables. Failure to take this into account might result in potential disqualification. Carefully read through https://2021.igem.org/Competition/Deliverables/Wiki to ensure that the wiki meeting all requirements.

### Default Wiki CSS
The iGEM wiki already has a fair amount of CSS applied to each of the pages. If you would like to remove that CSS, add the following CSS to a page between the `style` tags.
```html
<style> 
    #sideMenu,
    #top_title,
    .patrollink,
    #firstHeading,
    #home_logo,
    #sideMenu {
        display: none;
    }
    #content {
        padding: 0px;
        width: 100%;
        margin-top: -7px;
        margin-left: 0px;
        border: none;
    }
    body,
    html {
        background-color: white;
        width: 100%;
        height: 100%;
    }
    #bodyContent h1,
    #bodyContent h2,
    #bodyContent h3,
    #bodyContent h4,
    #bodyContent h5 {
        margin-bottom: 0px;
    }
    #bodyContent a[href ^="https://"], .link-https {
        padding-right: 0px;
    }
</style>
```
For more information of the iGEM default CSS, checkout https://2021.igem.org/Resources/Template_Documentation.

### Making Manual Changes
If you need to make changes to the iGEM wiki manually, you can go in and modify individual pages/templates using the MediaWiki UI. For more information on this checkout https://2021.igem.org/Resources/Wiki_Editing_Help.
