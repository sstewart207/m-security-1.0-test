#!/bin/bash
# Mommy Security v1.0 - Warmth & Protection For Your OS
# Nullifier Script: Scrubs birthDate from systemd userdb and masks enforcement sockets.

set -euo pipefail

# Hardcoded safe date as per Ageless Linux reference
SAFE_DATE="1970-01-01"
USERDB_DIR="/var/lib/systemd/userdb"

# 1. Scrub birthDate from userdb files
if [ -d "$USERDB_DIR" ]; then
    for user_file in "$USERDB_DIR"/*.user; do
        if [ ! -f "$user_file" ]; then continue; fi

        # Use Python for safe JSON handling
        python3 -c "
import json
import sys
import os

user_file = '$user_file'
safe_date = '$SAFE_DATE'

try:
    with open(user_file, 'r') as f:
        data = json.load(f)
    
    # Check if birthDate exists and is not already nullified
    if 'birthDate' in data and data['birthDate'] != safe_date:
        data['birthDate'] = safe_date
        
        # Write to a temporary file, then atomic rename
        temp_file = user_file + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Preserve original permissions and ownership
        stat_info = os.stat(user_file)
        os.chown(temp_file, stat_info.st_uid, stat_info.st_gid)
        os.chmod(temp_file, stat_info.st_mode)
        os.rename(temp_file, user_file)
        
        sys.exit(0) # Modified
    sys.exit(1) # Not modified
except Exception as e:
    sys.exit(2) # Error
"
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            logger -t mommy-security "Scrubbed birthDate in $user_file"
        fi
    done
fi

# 2. Mask enforcement sockets to prevent systemd from answering queries
# If the sockets are active, stop them first (only on systemd distros)
if command -v systemctl >/dev/null 2>&1; then
    systemctl stop systemd-userdbd.socket systemd-homed.socket >/dev/null 2>&1 || true
    systemctl mask --now systemd-userdbd.socket systemd-homed.socket >/dev/null 2>&1 || true
fi

# 3. Lock homectl defaults if possible (prevent future additions of birthDate)
# (Best effort)
if command -v homectl >/dev/null 2>&1; then
    # We masked homed, so homectl may just fail anyway, which is desired.
    true
fi
