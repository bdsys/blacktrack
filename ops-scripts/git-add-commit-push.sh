#/bin/bash
echo Staging all files, comitting using branch name q and pushing...
git add . && git commit -am "q" && git push
echo Done!
