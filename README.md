# asealfon.github.io

## Generator for Adam Sealfon's homepage

This repository contains the source code and publication data for my homepage. It uses a Python-based static site generator to convert a BibTeX database into an HTML page.

## Structure

* `publications.bib`: The source for all publications and theses.
* `template.html`: The HTML skeleton for the site.
* `build.py`: Python script that injects BibTeX data into the template.
* `style.css`: CSS layout.
* `index.html`: The generated homepage.
* `me.jpg`: Profile photo.

## How to Update the Page

### 1. Update Biography or Layout
Edit `template.html` to update the introductory text, links, or the HTML structure. Use the placeholders `{{publications}}` and `{{theses}}` where the generated lists should appear.

### 2. Add a New Publication
Add the entry to `publications.bib`. The script supports the following custom fields:
* `arxiv`: arXiv link.
* `eprint`: IACR ePrint link.
* `eccc`: ECCC link.
* `mit`: MIT Libraries link.
* `journal_version`: Used for conference papers that were invited to a journal version. Should be formatted as "Invited to [Journal Name]".
* `note`: Used for awards or other highlights.

### 3. Build the Site
Ensure you have the requirements installed:
```bash
python3 -m pip install bibtexparser pyparsing

Run the generator to update `index.html`:
```bash
python3 build.py
```