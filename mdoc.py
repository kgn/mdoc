'''
mdoc

Created by David Keegan on 3/15/12.
Copyright 2012 David Keegan.

GitHub markdown documentation generator for Objective-C

Comments in header files with three slashes(///) are collected up then dumped out for each method.
These comments may also contain markdown.

The command line takes to arguments, the first is the directory to recursivly search for header files.
The second is the readme file to write the markdown to. The second argument is optional, if it's left
off the markdown will be written to stdout.
'''

import os, sys

def markdownForHeader(root, header, output):
    methods = []
    comments = []
    currentComment = ''
    with open(header, 'rU') as source:
        for line in source:
            line = line.strip()
            if line.startswith('///'):
                comment = line.lstrip('/').strip()
                if not comment: continue
                currentComment += comment+'\n\n'
            elif line.startswith('-') or line.startswith('+'):
                methods.append(line)
                comments.append(currentComment)
                currentComment = ''
    if not methods: return
    output.write('###%s\n\n' % header[len(root)+1:])
    for method, comment in zip(methods, comments):
        output.write(comment)
        output.write('```\n%s\n```\n' % method)

def writeMarkdown(root, output):
    headers = (os.path.join(r,f) for r,d,l in os.walk(root) for f in l if os.path.splitext(f)[1] == '.h')
    for header in sorted(headers): markdownForHeader(root, header, output)

if len(sys.argv) == 1:
    print 'ERROR: you must provide a root directory'

if len(sys.argv) == 2:
    from StringIO import StringIO
    from contextlib import closing
    with closing(StringIO()) as output:
        writeMarkdown(sys.argv[1], output)
        print output.getvalue()

if len(sys.argv) == 3:
    with open(sys.argv[2], 'w') as output:
        writeMarkdown(sys.argv[1], output)
