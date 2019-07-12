#!/bin/bash
set -e

# VARS ---------------------------------------------------------------------------
ORGANIZATION_NAME=$(head -n 1 .circleci/vars/organization_name)
PROJECT_NAME=$(head -n 1 .circleci/vars/project_name)

# IMAGE INFO ----------------------------------------------------------------------
IMAGE_NAME=$ORGANIZATION_NAME/$PROJECT_NAME

# GIT INFO ------------------------------------------------------------------------
LATEST_COMMIT=$(git rev-parse HEAD)
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
CLEANED_BRANCH_NAME=${BRANCH_NAME//\//-}  # Slashes can't go through

# BUILD ---------------------------------------------------------------------------
docker build -t $IMAGE_NAME:$CLEANED_BRANCH_NAME .
docker build -t $IMAGE_NAME:$CLEANED_BRANCH_NAME-$LATEST_COMMIT .
echo $IMAGE_NAME:$CLEANED_BRANCH_NAME
