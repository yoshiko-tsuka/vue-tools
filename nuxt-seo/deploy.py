import yaml
import sys
import os
import re

# judge check if seo exists in yaml
def __judgeSeoParam(yml:str):
    if not yml.get('seo'):
        print('ERROR!!! seo param does not exist in deploy.yaml.')
        sys.exit()

def __rewriteSeo(filename: str, title:str, description: str):
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as html:
            data_lines = html.read()
            data_lines = re.sub(r'(?P<top>\<title\>).+?(?P<bottom>\<\/title\>)', r'\g<top>%s\g<bottom>' % title, data_lines)
            data_lines = re.sub(r'(?P<top>data\-hid\=\"description\" name\=\"description\" content=\").+?(?P<bottom>\"\>)', r'\g<top>%s\g<bottom>' % description, data_lines)
        with open(filename, mode="w", encoding='utf-8') as html:
            html.write(data_lines)
    else:
        print('ERROR!!! ' + filename + '.html does not exist.')
        sys.exit()

def deploy():
    # start messeage
    print(
        '************ start rewrite ************')

    with open('deploy.yml') as file:
        # the best way to stop getting the warning of yaml.load is to specify the Loader= argument
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        yml = yaml.load(file, Loader=yaml.BaseLoader)
        __judgeSeoParam(yml)
        for page in yml['seo']:
            filename = yml['path']['source'] + '/index.html'
            if page != 'root':
                filename = yml['path']['source'] + '/' + page + '/index.html'
            __rewriteSeo(filename, yml['seo'][page]['title'], yml['seo'][page]['description'])

    # end messeage
    print('************ end rewrite ************')


if __name__ == "__main__":
    deploy()
