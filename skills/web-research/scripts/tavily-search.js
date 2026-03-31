/**
 * tavily-search.js
 * Tavily Search API CLI
 * 
 * Usage: node tavily-search.js "search query" [count] [include_answer]
 * 
 * Note: Requires TAVILY_API_KEY environment variable
 */

const https = require('https');

const API_KEY = process.env.TAVILY_API_KEY || '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';
const BASE_URL = 'api.tavily.com';

if (!API_KEY) {
  console.log('⚠️  TAVILY_API_KEY not set');
  console.log('   Get your key at: https://tavily.com');
  console.log('   Export: export TAVILY_API_KEY=tvly-xxxxx');
}

function search(query, options = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      api_key: API_KEY,
      query: query,
      max_results: options.max_results || 10,
      include_answer: options.include_answer || false,
      include_raw_content: options.include_raw_content || false,
      ...options
    });

    const reqOptions = {
      hostname: BASE_URL,
      path: '/search',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
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

function formatResults(results) {
  let output = '\n🔍 Tavily Search Results\n';
  output += '='.repeat(50) + '\n';

  if (results.answer) {
    output += '\n📝 AI Answer:\n';
    output += '─'.repeat(30) + '\n';
    output += `${results.answer}\n`;
  }

  output += '\n📄 Results:\n';
  output += '─'.repeat(30) + '\n';

  results.results?.forEach((item, i) => {
    output += `${i + 1}. ${item.title}\n`;
    output += `   URL: ${item.url}\n`;
    if (item.content) {
      output += `   ${item.content.substring(0, 150)}...\n`;
    }
    if (item.score) {
      output += `   Score: ${(item.score * 100).toFixed(1)}%\n`;
    }
    output += '\n';
  });

  if (results.follow_up_questions) {
    output += '\n❓ Follow-up Questions:\n';
    results.follow_up_questions.forEach(q => output += `  - ${q}\n`);
  }

  return output;
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
🔍 Tavily Search CLI

Usage: 
  node tavily-search.js "search query" [count] [include_answer]

Options:
  count          Number of results (default: 10)
  include_answer Include AI-generated answer (true/false, default: true)

Examples:
  node tavily-search.js "AI startups Chile" 10 true
  node tavily-search.js "company research" 20

Environment:
  TAVILY_API_KEY - Your Tavily API key (get at https://tavily.com)
`);
    return;
  }

  const query = args[0];
  const count = parseInt(args[1]) || 10;
  const includeAnswer = args[2] !== 'false';

  console.log(`\n🔍 Searching: "${query}" (${count} results, answer: ${includeAnswer})\n`);

  if (!API_KEY) {
    console.error('❌ TAVILY_API_KEY not set');
    process.exit(1);
  }

  try {
    const results = await search(query, { max_results: count, include_answer: includeAnswer });
    console.log(formatResults(results));
  } catch (e) {
    console.error('Search failed:', e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { search, formatResults };
