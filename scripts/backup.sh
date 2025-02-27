#!/bin/bash
PROJECT_DIR=/app
DATA_DIR=/data
LOGS_DIR=$DATA_DIR/logs
BACKUPS_DIR=/backups # It's a folder for all files that should be kept, including site_media, certbot etc.
DOCKER_BACKUPS_DIR=/backups  # It's used for indicating a folder in a ocker container. Should be change both in docker-compose file and here.
DOCKER_COMPOSE_FILE=$PROJECT_DIR/build/docker-compose/docker-compose.yml
LOG_FILE=$LOGS_DIR/del_corso_backup_process.log

# Create the backup and logs directories.
mkdir -p $BACKUPS_DIR
mkdir -p $LOGS_DIR

# Get env variables
source $PROJECT_DIR/.env

# Get current datetime
date=$(date "+%Y-%m-%d")

echo "Start logging process on $date" > $LOG_FILE
PGPASSWORD=$POSTGRES_PASSWORD docker-compose -f $DOCKER_COMPOSE_FILE exec -T db mkdir -p $DOCKER_BACKUPS_DIR
PGPASSWORD=$POSTGRES_PASSWORD docker-compose -f $DOCKER_COMPOSE_FILE exec -T db pg_dump -U $POSTGRES_USER -d $POSTGRES_DB -f "$DOCKER_BACKUPS_DIR/${date}_backup.sql"
echo "Database backup has been created on ${date}" >> $LOG_FILE

rsync -a --stats --exclude="backups" --exclude="logs" "$DATA_DIR/" "$BACKUPS_DIR/"
echo "Data was copied on ${date}" >> $LOG_FILE

find $BACKUPS_DIR -name '*_backup.sql' -type f -mtime +5 -delete
echo "Old backup files were deleted" >> $LOG_FILE