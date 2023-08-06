from bs4 import BeautifulSoup
from markdown import markdown
def plain(mdText):
    '''
    convert markdown text to plain text
    :param mdText: a markdown string
    :return: a plain text
    '''
    return BeautifulSoup(markdown(mdText),'html.parser').get_text()

if __name__ == '__main__':
    md = '''# helloworld
**bord**

*test*
```
print("this is a python code")
```
'''
    print(plain(md))
