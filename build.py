import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

def format_authors(author_str):
    """Converts 'A and B and C' to 'A, B, and C'."""
    authors = author_str.split(' and ')
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    return f"{', '.join(authors[:-1])}, and {authors[-1]}"

def generate_site():
    # 1. Load the BibTeX data
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    try:
        with open('publications.bib', encoding='utf-8') as bibfile:
            db = bibtexparser.load(bibfile, parser)
    except Exception as e:
        print(f"Error loading bib file: {e}")
        return

    # 2. Sort and Categorize
    pubs = [e for e in db.entries if e.get('ENTRYTYPE') not in ['phdthesis', 'mastersthesis']]
    theses = [e for e in db.entries if e.get('ENTRYTYPE') in ['phdthesis', 'mastersthesis']]

    # pubs.sort(key=lambda x: x.get('year', '0'), reverse=True)
    # theses.sort(key=lambda x: x.get('year', '0'), reverse=True)

    def format_list(entries, show_year=True):
        html = ""
        for e in entries:
            title = e.get('title', '').strip('{}')
            authors = format_authors(e.get('author', ''))
            year = e.get('year', '')
            venue = e.get('journal', e.get('booktitle', e.get('school', '')))
            
            # Venue string logic: hide year for theses
            if show_year and year:
                venue_str = f"{venue}, {year}"
            else:
                venue_str = venue
            
            # Invited Journal Version logic
            invitation = e.get('journal_version', '')
            inv_str = ""
            if invitation:
                if invitation.startswith("Invited to "):
                    core = invitation.replace("Invited to ", "")
                    inv_str = f'Invited to <em>{core}</em><br/>'
                else:
                    inv_str = f'<em>{invitation}</em><br/>'
            
            # Highlight note (e.g. award) & Links
            note = e.get('note', '')
            highlight_note_str = f'<span class="highlightnote">{note}</span><br/>' if note else ""

            links = []
            link_keys = {'arxiv': 'arXiv', 'eprint': 'ePrint', 'eccc': 'ECCC', 'mit': 'MIT Libraries', 'url': 'URL'}
            for key, label in link_keys.items():
                if key in e: links.append(f'<a href="{e[key]}">{label}</a>')
            link_str = f"Available at [{', '.join(links)}]" if links else ""
            
            html += f"""
            <li>
                <strong>{title}</strong><br/>
                {authors}<br/>
                <em>{venue_str}</em><br/>
                {inv_str}{highlight_note_str}{link_str}
            </li>"""
        return html

    # 3. Inject into Template
    try:
        with open('template.html', 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Format publications with year, theses without
        final_html = template.replace('{{publications}}', format_list(pubs, show_year=True))
        final_html = final_html.replace('{{theses}}', format_list(theses, show_year=False))
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("Successfully built index.html from template.")
    except Exception as e:
        print(f"Error processing template: {e}")

if __name__ == "__main__":
    generate_site()

