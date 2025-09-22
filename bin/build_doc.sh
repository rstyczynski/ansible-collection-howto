#!/bin/bash
cd doc
asciidoctor-multipage -D testing 2.TESTING.adoc 
asciidoctor-multipage -D html 1.ORGANIZING.adoc
cd ..

