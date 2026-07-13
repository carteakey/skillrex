#!/usr/bin/env python3
"""
Toronto Weekend Digest — Data Collection Script
Scrapes multiple sources for weekend events in Toronto and outputs structured JSON.

Sources:
1. blogTO Radar (RSS → URL → Firecrawl) — weekly "things to do" article
2. To Do Canada (Firecrawl) — weekly categorized events
3. r/toronto (Reddit RSS) — community recommendations
4. Eventbrite (Firecrawl search) — indie/smaller events
"""

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from html.parser import HTMLParser


# ---------- Config ----------

ENV_PATH = os.path.expanduser("~/.agent/.env")
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")


def load_api_key():
    global FIRECRAWL_API_KEY
    if FIRECRAWL_API_KEY:
        return FIRECRAWL_API_KEY
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                if line.startswith("FIRECRAWL_API_KEY="):
                    FIRECRAWL_API_KEY = line.strip().split("=", 1)[1]
                    return FIRECRAWL_API_KEY
    return ""


# ---------- Helpers ----------

def curl_fetch(url, headers=None, timeout=30):
    cmd = ["curl", "-s", "-L", "--max-time", str(timeout)]
    default_headers = {"User-Agent": "Mozilla/5.0 (compatible; TorontoDigest/1.0)"}
    if headers:
        default_headers.update(headers)
    for k, v in default_headers.items():
        cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"


def firecrawl_scrape(url):
    key = load_api_key()
    if not key:
        return {"error": "No FIRECRAWL_API_KEY"}
    payload = {"url": url, "formats": ["markdown"], "onlyMainContent": True}
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "https://api.firecrawl.dev/v1/scrape",
             "-H", f"Authorization: Bearer {key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=90
        )
        data = json.loads(result.stdout)
        if data.get("success"):
            return {"markdown": data["data"].get("markdown", "")}
        return {"error": data.get("error", "Unknown")}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_search(query, limit=3):
    key = load_api_key()
    if not key:
        return []
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True}
    }
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "https://api.firecrawl.dev/v1/search",
             "-H", f"Authorization: Bearer {key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=90
        )
        data = json.loads(result.stdout)
        return data.get("data", []) if data.get("success") else []
    except Exception:
        return []


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_html(html_str):
    s = HTMLStripper()
    s.feed(html_str)
    return s.get_data()


def strip_md_links(text):
    """Remove markdown link formatting: [text](url) → text"""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text).strip()


def get_weekend_dates():
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7
    if days_until_friday == 0 and today.hour >= 18:
        days_until_friday = 7
    friday = today + timedelta(days=days_until_friday)
    saturday = friday + timedelta(days=1)
    sunday = friday + timedelta(days=2)
    return {
        "friday": friday.strftime("%b %d"),
        "saturday": saturday.strftime("%b %d"),
        "sunday": sunday.strftime("%b %d"),
        "label": f"{friday.strftime('%b %d')}–{sunday.strftime('%d')}",
        "month": friday.strftime("%B %Y")
    }


# ---------- Source 1: blogTO Radar ----------

