import os

cur_dir = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(cur_dir):
    root = root.replace(cur_dir, '')
    root = root.replace('/', '.')

    for filename in files:
        basename, ext = os.path.splitext(filename)
        if ext not in ['.py']:
            continue
        if basename in ['__init__']:
            continue

        exec('from views%s import %s' % (root, basename))
