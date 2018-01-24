from argparse import ArgumentParser
import os

'''
fly to server instead of argument parser
'''
from Choori.utility import render


def new(singular, plural, path):
    path = os.path.join(path, '{}'.format(singular))
    try:
        os.mkdir(path)
    except: pass
    path = os.path.join(path, '__init__.py')
    with open(path, "w+") as f:
        f.write(render('new/__init__.py.jinja', {'singular': singular, 'plural': plural}))

    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, 'config.py')
    with open(path, "a") as f:
        f.write(render('new/config.py.jinja', {'singular': singular, 'plural': plural}))


if __name__ == "__main__":
    parser = ArgumentParser(prog='choori')
    parser.add_argument('job')
    parser.add_argument('--singular', dest='singular')
    parser.add_argument('--plural', dest='plural')
    args = parser.parse_args()

    if args.job == 'init':
        path = os.path.join('.', 'crud')
        try:
            os.mkdir(path)
        except: pass
        _path = os.path.join(path, '__init__.py')
        open(_path, 'a').close()
        _path = os.path.join(path, 'user')
        new('user', 'users', path)

    if args.job == 'new':
        path = os.path.join('.', 'crud')
        new(args.singular, args.plural, path)
