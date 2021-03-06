'''
mdoc

Created by David Keegan on 3/15/12.
Copyright 2012 David Keegan.

GitHub markdown documentation generator for Objective-C

Comments in header files with three slashes(///) or block comments that start with two asterisks(/**)
are collected up then dumped out for each method. These comments may also contain markdown.

The command line takes to arguments, the first is the directory to recursivly search for header files.
The second is the readme file to write the markdown to. The second argument is optional, if it's left
off the markdown will be written to stdout.
'''

import os, sys

def markdownForHeader(root, header, output):
    currentInterface = ''
    interfaces = {currentInterface:{
        'methods': [],
        'comments': [],
        'properties': []
    }}
    currentComment = ''
    inBlockComment = False
    currentMethod = ''
    inMethodDelcaration = False
    with open(header, 'rU') as source:
        for line in source:
            line = line.strip()

            # comment
            if line.startswith('///'):
                comment = line.lstrip('/').strip()
                if not comment: continue
                currentComment += comment+'\n\n'

            # block comment
            elif line.startswith('/**'):
                comment = line.lstrip('/').lstrip('*').strip()
                if not comment: continue
                if comment.endswith('*/'):
                    comment = comment.rstrip('/').rstrip('*')
                    if not comment: continue
                    currentComment += comment+'\n\n'
                else:
                    currentComment += comment+'\n'
                    if currentComment.endswith('.'):
                        currentComment += ' '
                    inBlockComment = True
            elif line.endswith('*/'):
                comment = line.rstrip('/').rstrip('*')
                if not comment: continue
                currentComment += comment+'\n\n'
                inBlockComment = False
            elif inBlockComment:
                currentComment += line+'\n'
                if currentComment.endswith('.'):
                    currentComment += ' '

            # interface
            elif line.startswith('@interface'):
                currentInterface= line
                interfaces[currentInterface] = {
                    'methods': [],
                    'comments': [],
                    'properties': []
                }

            # property
            elif line.startswith('@property'):
                interfaces[currentInterface]['properties'].append(line)

            # method
            elif line.startswith('-') or line.startswith('+'):
                if line.endswith(';'):
                    interfaces[currentInterface]['methods'].append(line)
                    interfaces[currentInterface]['comments'].append(currentComment)
                    inMethodDelcaration = False
                    currentComment = ''
                    currentMethod = ''
                else:
                    currentMethod = line
                    inMethodDelcaration = True
            elif inMethodDelcaration:
                if line: currentMethod += ' '
                currentMethod += line
                if line.endswith(';'):
                    interfaces[currentInterface]['methods'].append(currentMethod)
                    interfaces[currentInterface]['comments'].append(currentComment)
                    inMethodDelcaration = False
                    currentComment = ''
                    currentMethod = ''


    if not interfaces: return
    output.write('##%s\n\n' % header[len(root):])
    for key,value in interfaces.iteritems():
        if key: output.write('###%s\n\n' % key)

        if value['properties']:
            output.write('```obj-c\n')
            for prop in value['properties']:
                output.write('%s\n'%prop)
            output.write('```\n\n')

        for method, comment in zip(value['methods'], value['comments']):
            output.write(comment)
            output.write('```obj-c\n%s\n```\n\n' % method)

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
