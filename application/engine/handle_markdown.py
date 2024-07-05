import markdown

def markdown_to_html(text:str) -> str:
    ''' Self-explanatory '''
    return markdown.markdown(text)