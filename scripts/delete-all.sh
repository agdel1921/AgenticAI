#!/usr/bin/env bash
# delete-all.sh — removes all AG_hr_onboarding_agent resources in reverse import order
# Usage: chmod +x scripts/delete-all.sh && ./scripts/delete-all.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment
source venv/bin/activate

echo "========================================="
echo " Acme HR Onboarding Agent — Delete"
echo "========================================="

# 1. Agent first (reverse order)
echo ""
echo "[1/3] Removing agent: AG_hr_onboarding_agent ..."
orchestrate agents remove -n AG_hr_onboarding_agent --kind native || true

# 2. Tools
echo ""
echo "[2/3] Removing tools ..."
orchestrate tools remove -n AG_SIM_get_required_paperwork || true
orchestrate tools remove -n AG_SIM_get_hr_contacts || true
orchestrate tools remove -n AG_SIM_generate_onboarding_checklist || true

# 3. Knowledge base
echo ""
echo "[3/3] Removing knowledge base: AG_SIM_hr_knowledge_base ..."
orchestrate knowledge-bases remove -n AG_SIM_hr_knowledge_base || true

echo ""
echo "========================================="
echo " Cleanup complete."
echo "========================================="
