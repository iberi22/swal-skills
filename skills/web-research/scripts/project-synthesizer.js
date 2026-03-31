/**
 * project-synthesizer.js
 * Synthesizes project data with web research for AI-driven insights
 * 
 * Usage: node project-synthesizer.js [project-name] [depth]
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const PROJECTS_DIR = 'E:\\scripts-python';
const OUTPUT_DIR = 'E:\\scripts-python\\synthesized';

// API Resource Manager
const resourceManager = require('E:\\scripts-python\\scripts\\api-resource-manager.js');

// Fallback providers (CLI-based)
const FALLBACK_PROVIDERS = {
  qwen: 'fallback_qwen_coder',
  claude: 'fallback_claude_code',
  gemini: 'fallback_gemini'
};

// Brave Search (regular web search)
function braveSearch(query, count = 10) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.search.brave.com',
      path: '/res/v1/web/search?q=' + encodeURIComponent(query) + '&count=' + count,
      method: 'GET',
      headers: { 'X-Subscription-Token': 'BSAEvfUNvFDtYsQuWztN_RPHmzitwkQ' }
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resourceManager.logRequest('brave');
          const json = JSON.parse(data);
          resolve(json.web?.results || []);
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// Tavily Search with AI answer
function tavilySearch(query, options = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      api_key: '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',
      query: query,
      max_results: options.max_results || 10,
      include_answer: options.include_answer !== false,
      search_depth: options.search_depth || 'basic'
    });

    const reqOptions = {
      hostname: 'api.tavily.com',
      path: '/search',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    };

    const req = https.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resourceManager.logRequest('tavily');
          resolve(JSON.parse(data));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Brave AI Search - uses Tavily for AI summaries instead of Brave's (Brave AI summarizer not available)
function braveAISearch(query, count = 10) {
  // Since Brave's AI Summarizer requires Pro AI plan (not available on current keys),
  // we use Tavily for AI-powered search instead
  return tavilySearch(query, {
    max_results: count,
    include_answer: true,
    search_depth: 'advanced'
  }).then(result => ({
    results: result.results || [],
    summary: result.answer,
    aiAnalysis: result.answer
  }));
}

// Tavily Search with AI answer
function tavilySearch(query, options = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      api_key: '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',
      query: query,
      max_results: options.max_results || 10,
      include_answer: options.include_answer !== false,
      search_depth: options.search_depth || 'advanced'
    });
    const reqOptions = {
      hostname: 'api.tavily.com',
      path: '/search',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    };
    const req = https.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } 
        catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Get project info from local repo
function getLocalProjectData(projectName) {
  const projectPath = path.join(PROJECTS_DIR, projectName);
  if (!fs.existsSync(projectPath)) return null;
  
  const data = {
    name: projectName,
    path: projectPath,
    files: [],
    readme: null,
    architecture: null,
    issues: [],
    lastCommit: null
  };
  
  // Read README
  const readmePath = path.join(projectPath, 'README.md');
  if (fs.existsSync(readmePath)) {
    data.readme = fs.readFileSync(readmePath, 'utf8').substring(0, 2000);
  }
  
  // Read architecture if exists
  const archPath = path.join(projectPath, '.gitcore', 'ARCHITECTURE.md');
  if (fs.existsSync(archPath)) {
    data.architecture = fs.readFileSync(archPath, 'utf8').substring(0, 1500);
  }
  
  // List key files
  try {
    const items = fs.readdirSync(projectPath, { withFileTypes: true })
      .filter(d => !d.name.startsWith('.') && d.name !== 'node_modules')
      .slice(0, 20);
    data.files = items.map(i => ({ name: i.name, type: i.isDirectory() ? 'dir' : 'file' }));
  } catch (e) {}
  
  return data;
}

// Main synthesis
async function synthesizeProject(projectName, depth = 2) {
  console.log('\n=== SYNTHESIZING PROJECT: ' + projectName + ' ===\n');
  
  // Check budget before proceeding (using new resource manager)
  const { logRequest: oldLogRequest, checkBudget } = require('E:\\scripts-python\\scripts\\api-usage-tracker.js');
  // Note: We'll use resourceManager.logRequest() in the search functions
  
  // 1. Get local project data
  console.log('[1] Fetching local project data...');
  const localData = getLocalProjectData(projectName);
  if (!localData) {
    console.log('Project not found locally:', projectName);
    return null;
  }
  
  // 2. Web research on the project domain (4 parallel searches)
  console.log('[2] Researching domain with Brave AI...');
  
  // Check if we should use fallback
  const status = resourceManager.getStatus();
  const tavilyStatus = status.providers?.tavily;
  const tavilyExhausted = tavilyStatus?.needsFallback || (tavilyStatus?.monthly?.percent >= 80);
  
  if (tavilyExhausted) {
    console.log('[⚠️] Tavily at ' + tavilyStatus?.monthly?.percent + '%, checking fallbacks...');
    const fallback = resourceManager.getFallbackProvider();
    if (fallback) {
      console.log('[→] Will use fallback:', fallback);
    }
  }
  
  const bravePromise = braveAISearch(projectName + ' AI technology 2026', depth === 3 ? 15 : 8);
  
  console.log('[3] Business model research...');
  const businessPromise = tavilySearch(projectName + ' business model monetization SaaS pricing 2026', {
    max_results: depth === 3 ? 15 : 8,
    include_answer: true,
    search_depth: 'advanced'
  });
  
  console.log('[4] Competitor analysis...');
  const competitorPromise = braveSearch(projectName + ' competitors alternatives 2026', depth === 3 ? 10 : 5);
  
  console.log('[5] Feature trends research...');
  const featuresPromise = tavilySearch(projectName + ' new features roadmap AI trends', {
    max_results: depth === 3 ? 10 : 5,
    include_answer: true,
    search_depth: 'basic'
  });
  
  const [braveResults, businessResults, competitorResults, featuresResults] = await Promise.all([
    bravePromise, businessPromise, competitorPromise, featuresPromise
  ]);
  
  // Extract Brave AI results (returns { results, summary, aiAnalysis })
  const braveSearchResults = braveResults.results || [];
  const braveAiSummary = braveResults.summary || braveResults.aiAnalysis || null;
  
  // 3. Compile comprehensive synthesis
  const synthesis = {
    project: projectName,
    timestamp: new Date().toISOString(),
    local: {
      hasReadme: !!localData.readme,
      hasArchitecture: !!localData.architecture,
      keyFiles: localData.files.slice(0, 10),
      description: localData.readme?.substring(0, 500)
    },
    research: {
      // Technical AI analysis
      technicalAI: {
        analysis: businessResults.answer || braveAiSummary || braveSearchResults[0]?.description || 'No analysis available',
        sources: braveSearchResults.slice(0, 5).map(r => ({ title: r.title, url: r.url })),
        aiSummary: braveAiSummary
      },
      // Business model analysis
      business: {
        analysis: businessResults.answer || 'No business analysis available',
        monetization: extractMonetization(businessResults.answer),
        pricing: extractPricing(businessResults.answer),
        sources: (businessResults.results || []).slice(0, 3).map(r => ({ title: r.title, url: r.url }))
      },
      // Competitor analysis
      competitors: {
        analysis: competitorResults.length > 0 ? 'Competitors found: ' + competitorResults.slice(0, 3).map(r => r.title).join(', ') : 'No competitors identified',
        sources: competitorResults.slice(0, 5).map(r => ({ title: r.title, url: r.url }))
      },
      // Feature opportunities
      features: {
        analysis: featuresResults.answer || 'No feature analysis available',
        opportunities: extractFeatures(featuresResults.answer, braveSearchResults),
        roadmap: extractRoadmap(featuresResults.answer),
        sources: (featuresResults.results || []).slice(0, 3).map(r => ({ title: r.title, url: r.url }))
      },
      followUps: businessResults.follow_up_questions || []
    },
    insights: [],
    recommendations: []
  };
  
  // Generate insights
  if (businessResults.answer) {
    synthesis.insights.push({ type: 'Technical', text: businessResults.answer.substring(0, 250) });
  }
  if (synthesis.research.business.monetization) {
    synthesis.insights.push({ type: 'Business Model', text: 'Monetization: ' + synthesis.research.business.monetization });
  }
  if (synthesis.research.features.opportunities.length > 0) {
    synthesis.insights.push({ type: 'Features', text: synthesis.research.features.opportunities.slice(0, 2).join('; ') });
  }
  
  // Generate recommendations
  synthesis.recommendations = generateRecommendations(synthesis);
  
  return synthesis;
}

// Helper: Extract monetization model
function extractMonetization(text) {
  if (!text) return null;
  const models = ['SaaS', 'subscription', 'freemium', 'one-time', 'usage-based', 'license', 'marketplace', 'B2B', 'B2C'];
  return models.filter(m => text.toLowerCase().includes(m.toLowerCase())).join(', ');
}

// Helper: Extract pricing info
function extractPricing(text) {
  if (!text) return null;
  const match = text.match(/\$\d+[\d,]*[\/\-]|\d+[\/\-]|(?:price|pricing|cost)[\s:]+[\$]?\d+/gi);
  return match ? match.slice(0, 3).join(', ') : null;
}

// Helper: Extract feature opportunities
function extractFeatures(text, braveResults) {
  const features = [];
  if (!text && braveResults && braveResults.length > 0) {
    return braveResults.slice(0, 3).map(r => r.title);
  }
  const keywords = ['AI', 'automation', 'integration', 'dashboard', 'analytics', 'real-time', 'collaboration', 'API'];
  keywords.forEach(kw => {
    if (text?.toLowerCase().includes(kw.toLowerCase())) {
      features.push(kw);
    }
  });
  return features.slice(0, 5);
}

// Helper: Extract roadmap hints
function extractRoadmap(text) {
  if (!text) return [];
  const hints = [];
  const roadmapKeywords = ['upcoming', 'roadmap', '2026', '2027', 'planned', 'coming soon', 'next version', 'beta'];
  roadmapKeywords.forEach(kw => {
    if (text.toLowerCase().includes(kw)) {
      hints.push(kw);
    }
  });
  return [...new Set(hints)].slice(0, 5);
}

// Helper: Generate recommendations
function generateRecommendations(synthesis) {
  const recs = [];
  
  // Business recommendations
  if (synthesis.research.business.monetization) {
    recs.push({
      area: 'Business Model',
      recommendation: 'Consider ' + synthesis.research.business.monetization.split(',')[0] + ' model'
    });
  }
  
  // Feature recommendations
  if (synthesis.research.features.opportunities.length > 0) {
    recs.push({
      area: 'Features',
      recommendation: 'Priority: ' + synthesis.research.features.opportunities.slice(0, 2).join(', ')
    });
  }
  
  // Competitor recommendations
  if (synthesis.research.competitors.analysis.length > 50) {
    recs.push({
      area: 'Competitors',
      recommendation: 'Monitor: ' + synthesis.research.competitors.sources[0]?.title?.substring(0, 50)
    });
  }
  
  return recs;
}

// Save synthesis
function saveSynthesis(synthesis) {
  if (!synthesis) return;
  
  const outputPath = path.join(OUTPUT_DIR, synthesis.project + '.json');
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(synthesis, null, 2));
  console.log('\n[SAVED] ' + outputPath);
  
  // Also save to Cortex if available
  try {
    const http = require('http');
    const cortexData = {
      type: 'project_synthesis',
      project: synthesis.project,
      timestamp: synthesis.timestamp,
      summary: (synthesis.research?.technicalAI?.analysis || '').substring(0, 200),
      businessModel: synthesis.research?.business?.monetization,
      opportunities: synthesis.research?.features?.opportunities?.join(', '),
      fullData: synthesis
    };
    
    const dataStr = JSON.stringify(cortexData);
    const req = http.request({
      hostname: 'localhost',
      port: 8003,
      path: '/memory',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(dataStr)
      }
    }, (res) => {
      if (res.statusCode === 200 || res.statusCode === 201) {
        console.log('[✅] Saved to Cortex');
      }
    });
    req.on('error', () => {});
    req.write(dataStr);
    req.end();
  } catch (e) {
    // Cortex not critical
  }
}

// Format for display
function formatSynthesis(synthesis) {
  if (!synthesis) return 'No synthesis available';
  
  let output = '\n';
  output += '╔══════════════════════════════════════════════════════════════╗\n';
  output += '║  PROJECT SYNTHESIS: ' + synthesis.project.padEnd(41) + '║\n';
  output += '╚══════════════════════════════════════════════════════════════╝\n';
  
  output += '\n📁 LOCAL DATA:\n';
  output += '─'.repeat(55) + '\n';
  output += '  README: ' + (synthesis.local.hasReadme ? '✅' : '❌') + '\n';
  output += '  Architecture: ' + (synthesis.local.hasArchitecture ? '✅' + '║' : '❌') + '\n';
  output += '  Key files: ' + synthesis.local.keyFiles.length + '\n';
  
  output += '\n🔬 TECHNICAL AI:\n';
  output += '─'.repeat(55) + '\n';
  output += '  ' + (synthesis.research.technicalAI?.analysis || 'N/A').substring(0, 200) + '...\n';
  
  output += '\n💰 BUSINESS MODEL:\n';
  output += '─'.repeat(55) + '\n';
  output += '  ' + (synthesis.research.business?.monetization || 'N/A') + '\n';
  output += '  Pricing: ' + (synthesis.research.business?.pricing || 'N/A') + '\n';
  
  output += '\n🏢 COMPETITORS:\n';
  output += '─'.repeat(55) + '\n';
  output += '  ' + synthesis.research.competitors?.analysis.substring(0, 150) + '\n';
  
  output += '\n✨ FEATURES & ROADMAP:\n';
  output += '─'.repeat(55) + '\n';
  output += '  Opportunities: ' + (synthesis.research.features?.opportunities?.join(', ') || 'N/A') + '\n';
  output += '  Roadmap hints: ' + (synthesis.research.features?.roadmap?.join(', ') || 'N/A') + '\n';
  
  output += '\n📚 SOURCES:\n';
  output += '─'.repeat(55) + '\n';
  if (synthesis.research.technicalAI?.sources) {
    synthesis.research.technicalAI.sources.slice(0, 3).forEach((s, i) => {
      output += '  ' + (i+1) + '. ' + s.title.substring(0, 50) + '\n';
    });
  }
  
  output += '\n💡 INSIGHTS:\n';
  output += '─'.repeat(55) + '\n';
  synthesis.insights.forEach(ins => {
    output += '  [' + ins.type + '] ' + ins.text.substring(0, 100) + '\n';
  });
  
  output += '\n🎯 RECOMMENDATIONS:\n';
  output += '─'.repeat(55) + '\n';
  synthesis.recommendations.forEach(rec => {
    output += '  [' + rec.area + '] ' + rec.recommendation.substring(0, 80) + '\n';
  });
  
  return output;
}

// Main
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
project-synthesizer.js - Synthesize project data with AI research

Usage: node project-synthesizer.js [project-name] [depth]
       node project-synthesizer.js --all [depth]

Examples:
  node project-synthesizer.js gestalt-rust 2
  node project-synthesizer.js --all 1
`);
    return;
  }
  
  const allMode = args[0] === '--all';
  const depth = parseInt(args[args.length - 1]) || 2;
  
  if (allMode) {
    // Get all projects
    const projects = fs.readdirSync(PROJECTS_DIR, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'node_modules')
      .map(d => d.name);
    
    console.log('Synthesizing ALL projects: ' + projects.length);
    
    for (const project of projects.slice(0, 20)) { // Limit to 20
      try {
        const synthesis = await synthesizeProject(project, depth);
        saveSynthesis(synthesis);
        console.log(formatSynthesis(synthesis));
      } catch (e) {
        console.log('Error with ' + project + ': ' + e.message);
      }
    }
  } else {
    const projectName = args[0];
    const synthesis = await synthesizeProject(projectName, depth);
    saveSynthesis(synthesis);
    console.log(formatSynthesis(synthesis));
  }
}

if (require.main === module) {
  main();
}

module.exports = { synthesizeProject, formatSynthesis };
