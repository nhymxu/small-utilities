#!/bin/bash

# Folder structure
# ~/Vault
#    ↳ backup
#    ↳ bin
#    ↳ documents
#    ↳ projects

# Cron setup
# 0 2 * * * sh ~/Vault/bin/vault-backup.sh

cd ~/Vault/backup/dotfiles

MACHINE=$(whoami)@$(hostname)
mkdir -p $MACHINE
cd $MACHINE

cp ~/.config/VSCodium/User/settings.json settings.json
cp ~/.s3cfg s3cfg
cp ~/.bash_extended bash_extended
cp ~/.ssh ssh -rf

codium --list-extensions > vscode-extension.txt
dconf dump /com/gexperts/Tilix/ > tilix.dconf

cd ~/Vault
s3cmd sync --delete-removed --exclude 'node_modules/*' --exclude '.git/*' --exclude '.venv/*' ./ s3://bucket-name/backup/

echo `date +"%D %T"` >> ~/.vault.log

notify-send \
	-u normal \
	-i /usr/share/icons/Adwaita/96x96/status/security-medium-symbolic.symbolic.png \
	"Vault sync succeded at `date +"%D %T"`"
