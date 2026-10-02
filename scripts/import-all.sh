#!/usr/bin/env bash
# import-all.sh — imports all AG_hr_onboarding_agent resources in dependency order
# Usage: chmod +x scripts/import-all.sh && ./scripts/import-all.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment
source venv/bin/activate

echo "========================================="
echo " Acme HR Onboarding Agent — Import"
echo "========================================="

# 1. Knowledge base (must exist before agent references it)
# NOTE: run from within the knowledge-bases/ dir so document paths resolve correctly
echo ""
echo "[1/3] Importing knowledge base: AG_SIM_hr_knowledge_base ..."
(cd knowledge-bases && orchestrate knowledge-bases import -f AG_SIM_hr_knowledge_base.yaml)

# 2. Tools
echo ""
echo "[2/3] Importing tools: AG_SIM_onboarding_tools ..."
orchestrate tools import -k python -f tools/AG_SIM_onboarding_tools.py

# 3. Agent
echo ""
echo "[3/3] Importing agent: AG_hr_onboarding_agent ..."
orchestrate agents import -f agents/AG_hr_onboarding_agent.yaml

echo ""
echo "========================================="
echo " Import complete!"
echo " Note: Knowledge base indexing may take"
echo " a few minutes. Check status with:"
echo "   orchestrate knowledge-bases status -n AG_SIM_hr_knowledge_base"
echo "========================================="
