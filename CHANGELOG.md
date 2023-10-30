<hr>

# Version 2.0.0

<hr>


## <ins>New Features</ins>


### Locations

- The sidebar now contains a new Tab “Locations” where locations are displayed in a tree structure
- Added new Special Control “Location” for types which enables types to be assigned to locations


### Assistant

- Reworked initial assistant
- It is now possible to select branches and profiles and DATAGERRY will automatically create the corresponding types for a quick start
- Added a link to the assistant in the toolbox (**Toolbox => Assistant**) so that it is possible to start it manually


## <ins>Changes</ins>

- Rework of the Feedback-Form (**Toolbox => Feedback**)
- When creating or editing a type it is no longer possible to proceed to the next step (or press the “Save”-button) if this step has invalid fields
- Added an “x” to be able to clear the filter input in the sidebar
- Types are now only deletable if no object instances exist of this type
- Dropped support for python 3.6, 3.7 and 3.8


## <ins>Bugfixes</ins>

- Fixed a bug displaying popup boxes behind the gray overlay background
- Fixed an error where the progress bar of a toast was not animated(Popup confirmations in the top right corner)
- Fixed a bug where saving a column config the input field would get an invalid red border. The red border now correctly only appear if the input field is empty when clicking the save button
- Fixed a display bug in Exportd list where the column name was “Name” instead of “Label” 
- Fixed an error where Links between objects where not displayed in the object overview
- Fixed a bug where the filter in the sidebar did not hide “Uncategorised” Types if the filter-input did not match
- Fixed an occurring error when pressing the “Show Tabs” button in the object overview when the object didn’t have any references 
- Fixed a bug where object counters where not correctly updated when switching between “Only Active Objects” and “All Objects”-Mode
- Fixed a display bug where other elements overlapped the sidebar when in cropped view
- Fixed an error when copying dates to clipboard resulting in output to be [object Object]
- Fixed bugs with the “Save” and “Cancel” button when creating new categories not working as intended
- Fixed an error occurring when closing popups via the “x” in the top right corner at several places in DATAGERRY
- Fixed stacking counters when interacting with bulk changes
- Fixed an error appearing when pressing to often and to fast references in object overviews
- Fixed a bug falsely displaying an error when objects are exported
- Fixed a bug where multiple clicks were required to change the order of a table column
- Fixed a visual bug where the scroll bar on text area fields was to small to be selected
- Fixed a visual bug for the type overview on the dashboard
- Fixed a visual bug hiding the filter field in the sidebar when cropping browser to mobile view mode
- Fixed several occurrences where parts of the application were not reloaded after changes took place
- Fixed a bug which cleared the table when clicking “Default configs” in object list
- Fixed a bug where the sidebar was not reloaded after deleting a type and still showing the deleted type


## <ins>Frontend Changes</ins>

- Bumped Angular packages to 15.2.4
- Bumped Angular package dependencies to fit Angular 15.2.4


## <ins>Backend Changes</ins>

- Bumped Python to Version 3.9.16
- Tests are run against MongoDB 4.4, 5.0 and 6.0 with Python 3.9 (Dropped tests for Python 3.7, 3.8 and MongoDB 4.2)
- Added location logics to backend
- Deleting an object with also delete the corresponding location


### Python Package Bumps

- **alabaster** to **0.7.13** (from 0.7.12)
- **altgraph** to **0.17.3** (from 0.17)
- **astroid** to **2.15.5** (from 2.5.1)
- **attrs** to **23.1.0** (from 20.3.0)
- **Authlib** to **1.2.1** (from 0.15.3)
- **Babel** to **2.12.1** (from 2.8.0)
- **blinker** to **1.6.2** (from 1.4.0)
- **Cerberus** to **1.3.4** (from 1.3.2)
- **certifi** to **2023.7.22** (from 2020.6.20)
- **cffi** to **1.15.1** (from 1.14.3)
- **chardet** to **5.1.0** (from 3.0.4)
- **click** to **8.1.3** (from 7.1.2)
- **coverage** to **7.2.7** (from 5.5)
- **cryptography** to **41.0.1** (from 3.4.7)
- **docutils** to **0.20.1** (from 0.16)
- **et-xmlfile** to **1.1.0** (from 1.0.1)
- **flake8** to **6.0.0** (from 3.8.4)
- **Flask** to **2.3.2** (from 1.1.2)
- **Flask-Cors** to **4.0.0** (from 3.0.9)
- **gunicorn** to **20.1.0** (from 20.0.4)
- **idna** to **3.4** (from 2.10)
- **imagesize** to **1.4.1** (from 1.2.0)
- **iniconfig** to **2.0.0** (from 1.1.1)
- **isort** to **5.12.0** (from 5.5.3)
- **itsdangerous** to **2.1.2** (from 1.1.0)
- **Jinja2** to **3.1.2** (from 2.11.2)
- **lazy-object-proxy** to **1.9.0** (from 1.4.3)
- **ldap3** to **2.9.1** (from 2.8.1)
- **MarkupSafe** to **2.1.3** (from 1.1.1)
- **mccabe** to **0.7.0** (from 0.6.1)
- **openpyxl** to **3.1.2** (from 3.0.5)
- **packaging** to **23.1** (from 20.4)
- **Pillow** to **10.0.0** (from 8.1.2)
- **pluggy** to **1.2.0** (from 0.13.1)
- **py** to **1.11.0** (from 1.10.0)
- **pyasn1** to **0.5.0** (from 0.4.8)
- **pycodestyle** to **2.10.0** (from 2.6.0)
- **pycparser** to **2.21** (from 2.20)
- **pycryptodome** to **3.18.0** (from 3.10.1)
- **pyflakes** to **3.0.1** (from 2.2.0)
- **Pygments** to **2.15.1** (from 2.7.1)
- **pyinstaller** to **5.1.3.0** (from 4.0)
- **pyinstaller-hooks-contrib** to **2023.4** (from 2020.8)
- **pylint** to **2.17.4** (from 2.7.2)
- **PyMySQL** to **1.1.0** (from 0.10.1)
- **pyOpenSSL** to **23.2.0** (from 19.0.0)
- **pyparsing** to **3.1.0** (from 2.4.7)
- **PyPDF2** to **3.0.1** (from 1.26.0)
- **pytest** to **7.4.0** (from 6.2.2)
- **pytest-cov** to **4.1.0** (from 2.11.1)
- **pytest-html** to **3.2.0** (from 3.1.1)
- **pytest-metadata** to **3.0.0** (from 1.11.0)
- **python-dateutil** to **2.8.2** (from 2.8.1)
- **pytz** to **2023.3** (from 2020.1)
- **reportlab** to **3.6.13** (from 3.5.50)
- **requests** to **2.31.0** (from 2.24.0)
- **six** to **1.16.0** (from 1.15.0)
- **snowballstemmer** to **2.2.0** (from 2.0.0)
- **Sphinx** to **7.0.1** (from 3.2.1)
- **sphinxcontrib-applehelp** to **1.0.4** (from 1.0.2)
- **sphinxcontrib-htmlhelp** to **2.0.1** (from 1.0.3)
- **sphinxcontrib-httpdomain** to **1.8.1** (from 1.7.0)
- **sphinxcontrib-serializinghtml** to **1.1.5** (from 1.1.4)
- **toml** to **0.10.2** (from 0.10.1)
- **urllib3** to **2.0.3** (from 1.25.10)
- **Werkzeug** to **2.3.6** (from 1.0.1)
- **wrapt** to **1.15.0** (from 1.12.1)
- **xhtml2pdf** to **0.2.11** (from 0.2.4)

