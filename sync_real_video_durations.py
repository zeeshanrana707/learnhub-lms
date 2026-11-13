import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import sqlite3
import re
from app.services.youtube import get_youtube_duration_minutes, extract_youtube_video_id
from concurrent.futures import ThreadPoolExecutor, as_completed

def sync_database_durations():
    conn = sqlite3.connect('instance/lms.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT l.id, c.id, c.title, m.id, m.title, l.title, l.duration_min, l.content 
        FROM lessons l 
        JOIN modules m ON l.module_id = m.id 
        JOIN courses c ON m.course_id = c.id 
        ORDER BY c.id, m.position, l.position
    ''')
    rows = cur.fetchall()

    print(f"Total lessons to inspect: {len(rows)}")

    # Specific fixes for known typos/broken IDs
    KNOWN_FIXES = {
        'UO98lJV3jHR': ('UO98lJQ3QGI', 'Corey Schafer Matplotlib Tutorial'),
        'yaY4_cQy5Y8': ('x9JiIFvlUwk', 'Aladdin Persson PyTorch Tensors'),
        'Gol_q8hk4ko': ('4jRBRDbJemM', 'StatQuest ROC and AUC'),
        'Kdsp6soqA7g': ('M59XSi503jY', 'StatQuest Confusion Matrix, Clearly Explained'),
        'Jy4wM2P21fA': ('v5cngxo4mIg', 'Aladdin Persson PyTorch Neural Network'),
        'wnK3huU9Op8': ('wnK3huU9Op8', 'CNNs in PyTorch'),
        'qaDe0qQZ5gk': ('qaDe0qQZ5gk', 'Pretrained ResNet Models')
    }

    # Apply known fixes to content first if needed
    for r in rows:
        lid, cid, ctitle, mid, mtitle, ltitle, dur, content = r
        m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', content or '')
        if m and m.group(1) in KNOWN_FIXES:
            old_vid = m.group(1)
            new_vid, note = KNOWN_FIXES[old_vid]
            new_content = content.replace(old_vid, new_vid)
            cur.execute('UPDATE lessons SET content = ? WHERE id = ?', (new_content, lid))
            print(f"Fixed typo ID in Lesson {lid} ({ltitle}): {old_vid} -> {new_vid}")

    conn.commit()

    # Re-fetch
    cur.execute('''
        SELECT l.id, c.id, c.title, m.id, m.title, l.title, l.duration_min, l.content 
        FROM lessons l 
        JOIN modules m ON l.module_id = m.id 
        JOIN courses c ON m.course_id = c.id 
        ORDER BY c.id, m.position, l.position
    ''')
    rows = cur.fetchall()

    vids_to_fetch = {}
    for r in rows:
        lid, cid, ctitle, mid, mtitle, ltitle, dur, content = r
        vid = extract_youtube_video_id(content)
        if vid:
            vids_to_fetch[vid] = content

    print(f"Querying real YouTube lengths for {len(vids_to_fetch)} unique videos...")
    dur_map = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_youtube_duration_minutes, url): vid for vid, url in vids_to_fetch.items()}
        for f in as_completed(futures):
            vid = futures[f]
            try:
                m = f.result()
                if m:
                    dur_map[vid] = m
            except Exception:
                pass

    print(f"Successfully retrieved exact durations for {len(dur_map)} / {len(vids_to_fetch)} videos")

    # Update lessons
    updated_count = 0
    for r in rows:
        lid, cid, ctitle, mid, mtitle, ltitle, dur, content = r
        vid = extract_youtube_video_id(content)
        real_min = dur_map.get(vid)
        if real_min and real_min != dur:
            cur.execute('UPDATE lessons SET duration_min = ? WHERE id = ?', (real_min, lid))
            updated_count += 1

    conn.commit()
    conn.close()

    print(f"\nSUCCESS: Updated {updated_count} lessons with exact real YouTube lengths!")

if __name__ == '__main__':
    sync_database_durations()
