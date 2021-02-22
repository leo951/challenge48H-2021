#!/bin/sh
i=1
base="photos produits/"
for f in 'photos produits'/*
do
    if [[ $f == *'.jpg' ]]; then
        mv "$f" 'photos produits'/$i.jpg
    fi
    if [[ $f == *'.JPG' ]]; then
        mv "$f" 'photos produits'/$i.JPG
    fi
    if [[ $f == *'.jpeg' ]]; then
        mv "$f" 'photos produits'/$i.jpeg
    fi
    if [[ $f == *'.png' ]]; then
        mv "$f" 'photos produits'/$i.png
    fi
    echo $base$i " -> done"
   ((i=i+1))
   
done
base="photos ambiance/"
((i=1))
for f in 'photos ambiance'/*
do
    if [[ $f == *'.jpg' ]]; then
        mv "$f" 'photos ambiance'/$i.jpg
    fi
    if [[ $f == *'.JPG' ]]; then
        mv "$f" 'photos ambiance'/$i.JPG
    fi
    if [[ $f == *'.jpeg' ]]; then
        mv "$f" 'photos ambiance'/$i.jpeg
    fi
    if [[ $f == *'.png' ]]; then
        mv "$f" 'photos ambiance'/$i.png
    fi
    echo $base$i " -> done"
   ((i=i+1))
done
read -p "Press any key to resume ..."