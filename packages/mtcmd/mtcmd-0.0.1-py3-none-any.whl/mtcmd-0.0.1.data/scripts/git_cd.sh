#!/bin/bash

# cd to a given directory and optionally do 'git pull' if the directory is a git repo

cd ${1}

if git rev-parse --git-dir > /dev/null 2>&1; then
    git pull
fi
