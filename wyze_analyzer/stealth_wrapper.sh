#!/bin/bash
# Stealth wrapper - renames process and runs command

# Rename process using exec -a
exec -a systemd "$@"

