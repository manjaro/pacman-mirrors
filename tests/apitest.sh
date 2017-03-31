#!/usr/bin/env bash

BRANCH=$( (pacman-mirrors --api --get-branch >&1) 2>&1 )
echo "branch is '${BRANCH}'"
