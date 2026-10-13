#!/bin/bash
# Linux/tmux launcher for the multi-bot stack (same shape as scalper's restart-all-ubuntu.sh).
# One tmux session "freqtrade": commander dashboard pane + one pane per bot whose config exists.
#   ./restart-all-ubuntu.sh        (re)start everything
#   ./restart-all-ubuntu.sh stop   stop everything
# Bots are forced into --dry-run (the config templates ship dry_run:false); FT_LIVE=1 trades for real.
# A bot whose port is already taken is skipped, never killed.

cd "$(dirname "$0")" || exit 1
SESSION=freqtrade
COMMANDER_PORT=${COMMANDER_PORT:-7100}

# name port strategy -> user_data/config_<name>_<port>.json (same table as start_all_bots.sh)
BOTS=(
  "bollinger 7101 BollingerBands_Strategy"
  "rsi_macd 7102 RSI_MACD_Strategy"
  "scalper 7103 Manual_Control_Strategy"
  "nfi 7104 NostalgiaForInfinityX7"
  "e0v1e 7105 E0V1E_v17"
  "dip_catcher 7106 DipDetectionStrategy"
  "mh 7107 MichaelHarrisStrategy"
  "fear 7108 BollingerBounceFearTrader"
)

port_busy() { ss -ltnH "sport = :$1" | grep -q .; }

stop() {
  tmux has-session -t "$SESSION" 2>/dev/null || return 0
  # Ctrl-C first so freqtrade shuts down cleanly (closes trades DB) before the panes go away
  for p in $(tmux list-panes -s -t "$SESSION" -F '#{pane_id}'); do tmux send-keys -t "$p" C-c; done
  sleep 3
  tmux kill-session -t "$SESSION"
}

stop
[ "$1" = stop ] && { echo "Stopped"; exit 0; }

DRY="--dry-run"
[ "$FT_LIVE" = 1 ] && DRY="" && echo "⚠️  FT_LIVE=1: bots trade with REAL money"

tmux new-session -d -s "$SESSION" -n stack -c "$PWD"
tmux set -t "$SESSION" pane-border-status top
tmux send-keys -t "$SESSION" "PORT=$COMMANDER_PORT ./start_commander.sh" C-m
tmux select-pane -t "$SESSION" -T "Commander :$COMMANDER_PORT"

started=0
for b in "${BOTS[@]}"; do
  read -r name port strategy <<<"$b"
  cfg="user_data/config_${name}_${port}.json"
  if [ ! -f "$cfg" ]; then echo "skip $name: no $cfg"; continue; fi
  if port_busy "$port"; then echo "skip $name: port $port already in use"; continue; fi
  pane=$(tmux split-window -t "$SESSION" -c "$PWD" -P -F '#{pane_id}')
  # dry-run gets its own DB so simulated trades never land in a config's live-trade DB
  db=${DRY:+--db-url sqlite:///tradesv3.$name.dryrun.sqlite}
  tmux send-keys -t "$pane" ".venv/bin/freqtrade trade -c $cfg --strategy $strategy $DRY $db" C-m
  tmux select-pane -t "$pane" -T "$name :$port"
  tmux select-layout -t "$SESSION" tiled >/dev/null
  started=$((started + 1))
done

host=${WT_PUBLIC_HOST:-$(hostname)}
echo "Started commander + $started bot(s) ${DRY:+(dry-run)} in tmux session '$SESSION'"
echo "Dashboard: http://$host:$COMMANDER_PORT   attach: tmux attach -t $SESSION"
