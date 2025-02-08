import os
import feedparser
import markdown2
import frontmatter
from datetime import datetime
from pathlib import Path

def clean_content(html_content):
    # Basic cleanup - you might want to add more processing
    return html_content.replace('<h3>', '### ').replace('</h3>', '\n')

def main():
    # Get RSS feed URL from environment variable
    rss_url = os.getenv('SUBSTACK_RSS_URL')
    if not rss_url:
        raise ValueError("SUBSTACK_RSS_URL environment variable is not set")

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    # Create _posts directory if it doesn't exist
    posts_dir = Path('_posts')
    posts_dir.mkdir(exist_ok=True)

    # Process each entry
    for entry in feed.entries:
        # Format the date for Jekyll
        date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
        formatted_date = date.strftime('%Y-%m-%d')
        
        # Create filename
        title_slug = entry.title.lower().replace(' ', '-')
        filename = f"{formatted_date}-{title_slug}.md"
        filepath = posts_dir / filename

        # Prepare the front matter
        post_data = {
            'layout': 'post',
            'title': entry.title,
            'date': date.strftime('%Y-%m-%d %H:%M:%S %z'),
            'categories': ['substack'],
            'tags': ['substack'],
            'author': entry.author,
            'original_link': entry.link
        }

        # Clean and prepare content
        content = clean_content(entry.content[0].value)

        # Combine front matter and content
        post = frontmatter.Post(content, **post_data)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

if __name__ == '__main__':
    main() 