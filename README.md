# Miami University's iGEM 2021 Team Website
![](https://img.shields.io/badge/-Website%20Under%20construction-orange)

## Table of Contents
- [Overview](#overview)
- [Requirements](#reqs)
- [How to Download](#download)
- [How to Sync with Wiki](#wikisync-setup)
- [iGEM Wiki General Information](#igem)

<a name="overview"/></a>
## Overview
The website for [Miami University's](https://miamioh.edu/) Team Website for the [iGEM 2021 Competition](https://2021.igem.org/Main_Page).

*Important note: There are a lot of strange and slopply looking design decisions that were made (For instance, a CSS file to undo CSS / A lack of templating). These decisions were made to take into account how iGEM's MediaWiki server handles file uploads.*

<a name="reqs"/></a>
## Requirements
- [ ] Git bash
- [ ] Python (version >= 3.0.0)
- [ ] Pip
- [ ] An [iGEM account](igem.org)
- [ ] An IDE of your choice ([VSCode](https://code.visualstudio.com/) recommended)

<a name="download"/></a>
## How to Download and Edit the Site
To download the site, simply execute the following command in Git bash.
```
$ git clone git@github.com:Kyle-L/iGEM-2021-Website.git
```
Once the repository is cloned, you can start editing the site by navigating to the `/iGEM-2020-Website/site` directory. When the site is synced to the wiki, `/iGEM-2020-Website/site` is the directory that will be synced.

<a name="wikisync-setup"/></a>
## How to Sync Site with Team Wiki
1. Check into the cloned repository's root.
```
cd iGEM-2021-Website/
```

2. Install Pipenv using pip, install pip if you haven't already.
```
pip install pipenv
```

3. Setup a virtual environment with Pipenv.
```
$ python -m venv env
```

4. Start the virtual environment
```
$ source env/bin/activate
```

5. Install the requirements
```
$ pip install -r requirements.txt
```

6. Create the file `.env` at the root of `/iGEM-2021-Website` with following information. Replace `Your_username` and `Your_password` with your iGEM info.
```
IGEM_USERNAME=Your_username
IGEM_PASSWORD=Your_password
```

7. Run `python wikisync.py`

<a name="igem"/></a>
## iGEM Wiki General Information

### Deliverables / Requirements
Please be conscientious of the requirements for the wiki and the expected deliverables. Failure to take this into account might result in potential disqualification. Carefully read through https://2021.igem.org/Competition/Deliverables/Wiki to ensure that the wiki meeting all requirements.

### Default Wiki CSS
The iGEM wiki already has a fair amount of CSS applied to each of the pages. If you would like to remove that CSS, add the following CSS to a page between the `style` tags.
```html
<style> 
#sideMenu, #top_title, .patrollink, #firstHeading, #home_logo, #sideMenu { display:none; }
#content { padding:0px; width:100%; margin-top:-7px; margin-left:0px; border:none; }
body, html { background-color:white; width: 100%; height: 100%; }
#bodyContent h1, #bodyContent h2, #bodyContent h3, #bodyContent h4, #bodyContent h5 { margin-bottom: 0px; }
#bodyContent a[href ^="https://"], .link-https { padding-right:0px; }
</style>
```
For more information of the iGEM default CSS, checkout https://2021.igem.org/Resources/Template_Documentation.

### Making Manual Changes
If you need to make changes to the iGEM wiki manually, you can go in and modify individual pages/templates using the MediaWiki UI. For more information on this checkout https://2021.igem.org/Resources/Wiki_Editing_Help.