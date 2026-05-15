#!/bin/bash
# ============================================================================
# Oracule Zero — Config Setup
# ============================================================================
# Copies config-templates/ into ~/.oracule/ on first run.
# Skips any file that already exists (never overwrites existing config).
# ============================================================================

set -e

ORACULE_DIR="$HOME/.oracule"
TEMPLATES_DIR="$(cd "$(dirname "$0")" && pwd)/config-templates"

echo ""
echo "Oracule Zero — Config Setup"
echo ""

if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "Error: config-templates/ not found alongside this script."
    echo "Are you running from the repo root?"
    exit 1
fi

if [ ! -d "$ORACULE_DIR" ]; then
    echo "Creating ~/.oracule/ directory..."
fi

cp -rn "$TEMPLATES_DIR/." "$ORACULE_DIR/"

echo "Done. Config written to ~/.oracule/"
echo ""
echo "Next steps:"
echo "  1. Edit ~/.oracule/agents/jade/config.yaml to customize"
echo "  2. Set your Discord bot token in the discord: section"
echo "  3. Run 'jade' to start"
echo ""
