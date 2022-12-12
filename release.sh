#!/bin/bash -e

if [ -z $1 ]; then
	CURRENT_VERSION=$(PYTHONPATH=. python3 -c 'import nss_cache; print(nss_cache.__version__)')
    a=( ${CURRENT_VERSION//./ } )
    (( a[${#a[@]}-1] += 1 ))
    NEW_VERSION=$(IFS=.; echo "${a[*]}")
else
    NEW_VERSION=$1
fi

echo Minting $NEW_VERSION
DATE=$(date +%Y-%m-%d)

sed -i "1c\.TH NSSCACHE 1 $DATE \"nsscache $NEW_VERSION\" \"User Commands\"" nsscache.1
sed -i "1c\.TH NSSCACHE.CONF 5 $DATE \"nsscache $NEW_VERSION\" \"File formats\"" nsscache.conf.5
sed -i "s/__version__ = '.*'/__version__ = '$NEW_VERSION'/" nss_cache/__init__.py


git commit -a -m "Mint version $NEW_VERSION"
git tag -s "version/$NEW_VERSION" -m "version/$NEW_VERSION"
