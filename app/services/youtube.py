"""
YouTube Metadata & Duration Service
Fetches accurate video length, extracts video IDs, and provides real-time duration synchronization.
"""

import urllib.request
import json
import re
from typing import Optional, Tuple

_DURATION_CACHE = {}

def extract_youtube_video_id(url_or_id: str) -> Optional[str]:
    """Extract standard 11-character YouTube video ID from any format."""
    if not url_or_id:
        return None
    s = str(url_or_id).strip()
    if len(s) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', s):
        return s
    m = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|v/|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})', s)
    return m.group(1) if m else None

def get_youtube_video_duration(url_or_id: str) -> Optional[int]:
    """
    Fetch exact duration in seconds from YouTube's public web player Innertube endpoint.
    Returns duration in seconds, or None if unavailable.
    """
    vid = extract_youtube_video_id(url_or_id)
    if not vid:
        return None

    if vid in _DURATION_CACHE:
        return _DURATION_CACHE[vid]

    # 1. Query YouTube Innertube Web Player API
    innertube_url = 'https://www.youtube.com/youtubei/v1/player'
    payload = {
        'videoId': vid,
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20240101.01.00'
            }
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        innertube_url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            length = body.get('videoDetails', {}).get('lengthSeconds')
            if length:
                sec = int(length)
                _DURATION_CACHE[vid] = sec
                return sec
    except Exception:
        pass

    # 2. Fallback: Parse watch page HTML
    try:
        watch_url = f"https://www.youtube.com/watch?v={vid}"
        w_req = urllib.request.Request(
            watch_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(w_req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'"approxDurationMs":"(\d+)"', html)
            if m:
                sec = int(m.group(1)) // 1000
                _DURATION_CACHE[vid] = sec
                return sec
            m2 = re.search(r'"lengthSeconds":"(\d+)"', html)
            if m2:
                sec = int(m2.group(1))
                _DURATION_CACHE[vid] = sec
                return sec
    except Exception:
        pass

    return None

def get_youtube_duration_minutes(url_or_id: str) -> Optional[int]:
    """Fetch exact duration in minutes (rounded to nearest minute)."""
    sec = get_youtube_video_duration(url_or_id)
    if sec is not None and sec > 0:
        return max(1, round(sec / 60))
    return None
