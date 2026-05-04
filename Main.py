import random
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import TK

socket.setdefaulttimeout(3)  # DNS解析最长等待3秒

suffixes = [
    'com', 'org', 'net', 'edu', 'cn', 'io', 'dev', 'info', 'biz', 'co',
    'gov', 'mil', 'int', 'xyz', 'top', 'vip', 'club', 'site', 'online',
    'shop', 'store', 'app', 'tech', 'cloud', 'ai', 'me', 'tv', 'cc', 'fm',
    'us', 'uk', 'de', 'jp', 'fr', 'au', 'ru', 'in', 'br', 'ca', 'it', 'es',
    'nl', 'kr', 'ch', 'se', 'no', 'pl', 'mx', 'be', 'at', 'dk', 'fi', 'ie',
    'nz', 'sg', 'hk', 'tw', 'la', 'gd', 'ms', 'am', 'im', 'to',
    'ac', 'name', 'pro', 'mobi', 'asia', 'tel', 'travel', 'jobs', 'cat',
    'post', 'aero', 'coop', 'museum', 'xxx', 'adult', 'sex', 'dating',
    'photography', 'guru', 'ninja', 'rocks', 'today', 'life', 'world',
    'news', 'media', 'blog', 'wiki', 'design', 'art', 'photo', 'video',
    'game', 'fun', 'love', 'live', 'social', 'team', 'zone', 'space',
    'email', 'link', 'click', 'webcam', 'software', 'solutions', 'services',
    'company', 'business', 'management', 'marketing', 'consulting',
    'agency', 'studio', 'works', 'center', 'institute', 'foundation',
    'education', 'school', 'college', 'university', 'training', 'course',
    'academy', 'degree', 'doctor', 'lawyer', 'attorney', 'legal', 'accountant',
    'finance', 'financial', 'money', 'cash', 'credit', 'loan', 'insurance',
    'tax', 'investments', 'capital', 'bank', 'trading', 'market', 'exchange',
    'stock', 'fund', 'wealth', 'asset', 'property', 'realestate', 'estate',
    'house', 'home', 'land', 'farm', 'garden', 'kitchen', 'bathroom',
    'bedroom', 'living', 'family', 'kids', 'baby', 'mom', 'dad', 'parent',
    'person', 'people', 'community', 'society', 'culture', 'history',
    'science', 'math', 'physics', 'chemistry', 'biology', 'geography',
    'environment', 'nature', 'earth', 'planet', 'space', 'universe',
    'galaxy', 'star', 'moon', 'sun', 'sky', 'weather', 'climate', 'season',
    'spring', 'summer', 'autumn', 'winter', 'day', 'night', 'morning',
    'evening', 'noon', 'midnight', 'hour', 'minute', 'second', 'time',
    'date', 'calendar', 'event', 'party', 'festival', 'holiday', 'vacation',
    'trip', 'tour', 'travel', 'journey', 'adventure', 'explore', 'discover',
    'experience', 'memory', 'moment', 'feeling', 'emotion', 'mood', 'spirit',
    'soul', 'mind', 'brain', 'heart', 'body', 'health', 'fitness', 'sport',
    'exercise', 'yoga', 'dance', 'music', 'song', 'album', 'artist', 'band',
    'concert', 'theater', 'movie', 'film', 'cinema', 'drama', 'comedy',
    'action', 'horror', 'thriller', 'romance', 'fantasy', 'scifi', 'anime',
    'manga', 'comic', 'book', 'novel', 'story', 'poem', 'quote', 'joke',
    'riddle', 'puzzle', 'game', 'play', 'fun', 'laugh', 'smile', 'happy',
    'joy', 'peace', 'love', 'hope', 'dream', 'wish', 'goal', 'plan', 'idea',
    'thought', 'concept', 'theory', 'fact', 'truth', 'reality', 'fiction',
    'fantasy', 'magic', 'mystery', 'secret', 'hidden', 'lost', 'found',
    'search', 'find', 'seek', 'look', 'see', 'watch', 'view', 'show', 'display',
    'present', 'introduce', 'announce', 'declare', 'state', 'say', 'tell',
    'speak', 'talk', 'chat', 'discuss', 'debate', 'argue', 'fight', 'battle',
    'war', 'peace', 'victory', 'defeat', 'win', 'lose', 'draw', 'tie', 'match',
    'contest', 'competition', 'tournament', 'league', 'team', 'player', 'coach',
    'referee', 'judge', 'jury', 'audience', 'fan', 'supporter', 'follower',
    'leader', 'boss', 'manager', 'director', 'president', 'ceo', 'cto', 'cfo',
    'coo', 'cio', 'cmo', 'cdo', 'cro', 'cso', 'cpo', 'cao', 'cco', 'cho',
    'cino', 'clo', 'cmo', 'cno', 'cpo', 'cqo', 'cro', 'cso', 'cto', 'cuo',
    'cvo', 'cwo', 'cxo', 'cyo', 'czo'
]

running = False

#并发处理
progress_counter = 0
progress_lock = threading.Lock()

def check_single_domain(name, suffix):
    global running, progress_counter
    if not running:
        return
    domain = f"{name}.{suffix}"
    TK.query_domain(domain)
    with progress_lock:
        progress_counter += 1

#猴子打印机函数
def infinite_Monkey():
    length = random.randint(1, 10)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def get_domain_name():
    if TK.selected_mode is None:
        return None
    if TK.selected_mode == "猴子模式":
        return infinite_Monkey()
    else:
        name = TK.TwoInput.get().strip()
        return name if name else None
        
def stop_query():
    global running
    running = False
    TK.reset_to_default()

def on_start_click():
    name = get_domain_name()
    if name is None:
        return
    TK.flash_start_button()
    threading.Thread(target=run_query, args=(name,), daemon=True).start()

def run_query(name):
    global running, progress_counter
    running = True
    progress_counter = 0
    total = len(suffixes)
    TK.init_progress(total)
    TK.start_progress_poll(lambda: progress_counter)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for suffix in suffixes:
            if not running:
                break
            futures.append(executor.submit(check_single_domain, name, suffix))
        for f in futures:
            f.result()
    
    running = False
    TK.stop_progress_poll()
    TK.update_progress(progress_counter)
    TK.stop_flash()

TK.Button3.config(command=on_start_click)
TK.Button4.config(command=stop_query)
TK.canvas.bind("<Enter>", TK.bind_mousewheel)
TK.canvas.bind("<Leave>", TK.unbind_mousewheel)

TK.top.mainloop()
