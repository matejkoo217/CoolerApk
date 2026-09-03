_A_='feed_comment_num'
_Az='hot_replies'
_Ay='hotReplyRows'
_Ax='from Web Client'
_Aw='created_at'
_Av='Keep-Alive'
_Au='X-App-Device'
_At='X-Api-Version'
_As='X-App-Code'
_Ar='X-App-Version'
_Aq='X-App-Token'
_Ap='X-Sdk-Locale'
_Ao='X-Sdk-Int'
_An='AZmV2N4UzN0UmZ3kDOzEzYgsjMwAjL2IjMwUjMuE0MRFEI7MkMxITM4AjMyAyOp1GZlJFI7kWbvFWaYByOgsDI7AyOzYGO3okVq1GWOlEez8WYLlkWKVWbllzX3pUTjFTcjx2aPVFR'
_Am='reply_items'
_Al='feed-favorite'
_Ak='feed-reply'
_Aj='feed-like'
_Ai='feed-article-message'
_Ah='message-title'
_Ag='avatar-item'
_Af='username-item'
_Ae='html.parser'
_Ad='connection'
_Ac='image.coolapk.com'
_Ab='127.0.0.1'
_Aa='/api/'
_AZ='static'
_AY='/emojis/'
_AX='emojis/'
_AW='public, max-age=31536000, immutable'
_AV='Cache-Control'
_AU='headline'
_AT='http://image.coolapk.com/feed_tag/2018/1112/11/001TCHNPzy7ksq3ly7k96-22498-o_1cs2vd92412jn1pteq4h1fap28pi-uid-408649@403x403.png'
_AS='entities'
_AR='replyRows'
_AQ='picArr'
_AP='device_title'
_AO='XMLHttpRequest'
_AN='X-Requested-With'
_AM='Accept-Encoding'
_AL='Connection'
_AK='User-Agent'
_AJ='com.coolapk.market'
_AI='original_images'
_AH='https://'
_AG='http://'
_AF='keep-alive'
_AE='timeout'
_AD='posts'
_AC='Location'
_AB='verify_title'
_AA='fans'
_A9='level'
_A8='hot_num'
_A7='commentnum'
_A6='follownum'
_A5='content_html'
_A4='favs'
_A3='summary'
_A2='coolapk.com'
_A1='POST'
_A0='api/'
_z='^(topic_|tag_)'
_y='likenum'
_x='pic'
_w='Topic'
_v='Heat'
_u='Discussions'
_t='Followers'
_s='replies'
_r='images'
_q='Content-Type'
_p='follow_num'
_o='comments'
_n='dateline'
_m='category'
_l='cover'
_k='src'
_j='Just now'
_i='https:'
_h='//'
_g='headers'
_f='#'
_e='replace'
_d='userAvatar'
_c='feed'
_b='0'
_a='img'
_Z='followers'
_Y=False
_X='/'
_W='discussions'
_V='time'
_U='device'
_T='tag'
_S='utf-8'
_R='Coolapk User'
_Q='heat'
_P='author'
_O='username'
_N='name'
_M='logo'
_L='likes'
_K='uid'
_J='description'
_I='avatar'
_H='code'
_G='title'
_F='div'
_E='message'
_D='data'
_C=True
_B=None
_A='id'
import asyncio,base64,datetime as dt,gzip,hashlib,json,logging,os,re,sqlite3,time,urllib.parse,zipfile,uuid,html
from pathlib import Path
import bcrypt,aiohttp
from aiohttp import web,ClientSession as _AiohttpClientSession,ClientTimeout,TCPConnector
from bs4 import BeautifulSoup
log=logging.getLogger('coolapk-browser')
class _PooledClientSession:
    def __init__(A,*C,**B):A._default_headers=dict(B.pop(_g,{})or{});A._default_timeout=B.pop(_AE,_B);A._ignored_args=B;A._session=_B
    async def __aenter__(A):A._session=get_global_session();return A
    async def __aexit__(A,exc_type,exc,tb):return _Y
    def _headers(A,headers=_B):
        B=headers
        if not B:return A._default_headers or _B
        C=A._default_headers.copy();C.update(B);return C
    def request(B,method,url,**A):
        if _g not in A or A[_g]is _B:
            C=B._headers()
            if C:A[_g]=C
        else:A[_g]=B._headers(A[_g])
        if A.get(_AE)is _B and B._default_timeout is not _B:A[_AE]=B._default_timeout
        return B._session.request(method,url,**A)
    def get(A,url,**B):return A.request('GET',url,**B)
    def post(A,url,**B):return A.request(_A1,url,**B)
    def put(A,url,**B):return A.request('PUT',url,**B)
    def delete(A,url,**B):return A.request('DELETE',url,**B)
