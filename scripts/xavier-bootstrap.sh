#!/usr/bin/env bash
# ============================================================
# NixOS Bootstrap — Xavier Memory System
# ============================================================
# SAFE VERSION: No hardcoded credentials. Uses .env file.
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$HOME/.xavier/env"

echo "📍 Xavier Memory Bootstrap — NixOS"
echo ""

# ── Step 1: Load or create .env ──
if [ -f "$ENV_FILE" ]; then
  echo "📄 Loading $ENV_FILE"
  source "$ENV_FILE"
else
  echo "📄 No .env found at $ENV_FILE"
  echo ""
  echo "   Copy the template:"
  echo "     mkdir -p ~/.xavier"
  echo "     cp .env.xavier.example ~/.xavier/env"
  echo "   Then edit with your real credentials and re-run."
  exit 1
fi

# ── Step 2: Dependencies ──
echo "🔍 Checking dependencies..."
for cmd in curl psql git; do
  if command -v $cmd &>/dev/null; then
    echo "  ✅ $cmd found"
  else
    echo "  ⚠️  $cmd not found — install via: nix-shell -p $cmd"
  fi
done
echo ""

# ── Step 3: Test connections ──
echo "🔌 Testing connections..."

if [ "$SUPABASE_SERVICE_KEY" = "***your-service-key-here***" ]; then
  echo "  ⚠️  Skipping Supabase check — placeholder key detected"
  echo "     Edit $ENV_FILE with your real key"
else
  SB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "apikey: $SUPABASE_SERVICE_KEY" \
    -H "Authorization: ***$SUPABASE_SERVICE_KEY" \
    "$SUPABASE_URL/rest/v1/$SUPABASE_TABLE?select=id&limit=1" 2>/dev/null || echo "FAIL")
  echo "  ✅ Supabase REST: $SB_STATUS"
fi

if command -v psql &>/dev/null; then
  NEON_CHECK=$(psql "$NEON_URL" -c "SELECT COUNT(*) FROM $NEON_TABLE" -t 2>/dev/null || echo "FAIL")
  if [ "$NEON_CHECK" != "FAIL" ]; then
    echo "  ✅ Neon: $NEON_CHECK records in $NEON_TABLE"
  else
    echo "  ❌ Neon: connection failed — check NEON_URL"
  fi
else
  echo "  ⚠️  psql not available — skip Neon check"
fi

echo ""
echo "=== XAVIER BOOTSTRAP COMPLETE ==="
echo "Config: $ENV_FILE"
echo "Skills: github.com/iberi22/swal-skills"
echo ""
echo "🐧 Now run agents will auto-connect via Xavier agent onboarding skill."
