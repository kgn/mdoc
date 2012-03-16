# mdoc [M↓]

GitHub markdown documentation generator for Objective-C

Comments in header files with three slashes(`///`) are collected up then dumped out for each method. These comments may also contain markdown.

The command line takes to arguments, the first is the directory to recursivly search for header files.

The second is the readme file to write the markdown to. The second argument is optional, if it's left off the markdown will be written to stdout.

Two examples of mdoc being used in the wild are on [BBlock](https://github.com/kgn/BBlock) and [KGLib](https://github.com/kgn/KGLib).