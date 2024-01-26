import pytest

from project.books.models import Book

javascript_injections = [
'''<SCRIPT>alert('XSS')</SCRIPT>''',
'''<SCRIPTSRC=http://ha.ckers.org/xss.js></SCRIPT>''',
'''<SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>''',
'''<BASEHREF="javascript:alert('XSS');//">''',
'''<BGSOUNDSRC="javascript:alert('XSS');">''',
'''<BODYBACKGROUND="javascript:alert('XSS');">''',
'''<BODY ONLOAD=alert('XSS')>''',
'''<DIVSTYLE="background-image:url(javascript:alert('XSS'))">''',
'''<DIVSTYLE="background-image:url(&#1;javascript:alert('XSS'))">''',
'''<DIV STYLE="width:expression(alert('XSS'));">''',
]

sql_injections = [
'''    ' having 1=1--''',
'''hi or 1=1 --"''',
'''hi' or 1=1 --''',
'''"hi"") or (""a""=""a"''',
'''hi or a=a''',
'''hi' or 'a'='a''',
'''hi') or ('a'='a''',
''''hi' or 'x'='x';''',
'''insert''',
'''like''',
'''limit''',
'''*(|(mail=*))''',
'''*(|(objectclass=*))''',
'''or''',
"""' or ''='""",
''' or 0=0 #"''',
'''' or 0=0 --''',
'''' or 0=0 #''',
'''" or 0=0 --''',
'''or 0=0 --''',
'''or 0=0 #''',
"""' or 1 --'""",
'''' or 1/*''',
"""; or '1'='1'""",
'''' or '1'='1''',
'''' or '1'='1'--''',
'''' or 1=1''',
'''' or 1=1 /*''',
'''' or 1=1--''',
'''' or 1=1-- ''',
''''/**/or/**/1/**/=/**/1''',
'''‘ or 1=1 --''',
'''" or 1=1--''',
'''or 1=1''',
'''or 1=1--''',
''' or 1=1 or ""=''',
"""' or 1=1 or ''='""",
]

def _create_test_book(name = "Funny book", author = "Author", year_published = 1992, book_type = "Fiction", status = "available"):
    return Book(name, author, year_published, book_type, status)


def test_book_default_constructor_correct_flow():
    book = _create_test_book()
    
    assert book.name == "Funny book"
    assert book.author == "Author"
    assert book.year_published == 1992
    assert book.book_type == "Fiction"
    assert book.status == 'available'


def test_book_repr():
    book = _create_test_book()
    
    assert str(book) == "Book(ID: None, Name: Funny book, Author: Author, Year Published: 1992, Type: Fiction, Status: available)"


@pytest.mark.parametrize('value', [
    "a"
    "a" * 64,
    "!@#$%^&*()-_=+[]{}|;:'\",.<>?/",
    "こんにちは, 你好, مرحبا",
    "<p>This is a string with <b>HTML</b> tags.</p>",
    "00123",
])
def test_book_name_correct(value):
    book = _create_test_book(name = value)


@pytest.mark.parametrize('value', [
    "",
    "a" * 65,
    "   This is a string with leading and trailing spaces.   ",
    "This is a string.\nIt has a newline character.",
    "This is a string with escape characters: \t\t",
    "This is a multiline string.\nIt has multiple lines.\nEach line ends with a newline character.",
    "This is a string with \x01 control \x02 characters.",
])
def test_book_name_incorrect(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)


@pytest.mark.parametrize('value', [
    "Andrzej Andrzej-Andrzejowski"
    "a"
    "a" * 64,
    "!@#$%^&*()-_=+[]{}|;:'\",.<>?/",
    "こんにちは, 你好, مرحبا",
])
def test_book_author_correct(value):
    book = _create_test_book(author = value)


