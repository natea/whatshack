
# 🔥 Fire Crawler - Web Scraping and Data Extraction Mode for Roo Code

This README.md provides comprehensive documentation for the Fire Crawler mode, including tool descriptions, parameter explanations, best practices, example usage, ethical considerations, use cases, and troubleshooting tips.

## Overview

Fire Crawler is a specialized mode that leverages Firecrawl's powerful web crawling and data extraction capabilities. This Roo mode enables you to gather, analyze, and structure web content efficiently for various use cases including research, competitive analysis, content aggregation, and data collection.

## Capabilities

- **Website Mapping**: Discover and map website structures
- **Recursive Crawling**: Explore websites with configurable depth and scope
- **Structured Data Extraction**: Extract specific data using natural language prompts
- **Content Scraping**: Retrieve precise content from web pages
- **Web Search**: Find and retrieve content across the web

## MCP.Composio.dev - Model Context Protocol Integration Platform

### What is MCP.Composio.dev?

MCP.Composio.dev is a managed Model Context Protocol (MCP) server platform that solves key challenges in AI agent integrations:

1. **Authentication & Authorization**: Built-in authentication support for 300+ applications, handling OAuth, API keys, and basic auth flows automatically.

2. **Pre-built MCP Servers**: Ready-to-use MCP servers for popular services like GitHub, Slack, Linear, Google Workspace, and many others.

3. **Standardized Integration**: Follows the Model Context Protocol specification, making it compatible with any MCP-compliant client.

## How It Works

MCP.Composio.dev serves as a bridge between AI applications and external services:

1. **Client Connection**: AI applications (like Cursor IDE, Claude Desktop) connect to Composio MCP servers
2. **Authentication Handling**: Composio manages all authentication flows securely
3. **Tool & Resource Exposure**: Composio exposes standardized tools and resources for each integrated service
4. **Execution & Response**: When tools are called, Composio handles the API interactions and returns formatted responses

## Key Benefits

- **Zero Setup Integration**: Connect to 300+ apps with minimal configuration
- **Authentication Management**: No need to handle complex OAuth flows or API key storage
- **Standardized Interface**: Consistent tool and resource patterns across all integrations
- **Framework Support**: Works with OpenAI, Vercel AI SDK, LangChain, CrewAI and other frameworks

## Example Use Cases

- Connect AI agents to productivity tools (Slack, Gmail, Notion)
- Enable AI workflows with development tools (GitHub, Linear, Jira)
- Create AI assistants with access to enterprise systems
- Build multi-service workflows that operate across different platforms

MCP.Composio.dev eliminates the complexity of building and maintaining individual MCP servers, allowing developers to focus on creating AI experiences rather than integration details.

## Available Tools

### 1. FIRECRAWL_MAP_URLS

Maps a website's URL structure to discover available pages.

```javascript
{
  "url": "https://example.com",       // Base URL to start mapping from
  "limit": 10,                        // Maximum number of URLs to return
  "includeSubdomains": false,         // Whether to include subdomains
  "ignoreSitemap": false              // Whether to ignore the sitemap
}
```

### 2. FIRECRAWL_CRAWL_URLS

Crawls websites recursively with configurable parameters.

```javascript
{
  "url": "https://example.com",                // Base URL to start crawling from
  "limit": 10,                                 // Maximum number of pages to crawl
  "maxDepth": 2,                               // Maximum depth to crawl
  "allowExternalLinks": false,                 // Whether to follow external links
  "allowBackwardLinks": true,                  // Whether to follow links to previously seen pages
  "includePaths": ["blog/*"],                  // Only include paths matching these patterns
  "excludePaths": ["admin/*"],                 // Exclude paths matching these patterns
  "scrapeOptions_onlyMainContent": true,       // Only extract main content
  "scrapeOptions_formats": ["markdown", "html"], // Output formats
  "scrapeOptions_waitFor": 1000                // Wait time in ms before scraping
}
```

### 3. FIRECRAWL_EXTRACT

Extracts structured data from web pages using natural language prompts or JSON schemas.

