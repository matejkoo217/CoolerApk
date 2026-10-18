# Comments (回复) were empty everywhere — root cause + fix

_2026-10-18, CoolerApk reader (MCS instance `dcb9f65db9f64cc8ab603df0de8e8019`, port 8125, repo `matejkoo217/CoolerApk`)._

## Symptom
Every feed showed `comments: []` / `hot_replies: []`, so the comment pane was blank — on posts with
13+ replies. The reader's own SPA was fine; the *data* never arrived.

## How it was diagnosed
`server.py::fetch_coolapk_feed_full()` fans out to **two** upstream calls with the *legacy* signature
(`get_v2_token_headers()` → UA `CoolMarket/11.0-2101202` + the md5-chain token):

```
/v6/feed/detail?id=<id>                       -> HTTP 200, full post   (works)
/v6/feed/replyList?id=<id>&discussMode=1...   -> HTTP 200, body: {"status":403,"message":"评论接口异常，请尝试升级到新版酷安"}
```

Reproduced outside the reader (token algorithm ported verbatim) and on a **control feed** (73572775,
which returned 9 comments in September) — so the reply endpoint is refused platform-wide for the old
client signature, not per post.

The reader already ships a **correct modern signature** — `get_server_api_headers()` →
`get_coolapk_token()` → bcrypt **v3** token derived from `libauth.so`, UA `CoolMarket/16.6.1-2608212-universal`
— and it uses it for search / topics / user space… but **not** for feed detail or replies. That was the gap.

Anonymous v3 attempts hit Coolapk's anti-abuse layer, which is the remaining blocker:

| attempt | result |
|---|---|
| v3 token + reader's shared device fingerprint | `评论接口异常` (replyList), `-415 检测到当前设备下最近登录账号过多` (detail) |
| v3 token + fresh random device | `err_request_captcha_v2` (当前访问需要验证码) |
| v3 token with current build number (16.6.4 / 2609291) | same as above — version was not the gate |
| web HTML `www.coolapk.com/feed/<id>` | HTTP 567 (region/bot blocked) |

`apk/detail` with the v3 token **does** work (that's how the current version `16.6.4 / 2609291` was read),
which proves the v3 signature itself is valid.

## What changed
`server.py` (all in the reply path; feed detail deliberately left on the signature it already works with):

1. `get_coolapk_token(_device=None)` — optional device override (defaults to the existing `_An`).
2. `get_reply_auth()` — reads optional `auth.json` next to `server.py` (untracked, survives
   `git reset --hard origin/main`):
   ```json
   {"device": "<fingerprint>", "login_token": "<account token>", "uid": "<uid>"}
   ```
3. `fetch_feed_replies()` — tries the **v3** signature first, then legacy **v2**, honours `auth.json`
   (`device` replaces the shared fingerprint; `login_token`/`uid` are appended as query params), and
   records the refusal reason in `_REPLY_REASON`.
4. The feed payload now carries **`comments_error`** when the comment list can't be fetched, so the
   reason is visible instead of a silent empty list.

## State after the change
Comments still need a **session** — Coolapk refuses anonymous replies from this host (shared-device flag
or captcha). The fix makes the reader correct and diagnosable; the last mile is a credential:

* put `{"login_token": "...", "uid": "..."}` (from a logged-in Coolapk session) into `auth.json` — the
  reader picks it up within 60 s, no restart;
* or `{"device": "Xiaomi;<model>;<build>;<random>"}` to try a clean fingerprint (Coolapk may answer with a
  captcha instead of the `-415` account-farming flag);
* next step if wanted: a login form in the reader UI (username+password → Coolapk `account/login` →
  token stored in `auth.json`), so credentials never leave the browser.

## Verify
```bash
curl -s http://192.168.0.10:8125/api/feed/74447004 | python3 -c \
  "import json,sys; d=json.load(sys.stdin)['data']; print(len(d.get('comments') or []), repr(d.get('comments_error')))"
# before: 0 []
# after : 0 '评论接口异常…'   (or N comments once auth.json is present)
```
