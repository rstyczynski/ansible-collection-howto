#!/bin/bash
cd doc
asciidoctor-multipage -D organizing 1.ORGANIZING.adoc
asciidoctor-multipage -D testing 2.TESTING.adoc 
cd ..

