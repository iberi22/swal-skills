/**
 * deep-research.js
 * Combined web research using Brave + Tavily
 * 
 * Usage: node deep-research.js "topic" [intensity]
 * 
 * Intensity: 1 (quick), 2 (normal), 3 (comprehensive)
 */

const https = require('https');

// API Keys
const BRAVE_API_KEY = 'BSAEvfUNvFDtYsQuWztN_RPHmzitwkQ';
const TAVILY_API_KEY = process.env.TAVILY_API_KEY || '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';

// Brave Search
function braveSearch(query, count = 10) {
  return new Promise((resolve, reject) => {
    const path = '/res/v1/web/search?q=' + encodeURIComponent(query) + '&count=' + count;
    const options = {
      hostname: 'api.search.brave.com',
      path: path,
      method: 'GET',
      headers: { 'X-Subscription-Token': BRAVE_API_KEY, 'Accept': 'application/json' }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const items = json.web?.results || [];
          resolve(items.map(r => ({
            title: r.title,
            url: r.url,
            description: r.description,
            age: r.age
          })));
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// Tavily Search
function tavilySearch(query, options = {}) {
  return new Promise((resolve, reject) => {
    if (!TAVILY_API_KEY) {
      resolve({ answer: null, results: [] });
      return;
    }

    const body = JSON.stringify({
      api_key: TAVILY_API_KEY,
      query: query,
      max_results: options.max_results || 10,
      include_answer: options.include_answer !== false
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
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Deep Research
async function deepResearch(topic, intensity) {
  intensity = intensity || 2;
  console.log('\n--- Deep Research: "' + topic + '" (intensity: ' + intensity + ') ---');
  console.log('='.repeat(50));

  const count = intensity === 1 ? 5 : intensity === 3 ? 20 : 10;

  // Run searches in parallel
  console.log('\n[*] Fetching from Brave...');
  const bravePromise = braveSearch(topic, count);

  console.log('[*] Fetching from Tavily...');
  const tavilyPromise = tavilySearch(topic, { max_results: count, include_answer: true });

  const [braveResults, tavilyResults] = await Promise.all([bravePromise, tavilyPromise]);

  // Compile report
  let report = '\n';
  report += '============================================\n';
  report += '        DEEP RESEARCH REPORT\n';
  report += '============================================\n';

  if (tavilyResults.answer) {
    report += '\n[AI ANALYSIS]\n';
    report += '--------------------------------------------\n';
    report += tavilyResults.answer + '\n';
  }

  const allResults = [
    ...(tavilyResults.results || []).map(r => ({ ...r, source: 'Tavily' })),
    ...braveResults.map(r => ({ ...r, source: 'Brave' }))
  ];

  // Dedupe by URL
  const seen = new Set();
  const unique = allResults.filter(r => {
    if (seen.has(r.url)) return false;
    seen.add(r.url);
    return true;
  });

  const sliceCount = intensity === 1 ? 5 : intensity === 3 ? 25 : 15;

  report += '\n[SOURCES - ' + unique.length + ' unique]\n';
  report += '--------------------------------------------\n';

  unique.slice(0, sliceCount).forEach((item, i) => {
    report += '\n' + (i + 1) + '. ' + item.title + '\n';
    report += '   [' + item.source + '] ' + item.url + '\n';
    if (item.description || item.content) {
      const text = item.description || item.content;
      report += '   ' + text.substring(0, 120) + '...\n';
    }
  });

  if (tavilyResults.follow_up_questions) {
    report += '\n[FOLLOW-UP QUESTIONS]\n';
    tavilyResults.follow_up_questions.forEach(q => report += '  - ' + q + '\n');
  }

  report += '\n' + '='.repeat(50) + '\n';
  report += 'Completed: ' + new Date().toISOString() + '\n';

  return report;
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(`
Deep Research Tool (Brave + Tavily)

Usage: node deep-research.js "topic" [intensity]

Intensity:
  1 = Quick (5 results)
  2 = Normal (10 results) - default
  3 = Comprehensive (20 results)

Examples:
  node deep-research.js "AI startups Chile" 2
  node deep-research.js "market analysis" 3

Environment:
  TAVILY_API_KEY - Optional, enables AI answers
`);
    return;
  }

  const topic = args[0];
  const intensity = parseInt(args[1]) || 2;

  try {
    const report = await deepResearch(topic, intensity);
    console.log(report);
  } catch (e) {
    console.error('Research failed:', e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { deepResearch, braveSearch, tavilySearch };
