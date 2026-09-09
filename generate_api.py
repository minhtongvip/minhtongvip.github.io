import json, os, re, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent / 'site'
DATA=ROOT/'data'
API=ROOT/'api'

def load(name):
    p=DATA/name
    if not p.exists(): return []
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception: return []

def clean(x):
    return x if x is not None else ''

def normalize(items, start_id=1):
    out=[]
    for i,a in enumerate(items, start_id):
        a=dict(a)
        a.setdefault('id',i)
        a.setdefault('content_id',a['id'])
        a.setdefault('app_name',a.get('name',''))
        a.setdefault('bundle_id',a.get('bundle',''))
        a.setdefault('app_icon',a.get('icon',''))
        a.setdefault('app_iconurl',a.get('icon',''))
        a.setdefault('app_version',(a.get('versions') or [{}])[0].get('version',''))
        a.setdefault('app_description',a.get('description',''))
        a['versions']=a.get('versions') or []
        out.append(a)
    return out

apps=normalize(load('apps.json'))
games=normalize(load('games.json'), len(apps)+1)
all_items=apps+games

def resp(items): return {'status':1,'error':0,'result':{'items':items,'list':items,'data':items}}
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

write(API/'apps.json',resp(all_items))
write(API/'categories.json',resp([{'id':0,'name':'Tất cả'},{'id':1,'name':'Ứng dụng'},{'id':2,'name':'Game'}]))
write(API/'top_new.json',resp(all_items[:50]))
write(API/'top_download.json',resp(all_items[:50]))
write(API/'hot.json',resp(all_items[:50]))
write(API/'featured.json',resp(all_items[:20]))
for a in all_items:
    aid=a['id']
    write(API/'apps'/f'{aid}.json',resp([a]))
    write(API/'versions'/f'{aid}.json',resp(a.get('versions',[])))

# Compatibility endpoints for the original AppVN/Appota URL shapes.
endpoints={
 'w/content/categories':resp([{'id':0,'name':'Tất cả'},{'id':1,'name':'Ứng dụng'},{'id':2,'name':'Game'}]),
 'w/content/top_hot':resp(all_items[:50]),
 'w/content/top_newest':resp(all_items[:50]),
 'w/content/top_download':resp(all_items[:50]),
 'w/content/search':resp(all_items),
 'w/content/view':resp(all_items[:1]),
 'w/content/download':resp(all_items[:1]),
 'w/content/ads':{'status':1,'error':0,'result':{'items':[]}},
 'w/content/hot_keyword':resp([{'keyword':a.get('name','')} for a in all_items[:30]]),
 'content/categories':resp([{'id':0,'name':'Tất cả'},{'id':1,'name':'Ứng dụng'},{'id':2,'name':'Game'}]),
 'content/get_categories':resp([{'id':0,'name':'Tất cả'},{'id':1,'name':'Ứng dụng'},{'id':2,'name':'Game'}]),
 'content/top_new':resp(all_items[:50]),
 'content/top_download':resp(all_items[:50]),
 'content/hot':resp(all_items[:50]),
 'content/featured':resp(all_items[:20]),
 'content/search':resp(all_items),
 'content/suggestion':resp(all_items[:20]),
 'content/list_suggestion':resp(all_items[:20]),
 'content/recommend':resp(all_items[:20]),
 'content/detail':resp(all_items[:1]),
 'content/download':resp(all_items[:1]),
 'content/hot_keywords':resp([{'keyword':a.get('name','')} for a in all_items[:30]]),
 'r/content/search':resp(all_items),
 'r/content/download':resp(all_items[:1]),
}
for rel,obj in endpoints.items(): write(API/rel,obj)

# Put compatibility paths at the URL root, because the IPA patch keeps the original /w/... and /content/... suffixes.
for rel in list(endpoints):
    src=API/rel; dst=ROOT/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(src.read_text(encoding='utf-8'),encoding='utf-8')

write(ROOT/'api'/'meta.json',{'status':1,'error':0,'result':{'app_count':len(all_items),'generated_by':'generate_api.py'}})
print(f'Generated {len(all_items)} apps/games and {len(endpoints)} compatibility endpoints')
