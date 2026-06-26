#!/usr/bin/env bash
# ============================================================
# NixOS Bootstrap — Xavier Memory System
# ============================================================
# Run this once after installing NixOS to connect to Xavier's
# memory store (Neon + Supabase).
#
# Usage: bash nixos-bootstrap.sh
# ============================================================

set -euo pipefail

echo "📍 Xavier Memory Bootstrap — NixOS"
echo ""

# ── Step 1: Dependencies ──
echo "🔍 Checking dependencies..."
for cmd in curl psql git gh; do
  if command -v $cmd &>/dev/null; then
    echo "  ✅ $cmd found"
  else
    echo "  ⚠️  $cmd not found — installing via nix-shell"
    nix-shell -p $cmd --run "echo '  ✅ $cmd installed temporarily'"
    echo "  💡 Add $cmd to environment.systemPackages in configuration.nix"
  fi
done

echo ""

# ── Step 2: Connection Strings ──
# These will be loaded from .env or prompted
ENV_FILE="$HOME/.xavier/env"
if [ -f "$ENV_FILE" ]; then
  echo "📄 Loading $ENV_FILE"
  source "$ENV_FILE"
else
  echo "📄 No $ENV_FILE found — creating from template"
  mkdir -p "$HOME/.xavier"
  cat > "$ENV_FILE" << 'ENVEOF'
# Xavier Memory — NixOS
SUPABASE_URL=https://auuhejigwpwdkqsoaoht.supabase.co
SUPABASE_SERVICE_KEY=eyJhbG…yAxc
SUPABASE_TABLE=memories

NEON_URL=postgresql://neondb_owner:npg_Sbx0M4izGORs@ep-morning-block-angd7x5n-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
NEON_TABLE=memories_supabase_mirror
ENVEOF
  echo "  ✅ Template created at $ENV_FILE"
  echo "  ⚠️  EDIT the file and insert your actual API keys"
  echo "     Then re-run this script"
  exit 1
fi

echo ""

# ── Step 3: Connectivity Test ──
echo "🔌 Testing connections..."

# Supabase REST
SB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: ***$SUPABASE_SERVICE_KEY" \
  "$SUPABASE_URL/rest/v1/$SUPABASE_TABLE?select=id&limit=1" 2>/dev/null || echo "FAIL")

if [ "$SB_STATUS" = "200" ]; then
  echo "  ✅ Supabase REST: $SB_STATUS"
else
  echo "  ❌ Supabase REST: $SB_STATUS — check SUPABASE_SERVICE_KEY in $ENV_FILE"
fi

# Neon PostgreSQL
if command -v psql &>/dev/null; then
  NEON_CHECK=$(psql "$NEON_URL" -c "SELECT COUNT(*) FROM $NEON_TABLE" -t 2>/dev/null || echo "FAIL")
  if [ "$NEON_CHECK" != "FAIL" ]; then
    echo "  ✅ Neon PostgreSQL: $NEON_CHECK records in $NEON_TABLE"
  else
    echo "  ❌ Neon PostgreSQL: connection failed — check NEON_URL in $ENV_FILE"
  fi
else
  echo "  ⚠️  psql not available — skip Neon check"
fi

echo ""

# ── Step 4: Pull Latest Skills ──
echo "📦 Pulling Xavier skills..."
if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
  SKILL_DIR="$HOME/.xavier/skills"
  mkdir -p "$SKILL_DIR"
  
  # Download xavier-agent-onboarding skill
  curl -sL "https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/xavier-agent-onboarding/SKILL.md" \
    -o "$SKILL_DIR/xavier-agent-onboarding.md"
  curl -sL "https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/xavier-agent-onboarding/DISCOVERY.md" \
    -o "$SKILL_DIR/xavier-agent-onboarding-discovery.md"
  
  echo "  ✅ Skills downloaded to $SKILL_DIR"
else
  echo "  ⚠️  gh not authenticated — skills location:"
  echo "     https://github.com/iberi22/swal-skills/tree/main/skills/xavier-agent-onboarding"
fi

echo ""

# ── Step 5: Summary ──
echo "=== XAVIER BOOTSTRAP COMPLETE ==="
echo ""
echo "✅ Connected to:"
echo "   Supabase: $SUPABASE_URL"
echo "   Neon:     $NEON_TABLE"
echo ""
echo "📂 Key locations:"
echo "   Config:   $ENV_FILE"
echo "   Skills:   $HOME/.xavier/skills/"
echo ""
echo "📋 Next steps:"
echo "   1. Install psql: nix-shell -p postgresql"
echo "   2. Install gh:   nix-shell -p gh"
echo "   3. Configure Xavier to use these credentials"
echo "   4. The xavier-agent-onboarding skill handles the rest"
echo ""
echo "🐧 Welcome to NixOS. Xavier remembers."
