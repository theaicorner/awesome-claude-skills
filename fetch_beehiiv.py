#!/usr/bin/env python3
"""
Fetch newsletters from Beehiiv API and add to content library
Usage: python3 fetch_beehiiv.py YOUR_API_KEY YOUR_PUBLICATION_ID
"""

import sys
import json
import requests
from datetime import datetime
import re


def strip_html(html_content):
    """Remove HTML tags and clean up content"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text


def fetch_beehiiv_posts(api_key, publication_id):
    """Fetch all published posts from Beehiiv"""

    base_url = f"https://api.beehiiv.com/v2/publications/{publication_id}/posts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    all_posts = []
    page = 1
    limit = 50  # Max per page

    print(f"Fetching newsletters from Beehiiv...")

    while True:
        params = {
            "status": "confirmed",  # Only published posts
            "page": page,
            "limit": limit
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            posts = data.get('data', [])

            if not posts:
                break

            print(f"  Page {page}: Found {len(posts)} newsletters")
            all_posts.extend(posts)

            # Check if there are more pages
            if len(posts) < limit:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            break

    print(f"\n✅ Total newsletters fetched: {len(all_posts)}")
    return all_posts


def parse_beehiiv_posts(posts):
    """Convert Beehiiv posts to content library format"""

    parsed_posts = []

    for post in posts:
        try:
            # Extract key fields
            title = post.get('title', 'Untitled')

            # Get publish date
            published_at = post.get('published_at') or post.get('created')
            if published_at:
                # Parse ISO date
                date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%b %d, %Y')
            else:
                date_str = 'Unknown date'

            # Get content - try different fields
            content_html = (post.get('content_html') or
                          post.get('web_content') or
                          post.get('preview_text') or
                          '')

            # Strip HTML tags
            content = strip_html(content_html)

            # Only add if we have substantial content
            if len(content) > 100:
                parsed_posts.append({
                    'platform': 'The AI Corner Newsletter',
                    'date': date_str,
                    'title': title,
                    'content': content,
                    'type': 'newsletter',
                    'beehiiv_id': post.get('id')
                })

                print(f"  ✓ {title[:60]}... ({len(content)} chars)")

        except Exception as e:
            print(f"  ✗ Error parsing post: {e}")
            continue

    return parsed_posts


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 fetch_beehiiv.py YOUR_API_KEY YOUR_PUBLICATION_ID")
        print("\nTo find your Publication ID:")
        print("1. Go to your Beehiiv dashboard")
        print("2. Check the URL: beehiiv.com/dashboard/{publication_id}")
        print("3. Or go to Settings → General → Publication ID")
        sys.exit(1)

    api_key = sys.argv[1]
    publication_id = sys.argv[2]

    print("="*60)
    print("BEEHIIV NEWSLETTER FETCHER")
    print("="*60)

    # Fetch from Beehiiv
    beehiiv_posts = fetch_beehiiv_posts(api_key, publication_id)

    if not beehiiv_posts:
        print("\n❌ No newsletters found. Check your API key and Publication ID.")
        sys.exit(1)

    # Parse posts
    print("\nParsing newsletters...")
    newsletters = parse_beehiiv_posts(beehiiv_posts)
    print(f"\n✅ Parsed {len(newsletters)} newsletters")

    # Load existing content library
    library_path = 'content_library.json'
    try:
        with open(library_path, 'r', encoding='utf-8') as f:
            existing_content = json.load(f)
        print(f"\n📚 Loaded existing library: {len(existing_content)} items")
    except FileNotFoundError:
        print(f"\n📚 No existing library found, creating new one")
        existing_content = []

    # Add newsletters to library (avoid duplicates)
    existing_titles = {item.get('title') for item in existing_content}
    new_count = 0

    for newsletter in newsletters:
        if newsletter['title'] not in existing_titles:
            existing_content.append(newsletter)
            new_count += 1

    print(f"   Added {new_count} new newsletters")
    print(f"   Skipped {len(newsletters) - new_count} duplicates")

    # Save updated library
    with open(library_path, 'w', encoding='utf-8') as f:
        json.dump(existing_content, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print(f"✅ SUCCESS!")
    print(f"📊 Total content library: {len(existing_content)} items")
    print(f"   - {len([x for x in existing_content if x['type'] == 'post'])} LinkedIn posts")
    print(f"   - {len([x for x in existing_content if x['type'] == 'article'])} articles")
    print(f"   - {len([x for x in existing_content if x['type'] == 'newsletter'])} newsletters")
    print(f"\n💾 Saved to: {library_path}")
    print("="*60)


if __name__ == '__main__':
    main()
