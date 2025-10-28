# Using the Beehiiv Fetcher in Claude Code

## What You Need

1. **Beehiiv API Key**
   - Go to: Beehiiv Dashboard → Settings → Integrations → API
   - Create or copy your API key

2. **Publication ID**
   - Check your Beehiiv dashboard URL: `beehiiv.com/dashboard/{publication_id}`
   - Or go to: Settings → General → Publication ID

## Step-by-Step in Claude Code

### Option 1: Run Directly in Claude Code

1. Open Claude Code in your terminal:
   ```bash
   claude-code
   ```

2. Tell Claude Code to run the script:
   ```
   Run fetch_beehiiv.py with my API key: sk_YOUR_KEY and publication ID: pub_YOUR_ID
   ```

3. Claude Code will:
   - Install any missing dependencies (requests)
   - Run the script
   - Show you the results

### Option 2: Run It Yourself

1. Make sure you have the files:
   - `fetch_beehiiv.py` (the script)
   - `content_library.json` (your existing content)

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Run the script:
   ```bash
   python3 fetch_beehiiv.py YOUR_API_KEY YOUR_PUBLICATION_ID
   ```

   Example:
   ```bash
   python3 fetch_beehiiv.py sk_abc123xyz pub_def456uvw
   ```

## What It Does

1. ✅ Connects to Beehiiv API
2. ✅ Fetches all your published newsletters
3. ✅ Cleans the HTML content to plain text
4. ✅ Adds them to your `content_library.json`
5. ✅ Avoids duplicates

## Troubleshooting

**"Error fetching posts"**
- Check your API key is correct
- Make sure the API key has read permissions
- Verify your Publication ID

**"No newsletters found"**
- Confirm you have published newsletters in Beehiiv
- Check that status="confirmed" in the API matches your posts

**"ModuleNotFoundError: No module named 'requests'"**
- Run: `pip install requests`

## After Running

Your `content_library.json` will now have:
- LinkedIn posts
- AI Corner articles
- Beehiiv newsletters

Ready for the MCP server!

## Next Step

Once you've run this and have your newsletters added, we'll build the MCP server that lets Claude search through all this content semantically.
