from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def get_pdf_reader(input_pdf) -> tuple:
    """ Try to open and return a pdf.
        Returns tuple with either pdf or None as first item,
        and Either an error or None as second.
    """
    try:
        pdf = PdfReader(input_pdf)
    except PdfReadError:
        raise ValueError('Invalid PDF file')
    return pdf

def get_page_range(input_pdf) -> tuple:
    """ Return page range as 1-indexed. End of range is included. """
    pdf = get_pdf_reader(input_pdf)
    number_of_pages = len(pdf.pages)
    return (1, number_of_pages)

def is_valid_page_range(pdf, start_page, end_page):
    """ Check so requested pages are within range.
        Returns tuple with is_valid and Error to throw otherwise.
    """
    number_of_pages = len(pdf.pages)
    if start_page < 1:
        raise IndexError('Start page is out of range')
    if end_page > number_of_pages:
        raise IndexError('End page is out of range')
    return True

def extract_text(input_pdf, start_page: int=None, end_page: int=None) -> str:
    """ Extract text from pdf in range start_page to end_page (inclusive). """
    # Create a pdf reader
    pdf = get_pdf_reader(input_pdf)
    
    # Check valid range of pages
    if start_page == None: start_page = 1
    if end_page == None: end_page = len(pdf.pages)
    is_valid_page_range(pdf, start_page, end_page)

    # Read specified pages (start page is 0)
    text = ''
    for page_number in range(start_page-1, end_page):
        page = pdf.pages[page_number]
        text += page.extract_text() + '\n'
    return text

if __name__ == '__main__':
    page_range = get_page_range('test-pdf.pdf')
    print(page_range)
    text = extract_text('test-pdf.pdf', *page_range)
    print(text)