ClientSession=_PooledClientSession
ROUTER_HOST=_Ab
ROUTER_PORT=int(os.environ.get('ROUTER_PORT',os.environ.get('PORT',8123)))
TARGET_BASE='https://coolapk.com'
DEFAULT_MODE='direct'
API_BASE='https://www.coolapk.com'
ALLOWED_DOMAINS=[_A2,'m.coolapk.com','www.coolapk.com',_Ac,'avatar.coolapk.com']
CHINA_ALLOWED_IPS=['119.29.29.99','119.29.29.98','119.28.28.98']
_HOP_HEADERS={_Ad,_AF,'proxy-authenticate','proxy-authorization','te','trailers','transfer-encoding','upgrade','content-length','content-encoding'}
CORS_HEADERS={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET, POST, PUT, DELETE, OPTIONS, HEAD','Access-Control-Allow-Headers':'Content-Type, Authorization, X-Requested-With'}
def is_china_domain(hostname):
    A=hostname;A=A.lower()if A else''
    for B in ALLOWED_DOMAINS:
        if A==B or A.endswith('.'+B):return _Y
    return _C
def bypass_china_lock(url_str):
    B=url_str
    if not B:return B
    D=urllib.parse.urlparse(B);C=D.hostname
    if not C:return B
    if C in(_Ab,'localhost'):return B
    if not is_china_domain(C):return B
    A=C
    if A.startswith('m.'):A=A[2:]
    elif A.startswith('www.'):A=A[4:]
    if A.startswith(_A2):A=_A2
    if C!=A:return B.replace(C,A,1)
    return B
def make_proxy_url(raw_url):
    B=raw_url
    if not B:return''
    A=str(B).strip()
    if A.startswith('/proxy?url='):return A
    if A.startswith(_h):A=_i+A
    elif A.startswith(_AG):A=_AH+A[7:]
    C=urllib.parse.quote(A,safe='');return f"/proxy?url={C}"
def coolapk_thumbnail_url(raw_url,size='s'):
    D=raw_url
    if not D:return''
    A=str(D).strip()
    if A.startswith(_h):A=_i+A
    elif A.startswith(_AG):A=_AH+A[7:]
    B=urllib.parse.urlsplit(A);E=(B.hostname or'').lower();C=B.path
    if E==_Ac and'/feed/'in C and not re.search('\\.[sm]\\.jpg$',C,re.I):C=f"{C}.{size}.jpg";return urllib.parse.urlunsplit((B.scheme or'https',B.netloc,C,B.query,B.fragment))
    return A
def make_media_url(raw_url):
    B=raw_url
    if not B:return''
    A=str(B).strip()
    if A.startswith(_h):A=_i+A
    elif A.startswith(_AG):A=_AH+A[7:]
    return make_proxy_url(A)
def rewrite_links_in_html(html,base_url=''):
    A=html
    if not A:return A
    B='(?P<attr>href|src)="(?P<url>(?:https?:)?//[^"]*?(?:coolapk\\.com)[^"]*)"'
    def C(match):
        B=match;C=B.group('attr');A=B.group('url')
        if A.startswith(_h):A=_i+A
        D=make_proxy_url(A);return f'{C}="{D}"'
    try:return re.sub(B,C,A)
    except Exception:return A
def translate_relative_time(raw_text):
    E='mo ago';D='m ago';C=raw_text;B='w ago'
    if not C:return _j
    A=str(C).strip();F=[('刚刚',_j),('昨天','Yesterday'),('前天','2 days ago'),('秒前','s ago'),('分钟前',D),('分前',D),('小时前','h ago'),('个星期前',B),('星期前',B),('周前',B),('天前','d ago'),('个月前',E),('月前',E),('年前','y ago')]
    for(G,H)in F:A=A.replace(G,H)
    return A
def format_stat_number(val,unit=''):
    D=val;B=unit
    if D is _B or D=='':return''
    C=str(D).strip()
    if'万'in C:
        E=C.replace('万','').strip()
        try:
            A=float(E)
            if A>=100:return f"{A/100:.1f}M {B}".strip()
            return f"{A*10:.0f}k {B}".strip()
        except Exception:return f"{C} {B}".strip()
    try:
        A=float(C)
        if A>=1000000:return f"{A/1000000:.1f}M {B}".strip()
        elif A>=1000:return f"{A/1000:.1f}k {B}".strip()
        elif A>0:return f"{int(A)} {B}".strip()
        else:return''
    except Exception:return f"{C} {B}".strip()
def parse_coolapk_feeds(html):
    Y=BeautifulSoup(html,_Ae);Z=Y.find_all(_F,style=lambda s:s and'background-color: #FFFFFF'in s and'border-radius: 12px'in s);K=[]
    for A in Z:
        L=A.find(_F,class_=_Af);G,C,D=_R,'',''
        if L:
            E=L.find_all('p')
            if len(E)>=1:G=E[0].get_text(strip=_C)
            if len(E)>=2:
                C=E[1].get_text(strip=_C);M=E[1].find('span')
                if M:D=M.get_text(strip=_C);C=C.replace(D,'').strip()
        C=translate_relative_time(C)
        if D:D=f"from {D.replace("来自 ","").strip()}"
        H=A.find(_F,class_=_Ag);F=H.find(_a)[_k]if H and H.find(_a)else''
        if F:F=make_proxy_url(F)
        N=A.find(_F,class_=_Ah);O=N.get_text(strip=_C)if N else'';I=A.find(_F,class_=_Ai);J=''
        if I:
            for P in I.find_all('a'):
                if'查看更多'in P.get_text():P.decompose()
            J=I.get_text(strip=_C)
        Q=A.find(_F,class_='message-image-group');R=[]
        if Q:
            for a in Q.find_all(_a):
                S=a.get(_k)
                if S:R.append(make_proxy_url(S))
        B='';T=re.search('message-image-(?:item-)?([0-9]+)',str(A))
        if T:B=T.group(1)
        if not B:
            U=re.search('/feed/([0-9]+)',str(A))
            if U:B=U.group(1)
        if not B:B=f"feed_{abs(hash(G+O+J[:30]))}"
        V=A.find(_F,class_=_Aj);W=A.find(_F,class_=_Ak);X=A.find(_F,class_=_Al);b=V.get_text(strip=_C)if V else _b;c=W.get_text(strip=_C)if W else _b;d=X.get_text(strip=_C)if X else _b;K.append({_A:B,_P:G,_I:F,_V:C,_U:D,_G:O,_A3:J,_r:R,_L:b,_s:c,_A4:d,'url':f"/feed/{B}"if B else''})
    return K
def parse_coolapk_feed_detail(html,feed_id=''):
    B=BeautifulSoup(html,_Ae);O=B.find(_F,class_=_Ah);Y=O.get_text(strip=_C)if O else'';P=B.find(_F,class_=_Af);Q,F,K='酷友','',''
    if P:
        D=P.find_all('p')
        if len(D)>=1:Q=D[0].get_text(strip=_C)
        if len(D)>=2:
            F=D[1].get_text(strip=_C);R=D[1].find('span')
            if R:K=R.get_text(strip=_C);F=F.replace(K,'').strip()
    L=B.find(_F,class_=_Ag);G=L.find(_a)[_k]if L and L.find(_a)else''
    if G:G=make_proxy_url(G)
    C=B.find(_F,class_=[_Ai,'feed-message','message-content','feed-detail-message','feed-content'])
    if not C:C=B.find(_F,class_='card-body')or B.find(_F,class_='message-detail')
    def Z(txt):
        if not txt:return _C
        for A in['粤ICP备','举报电话','jubao@coolapk.com','增值电信业务','APP备案号','网络文化','不良信息举报']:
            if A in txt:return _C
        return _Y
    S='';H=[];M=[]
    if C:
        a=C.get_text(strip=_C)
        if not Z(a):
            for E in C.find_all(_a):
                A=E.get(_k,'')
                if A:
                    if A.startswith(_h):A=_i+A
                    I=make_media_url(A);J=make_media_url(coolapk_thumbnail_url(A));H.append(J);M.append(I);E[_k]=J;E['data-full']=I
            S=str(C)
    if not H:
        for E in B.find_all(_a):
            A=E.get(_k,'')
            if A and _c in A and not _I in A:
                if A.startswith(_h):A=_i+A
                I=make_media_url(A);J=make_media_url(coolapk_thumbnail_url(A));H.append(J);M.append(I)
    T=[];N=B.find(_F,class_='hot-reply-footer')
    if N and N.parent:
        for b in N.parent.find_all(_F,class_=lambda c:c and'reply-item'in c):
            U=b.get_text(strip=_C)
            if U:T.append(U)
    V=B.find(_F,class_=_Aj);W=B.find(_F,class_=_Ak);X=B.find(_F,class_=_Al);c=V.get_text(strip=_C)if V else _b;d=W.get_text(strip=_C)if W else _b;e=X.get_text(strip=_C)if X else _b;return{_A:feed_id,_G:Y,_P:Q,_I:G,_V:F,_U:K,_A5:S,_r:H,_AI:M,_L:c,_s:d,_A4:e,_Am:T}
STD_B64='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
def _find_blob(libauth_bytes):
    G=re.findall(b'[A-Za-z0-9+/]{1000,}',libauth_bytes);A=_B;B=-1.
    for C in G:
        try:D=base64.b64decode(C,validate=_C)
        except Exception:continue
        if not D:continue
        E=bytes(A^90 for A in D);H=sum(1 for A in E if 32<=A<127);F=H/len(E)
        if F>B:B=F;A=C
    return A
def _shift_last_char_minus_5(s):A=STD_B64.index(s[-1]);return s[:-1]+STD_B64[(A-5)%64]
_cached_token=_B
_cached_token_ts=0
def get_coolapk_token():
    B=b'&';A='ascii';global _cached_token,_cached_token_ts;C=int(time.time())
    if _cached_token and C-_cached_token_ts<45:return _cached_token
    H=os.path.join(os.path.dirname(__file__),'libauth.so');I=_An;E=2608212;J=_AJ
    try:
        with open(H,'rb')as K:L=K.read()
        M=_find_blob(L);N=base64.b64decode(M);O=bytes(A^90 for A in N)
        for P in range(30):
            D=C+P;F=(D+E)%100*4+128;Q=O[F:F+128];R=base64.b64decode(Q);S=hashlib.md5(I.encode(_S)).hexdigest().encode(A);G=J.encode(_S)+B+R+B+S+B+str(D).encode(A)+B+str(E).encode(A);T=hashlib.md5(base64.b64encode(G)).hexdigest().encode(A);U=base64.b64encode(f"{D:x}/{hashlib.md5(G).hexdigest()}".encode(A)).decode(A).rstrip('=');V=_shift_last_char_minus_5(U[:22]);W=f"$2y$10${V}".encode(A)
            try:X=bcrypt.hashpw(T,W);_cached_token='v3'+base64.b64encode(X).decode(A).rstrip('=');_cached_token_ts=C;return _cached_token
            except ValueError:continue
    except Exception as Y:log.error('Failed to generate Coolapk token: %s',Y)
    return'v3'
def get_server_api_headers():A='2608212';B=get_coolapk_token();C=_An;return{_AK:'Dalvik/2.1.0 (Linux; U; Android 15; 22081212C Build/AQ3A.250226.002) (#Build; Redmi; 22081212C; AQ3A.250226.002; HyperOS_3.0; 3.0.1.0) +CoolMarket/16.6.1-2608212-universal',_AL:_Av,_AM:'gzip',_AN:_AO,_Ao:'35',_Ap:'zh-CN','X-App-Id':_AJ,_Aq:B,_Ar:'16.6.1',_As:A,_At:'16',_Au:C,'X-Dark-Mode':_b,'X-App-Channel':'coolapk','X-App-Mode':'universal','X-App-Supported':A}
IN_MEMORY_COMMENTS={}
_comment_counter=0
def format_timestamp(ts):
    if not ts:return _j
    try:
        A=int(time.time())-int(ts)
        if A<60:return _j
        elif A<3600:return f"{A//60}m ago"
        elif A<86400:return f"{A//3600}h ago"
        elif A<2592000:return f"{A//86400}d ago"
        else:return dt.datetime.fromtimestamp(int(ts)).strftime('%m-%d')
    except Exception:return _j
def get_feed_comments(feed_id):B=str(feed_id);A=IN_MEMORY_COMMENTS.get(B,[]);return[{_A:A[_A],'feed_id':B,_P:A[_P],_I:A[_I],_U:A[_U],_E:A[_E],_V:format_timestamp(A[_Aw]),_L:A.get(_L,0)}for A in A]
def add_feed_comment(feed_id,author,message,avatar='',device=''):
    global _comment_counter;A=str(feed_id)
    if A not in IN_MEMORY_COMMENTS:IN_MEMORY_COMMENTS[A]=[]
    _comment_counter+=1;B=int(time.time());C={_A:_comment_counter,'feed_id':A,_P:author or _R,_I:avatar or'',_U:device or _Ax,_E:message,_Aw:B,_L:0};IN_MEMORY_COMMENTS[A].append(C);return _comment_counter
_cached_server_topics=[]
_cached_server_topics_ts=0
_topic_id_to_name={'22498':'ProjectTreble','12253':'Magisk','17113':'Magisk模块','101468':'ColorOS17','134892':'鸿蒙7','115557':'充电头兴趣小组','126930':'数码日常'}
async def fetch_coolapk_topics_from_server(page=1):
    D=page;global _cached_server_topics,_cached_server_topics_ts,_topic_id_to_name;F=time.time()
    if D==1 and _cached_server_topics and F-_cached_server_topics_ts<300:return _cached_server_topics
    I=get_server_api_headers();J=f"https://api.coolapk.com/v6/topic/tagList?page={D}";K=ClientTimeout(total=15);C=[]
    try:
        async with ClientSession(headers=I,timeout=K)as L:
            async with L.get(J)as G:
                if G.status==200:
                    M=await G.json(content_type=_B);N=M.get(_D,[])
                    for A in N:
                        if not isinstance(A,dict):continue
                        E=str(A.get(_A)or'');B=A.get(_G)or''
                        if not B:continue
                        if E:_topic_id_to_name[E]=B
                        O=make_proxy_url(A.get(_M)or'');P=make_proxy_url(A.get(_l)or'');Q=A.get(_A6,0);H=A.get(_A7,0);R=format_stat_number(Q,_t);S=format_stat_number(H,_u);T=format_stat_number(H,_v);C.append({_A:E,_N:B,_T:f"#{B}#",_m:_w,_M:O,_l:P,_Z:R,_Q:T,_W:S,_J:A.get(_J)or f"Community discussions for #{B}#."})
                    if D==1 and C:_cached_server_topics=C;_cached_server_topics_ts=F
    except Exception as U:log.error('Error fetching topics from server: %s',U)
    return C or _cached_server_topics
def clean_coolapk_text(text):
    A=text
    if not A:return''
    A=str(A).replace('<!--break-->','')
    def B(m):
        A=m.group(1)or''
        try:B=urllib.parse.unquote(A).strip('# ')
        except Exception:B=A.strip('# ')
        return f"#{B}#"
    A=re.sub('<a[^>]*class=["\\x27]feed-link-tag["\\x27][^>]*href=["\\x27][^"\\x27]*["\\x27][^>]*>#?([^<#]+)#?</a>',B,A,flags=re.I);A=re.sub('<(?!/?a\\b)[^>]+>','',A);return A.strip()
def normalize_api_feed(item):
    A=item;I=str(A.get(_A)or'');O=A.get(_O)or _R;P=make_proxy_url(A.get(_d)or'');Q=format_timestamp(A.get(_n)or 0);B=A.get(_AP,'')
    if B:R=B.replace('来自 ','').strip();B=f"from {R}"
    C=A.get(_G)or'';S=''if C.endswith('的动态')or C.endswith('的点评')or C=='动态详情'else C;T=A.get(_E)or A.get(_J)or'';J=clean_coolapk_text(T);K=A.get(_x)or A.get(_l)or'';D=make_media_url(coolapk_thumbnail_url(K));L=A.get(_AQ)or[];E=[make_media_url(A)for A in L if A];F=[make_media_url(coolapk_thumbnail_url(A))for A in L if A]
    if D and D not in F:F.insert(0,D)
    G=make_media_url(K)
    if G and G not in E:E.insert(0,G)
    U=A.get(_Ay)or A.get(_AR)or[];M=[]
    for H in U:
        if isinstance(H,dict):
            V=H.get(_O,_R);N=clean_coolapk_text(H.get(_E,''))
            if N:M.append(f"{V}: {N}")
    W=str(A.get(_K)or'');return{_A:I,_K:W,_G:S,_P:O,_I:P,_V:Q,_U:B,_x:D,_A3:J,_A5:J,_r:F,_AI:E,_L:str(A.get(_y,0)),_s:str(A.get('replynum',0)),_A4:str(A.get('favnum',0)),'url':f"/feed/{I}",_Am:M}
def get_v2_token_headers():A=str(uuid.uuid4());B=int(time.time());C='0x'+hex(B)[2:];D=hashlib.md5(str(B).encode()).hexdigest();E=f"token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{D}${A}&com.coolapk.market";F=hashlib.md5(base64.b64encode(E.encode())).hexdigest();G=F+A+C;return{_AK:'Dalvik/2.1.0 (Linux; U; Android 10; Redmi K30 5G MIUI/V12.0.3.0.QGICMXM) (#Build; Redmi; Redmi K30 5G; QKQ1.191222.002 test-keys; 10) +CoolMarket/11.0-2101202',_AN:_AO,'X-App-Id':_AJ,_Aq:G,_Ao:'29',_Ap:'zh-CN',_Ar:'11.0',_At:'11',_As:'2101202',_Au:A,_AM:'gzip',_AL:_Av}
_global_http_session=_B
def get_global_session():
    global _global_http_session
    if _global_http_session is _B or _global_http_session.closed:A=TCPConnector(limit=300,limit_per_host=100,keepalive_timeout=120,force_close=_Y,ttl_dns_cache=300,enable_cleanup_closed=_C);B=ClientTimeout(total=12,connect=4,sock_connect=4,sock_read=10);_global_http_session=_AiohttpClientSession(connector=A,timeout=B,auto_decompress=_C)
    return _global_http_session
async def close_global_session():
    global _global_http_session;A=_global_http_session;_global_http_session=_B
    if A is not _B and not A.closed:await A.close()
_feed_detail_cache={}
def get_cached_feed(feed_id):
    A=_feed_detail_cache.get(str(feed_id))
    if A:
        B,C=A
        if time.time()-B<300:return C
def set_cached_feed(feed_id,data):_feed_detail_cache[str(feed_id)]=time.time(),data
async def fetch_coolapk_feed_full(feed_id):
    z='reply_rows';h='pics';Q='dateline_text';D=feed_id;i=get_cached_feed(D)
    if i:return i
    j=get_global_session();A0=get_v2_token_headers();A1=get_v2_token_headers();A2=f"https://api.coolapk.com/v6/feed/detail?id={D}";A3=f"https://api.coolapk.com/v6/feed/replyList?id={D}&discussMode=1&page=1";A4=j.get(A2,headers=A0);A5=j.get(A3,headers=A1)
    try:R,S=await asyncio.gather(A4,A5,return_exceptions=_C)
    except Exception as G:log.error('Failed to gather feed data for %s: %s',D,G);return
    B={}
    if not isinstance(R,Exception)and R.status==200:
        try:
            F=await R.read()
            try:F=gzip.decompress(F)
            except Exception:pass
            T=json.loads(F.decode(_S,_e));B=T.get(_D,{})
        except Exception as G:log.error('Error decoding feed detail %s: %s',D,G)
    def U(item):
        A=[];D=item.get(_AQ)
        if isinstance(D,list):
            for B in D:
                if B and isinstance(B,str)and B.strip():A.append(make_media_url(coolapk_thumbnail_url(B.strip())))
        C=item.get(_x)
        if C and isinstance(C,str)and C.strip():
            E=make_media_url(coolapk_thumbnail_url(C.strip()))
            if E not in A:A.append(E)
        return A
    def k(reply_rows):
        C=reply_rows;B=[]
        if not isinstance(C,list):return B
        for A in C:
            if not isinstance(A,dict):continue
            D=A.get(_O,_R);E=A.get('rusername','');F=A.get(_E,'');G=make_proxy_url(A.get(_d)or'');H=A.get(Q)or format_timestamp(A.get(_n)or 0);I=A.get(_y,0);J=U(A);B.append({_A:A.get(_A),_K:str(A.get(_K)or''),_P:D,'reply_to':E,'reply_to_uid':str(A.get('ruid')or''),_I:G,_E:F,_V:translate_relative_time(H),_L:I,h:J})
        return B
    l=[]
    if not isinstance(S,Exception)and S.status==200:
        try:
            F=await S.read()
            try:F=gzip.decompress(F)
            except Exception:pass
            T=json.loads(F.decode(_S,_e));m=T.get(_D,[])
            if isinstance(m,list):
                for A in m:
                    if not isinstance(A,dict):continue
                    V=A.get(_O,'酷友');H=A.get(_E,'');W=make_proxy_url(A.get(_d)or'');X=A.get(Q)or format_timestamp(A.get(_n)or 0);Y=A.get(_y,0);I=A.get(_AP,'')
                    if I and not I.startswith('来自'):I=f"来自 {I}"
                    J=U(A);Z=k(A.get(_AR,[]))
                    if H or J:l.append({_A:A.get(_A),_K:str(A.get(_K)or''),_P:V,_I:W,_E:H,_V:translate_relative_time(X),_L:Y,_U:I,h:J,z:Z})
        except Exception as G:log.error('Error decoding replies %s: %s',D,G)
    if not B:return
    A6=B.get(_O)or _R;A7=make_proxy_url(B.get(_d)or'');A8=B.get(Q)or format_timestamp(B.get(_n)or 0);A9=translate_relative_time(A8);L=B.get(_AP)or''
    if L:AA=L.replace('来自 ','').strip();L=f"from {AA}"
    M=B.get(_G)or'';AB=''if M.endswith('的动态')or M.endswith('的点评')or M=='动态详情'else M;AC=clean_coolapk_text(B.get(_E)or'');a=B.get('message_raw_output')or'';K='';N=[];b=[]
    if a and a.startswith('['):
        try:
            AD=json.loads(a);c=[]
            for O in AD:
                n=O.get('type')
                if n=='text':
                    for AE in O.get(_E,'').split('\n'):
                        o=clean_coolapk_text(AE)
                        if o.strip():c.append(f"<p style='margin-bottom:12px;font-size:15px;line-height:1.8;'>{html.escape(o)}</p>")
                elif n=='image':p=O.get('url')or'';q=make_media_url(coolapk_thumbnail_url(p));d=make_media_url(p);N.append(q);b.append(d);AF=html.escape(clean_coolapk_text(O.get(_J)or''));c.append(f"<div style='text-align:center;margin:16px 0;'><img src='{q}' data-full='{d}' style='max-width:100%;border-radius:10px;cursor:zoom-in;' onclick='openLightbox(\"{d}\", event)'><p style='font-size:12px;color:#888;margin-top:6px;'>{AF}</p></div>")
            K=''.join(c)
        except Exception as AG:log.debug('Failed to parse message_raw_output JSON: %s',AG)
    r=B.get(_x)or B.get(_l)or'';C=make_media_url(coolapk_thumbnail_url(r));E=make_media_url(r)
    if C and K:AH=f"<div class='article-title-cover' style='margin:0 0 20px 0;text-align:center;'><img src='{C}' data-full='{E}' style='max-width:100%;border-radius:12px;cursor:zoom-in;box-shadow:var(--shadow-sm);' onclick='openLightbox(\"{E}\", event)'></div>";K=AH+K
    s=B.get(_AQ)or[];e=[make_media_url(coolapk_thumbnail_url(A))for A in s if A];f=[make_media_url(A)for A in s if A]
    if C and C not in e:e.insert(0,C)
    if E and E not in f:f.insert(0,E)
    if N:t=([C]if C and C not in N else[])+N;u=([E]if E and E not in b else[])+b
    else:t=e;u=f
    g=[]
    for A in B.get(_Ay)or[]:
        V=A.get(_O,_R);H=clean_coolapk_text(A.get(_E,''));W=make_proxy_url(A.get(_d)or'');AI=A.get(Q)or format_timestamp(A.get(_n)or 0);X=translate_relative_time(AI);Y=A.get(_y,0);J=U(A);Z=k(A.get(_AR,[]))
        if H or J:g.append({_A:A.get(_A),_K:str(A.get(_K)or''),_P:V,_I:W,_E:H,_V:X,_L:Y,h:J,z:Z})
    v=set();w=[]
    for x in g+l:
        P=x.get(_A)
        if P and P in v:continue
        if P:v.add(P)
        w.append(x)
    y={_A:str(B.get(_A)or D),_K:str(B.get(_K)or''),_P:A6,_I:A7,_V:A9,_U:L,_G:AB,_x:C,_A3:AC,_A5:K,_r:t,_AI:u,_L:str(B.get(_y,0)),_s:str(B.get('replynum',0)),_A4:str(B.get('favnum',0)),_Az:g,_o:w};set_cached_feed(D,y);return y
async def fetch_coolapk_topic_feeds(tag_id_or_name,tag_title=_B,page=1,subtab='all'):
    J='featured';I='hot';F=subtab;C=page;K=get_server_api_headers();A=re.sub(_z,'',str(tag_id_or_name).replace(_f,'').strip(),flags=re.I).strip()
    if A.isdigit()and A in _topic_id_to_name:A=_topic_id_to_name[A]
    L=A.isdigit();B=tag_title or A;D=''
    if F in('latest','lastupdate',_n):D='&sort=lastupdate'
    elif F in(_Q,I,J):D='&sort=hot'
    if L:H=[*([f"https://api.coolapk.com/v6/search?type=feed&searchValue={urllib.parse.quote(B)}&page={C}{D}"]if B else[]),f"https://api.coolapk.com/v6/product/feedList?id={A}&type=feed&page={C}"]
    else:H=[*([f"https://api.coolapk.com/v6/search?type=feed&searchValue={urllib.parse.quote(B)}&page={C}{D}"]if B else[]),f"https://api.coolapk.com/v6/page/dataList?url=/topic/tagFeedList?tag={urllib.parse.quote(B)}&page={C}"]
    M=ClientTimeout(total=15);N=get_global_session()
    async def O(url):
        try:
            async with N.get(url,headers=K,timeout=M)as B:
                if B.status!=200:return[]
                C=await B.json(content_type=_B);A=C.get(_D,[]);D=list(A.values())if isinstance(A,dict)else A if isinstance(A,list)else[];return[normalize_api_feed(A)for A in D if isinstance(A,dict)and(A.get(_A)or A.get(_E))]
        except Exception as E:log.debug('Topic feed source failed for %s: %s',url,E);return[]
    P=await asyncio.gather(*(O(A)for A in H),return_exceptions=_C);E=[]
    for G in P:
        if isinstance(G,Exception):continue
        if G:E=G;break
    if F in(_Q,I,J)and E:
        try:E.sort(key=lambda x:int(x.get(_L)or 0)*2+int(x.get(_s)or 0),reverse=_C)
        except Exception:pass
    return E
async def search_coolapk_topics(query,page=1):
    H=get_server_api_headers();I=ClientTimeout(total=10);B=[];C=re.sub(_z,'',str(query).replace(_f,'').strip(),flags=re.I).strip()
    if not C:return[]
    J=f"https://api.coolapk.com/v6/search?type=tag&searchValue={urllib.parse.quote(C)}&page={page}"
    try:
        async with ClientSession(headers=H,timeout=I)as K:
            async with K.get(J)as F:
                if F.status==200:
                    L=await F.json(content_type=_B);M=L.get(_D,[])
                    for N in M:
                        for A in N.get(_AS,[]):
                            D=A.get(_G)
                            if not D:continue
                            O=str(A.get(_A)or C);G=A.get(_M)or'';P=A.get(_A6)or A.get(_p);Q=A.get(_A7)or A.get(_A_);R=A.get(_A8)or A.get(_Q);B.append({_A:O,_N:D,_T:f"#{D}#",_M:make_proxy_url(G)if G else make_proxy_url(_AT),_Z:format_stat_number(P,_t),_W:format_stat_number(Q,_u),_Q:format_stat_number(R,_v),_J:A.get(_J)or f"Topic community hub for #{D}#."})
    except Exception as A:log.error('Error searching topics: %s',A)
    if not B:
        S=await fetch_coolapk_topics_from_server(page=1)
        for E in S:
            if C.lower()in E[_N].lower()and not any(A[_A]==E[_A]for A in B):B.append(E)
    return B
async def fetch_coolapk_topic_detail(topic_key):
    A=re.sub(_z,'',str(topic_key).replace(_f,'').strip(),flags=re.I).strip()
    if not A:return
    if A.isdigit()and A in _topic_id_to_name:A=_topic_id_to_name[A]
    Q=await fetch_coolapk_topics_from_server(page=1);M=next((B for B in Q if B[_A]==A or B[_N].lower()==A.lower()or B.get(_T,'').replace(_f,'').lower()==A.lower()),_B)
    if M:return M
    N=get_server_api_headers();O=ClientTimeout(total=10)
    if A.isdigit():
        try:
            async with ClientSession(headers=N,timeout=O)as F:
                async with F.get(f"https://api.coolapk.com/v6/product/detail?id={A}")as C:
                    if C.status==200:
                        G=await C.json(content_type=_B);D=G.get(_D)
                        if D and D.get(_G):I=D.get(_G);R=D.get('follow_num_txt')or str(D.get(_p)or'');S=D.get('feed_comment_num_txt')or str(D.get(_A_)or'');T=D.get('hot_num_txt')or str(D.get(_A8)or'');return{_A:A,_N:I,_T:f"#{I}#",_m:'Device Hub',_M:make_proxy_url(D.get(_M)or''),_Z:format_stat_number(R,_t),_W:format_stat_number(S,_u),_Q:format_stat_number(T,_v),_J:D.get(_J)or f"{I} discussions and device hub."}
                for U in range(2,6):
                    async with F.get(f"https://api.coolapk.com/v6/topic/tagList?page={U}")as C:
                        if C.status==200:
                            V=await C.json(content_type=_B)
                            for P in V.get(_D,[]):
                                J=str(P.get(_A)or'');K=P.get(_G)or''
                                if J and K:_topic_id_to_name[J]=K
                                if J==A:A=K;break
                        if not A.isdigit():break
                async with F.get(f"https://api.coolapk.com/v6/topic/tagDetail?id={A}")as C:
                    if C.status==200:
                        G=await C.json(content_type=_B);B=G.get(_D)
                        if B and B.get(_G):E=B.get(_G);return{_A:A,_N:E,_T:f"#{E}#",_m:_w,_M:make_proxy_url(B.get(_M)or''),_Z:format_stat_number(B.get(_A6),_t),_W:format_stat_number(B.get(_A7),_u),_Q:format_stat_number(B.get(_A8),_v),_J:B.get(_J)or f"Discussion hub for #{E}#."}
        except Exception as H:log.debug('Numeric topic lookup error: %s',H)
    try:
        async with ClientSession(headers=N,timeout=O)as F:
            async with F.get(f"https://api.coolapk.com/v6/topic/tagDetail?tag={urllib.parse.quote(A)}")as C:
                if C.status==200:
                    G=await C.json(content_type=_B);B=G.get(_D)
                    if B and B.get(_G):E=B.get(_G);return{_A:str(B.get(_A)or A),_N:E,_T:f"#{E}#",_m:_w,_M:make_proxy_url(B.get(_M)or''),_Z:format_stat_number(B.get(_A6),_t),_W:format_stat_number(B.get(_A7),_u),_Q:format_stat_number(B.get(_A8),_v),_J:B.get(_J)or f"Discussion hub for #{E}#."}
    except Exception as H:log.debug('Tag detail lookup error: %s',H)
    try:
        L=await search_coolapk_topics(A,page=1)
        if L:W=next((B for B in L if B[_N].lower()==A.lower()),L[0]);return W
    except Exception as H:log.debug('Topic search fallback error: %s',H)
    return{_A:A,_N:A,_T:f"#{A}#",_m:_w,_M:make_proxy_url(_AT),_Z:'',_W:'',_Q:'',_J:f"Community discussions for #{A}#."}
async def fetch_coolapk_search_feeds(query,page=1):
    D=get_server_api_headers();E=f"https://api.coolapk.com/v6/search?type=feed&searchValue={urllib.parse.quote(query)}&page={page}";F=ClientTimeout(total=15);B=[]
    try:
        async with ClientSession(headers=D,timeout=F)as G:
            async with G.get(E)as C:
                if C.status==200:
                    H=await C.json(content_type=_B)
                    for A in H.get(_D,[]):
                        if isinstance(A,dict)and(A.get(_A)or A.get(_E)):B.append(normalize_api_feed(A))
    except Exception as I:log.error('Error searching feeds: %s',I)
    return B
async def fetch_coolapk_search_users(query,page=1):
    D=get_server_api_headers();E=re.sub('^@','',str(query).strip());F=f"https://api.coolapk.com/v6/search?type=user&searchValue={urllib.parse.quote(E)}&page={page}";G=ClientTimeout(total=10);B=[]
    try:
        H=get_global_session()
        async with H.get(F,headers=D,timeout=G)as C:
            if C.status==200:
                I=await C.json(content_type=_B)
                for A in I.get(_D,[]):
                    if isinstance(A,dict)and(A.get(_K)or A.get(_O)):J=str(A.get(_K)or'').strip();K=A.get(_O)or A.get('displayUsername')or _R;L=A.get(_d)or A.get('userBigAvatar')or A.get('userSmallAvatar')or'';M=make_proxy_url(L);N=A.get('bio')or'';O=A.get(_A9)or 0;P=format_stat_number(A.get(_AA,0));Q=A.get(_AB)or'';B.append({_K:J,_O:K,_I:M,'bio':N,_A9:O,_Z:P,_AB:Q})
    except Exception as R:log.error('Error searching users: %s',R)
    return B
async def fetch_coolapk_main_feeds(source=_AU,page=1):
    P='feed_article';O='article';N='entityType';M='officialEvaluation';L='editorChoice';C=page;B=source;Q=get_server_api_headers();J=ClientTimeout(total=15);D=[]
    if B in(_AU,L):E=f"https://api.coolapk.com/v6/main/headline?page={C}"
    elif B in('feeds','latest','ranking'):E=f"https://api.coolapk.com/v6/page/dataList?url=V9_HOME_TAB_RANKING&page={C}"
    elif B in('reviews',M,'news'):E=f"https://api.coolapk.com/v6/page/dataList?url=V11_HOME_TAB_NEWS&page={C}"
    else:E=f"https://api.coolapk.com/v6/main/headline?page={C}"
    try:
        async with ClientSession(headers=Q,timeout=J)as H:
            async with H.get(E)as F:
                if F.status==200:
                    R=await F.json(content_type=_B);S=R.get(_D,[])
                    for A in S:
                        if not isinstance(A,dict):continue
                        if A.get(N)in(_c,O,P)or A.get(_A)and A.get(_O):D.append(normalize_api_feed(A))
                        elif A.get(_AS):
                            for G in A[_AS]:
                                if isinstance(G,dict)and(G.get(N)in(_c,O,P)or G.get(_A)and G.get(_O)):D.append(normalize_api_feed(G))
    except Exception as I:log.error('Failed to fetch live API feeds from %s: %s',E,I)
    if not D and B in(L,M):
        try:
            K=f"https://coolapk.com/{B}?page={C}";T=get_apk_request_headers(K)
            async with ClientSession(headers=T,timeout=J)as H:
                async with H.get(K)as F:
                    if F.status==200:U=await F.text(encoding=_S,errors=_e);D=parse_coolapk_feeds(U)
        except Exception as I:log.error('Fallback scrape error: %s',I)
    return D
def get_apk_request_headers(target_url,client_headers=_B):
    G='https://coolapk.com/';F='Referer';E=client_headers;D=target_url;A=urllib.parse.urlparse(D);H=any(A in D.lower()for A in('.jpg','.jpeg','.png','.webp','.gif'))or A.hostname and('image.'in A.hostname or'avatar.'in A.hostname);I='image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'if H else'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8';J={_AK:'Mozilla/5.0 (Linux; Android 10; KJAQIBuild/KJAQI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 coolapk-market/v8.5.0','Accept':I,'Accept-Language':'zh-CN,zh;q=0.9',_AM:'gzip, deflate, br',F:G,_AL:_AF,'Host':A.hostname or _A2};B=J.copy()
    if E:
        for(K,L)in E.items():
            C=K.lower()
            if C in('user-agent','host','referer'):continue
            if C not in{_Ad,_AF,'proxy-connection'}:B[C]=L
    B[F]=G;return B
_active_api_requests=0
_image_semaphore=asyncio.Semaphore(int(os.environ.get('IMAGE_CONCURRENCY','8')))
_IMAGE_CACHE={}
_IMAGE_CACHE_MAX_BYTES=67108864
_image_cache_current_bytes=0
_image_inflight={}
def _remember_image(target_url,body,content_type):
    B=target_url;A=body;global _image_cache_current_bytes
    if len(A)>2097152:return
    if _image_cache_current_bytes+len(A)>_IMAGE_CACHE_MAX_BYTES:
        D=list(_IMAGE_CACHE.keys())[:len(_IMAGE_CACHE)//3+1]
        for E in D:F,G=_IMAGE_CACHE.pop(E,(b'',''));_image_cache_current_bytes=max(0,_image_cache_current_bytes-len(F))
    C=_IMAGE_CACHE.get(B)
    if C:_image_cache_current_bytes-=len(C[0])
    _IMAGE_CACHE[B]=A,content_type;_image_cache_current_bytes+=len(A)
class PrioritizeAPI:
    async def __aenter__(A):global _active_api_requests;_active_api_requests+=1;return A
    async def __aexit__(A,exc_type,exc,tb):global _active_api_requests;_active_api_requests=max(0,_active_api_requests-1);return _Y
async def _proxy_image(request,target_url,headers):
    O='X-Image-Cache';H=request;G='Content-Length';B=target_url;I='W/"'+hashlib.sha256(B.encode(_S)).hexdigest()+'"';E={**CORS_HEADERS,_AV:_AW,'ETag':I,'X-Image-Proxy':'memory-stream'}
    if H.headers.get('If-None-Match')==I:return web.Response(status=304,headers=E)
    global _IMAGE_CACHE,_image_cache_current_bytes
    if B in _IMAGE_CACHE:C,F=_IMAGE_CACHE[B];return web.Response(body=C,status=200,headers={**E,_q:F,G:str(len(C)),O:'HIT'})
    P=get_global_session();Q=ClientTimeout(total=30,connect=6,sock_connect=6,sock_read=25)
    try:
        async with _image_semaphore:
            async with P.get(B,headers=headers,allow_redirects=_Y,timeout=Q)as A:
                if A.status in(301,302,303,307,308):
                    J=A.headers.get(_AC,'')
                    if J:return web.Response(status=A.status,headers={**E,_AC:make_proxy_url(bypass_china_lock(urllib.parse.urljoin(B,J)))})
                    return web.Response(status=A.status,headers=E)
                F=A.headers.get(_q,'image/jpeg')
                if A.status!=200:C=await A.read();return web.Response(status=A.status,body=C,headers={**CORS_HEADERS,_q:F})
                K=A.headers.get(G);L={**E,_q:F,O:'MISS'}
                if K:L[G]=K
                D=web.StreamResponse(status=200,headers=L);await D.prepare(H);M=[]
                try:
                    async for N in A.content.iter_chunked(65536):await D.write(N);M.append(N)
                    await D.write_eof()
                except(ConnectionResetError,asyncio.CancelledError):raise
                except Exception as R:
                    log.debug('Image streaming interrupted for %s: %s',B,R)
                    try:await D.write_eof()
                    except Exception:pass
                    return D
                C=b''.join(M);_remember_image(B,C,F);return D
    except(asyncio.CancelledError,ConnectionResetError):raise
    except Exception as S:log.debug('Image upstream fetch failed for %s: %s',B,S);return web.Response(status=502,text='Image proxy failed',headers=CORS_HEADERS)
async def proxy_request(request,target_url):
    N='text/html';C=request;A=target_url;O=any(B in A.lower()for B in('.jpg','.jpeg','.png','.webp','.gif','.svg','.ico','.bmp'))or'image'in A.lower()or _I in A.lower();A=bypass_china_lock(A);F=get_apk_request_headers(A,C.headers)
    if O and C.method=='GET':return await _proxy_image(C,A,F)
    P=ClientTimeout(total=30,connect=6,sock_connect=6,sock_read=25);Q=get_global_session()
    try:
        G=C.method;R=await C.read()if G in(_A1,'PUT','PATCH')else _B
        async with Q.request(G,A,data=R,headers=F,allow_redirects=_Y,timeout=P)as B:
            H=await B.read();D=B.headers.get(_q,N);E=CORS_HEADERS.copy()
            if D:E[_q]=D
            if B.status in(301,302,303,307,308):
                I=B.headers.get(_AC,'')
                if I:E[_AC]=make_proxy_url(bypass_china_lock(urllib.parse.urljoin(A,I)))
            J=web.Response(status=B.status,body=H,headers=E)
            if B.status==200 and N in D:
                try:
                    K=H.decode(_S,errors=_e);L=rewrite_links_in_html(K,A)
                    if L!=K:J.text=L
                except Exception:pass
            return J
    except Exception as M:log.error('Proxy request failed for %s: %s',A,M);return web.Response(status=502,text=f"Proxy error: {M}",headers=CORS_HEADERS)
async def fetch_coolapk_user_space(user_key,page=1):
    R='fans_num';O=user_key;F='be_like_num';E='follow';D='feed_count';G=get_server_api_headers();C=str(O).replace('@','').strip()
    if not C:return
    B=C;H=get_global_session()
    if not B.isdigit():
        S=f"https://api.coolapk.com/v6/search?type=user&searchValue={urllib.parse.quote(C)}"
        try:
            async with H.get(S,headers=G)as P:
                if P.status==200:
                    T=await P.read();U=json.loads(T.decode(_S,_e));I=U.get(_D,[])
                    if isinstance(I,list)and len(I)>0:B=str(I[0].get(_K)or'')
        except Exception as J:log.debug('Failed searching user by name %s: %s',C,J)
    if not B or not B.isdigit():return
    V=f"https://api.coolapk.com/v6/user/space?uid={B}";W=f"https://api.coolapk.com/v6/user/feedList?uid={B}&page={page}"
    try:
        X=H.get(V,headers=G);Y=H.get(W,headers=G);K,L=await asyncio.gather(X,Y,return_exceptions=_C);A={}
        if not isinstance(K,Exception)and K.status==200:Z=await K.read();A=json.loads(Z.decode(_S,_e)).get(_D,{})
        M=[]
        if not isinstance(L,Exception)and L.status==200:a=await L.read();M=json.loads(a.decode(_S,_e)).get(_D,[])
        b={_K:str(A.get(_K)or B),_O:A.get(_O,C),_I:make_proxy_url(A.get(_d)or''),_l:make_proxy_url(A.get(_l)or A.get('userBackground')or A.get('background')or''),_A9:int(A.get(_A9)or 0),'bio':A.get('bio')or A.get('subTitle')or _R,'feeds_count':int(A.get(_c)or A.get(D)or 0),D:int(A.get(_c)or A.get(D)or 0),_c:int(A.get(_c)or A.get(D)or 0),'following_count':int(A.get(E)or A.get(_p)or 0),_p:int(A.get(E)or A.get(_p)or 0),E:int(A.get(E)or A.get(_p)or 0),'followers_count':int(A.get(_AA)or A.get(R)or 0),_AA:int(A.get(_AA)or A.get(R)or 0),'likes_count':int(A.get(F)or A.get(_L)or 0),_L:int(A.get(F)or A.get(_L)or 0),F:int(A.get(F)or A.get(_L)or 0),_AB:A.get(_AB,'')};Q=[]
        if isinstance(M,list):
            for N in M:
                if isinstance(N,dict)and N.get(_A):Q.append(normalize_api_feed(N))
        return{_H:0,'user':b,_AD:Q}
    except Exception as J:log.error('Failed to fetch user space for %s: %s',O,J);return
async def fetch_coolapk_devices(page=1,query='',timeout_seconds=20):
    J='product_id';B=page;B=str(B);E=f"https://m.coolapk.com/mp/productSelector/configSearch?page={B}";C=get_apk_request_headers(E);C[_AN]=_AO;C['Accept']='application/json, text/javascript, */*; q=0.01';K=ClientTimeout(total=timeout_seconds);D=str(query).strip().lower();L=get_global_session()
    try:
        async with L.post(E,data=f"page={B}".encode(),headers=C,timeout=K)as F:
            if F.status!=200:return
            M=await F.json(content_type=_B)
    except Exception as N:log.debug('Device fetch failed: %s',N);return
    O=M.get('phoneList',[]);G=[]
    for A in O:
        if not isinstance(A,dict):continue
        H=A.get('product_title','')or'';I=A.get('product_specs',[])or[]
        if D and not(D in H.lower()or any(D in str(A).lower()for A in I)):continue
        P=make_proxy_url(A.get(_M,''))if A.get(_M)else'';G.append({_A:A.get(_A),J:A.get(J),_G:H,'version':A.get(_G,''),_M:P,'specs':I,'is_new':A.get('is_new_product',_Y)})
    return G
async def _handle_api_request(request,path):
    r='emojis';q='devices';p='query';o='total';n='source';Z='topics';Y='q';N='1';H='page';C=request;A=path
    async with PrioritizeAPI():
        if A in('api/feeds','/api/feeds'):
            a=C.query.get(n,_AU);B=C.query.get(H,N);D=int(B)if B.isdigit()else 1
            try:b=await fetch_coolapk_main_feeds(source=a,page=D);return web.json_response({_H:0,n:a,H:D,o:len(b),_D:b},headers=CORS_HEADERS)
            except Exception as I:log.error('Failed to fetch feeds: %s',I);return web.json_response({_H:500,_E:str(I),_D:[]},headers=CORS_HEADERS)
        if A.startswith('api/feed/')or A.startswith('/api/feed/'):
            J=[A for A in A.rstrip(_X).split(_X)if A and A!='api']
            if len(J)>=2:
                K=J[1]
                if C.method==_A1:
                    try:
                        Q=await C.json();s=Q.get(_P,_R);c=Q.get(_E,'').strip();t=Q.get(_I,'');u=Q.get(_U,_Ax)
                        if not c:return web.json_response({_H:400,_E:'Comment message cannot be empty'},headers=CORS_HEADERS)
                        v=add_feed_comment(K,s,c,t,u);w=get_feed_comments(K);return web.json_response({_H:0,_A:v,_D:w},headers=CORS_HEADERS)
                    except Exception as I:return web.json_response({_H:500,_E:str(I)},headers=CORS_HEADERS)
                if len(J)>=3 and J[2]==_o:L=await fetch_coolapk_feed_full(K);V=get_feed_comments(K);d=L.get(_o,[])if L else[];x=V+d;return web.json_response({_H:0,_D:x,'native_count':len(d)},headers=CORS_HEADERS)
                L=await fetch_coolapk_feed_full(K)
                if not L:L={_A:K,_G:'Post Details',_P:_R,_I:'',_V:_j,_U:'',_A3:'',_A5:'',_r:[],_Az:[],_o:[]}
                V=get_feed_comments(K);e=dict(L);e[_o]=V+L.get(_o,[]);return web.json_response({_H:0,_D:e},headers=CORS_HEADERS)
        if A in('api/topics','/api/topics','api/groups','/api/groups'):
            E=C.query.get(Y,'').strip().lower();B=C.query.get(H,N);D=int(B)if B.isdigit()else 1;W=await fetch_coolapk_topics_from_server(page=D);R=[]
            for G in W:
                if E:
                    X=E.replace(_f,'').strip()
                    if X not in G[_N].lower()and X not in G.get(_T,'').lower()and X not in G.get(_J,'').lower():continue
                R.append(G)
            return web.json_response({_H:0,o:len(R),_D:R,Z:R},headers=CORS_HEADERS)
        if A in('api/hot_searches','/api/hot_searches'):
            W=await fetch_coolapk_topics_from_server(page=1);f=[]
            for G in W[:10]:f.append({'text':G[_N],'sub':(G.get(_J)or'热门讨论')[:24],_Q:G.get(_Q,'')})
            return web.json_response({_H:0,_D:f},headers=CORS_HEADERS)
        if A.startswith(('api/topic/','/api/topic/','api/group/','/api/group/')):
            y=urllib.parse.unquote(A.rstrip(_X).split(_X)[-1]).strip();M=re.sub(_z,'',y.replace(_f,'').strip(),flags=re.I).strip();B=C.query.get(H,N);D=int(B)if B.isdigit()else 1;z=C.query.get('subtab')or C.query.get('sort','all');F=await fetch_coolapk_topic_detail(M)
            if not F:F={_A:M,_N:M,_T:f"#{M}#",_m:_w,_M:make_proxy_url(_AT),_Z:'',_W:'',_Q:'',_J:f"Community discussions for #{M}#."}
            A0=F.get(_A)or M;S=await fetch_coolapk_topic_feeds(A0,tag_title=F.get(_N),page=D,subtab=z)
            if not F.get(_W)and S:F[_W]=f"{len(S)}+ Discussions"
            return web.json_response({_H:0,'topic':F,'group':F,_T:F.get(_T,f"#{F.get(_N,M)}#"),'total_posts':len(S),_AD:S},headers=CORS_HEADERS)
        if A in('api/devices','/api/devices'):
            B=C.query.get(H,N);D=int(B)if B.isdigit()else 1
            try:
                g=await fetch_coolapk_devices(page=D,timeout_seconds=20)
                if g is _B:return web.json_response({_H:502,_E:'Upstream error',_D:[]},headers=CORS_HEADERS)
                return web.json_response({_H:0,H:D,_D:g},headers=CORS_HEADERS)
            except Exception as I:log.error('Failed to fetch devices: %s',I);return web.json_response({_H:500,_E:str(I),_D:[]},headers=CORS_HEADERS)
        if A in('api/search','/api/search'):
            E=C.query.get(Y,'').strip()
            if not E and C.method==_A1:
                try:h=await C.json();E=(h.get(p,'')or h.get(Y,'')).strip()
                except Exception:pass
            if not E:return web.json_response({_H:0,Z:[],q:[],_AD:[],_D:[]},headers=CORS_HEADERS)
            A1=E.lower();i=re.sub(_z,'',A1.replace(_f,'').strip(),flags=re.I).strip();B=C.query.get(H,N);D=int(B)if B.isdigit()else 1;A2=asyncio.create_task(search_coolapk_topics(i,page=1));A3=asyncio.create_task(fetch_coolapk_devices(page=1,query=i,timeout_seconds=10));A4=asyncio.create_task(fetch_coolapk_search_feeds(E,page=D));A5=asyncio.create_task(fetch_coolapk_search_users(E,page=D));O,T,P,U=await asyncio.gather(A2,A3,A4,A5,return_exceptions=_C)
            if isinstance(O,Exception):log.debug('Topic search failed: %s',O);O=[]
            if isinstance(T,Exception)or T is _B:T=[]
            if isinstance(P,Exception):log.debug('Post search failed: %s',P);P=[]
            if isinstance(U,Exception):log.debug('User search failed: %s',U);U=[]
            return web.json_response({_H:0,p:E,'users':U,Z:O,'groups':O,q:T,_AD:P,_D:P},headers=CORS_HEADERS)
        if A.startswith(('api/user/','/api/user/')):
            J=A.lstrip(_X).split(_X)
            if len(J)>=3:
                A6=J[2];B=C.query.get(H,N);D=int(B)if B.isdigit()else 1;j=await fetch_coolapk_user_space(A6,page=D)
                if j:return web.json_response(j,headers=CORS_HEADERS)
                return web.json_response({_H:404,_E:'User not found'},headers=CORS_HEADERS)
        if A.startswith(('static/emojis/','/static/emojis/',_AX,_AY)):
            A7=os.path.basename(A);k=os.path.join(os.path.dirname(__file__),_AZ,r,A7)
            if os.path.isfile(k):l=CORS_HEADERS.copy();l[_AV]=_AW;return web.FileResponse(k,headers=l)
            return web.Response(status=404,text='Emoji not found',headers=CORS_HEADERS)
        if A in('api/emojis','/api/emojis'):
            m=os.path.join(os.path.dirname(__file__),_AZ,r,'emojis.json')
            if os.path.isfile(m):
                with open(m,'r',encoding=_S)as A8:A9=json.load(A8)
                return web.json_response({_H:0,_D:A9},headers=CORS_HEADERS)
        if A.startswith(_A0)or A.startswith(_Aa):AA=A[len(_A0):]if A.startswith(_A0)else A[len(_Aa):];AB=f"{API_BASE}/v2/{AA}";return await proxy_request(C,AB)
        return web.Response(status=404,text='API not found',headers=CORS_HEADERS)
async def browser_handler(request):
    N='proxy';M='/_proxy';L='_proxy';E='mode';B=request;A=B.match_info.get('path','')
    if B.method=='OPTIONS':return web.Response(status=204,headers=CORS_HEADERS)
    if A in('_mode','/_mode'):return web.json_response({E:DEFAULT_MODE},headers=CORS_HEADERS)
    if A in('_bypass','/_bypass'):
        try:O=await B.json();P=O.get(E,'direct');return web.json_response({'bypass_mode':P},headers=CORS_HEADERS)
        except Exception:return web.Response(status=400,text='Invalid JSON',headers=CORS_HEADERS)
    if A in('_status','/_status'):return web.json_response({E:DEFAULT_MODE,'target':TARGET_BASE,'allowed_domains':ALLOWED_DOMAINS,'bypass_active':_C,'port':ROUTER_PORT,'status':'online'},headers=CORS_HEADERS)
    if A in(L,M,N,'/proxy')or A.startswith((L,M,N)):
        F=B.query_string;D=''
        if F:
            for G in F.split('&'):
                if G.startswith('url='):D=G[4:];break
        if not D:return web.Response(status=400,text='Missing url parameter',headers=CORS_HEADERS)
        try:C=urllib.parse.unquote(D)
        except Exception:return web.Response(status=400,text='Invalid URL parameter',headers=CORS_HEADERS)
        C=bypass_china_lock(C);return await proxy_request(B,C)
    if A.startswith(('static/','/static/',_AX,_AY)):
        if A.startswith((_AX,_AY)):H=os.path.join(_AZ,A.lstrip(_X))
        else:H=A.lstrip(_X)
        I=os.path.join(os.path.dirname(__file__),H)
        if os.path.isfile(I):J=CORS_HEADERS.copy();J[_AV]=_AW;return web.FileResponse(I,headers=J)
        return web.Response(status=404,text='Static file not found',headers=CORS_HEADERS)
    if A.startswith((_A0,_Aa)):return await _handle_api_request(B,A)
    if A==''or A==_X or A.startswith(('feed/','/feed/'))and not A.startswith(_A0):
        K=os.path.join(os.path.dirname(__file__),'index.html')
        if os.path.isfile(K):return web.FileResponse(K,headers=CORS_HEADERS)
        return web.Response(status=404,text='index.html not found',headers=CORS_HEADERS)
    C=f"{TARGET_BASE}/{A}"
    if B.query_string:C+='?'+B.query_string
    C=bypass_china_lock(C);return await proxy_request(B,C)
async def main():
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(message)s');B=web.Application();B.router.add_route('*','/{path:.*}',browser_handler);A=web.AppRunner(B);await A.setup();C=web.TCPSite(A,ROUTER_HOST,ROUTER_PORT);await C.start();log.info('Coolapk PC Browser running on http://%s:%s',ROUTER_HOST,ROUTER_PORT);log.info('Target: %s',TARGET_BASE);log.info('China lock bypass: Active (matching APK network_security_config)')
    try:await asyncio.Event().wait()
    except asyncio.CancelledError:pass
    finally:await A.cleanup();await close_global_session()
if __name__=='__main__':asyncio.run(main())