def fetch_blogto_radar():
    """Get blogTO weekly radar article URL from RSS, then scrape via Firecrawl."""
    events = []
    raw = curl_fetch("https://www.blogto.com/rss/articles.xml")
    if not raw or raw.startswith("ERROR"):
        return events

    # Find latest "things to do" article URL
    items = re.findall(r'<item>(.*?)</item>', raw, re.DOTALL)
    radar_url = None
    for item in items:
        title_match = re.search(r'<title>(.*?)</title>', item)
        if title_match and 'things to do' in title_match.group(1).lower():
            link_match = re.search(r'<link>(.*?)</link>', item)
            if link_match:
                radar_url = link_match.group(1)
                break

    if not radar_url:
        return events

    # Scrape the article with Firecrawl for clean markdown
    result = firecrawl_scrape(radar_url)
    md = result.get("markdown", "")
    if not md:
        return events

    lines = md.split('\n')
    current_category = "Top Picks"
    
    # blogTO Firecrawl markdown structure per event:
    #   - [Event Name](url)            ← event link (starts with "- [")
    #   ...empty lines...
    #   Date (e.g. "April 23")
    #   ...empty lines + "Add to my Events"...
    #   [Event Name](url)              ← repeated link
    #   ...empty lines...
    #   Description text
    #   ...empty lines...
    #   Location text
    #   ...empty lines + "Add to my Events"...
    #
    # Category headers: - ##### Category Name  (e.g. "- ##### Art events")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Category header: - ##### Category Name
        cat_match = re.match(r'^-\s+#{1,5}\s+(.+)', line)
        if cat_match:
            cat = cat_match.group(1).strip()
            # Filter out newsletter promo
            if 'newsletter' not in cat.lower():
                current_category = cat
            i += 1
            continue
        
        # Event link: - [Event Name](url)
        evt_match = re.match(r'^-\s+\[(.+?)\]\((https://www\.blogto\.com/events/[^)]+)\)', line)
        if evt_match:
            event_name = strip_md_links(evt_match.group(1))
            event_url = evt_match.group(2)
            event_date = ""
            event_desc = ""
            event_location = ""
            
            # Scan forward to find date, description, location
            # blogTO pattern: - [Event](url) → date → "Add to my Events" → [Event](url) → desc → location → "Add to my Events"
            # There are lots of empty lines between sections (up to 60 lines per event block)
            j = i + 1
            phase = 'date'  # phases: date → repeat_link → desc → location
            while j < min(i + 80, len(lines)):
                inner = lines[j].strip()
                
                # Skip empty lines
                if not inner:
                    j += 1
                    continue
                
                # Skip "Add to my Events" noise
                if inner == 'Add to my Events':
                    j += 1
                    continue
                
                # Phase: date
                if phase == 'date':
                    if re.match(r'^[A-Z][a-z]+ \d{1,2}', inner) and 'http' not in inner:
                        event_date = inner
                        phase = 'repeat_link'
                        j += 1
                        continue
                    # Sometimes date is missing, skip to repeat link
                    if event_url in inner:
                        phase = 'desc'
                        j += 1
                        continue
                    j += 1
                    continue
                
                # Phase: repeat_link (second occurrence of the event link)
                if phase == 'repeat_link':
                    if event_url in inner:
                        phase = 'desc'
                    j += 1
                    continue
                
                # Phase: description
                if phase == 'desc':
                    if len(inner) > 10 and 'add to my' not in inner.lower() and '#' not in inner[:3]:
                        event_desc = inner
                        phase = 'location'
                    j += 1
                    continue
                
                # Phase: location
                if phase == 'location':
                    if len(inner) > 2 and len(inner) < 80 and '#' not in inner[:3] and 'http' not in inner and inner != 'Add to my Events':
                        event_location = inner
                    break
                
                j += 1
            
            events.append({
                "name": event_name,
                "date": event_date,
                "description": event_desc,
                "location": event_location,
                "category": current_category,
                "source": "blogTO",
                "url": event_url
            })
        
        i += 1

    return events


# ---------- Source 2: To Do Canada ----------

