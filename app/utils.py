from bs4 import BeautifulSoup

TAGS = ['div','a','b','p','img','em','strong','font','ol','ul','li','br','i','dl','hr','center','del','u','strike']

ATTRS = ['src',
        'align',
        'width',
        'alt',
        'size']


'''
acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
      'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
      'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
      'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
      'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
      'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
      'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
      'thead', 'tr', 'tt', 'u', 'ul', 'var']

acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
  'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
  'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
  'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
  'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
  'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
  'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
  'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
  'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
  'usemap', 'valign', 'value', 'vspace', 'width']
'''

def clean_html( fragment ):
    soup = BeautifulSoup( fragment )
    removed = False
    for tag in soup.findAll(True): # find all tags
        if tag.name not in TAGS:
            tag.hidden=True # remove the bad ones
            removed = True
        else: # it might have bad attributes
                # a better way to get all attributes?
                for attr in tag.attrs:
                    if attr not in ATTRS:
                        tag[attr]=''

        # turn it back to html
    return soup.prettify()
