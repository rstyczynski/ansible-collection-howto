#!/bin/bash
cd doc

# README 2 index.html
asciidoctor ../README.adoc -o index.html

# multipage documentation
asciidoctor-multipage -D organizing 1.ORGANIZING.adoc
asciidoctor-multipage -D testing 2.TESTING.adoc 

# html documentation
asciidoctor 1.ORGANIZING.adoc
asciidoctor 2.TESTING.adoc

cd ..