def fetch_todocanada():
    events = []
    result = firecrawl_scrape("https://www.todocanada.ca/things-to-do-in-toronto-this-weekend/")
    md = result.get("markdown", "")
    if not md:
        return events

    # Category headers: ## **I. Live Music**, ### **EDM Concerts/Concert Tours**
    current_category = "General"
    sub_category = ""
    
    # Track section boundaries — only parse sections I-IV (concrete events)
    # Section V+ is evergreen/promotional links
    in_event_section = True
    event_sections = {'live music', 'live theatre', 'sports', 'festivals', 'exhibitions', 'food'}
    
    lines = md.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Major section headers: ## **I. Live Music**
        major_cat = re.match(r'^#{1,3}\s+\*?\*?(?:I+V?I?V?\.?\s+)?(.+?)(?:\*\*)?\s*$', line)
        if major_cat and line.startswith('#'):
            cat = major_cat.group(1).strip().rstrip('*').strip()
            # Check if we've hit Section V (Exhibitions, Food Events, Other)
            # This section has evergreen links, not concrete weekend events
            cat_lower = cat.lower()
            if any(w in cat_lower for w in ['exhibition', 'food event', 'other activit']):
                in_event_section = False
            elif any(w in cat_lower for w in event_sections):
                in_event_section = True
                current_category = cat
                sub_category = ""
            
            # Sub-category headers: ### **EDM Concerts/Concert Tours**
            sub_match = re.match(r'^#{1,3}\s+\*?\*?(.+?)\*?\*?\s*$', line)
            if sub_match:
                sub = sub_match.group(1).strip().rstrip('*').strip()
                if len(sub) < 60 and 'click' not in sub.lower() and 'share' not in sub.lower():
                    sub_category = sub
                    if not current_category or current_category == "General":
                        current_category = sub
            i += 1
            continue
        
        # Skip non-event sections
        if not in_event_section:
            i += 1
            continue
        
        if not line:
            i += 1
            continue
        
        # Event format: - [**Event Name**](url) on Day, Month XX | HH:MM PM @ Venue
        # Also: - [Event Name](url) on Day, Month XX \| HH:MM PM @ Venue
        evt_match = re.match(
            r'^-\s+\[?\*?\*?\s*(.+?)\s*\*?\*?\]?\s*(?:\([^)]*\))?\s+on\s+(.+?)$',
            line
        )
        if evt_match:
            name = re.sub(r'[\[\]*]', '', evt_match.group(1)).strip()
            detail = evt_match.group(2).strip().rstrip('\\')
            
            # Extract time and venue from detail: "Friday, April 24 \| 07:00 PM @ The Danforth Music Hall"
            event_date = ""
            event_location = ""
            
            # Split on @ for venue
            if ' @ ' in detail:
                detail_part, event_location = detail.rsplit(' @ ', 1)
                detail = detail_part.strip()
            
            # Split on | or \ for time  
            if ' | ' in detail:
                detail, time_part = detail.rsplit(' | ', 1)
                event_date = detail.strip()
                if time_part.strip():
                    event_date = f"{event_date}, {time_part.strip()}"
            elif ' \\| ' in detail:
                detail, time_part = detail.rsplit(' \\| ', 1)
                event_date = detail.strip()
                if time_part.strip():
                    event_date = f"{event_date}, {time_part.strip()}"
            else:
                event_date = detail
            
            # Clean up date: remove trailing backslashes
            event_date = event_date.rstrip('\\').strip()
            
            # Skip noise
            skip_words = ['click to', 'share on', 'published', 'http', 'sign up', 'subscribe', 
                          'free fun', 'kids', 'april in toronto', 'you may', 'concert tour',
                          'headliner', 'live concert']
            if len(name) < 5 or any(w in name.lower() for w in skip_words):
                i += 1
                continue
            
            # Use sub_category if available, otherwise current_category
            cat = sub_category if sub_category and sub_category != current_category else current_category
            if cat in ('General', ''):
                cat = "Events"
            
            events.append({
                "name": name,
                "date": event_date,
                "description": "",
                "location": event_location,
                "category": cat,
                "source": "To Do Canada",
                "url": "https://www.todocanada.ca/things-to-do-in-toronto-this-weekend/"
            })
            i += 1
            continue
        
        # Ongoing events: - Event Name until Date @ Venue
        ongoing_match = re.match(r'^-\s+\*?\*?(.+?)\*?\*?\s+until\s+(.+?)(?:\s+@\s+(.+?))?$', line)
        if ongoing_match:
            name = re.sub(r'[\[\]*]', '', ongoing_match.group(1)).strip()
            until_date = ongoing_match.group(2).strip()
            venue = ongoing_match.group(3).strip() if ongoing_match.group(3) else ""
            
            skip_words = ['click to', 'share on', 'published', 'http', 'sign up', 'subscribe', 'free fun']
            if len(name) < 5 or any(w in name.lower() for w in skip_words):
                i += 1
                continue
            
            cat = sub_category if sub_category else (current_category if current_category != "General" else "Events")
            events.append({
                "name": name,
                "date": f"until {until_date}",
                "description": "",
                "location": venue,
                "category": cat,
                "source": "To Do Canada",
                "url": "https://www.todocanada.ca/things-to-do-in-toronto-this-weekend/"
            })
            i += 1
            continue
        
        i += 1
    
    return events


# ---------- Source 3: r/toronto ----------

def fetch_reddit_toronto():
    events = []
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    # The auto-mod thread is titled "Things to do in Toronto - Week of..."
    for query in ["things+to+do+in+toronto+week", "what+are+you+doing+this+weekend+toronto"]:
        raw = curl_fetch(
            f"https://www.reddit.com/r/toronto/search.rss?q={query}&restrict_sr=on&sort=new&t=week&limit=3"
        )
        if not raw or raw.startswith("ERROR") or "blocked" in raw.lower():
            continue

        try:
            root = ET.fromstring(raw)
            for entry in root.findall('atom:entry', ns)[:2]:
                title_el = entry.find('atom:title', ns)
                link_el = entry.find('atom:link', ns)
                content_el = entry.find('atom:content', ns)

                title = title_el.text if title_el is not None and title_el.text else ""
                link = link_el.get('href', '') if link_el is not None else ''
                content_html = content_el.text if content_el is not None and content_el.text else ""
                content = strip_html(content_html)[:300]

                if title and not any(e['name'] == title for e in events):
                    events.append({
                        "name": title,
                        "date": "",
                        "description": content[:200],
                        "location": "",
                        "category": "Community Picks",
                        "source": "r/toronto",
                        "url": link
                    })
        except ET.ParseError:
            pass

    return events


# ---------- Source 4: Eventbrite ----------

