##############################################################################
# initialize.
cd ~/projects/
git clone git@bitbucket.org:iogf/ysx.git ysx-code
##############################################################################
# push master.
cd ~/projects/ysx-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;

git status
git add *
git commit -a
git push -u origin master
##############################################################################
# push development.
cd ~/projects/ysx-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;

git status
git add *
git commit -a
git push -u origin development

##############################################################################
# install ysx.
cd ~/projects/ysx-code
sudo bash -i
python setup.py install
rm -fr build
exit
##############################################################################
# get it on pip.

cd ~/projects/ysx-code
python setup.py sdist register upload
rm -fr dist
##############################################################################
# create the develop branch
git branch -a
git checkout -b development
git push --set-upstream origin development


