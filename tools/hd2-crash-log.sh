#!/usr/bin/env bash
# hd2-crash-log.sh — crash logger for Helldivers 2.
#
# Usage:
#   tools/hd2-crash-log.sh [launcher args...]
#
# Runs a Helldivers 2 launcher (default: the proton run from
# helldivers2-complete-launch.sh) and, whenever it exits non-zero or a fresh
# minidump appears in the Proton crash/data folders, appends a timestamped
# entry to logs/hd2-crash.log and copies the new .dmp files into
# logs/dumps/<timestamp>/. Idle runs produce no log churn.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${HD2_PREFIX:-$HOME/.local/share/Steam/steamapps/compatdata/553850/pfx}"
CRASH="$PREFIX/drive_c/users/steamuser/AppData/Roaming/Arrowhead/Helldivers2"
DUMPS="$CRASH/dumps"
REPORTS="$CRASH/crash_data/reports"
LOGDIR="$HERE/logs"
LOG="$LOGDIR/hd2-crash.log"
BACKUP="$LOGDIR/dumps"

mkdir -p "$LOGDIR" "$BACKUP"

log_event() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" >> "$LOG"; }

# List the .dmp files present right now (sorted, one path per line).
dump_list() { find "$DUMPS" "$REPORTS" -type f -name '*.dmp' -printf '%p\n' 2>/dev/null | sort; }

# Run the game launcher (passed as $1...), then log the exit status and fold any
# newly-created crash dumps into $BACKUP. Output is left visible so the user
# sees the launch, while our entries go to $LOG.
run_launcher() {
    local before_list rc new
    before_list="$(dump_list)"
    "$@"  # (no redirection here, so the user sees the launch)
    rc=$?
    new="$(dump_list | comm -13 - <(echo "$before_list"))"
    if [ "$rc" -ne 0 ] || [ -n "$new" ]; then
        log_event "RUN exit=$rc args=$*"
        if [ -n "$new" ]; then
            log_event "NEW_CRASH_DUMPS:"
            printf '  %s\n' "$new" | sed 's/^/    /' >> "$LOG"
        fi
        if [ -n "$new" ]; then
            mkdir -p "$BACKUP/$(date -u '+%Y%m%dT%H%M%SZ')"
            while IFS= read -r f; do
                [ -n "$f" ] || continue
                cp -p "$f" "$BACKUP/$(date -u '+%Y%m%dT%H%M%SZ')/$(basename "$f")"
                log_event "  saved $f -> $BACKUP/$(date -u '+%Y%m%dT%H%M%SZ')/$(basename "$f")"
            done <<< "$new"
        fi
    else
        log_event "RUN ok exit=$rc args=$*"
    fi
    return $rc
}

if [ "$#" -eq 0 ]; then
    # Default launcher: Proton Experimental, matching helldivers2-complete-launch.sh
    export PROTON_NO_ESYNC=1 PROTON_NO_FSYNC=1 DXVK_ASYNC=1 WINEDEBUG=-all
    run_launcher proton run "$HOME/.local/share/Steam/steamapps/common/Helldivers 2/bin/helldivers2.exe"
else
    run_launcher "$@"
fi