def fetch_eventbrite():
    events = []
    url = "https://www.eventbrite.com/d/canada--toronto/events--this-weekend/"
    result = firecrawl_scrape(url)
    md = result.get("markdown", "")
    
    if not md:
        events.append({
            "name": "Eventbrite — This Weekend in Toronto",
            "date": "",
            "description": "Browse full weekend listings",
            "location": "",
            "category": "Events",
            "source": "Eventbrite",
            "url": url
        })
        return events
    
    # Eventbrite markdown structure (Firecrawl):
    # [**EVENT NAME**](https://eventbrite.ca/e/...)
    # 
    # Friday at 10:30 PM
    # 
    # Toronto · Nuvo Toronto
    # 
    # From CA$0.00
    
    lines = md.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Event link: [**EVENT NAME**](url) — the actual event title format
        # Skip markdown image lines: - [![...primary image](url)]
        if line.startswith('![') or '- ![' in line:
            i += 1
            continue
        
        # Match the actual Eventbrite event format: [**EVENT NAME**](https://eventbrite.ca/e/...)
        evt_match = re.match(r'^\[?\*\*(.+?)\*\*\]?\(https://www\.eventbrite\.ca/e/', line)
        if not evt_match:
            # Also try plain link format: [Event Name](https://eventbrite.ca/e/...)
            evt_match = re.match(r'^\[(.+?)\]\(https://www\.eventbrite\.ca/e/', line)
        if evt_match:
            name = re.sub(r'[\[\]*]', '', evt_match.group(1)).strip()
            # Strip leading ! artifacts from markdown image syntax
            name = re.sub(r'^!+', '', name).strip()
            # Clean up: remove escaped pipes \\| and trailing info
            name = re.sub(r'\s*\\\\?\|.*$', '', name).strip()
            name = re.sub(r'\s*[|–—].*$', '', name).strip()
            # Skip image artifacts
            if not name or len(name) < 4 or 'internet explorer' in name.lower() or 'primary image' in name.lower():
                i += 1
                continue
            
            # Scan forward for date and venue
            event_date = ""
            event_location = ""
            j = i + 1
            while j < min(i + 15, len(lines)):
                inner = lines[j].strip()
                
                # Date pattern: "Friday at 10:30 PM" or "Saturday at 8:00 PM" or "Apr 24"
                if not event_date:
                    day_match = re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+at\s+(.+)', inner)
                    date_match = re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}', inner)
                    multi_day = re.match(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+(.+)', inner)
                    if day_match:
                        event_date = inner
                        j += 1
                        continue
                    elif date_match:
                        event_date = inner
                        j += 1
                        continue
                    elif multi_day:
                        event_date = inner
                        j += 1
                        continue
                
                # Venue pattern: "Toronto · Venue Name"
                if ' · ' in inner and 'toronto' in inner.lower():
                    parts = inner.split(' · ')
                    event_location = parts[-1].strip()
                    j += 1
                    continue
                
                # Price line = we're past the event info
                if inner.startswith('From CA$') or inner.startswith('Free'):
                    break
                
                # Next event link = stop
                if 'eventbrite.ca/e/' in inner:
                    break
                
                j += 1
            
            events.append({
                "name": name,
                "date": event_date,
                "description": "",
                "location": event_location,
                "category": "Events",
                "source": "Eventbrite",
                "url": url
            })
        
        i += 1
    
    # Cap at 15 events to avoid bloat
    events = events[:15]
    
    if not events:
        events.append({
            "name": "Eventbrite — This Weekend in Toronto",
            "date": "",
            "description": "Browse full weekend listings",
            "location": "",
            "category": "Events",
            "source": "Eventbrite",
            "url": url
        })
    
    return events


# ---------- Main ----------

def main():
    weekend = get_weekend_dates()
    print(f"=== Toronto Weekend Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    print(f"Weekend: {weekend['label']}")
    print()

    all_events = []

    print("1. Fetching blogTO Radar...")
    blogto = fetch_blogto_radar()
    print(f"   Found {len(blogto)} events")
    all_events.extend(blogto)

    print("2. Fetching To Do Canada...")
    todocanada = fetch_todocanada()
    print(f"   Found {len(todocanada)} events")
    all_events.extend(todocanada)

    print("3. Fetching r/toronto...")
    reddit = fetch_reddit_toronto()
    print(f"   Found {len(reddit)} posts")
    all_events.extend(reddit)

    print("4. Fetching Eventbrite...")
    eventbrite = fetch_eventbrite()
    print(f"   Found {len(eventbrite)} events")
    all_events.extend(eventbrite)

    # Dedup by normalized name (fuzzy: lowercase, remove punctuation/special chars, keep 50 chars)
    seen = set()
    deduped = []
    for e in all_events:
        key = re.sub(r'[^a-z0-9 ]', '', e['name'].lower()).strip()
        key = re.sub(r'\s+', ' ', key)[:50]
        if key and key not in seen and len(key) > 3:
            seen.add(key)
            deduped.append(e)

    print(f"\nTotal raw: {len(all_events)} → After dedup: {len(deduped)}")

    output = {
        "timestamp": datetime.now().isoformat(),
        "weekend": weekend,
        "total_events": len(deduped),
        "events": deduped
    }

    print("\n=== JSON OUTPUT ===")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
