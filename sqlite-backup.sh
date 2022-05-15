#!/bin/bash -x

# Ensure script stops when commands fail.
set -e

# Backup & compress our database to the temp directory.
sqlite3 /path/to/db '.backup /tmp/db'
gzip /tmp/db

# Upload backup to S3 using a rolling daily naming scheme.
# daily `date +%d`
# hourly `date +%H`
# day-hourly `date +%d%H`
aws s3 cp /tmp/db.gz s3://mybucket/db-`date +%d`.gz

# Notify dead man that back up completed successfully.
curl -d s=$? https://nosnch.in/xxxxxxxxxx &> /dev/null

# Restore way
# sqlite3 /path/to/backup 'PRAGMA integrity_check'
