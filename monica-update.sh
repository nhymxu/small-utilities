#!/usr/bin/env bash
# This script help update local monica instance to specific version
# Docs: https://github.com/monicahq/monica/blob/master/docs/installation/update.md
# Usage: ./update.sh v3.3.0

if [ -z "$1" ]
then
    echo "Not have version define."
    echo "Usage: ./update.sh v3.4.0"
    exit 1
fi

echo "===== Change to working dir"
cd public_html
echo "$PWD"

echo "===== Get latest tags from GitHub"
git fetch

echo "===== Clone the desired version"
git checkout tags/$1

echo "===== Update the dependencies of the project"
#composer install --no-interaction --no-dev --ignore-platform-reqs
rm -rf vendor && composer install

echo "===== Install frontend packages"
rm -rf node_modules && yarn install

echo "===== Build the assets (js, css)"
yarn run production

echo "===== make the proper update"
php artisan monica:update --force

echo "===== ALL DONE ====="