```javascript
{
  "urls": ["https://example.com/products/*"],  // URLs to extract data from (supports wildcards)
  "prompt": "Extract product names, prices, and descriptions", // Natural language prompt
  "schema": {                                  // Alternative: JSON schema
    "products": [{
      "name": "string",
      "price": "number",
      "description": "string"
    }]
  },
  "enable_web_search": false                   // Whether to follow external links
}
```

### 4. FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM

Scrapes specific content from web pages with formatting options.

```javascript
{
  "url": "https://example.com",                // URL to scrape
  "onlyMainContent": true,                     // Only extract main content
  "formats": ["markdown"],                     // Output formats
  "waitFor": 1000,                             // Wait time in ms before scraping
  "actions": [                                 // Optional: Actions to perform before scraping
    {"type": "click", "selector": ".button"}
  ]
}
```

### 5. FIRECRAWL_SEARCH

Performs web searches and returns relevant results.

```javascript
{
  "query": "web scraping best practices",      // Search query
  "limit": 5,                                  // Maximum number of results
  "country": "US",                             // Country code for search results
  "lang": "en",                                // Language code for search results
  "formats": ["markdown"]                      // Output formats
}
```

### 6. FIRECRAWL_CRAWL_JOB_STATUS

Checks the status of a crawl job.

```javascript
{
  "id": "job-uuid-here"                        // ID of the crawl job
}
```

### 7. FIRECRAWL_CANCEL_CRAWL_JOB

Cancels a running crawl job.

```javascript
{
  "id": "job-uuid-here"                        // ID of the crawl job
}
```

## Best Practices

1. **Start Small**: Begin with smaller crawls and gradually expand scope
2. **Use Limits**: Always set appropriate limits to prevent excessive crawling
3. **Focus Crawling**: Use includePaths/excludePaths to target relevant content
4. **Respect Websites**: Add delays between requests and don't overload servers
5. **Monitor Jobs**: Use job status checks for long-running crawls
6. **Cancel When Needed**: Cancel unnecessary crawl jobs to save resources

## Example Usage

### Mapping a Website Structure

```javascript
// Example of mapping a website structure
{
  "server_name": "firecrawl",
  "tool_name": "FIRECRAWL_MAP_URLS",
  "arguments": {
    "url": "https://example.com",
    "limit": 10
  }
}
```

### Extracting Product Information

```javascript
// Example of extracting product information
{
  "server_name": "firecrawl",
  "tool_name": "FIRECRAWL_EXTRACT",
  "arguments": {
    "urls": ["https://example.com/products/*"],
    "prompt": "Extract product names, prices, and descriptions"
  }
}
```

### Searching for Information

```javascript
// Example of searching for information
{
  "server_name": "firecrawl",
  "tool_name": "FIRECRAWL_SEARCH",
  "arguments": {
    "query": "web scraping best practices",
    "limit": 5
  }
}
```

## Ethical Considerations

When using the Fire Crawler mode, always consider these ethical guidelines:

1. **Respect Terms of Service**: Always review and comply with a website's terms of service
2. **Respect robots.txt**: Honor the directives in robots.txt files
3. **Rate Limiting**: Implement delays between requests to avoid overwhelming servers
4. **Data Privacy**: Handle personal information responsibly and in compliance with regulations
5. **Attribution**: Properly attribute content to its original source when republishing
6. **Transparency**: Be honest about your scraping activities and their purpose

## Use Cases

- **Market Research**: Gather competitor pricing and product information
- **Content Aggregation**: Collect news articles, blog posts, or other content
- **Data Analysis**: Extract structured data for analysis and insights
- **Lead Generation**: Gather contact information from business directories
- **Academic Research**: Collect data for research projects
- **SEO Analysis**: Monitor keyword rankings and content performance

## Troubleshooting

- **Rate Limiting**: If you encounter 429 errors, increase delays between requests
- **Blocked Access**: Some websites may block scraping; respect their terms of service
- **Timeout Errors**: For large crawls, use smaller batches and monitor job status
- **Data Quality**: Verify extracted data for accuracy and completeness
- **Format Issues**: Try different output formats if content isn't properly extracted
