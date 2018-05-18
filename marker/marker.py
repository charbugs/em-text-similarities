import requests 
import spacy
from bs4 import BeautifulSoup, Comment
from collections import defaultdict
import itertools


DESCRIPTION = """<div>
    This marker highlights <b>text similarities</b> between this
    web page and another to compare with. It will also show snippets 
    of the corresponding text parts of the other page.
</div>"""

REPORT = """<div>
    Click the highlighted text (if any) to see the corresponding parts 
    of the web page to compare with.
</div>"""

POPUP_CONTENT ="""<div>
    %s <span style="color:dodgerblue">%s</span> %s
    
</div>"""

SNIPPET_CONTEXT = 10

class WebPageConnectionException(Exception):
    pass


###########################################################
# Marker API
###########################################################

def get_setup():
    return {
        'title': 'Web Page Comparision',
        'description': DESCRIPTION,
        'inputs': [
            {
                'label': 'URL of page to compare with',
                'id': 'target_url',
                'type': 'text'
            },
            {
                'label': 'Minimun span of words to match',
                'id': 'min_n',
                'type': 'text'
            }
        ],
	    'supportedLanguages': 'German',
	    'homepage': 'https://github.com/charbugs/em-text-similarities'
    }

def get_markup(markup_request):

    source_tokens = markup_request['tokens']

    try:
        min_n = parse_positive_int(markup_request['inputs']['min_n'])
    except ValueError:
        return { 'error': 'Span must be an positive integer.'}

    target_url = markup_request['inputs']['target_url']
    
    try:
        target_tokens = get_target_tokens(target_url)
    except WebPageConnectionException:
        return { 'error': 'Could not establish a connection to: %s' % (target_url) }

    matches = find_ngram_matches(source_tokens, target_tokens, min_n)
    markup = []

    for source_match, target_match in matches.items():
        
        markup.append({ 
            'group': get_group(source_match),
            'gloss': get_gloss(target_tokens, target_match, target_url)
        })

    return { 'markup': markup, 'report': REPORT }

###########################################################
# Parse user input
###########################################################

def parse_positive_int(n):
    n = int(n)
    if n < 0:
        raise ValueError
    return n

###########################################################
# Get tokens from target page
###########################################################

def get_target_tokens(url):
    possible_urls = get_possible_urls(url)
    html = get_html_from_url(possible_urls)
    text = get_text_from_html(html)
    return tokenize(text)

def get_possible_urls(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return ['https://' + url, 'http://' + url]
    else:
        return [url]

def get_html_from_url(possible_urls):
    resp = None

    for url in possible_urls:
        try: 
            resp = requests.get(url)
            break
        except:
            continue
    
    if not resp:
        raise WebPageConnectionException
    elif resp.status_code != 200:
        raise WebPageConnectionException
    else:
        return resp.text

def get_text_from_html(html):
    text_nodes = BeautifulSoup(html).find('body').find_all(string=True)
    text_nodes = filter(is_relevant_text_node, text_nodes)
    text_nodes = map(lambda node: node.strip(), text_nodes)
    return u' '.join(text_nodes)

def is_relevant_text_node(node):
    if not node.strip():
        return False
    if node.parent.name in ['style', 'script']:
        return False
    if isinstance(node, Comment):
        return False
    return True

def tokenize(text):
    doc = spacy.load('de_core_news_sm').tokenizer(text)
    return [token.text for token in doc if token.text.strip()]

###########################################################
# Compare ngrams
###########################################################

def find_ngram_matches(source, target, n):
    source.append(None)
    source = tuple(source)
    target = tuple(target)
    matches = {}
    i = 0
    while i < len(source) - n:
        x = 1
        pos = 0
        j = 0
        while True:
            pos = match(target, source[i:i+x])
            if pos == -1:
                x -= 1
                break
            else:
                j = pos
                x += 1
        if x >= n:
            matches[(i, i+x)] = (j, j+x)
            i += x
        else:
            i += 1
    return matches

def match(iterable, sequence):
    sequence = tuple(sequence)
    for i, ngram in enumerate(ngrams(iterable, len(sequence))):
        if ngram == sequence:
            return i
    return -1

def ngrams(iterable, n):
    tees = itertools.tee(iterable, n)
    for i, t in enumerate(tees):
        for _ in xrange(i):
            next(t, None)
    return itertools.izip(*tees)

###########################################################
# Compile markup response
###########################################################

def get_group(source_match):
    return { 'first': source_match[0], 'last': source_match[1] -1 }

def get_gloss(target_tokens, target_match, target_url):
    left = target_match[0] - SNIPPET_CONTEXT
    left = 0 if left < 0 else left
    right = target_match[1] + SNIPPET_CONTEXT
    right = len(target_tokens) if right > len(target_tokens) else right
    
    return POPUP_CONTENT % (
        ' '.join(target_tokens[left : target_match[0]]),
        ' '.join(target_tokens[target_match[0] : target_match[1]]),
        ' '.join(target_tokens[target_match[1] : right])
    )

def trim_string(string, max):
    return string if len(string) <= max else string[0:max-1] + u'\u2026'

