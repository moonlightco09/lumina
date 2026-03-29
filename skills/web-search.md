# Web Search Skill

When the user asks you to search the web, search for something online, or find current information:

1. Use the `run_command` tool with: `curl -s "https://ddg-webapp-aagd.vercel.app/url?q=QUERY" | head -c 2000`
   Replace QUERY with the search terms (use + between words)
2. Parse the results and summarize what you find
3. Always mention your sources

Example: User asks "search for latest Python news"
→ run_command: `curl -s "https://ddg-webapp-aagd.vercel.app/url?q=latest+python+news" | head -c 2000`
