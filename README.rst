===========
fdr
===========


.. image:: https://img.shields.io/pypi/v/fdr.svg
        :target: https://pypi.python.org/pypi/fdr

.. image:: https://img.shields.io/travis/jonathanchukinas/fdr.svg
        :target: https://travis-ci.org/jonathanchukinas/fdr

.. image:: https://readthedocs.org/projects/fdr/badge/?version=latest
        :target: https://fdr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Validate a Function & Design Requirements document.

* Free software: MIT license
* Documentation: https://fdr.readthedocs.io.


Quick Start
------------

J&J Quick Start
''''''''''''''''''''''
1. **Install Python**
    a. Navigate to J&J App Store. You may need to use Internet Explorer. Users have had difficulty with Chrome.
    #. Search ``Python``. You should see something similar to ``Python 3.6``. Add it to cart and install.
    #. No restart is required.
#. **Run Command Prompt with Elevated Privileges**
    a. Do not call IRIS.
    #. Hit the ``Windows Key`` and type ``cmd`` to search for the Windows command prompt
    #. Right-click ``cmd`` and select ``open file location``. This opens File Explorer.
    #. Right-click on the ``cmd`` icon and select ``Run with elevated privileges``.
#. **Install** ``dps-rtm``
    a. In Command Prompt, type ``pip install dps-rtm``
    #. If this throws an error, try instead: ``python -m pip install dps-rtm``. Hint: the up-arrow accesses previous commands to reduce the amount of typing you need to do.
    #. Note: You might see a note about ``pip`` being out of date. This is ok, but feel free to update it as suggested.
#. **Run** ``rtm``
    a. In Command Prompt, type ``rtm``

Validation Rules
-----------------
General Notes
'''''''''''''
- The FDR sheet must have the title 'Procedure Based Requirements'
- If multiples headers share the same name, only the first will be used.
- All columns get checked for 1) Exist and 2) Correct left-to-right order.

ID
''
- not empty
- sorts alphabetically
- if procedure step, is formatted "P###" e.g. P010 
- if need, input or output, is formatted "P###-###" where first three digits correlate to procedure step. e.g. P010-010. 

Cascade Block
'''''''''''''
- one and only one cell gets marked (WorkItemObject)
- no missing steps (CascadeObject)
- each requirements path starts with Procedure Step (CascadeObject)
- each requirements path terminates in 'F' (CascadeObject)
- all DO Solution levels get used (CascadeObject) *
- only contains characters X or F

Cascade Level
'''''''''''''
- not empty
- validated input list
- matches selection in Cascade Block (WorkItemObject)
- is "procedure step", "voc user need", "busniess need", "risk need", "design input" or "design output"

Requirement Statement
'''''''''''''''''''''
- Not empty (WorkItemObject)
- CHILD - valid pointer (CascadeObject)
- ADDITIONALPARENT 
- valid pointer (CascadeObject)
- check for ______ hashtags e.g. #Function, #MatingParts (WorkItemObject)
- report on extra tags found? (WorkItemObject)

Requirement Rationale
'''''''''''''''''''''
- not empty

VorV Strategy
'''''''''''''
- not empty
- if "business need", strategy is not required. all others require a strategy

VorV Results
''''''''''''
- not empty
- if "business need", results are not required. all others require results
- if windchill number is present, check its formatting. (10 digits)
- print report of applicable documents? 

Devices
'''''''
- not empty
- no repeats in cell
- print report of device list?

DO Features
'''''''''''
- not empty
- if contains features that are CTQs, CTQ ID should be formatted as "(CTQ##)"
- if contains features that are CTQs, check that CTQ Y/N column is "yes"
- print report of CTQ IDs and correlated features/devices?

CTQ Y/N
'''''''
- not empty
- validated input list
- is "yes", "no", "N/A", or " - " (only procedure step can have " - ")
- if yes, check for CTQ IDs in DO Features column

Other
'''''
- 'N/A' check? (WorkItemObject)
- " - " check