@pytest.mark.parametrize('value', [
    "",
    "a" * 65,
    "   This is a string with leading and trailing spaces.   ",
    "<p>This is a string with <b>HTML</b> tags.</p>",
    "This is a string.\nIt has a newline character.",
    "This is a string with escape characters: \t\t",
    "This is a multiline string.\nIt has multiple lines.\nEach line ends with a newline character.",
    "This is a string with \x01 control \x02 characters.",
])
def test_book_author_incorrect(value):
    with pytest.raises(Exception):
        book = _create_test_book(author = value)


@pytest.mark.parametrize('value', [
    "a"
    "a" * 20,
    "type (type)"
])
def test_book_book_type_correct(value):
    book = _create_test_book(book_type = value)


@pytest.mark.parametrize('value', [
    "",
    "a" * 21,
    "!@#$%^&*-_=+[]{}|;:'\",.<>?/",
    "こんにちは, 你好, مرحبا",
    "   This is a string with leading and trailing spaces.   ",
    "<p>This is a string with <b>HTML</b> tags.</p>",
    "This is a string.\nIt has a newline character.",
    "This is a string with escape characters: \t\t",
    "This is a multiline string.\nIt has multiple lines.\nEach line ends with a newline character.",
    "This is a string with \x01 control \x02 characters.",
])
def test_book_book_type_incorrect(value):
    with pytest.raises(Exception):
        book = _create_test_book(book_type = value)


@pytest.mark.parametrize('value', [
    "available",
    "unavailable",
])
def test_book_status_correct(value):
    book = _create_test_book(status = value)


@pytest.mark.parametrize('value', [
    "",
    "a" * 5,
    "a" * 21,
    "!@#$%^&*-_=+[]{}|;:'\",.<>?/",
    "こんにちは, 你好, مرحبا",
    "   This is a string with leading and trailing spaces.   ",
    "<p>This is a string with <b>HTML</b> tags.</p>",
    "This is a string.\nIt has a newline character.",
    "This is a string with escape characters: \t\t",
    "This is a multiline string.\nIt has multiple lines.\nEach line ends with a newline character.",
    "This is a string with \x01 control \x02 characters.",
])
def test_book_status_incorrect(value):
    with pytest.raises(Exception):
        book = _create_test_book(status = value)


@pytest.mark.parametrize('value', [
    1992,
    2050,
    1780
])
def test_book_year_correct(value):
    book = _create_test_book(year_published = value)


@pytest.mark.parametrize('value', [
    "1992",
    "13.01.2021",
    "",
    "a" * 5,
    "a" * 21,
    "!@#$%^&*-_=+[]{}|;:'\",.<>?/",
    "こんにちは, 你好, مرحبا",
    "   This is a string with leading and trailing spaces.   ",
    "<p>This is a string with <b>HTML</b> tags.</p>",
    "This is a string.\nIt has a newline character.",
    "This is a string with escape characters: \t\t",
    "This is a multiline string.\nIt has multiple lines.\nEach line ends with a newline character.",
    "This is a string with \x01 control \x02 characters.",
])
def test_book_year_incorrect(value):
    with pytest.raises(Exception):
        book = _create_test_book(year_published = value)

@pytest.mark.parametrize('value', javascript_injections)
def test_book_name_xss(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)

@pytest.mark.parametrize('value', javascript_injections)
def test_book_author_xss(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        
@pytest.mark.parametrize('value', javascript_injections)
def test_book_book_type_xss(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        
@pytest.mark.parametrize('value', javascript_injections)
def test_book_status_xss(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        

@pytest.mark.parametrize('value', sql_injections)
def test_book_name_sql_injection(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)

@pytest.mark.parametrize('value', sql_injections)
def test_book_author_sql_injection(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        
@pytest.mark.parametrize('value', sql_injections)
def test_book_book_type_sql_injection(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        
@pytest.mark.parametrize('value', sql_injections)
def test_book_status_sql_injection(value):
    with pytest.raises(Exception):
        book = _create_test_book(name = value)
        

