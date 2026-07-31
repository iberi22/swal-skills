#!/usr/bin/env node
/**
 * SWAL Skill Provider
 * 
 * Dynamic skill loader for all coding agents.
 * Fetches skills from raw GitHub URLs or local cache.
 * 
 * Usage:
 *   node skill-provider.js list              - List all available skills
 *   node skill-provider.js get <skill-id>    - Get skill content
 *   node skill-provider.js install <skill-id> - Install skill locally
 *   node skill-provider.js search <query>    - Search skills by tag/name
 *   node skill-provider.js recipes            - List all POML recipes
 *   node skill-provider.js recipe <recipe-id> - Get recipe content
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const REGISTRY_PATH = path.join(__dirname, 'manifest.yaml');
const CACHE_DIR = path.join(__dirname, '.skill-cache');
const REGISTRY_RAW_URL = 'https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/_registry/manifest.yaml';
const OPENCLAW_SKILLS_DIR = 'C:\\Users\\belal\\clawd\\skills';
const CODEX_SKILLS_DIR = 'C:\\Users\\belal\\.codex\\skills';
const AGENTS_SKILLS_DIR = 'C:\\Users\\belal\\clawd\\agents';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(color, ...args) {
  console.log(`${color}${args.join(' ')}${colors.reset}`);
}

function logInfo(...args) { log(colors.blue, '[INFO]', ...args); }
function logSuccess(...args) { log(colors.green, '[OK]', ...args); }
function logWarn(...args) { log(colors.yellow, '[WARN]', ...args); }
function logError(...args) { log(colors.red, '[ERROR]', ...args); }

// Fetch URL content
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    protocol.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        fetchUrl(res.headers.location).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Parse YAML properly - extract skills manually
function parseYaml(content) {
  const lines = content.split('\n');
  const result = { skills: [], recipes: [] };
  let currentSkill = null;
  let inSkills = false;
  let inRecipes = false;
  let currentKey = '';
  
  for (let line of lines) {
    // Track sections
    if (line.trim() === 'skills:') { inSkills = true; inRecipes = false; continue; }
    if (line.trim() === 'recipes:') { inRecipes = true; inSkills = false; continue; }
    
    if (!inSkills && !inRecipes) continue;
    if (line.trim().startsWith('#')) continue;
    
    // New skill entry
    const skillMatch = line.match(/^\s+-\s+id:\s*"?([^"]+)"?\s*$/);
    if (skillMatch) {
      if (currentSkill) {
        if (inSkills) result.skills.push(currentSkill);
        if (inRecipes) result.recipes.push(currentSkill);
      }
      currentSkill = { id: skillMatch[1] };
      continue;
    }
    
    if (!currentSkill) continue;
    
    // Skill properties
    const propMatch = line.match(/^\s+(\w+):\s*(.*)$/);
    if (propMatch) {
      const key = propMatch[1];
      let value = propMatch[2].trim().replace(/^["']|["']$/g, '');
      // Handle array-like values (comma-separated)
      if (value.includes(',')) {
        value = value.split(',').map(v => v.trim());
      }
      currentSkill[key] = value;
    }
  }
  
  // Add last skill
  if (currentSkill) {
    if (inSkills) result.skills.push(currentSkill);
    if (inRecipes) result.recipes.push(currentSkill);
  }
  
  return result;
}

// Load manifest
async function loadManifest() {
  let content;
  
  // Try local first
  if (fs.existsSync(REGISTRY_PATH)) {
    logInfo('Loading manifest from local cache');
    content = fs.readFileSync(REGISTRY_PATH, 'utf8');
  } else {
    // Fetch from GitHub
    logInfo('Fetching manifest from GitHub');
    try {
      content = await fetchUrl(REGISTRY_RAW_URL);
      // Cache it
      fs.mkdirSync(path.dirname(REGISTRY_PATH), { recursive: true });
      fs.writeFileSync(REGISTRY_PATH, content);
    } catch (e) {
      logError('Failed to fetch manifest:', e.message);
      process.exit(1);
    }
  }
  
  return parseYaml(content);
}

// List all skills
function listSkills(manifest, filter = null) {
  const skills = manifest.skills || [];
  
  console.log(`\n${colors.bright}${colors.cyan}Available Skills (${skills.length}):${colors.reset}\n`);
  
  for (const skill of skills) {
    if (filter && !skill.id.includes(filter) && !skill.name.toLowerCase().includes(filter.toLowerCase())) {
      continue;
    }
    
    const visibility = skill.visibility === 'public' ? `${colors.green}[PUBLIC]${colors.reset}` : `${colors.yellow}[PRIVATE]${colors.reset}`;
    const agents = skill.agents ? (Array.isArray(skill.agents) ? skill.agents.join(', ') : skill.agents) : 'all';
    const tags = skill.tags ? (Array.isArray(skill.tags) ? skill.tags.join(', ') : skill.tags) : '';
    
    console.log(`${colors.bright}${skill.id}${colors.reset} ${visibility}`);
    console.log(`  Name: ${skill.name}`);
    console.log(`  Category: ${skill.category}`);
    console.log(`  Agents: ${agents}`);
    if (tags) console.log(`  Tags: ${tags}`);
    if (skill.dependencies && skill.dependencies.length > 0) {
      const deps = Array.isArray(skill.dependencies) ? skill.dependencies.join(', ') : skill.dependencies;
      console.log(`  Dependencies: ${deps}`);
    }
    console.log('');
  }
}

// List recipes
function listRecipes(manifest) {
  const recipes = manifest.recipes || [];
  
  console.log(`\n${colors.bright}${colors.cyan}POML Recipes (${recipes.length}):${colors.reset}\n`);
  
  for (const recipe of recipes) {
    const topology = recipe.topology || 'solo';
    console.log(`${colors.bright}${recipe.id}${colors.reset} - ${recipe.name} (${recipe.department})`);
    console.log(`  Path: ${recipe.path}`);
    console.log(`  Topology: ${topology}`);
    if (recipe.trigger) {
      console.log(`  Trigger: ${recipe.trigger}`);
    }
    console.log('');
  }
}

// Get skill content
async function getSkill(skillId, manifest) {
  const skills = manifest.skills || [];
  const skill = skills.find(s => s.id === skillId);
  
  if (!skill) {
    logError(`Skill not found: ${skillId}`);
    return;
  }
  
  if (skill.visibility === 'private' && !skill.raw_url) {
    logError(`Skill ${skillId} is private. Install from local source.`);
    return;
  }
  
  if (!skill.raw_url) {
    logError(`No raw_url for skill ${skillId}`);
    return;
  }
  
  logInfo(`Fetching ${skillId} from GitHub...`);
  try {
    const content = await fetchUrl(skill.raw_url);
    console.log(content);
  } catch (e) {
    logError(`Failed to fetch skill:`, e.message);
  }
}

// Get recipe content
async function getRecipe(recipeId, manifest) {
  const recipes = manifest.recipes || [];
  const recipe = recipes.find(r => r.id === recipeId);
  
  if (!recipe) {
    logError(`Recipe not found: ${recipeId}`);
    return;
  }
  
  const rawUrl = recipe.raw_url || `https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/${recipe.path}`;
  
  logInfo(`Fetching ${recipeId} from GitHub...`);
  try {
    const content = await fetchUrl(rawUrl);
    console.log(content);
  } catch (e) {
    logError(`Failed to fetch recipe:`, e.message);
  }
}

// Install skill locally
async function installSkill(skillId, manifest, target = 'openclaw') {
  const skills = manifest.skills || [];
  const skill = skills.find(s => s.id === skillId);
  
  if (!skill) {
    logError(`Skill not found: ${skillId}`);
    return;
  }
  
  if (skill.visibility === 'private' && !skill.raw_url) {
    // Private skill - copy from local
    const localPath = path.join(REGISTRY_PATH, '..', skill.path);
    if (!fs.existsSync(localPath)) {
      logError(`Local skill not found: ${localPath}`);
      return;
    }
    
    let targetDir;
    if (target === 'openclaw') {
      targetDir = path.join(OPENCLAW_SKILLS_DIR, skill.id);
    } else if (target === 'codex') {
      targetDir = path.join(CODEX_SKILLS_DIR, skill.id);
    } else {
      targetDir = path.join(AGENTS_SKILLS_DIR, target, 'skills', skill.id);
    }
    
    fs.mkdirSync(targetDir, { recursive: true });
    const files = fs.readdirSync(path.dirname(localPath));
    const skillDir = path.dirname(localPath);
    
    for (const file of files) {
      if (file === path.basename(localPath)) continue;
      try {
        fs.copyFileSync(path.join(skillDir, file), path.join(targetDir, file));
      } catch (e) {}
    }
    
    logSuccess(`Installed ${skillId} to ${targetDir}`);
    return;
  }
  
  if (!skill.raw_url) {
    logError(`No raw_url for skill ${skillId}`);
    return;
  }
  
  // Fetch and cache
  logInfo(`Fetching ${skillId}...`);
  try {
    const content = await fetchUrl(skill.raw_url);
    
    let targetDir;
    if (target === 'openclaw') {
      targetDir = path.join(OPENCLAW_SKILLS_DIR, skill.id);
    } else if (target === 'codex') {
      targetDir = path.join(CODEX_SKILLS_DIR, skill.id);
    } else {
      targetDir = path.join(AGENTS_SKILLS_DIR, target, 'skills', skill.id);
    }
    
    fs.mkdirSync(targetDir, { recursive: true });
    fs.writeFileSync(path.join(targetDir, 'SKILL.md'), content);
    
    logSuccess(`Installed ${skillId} to ${targetDir}`);
  } catch (e) {
    logError(`Failed to install skill:`, e.message);
  }
}

// Search skills
function searchSkills(query, manifest) {
  const skills = manifest.skills || [];
  const results = skills.filter(s => 
    s.id.includes(query) ||
    s.name.toLowerCase().includes(query.toLowerCase()) ||
    (s.tags && s.tags.some(t => t.includes(query))) ||
    (s.description && s.description.toLowerCase().includes(query.toLowerCase()))
  );
  
  if (results.length === 0) {
    logWarn(`No skills found matching: ${query}`);
    return;
  }
  
  console.log(`\n${colors.bright}Search results for "${query}" (${results.length}):${colors.reset}\n`);
  listSkills({ skills: results });
}

// Sync all public skills to OpenClaw
async function syncAll(manifest, target = 'openclaw') {
  const skills = manifest.skills || [];
  const publicSkills = skills.filter(s => s.visibility === 'public' && s.raw_url);
  
  logInfo(`Syncing ${publicSkills.length} public skills to ${target}...`);
  
  let installed = 0;
  for (const skill of publicSkills) {
    try {
      await installSkill(skill.id, manifest, target);
      installed++;
    } catch (e) {
      logWarn(`Failed to install ${skill.id}:`, e.message);
    }
  }
  
  logSuccess(`Synced ${installed}/${publicSkills.length} skills`);
}

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
${colors.bright}SWAL Skill Provider${colors.reset}
${colors.cyan}A dynamic skill loader for all coding agents${colors.reset}

Usage:
  ${colors.green}list${colors.reset}                   List all available skills
  ${colors.green}list --public${colors.reset}          List only public skills
  ${colors.green}list --private${colors.reset}         List only private skills
  ${colors.green}recipes${colors.reset}                List all POML recipes
  ${colors.green}get <skill-id>${colors.reset}          Get skill content
  ${colors.green}recipe <recipe-id>${colors.reset}      Get recipe content
  ${colors.green}install <skill-id>${colors.reset}     Install skill to OpenClaw
  ${colors.green}install <skill-id> --codex${colors.reset}  Install to Codex
  ${colors.green}install <skill-id> --agent <name>${colors.reset}  Install to specific agent
  ${colors.green}sync${colors.reset}                    Sync all public skills
  ${colors.green}search <query>${colors.reset}          Search skills
  ${colors.green}help${colors.reset}                     Show this help

Examples:
  node skill-provider.js list
  node skill-provider.js get nextjs
  node skill-provider.js install astro --codex
  node skill-provider.js search tailwind
  node skill-provider.js sync
`);
    return;
  }
  
  const manifest = await loadManifest();
  
  switch (command) {
    case 'list':
      const filter = args[1];
      if (filter === '--public') {
        listSkills({ skills: manifest.skills.filter(s => s.visibility === 'public') });
      } else if (filter === '--private') {
        listSkills({ skills: manifest.skills.filter(s => s.visibility === 'private') });
      } else {
        listSkills(manifest, filter);
      }
      break;
      
    case 'recipes':
      listRecipes(manifest);
      break;
      
    case 'get':
      if (!args[1]) {
        logError('Usage: get <skill-id>');
      } else {
        await getSkill(args[1], manifest);
      }
      break;
      
    case 'recipe':
      if (!args[1]) {
        logError('Usage: recipe <recipe-id>');
      } else {
        await getRecipe(args[1], manifest);
      }
      break;
      
    case 'install':
      if (!args[1]) {
        logError('Usage: install <skill-id> [--codex|--agent <name>]');
      } else {
        let target = 'openclaw';
        if (args.includes('--codex')) target = 'codex';
        const agentIndex = args.indexOf('--agent');
        if (agentIndex !== -1 && args[agentIndex + 1]) target = args[agentIndex + 1];
        
        await installSkill(args[1], manifest, target);
      }
      break;
      
    case 'sync':
      let syncTarget = 'openclaw';
      if (args[1] === '--codex') syncTarget = 'codex';
      if (args[1] === '--all') {
        await syncAll(manifest, 'openclaw');
        await syncAll(manifest, 'codex');
      } else {
        await syncAll(manifest, syncTarget);
      }
      break;
      
    case 'search':
      if (!args[1]) {
        logError('Usage: search <query>');
      } else {
        searchSkills(args[1], manifest);
      }
      break;
      
    default:
      logError(`Unknown command: ${command}`);
      console.log('Run without arguments to see help.');
  }
}

main().catch(console.error);
