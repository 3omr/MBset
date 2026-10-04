# Setup guide — install the skill and connect your own Telegram

For anyone who receives this skill. Everything runs on your machine with your own accounts; nothing
here is tied to the person who made it.

> **بالعربي باختصار:** انسخ فولدر السكيل، شغّل `install.sh`، وبعدين لو عايز تنزّل ملفات من تليجرام
> اعمل `telegram setup` **بنفسك** مرة واحدة بحسابك. التفاصيل تحت.

---

## 1. Put the skill where your agent finds it

Copy the whole `mbset-module-curator/` folder (keep its structure) to one of:

| Agent | Folder |
| :--- | :--- |
| Claude Code (all projects) | `~/.claude/skills/mbset-module-curator/` |
| Claude Code (one project) | `<project>/.claude/skills/mbset-module-curator/` |
| Codex / generic agents | `<project>/.agents/skills/mbset-module-curator/` |
| Antigravity / Gemini | `~/.gemini/antigravity/skills/mbset-module-curator/` |

In the commands below, `<skill>` is that folder. Your modules can live anywhere, e.g.
`~/MBset/<University>/<Module>/` with the sources in `<Module>/Raw_PDF_Questions/`.

## 2. Tools — automatic

Nothing to do: the first time your agent uses the skill it runs `mbset.py doctor --fix`, which puts the
Python packages in `<skill>/.venv` and installs Tesseract / Poppler with apt (Linux) or brew (macOS). If
that needs your password, the agent shows you one command to run. Windows: use WSL (Ubuntu).

To do it yourself ahead of time:
```bash
bash <skill>/scripts/install.sh --telegram          # leave out --telegram if you never use Telegram
```

## 3. Connect YOUR Telegram account (optional, once)

The downloader logs in as you, so it can fetch files from every channel or group you can see — public
or private. Your credentials stay on your computer.

**3.1 Get your API keys** (2 minutes)
1. Open <https://my.telegram.org> and log in with your phone number (the code arrives in the Telegram app).
2. Click **API development tools**.
3. Fill the form: *App title* and *Short name* can be anything (e.g. `mbset`), *Platform*: Desktop. Submit.
4. Keep the page open: you need **App api_id** (a number) and **App api_hash** (32 characters).

**3.2 Run the setup yourself** — in a normal terminal window (or the Terminal tab of the Claude desktop
app), not through the agent, because you type the answers:

```bash
python3 <skill>/scripts/mbset.py telegram setup
```

It asks for `api_id`, `api_hash` (hidden while you type), then your phone number, the login code Telegram
sends you, and your 2FA password if you have one. They are saved only in `~/.config/mbset/`
(readable by you only). Check any time with:

```bash
python3 <skill>/scripts/mbset.py telegram status
```

> Never paste your api_hash, login code or password into a chat with an AI agent. The skill tells the
> agent to never ask for them; if one does, refuse and run `telegram setup` yourself.

**3.3 Download a module's files**

```bash
M="$HOME/MBset/My University/Endocrinology"
python3 <skill>/scripts/mbset.py telegram download "$M" https://t.me/somechannel/120-160
python3 <skill>/scripts/mbset.py telegram download "$M" --links-file links.md
python3 <skill>/scripts/mbset.py inventory "$M"
```

- Links can be single posts (`…/120`), ranges (`…/120-160`), or posts of private channels/groups you
  joined (`https://t.me/c/1234567890/55` — copy it with *Copy Post Link*).
- `--links-file` takes any text or markdown file and uses every t.me link in it, in order.
- Files land in `$M/Raw_PDF_Questions/`; posts already downloaded are skipped, identical files are kept
  once. `--dry-run` lists the posts without logging in.

**3.4 One message that links to many others — scan first, then choose**

```bash
python3 <skill>/scripts/mbset.py telegram scan "$M" https://t.me/somechannel/120   # downloads nothing
python3 <skill>/scripts/mbset.py telegram download "$M" --from-scan --pick 1,3-9 --skip-types video
```

- `scan` reads the post, its album and every Telegram link in it (written, hidden behind words, or on
  buttons), then the posts those link to, two levels deep (`--depth`), each post once. `--comments` also
  reads the post's comments.
- It writes `$M/.mbset/telegram_scan.md`: where each file came from, its type and size, and which files are
  duplicates or already in the module. Invite links, channel links and outside links (Drive, YouTube…) are
  only listed: nothing is joined or opened.
- The agent shows you that summary and downloads only the files you choose.

To disconnect: delete `~/.config/mbset/telegram*` and, optionally, end the session in Telegram →
Settings → Devices.

## 4. First run — the agent sets the skill up with you

The first time you use the skill, the agent runs a short setup and saves your answers in
`~/.config/mbset/config.yaml` (it never asks again; change them any time with `mbset.py init`):
1. **Your faculty**: Damietta and Assiut tag systems are built in. For any other faculty the agent asks how
   your sources are named (finals, midterms, formatives, quizzes, department books, professors…) and builds
   your faculty's tag system with you, previewing it on your real filenames.
2. **Who does the heavy work** (below).
3. **Telegram**: yes / no (if yes, step 3 above).
4. **Reply language.**

## 5. Choose who does the heavy work

Transcription and review are split into small briefs. The first time, the agent asks you who runs them:
**Claude subagents** (nothing to install), a delegate CLI you have (Codex, Antigravity, Cursor,
OpenCode…), or the main agent alone. See `workers.md`.

## 6. First module

```bash
S=<skill>/scripts/mbset.py
python3 $S inventory "$M" [--university Damietta|Assiut]
python3 $S ocr "$M" && python3 $S parse "$M" && python3 $S route "$M"
```
then follow `SKILL.md` §2. Ask your agent: *"use the mbset-module-curator skill on <module folder>"*.

## Troubleshooting

| Message | Fix |
| :--- | :--- |
| `Telethon is not installed` | `python3 <skill>/scripts/mbset.py doctor --fix --telegram` |
| `no Telegram API credentials` / `session not logged in` | run `telegram setup` yourself (step 3.2) |
| `telegram setup is interactive` | you ran it through an agent; run it in your own terminal window |
| `Telegram asks to wait Ns` | Telegram's rate limit; the downloader waits and continues |
| `post has no downloadable media` / `no_media` | the post is text only; it is recorded and skipped |
| `doctor`: tesseract / pdftoppm missing | `doctor --fix`, or run the command it prints (needs your password) |

---

## دليل سريع بالعربي

**1. ثبّت السكيل:** انسخ فولدر `mbset-module-curator` كله في `~/.claude/skills/` (لو بتستخدم Claude Code)،
أو في `.agents/skills/` جوه المشروع.

**2. الأدوات بتتثبّت لوحدها:** أول ما الـ agent يستخدم السكيل بيشغّل `doctor --fix`، وده بيثبّت كل حاجة لوحده.
لو محتاج باسورد الجهاز، هيوريك أمر واحد تشغّله إنت. ولو عايز تجهّز من الأول بنفسك:
```bash
bash <skill>/scripts/install.sh --telegram
```

**3. اربط تليجرام بحسابك إنت** (مرة واحدة، ولو محتاج تنزّل ملفات من تليجرام بس):
1. افتح <https://my.telegram.org> وادخل برقم موبايلك. الكود هيوصلك على تطبيق تليجرام.
2. ادخل على **API development tools**، واملا الفورم بأي اسم (مثلاً `mbset`)، واختار Desktop.
3. هيظهرلك **api_id** (رقم) و **api_hash** (32 حرف).
4. شغّل الأمر ده **بنفسك** في terminal عادي (أو تاب Terminal في تطبيق Claude)، مش عن طريق الـ agent:
   ```bash
   python3 <skill>/scripts/mbset.py telegram setup
   ```
   هيطلب منك الـ api_id والـ api_hash، وبعدين رقمك والكود اللي هيوصلك (والباسورد لو عامل تحقق بخطوتين).
   كل ده بيتحفظ على جهازك بس في `~/.config/mbset/`.
5. ما تبعتش الـ api_hash ولا الكود ولا الباسورد لأي AI في الشات خالص.

**4. نزّل ملفات موديول:**
```bash
python3 <skill>/scripts/mbset.py telegram download "<فولدر الموديول>" https://t.me/channel_name/120-160
```
- الملفات بتنزل في `Raw_PDF_Questions` جوه الموديول.
- اللي نزل قبل كده مش بينزل تاني.
- لو القناة أو الجروب برايفت وإنت عضو فيه: انسخ لينك البوست من "Copy Post Link" (هيبقى شكله `t.me/c/...`) واستخدمه عادي.
- **رسالة فيها لينكات لرسايل تانية:** `telegram scan "<فولدر الموديول>" <لينك الرسالة>`. بيقرا الرسالة والألبوم وكل
  لينك تليجرام جواها والرسايل اللي بتشاور عليها (لحد مستويين)، ومش بينزّل أي حاجة. بيعملك ملخص بكل ملف: جه منين،
  نوعه، حجمه، متكرر ولا لأ. الـ agent يعرضه عليك، وبعد ما تختار: `telegram download … --from-scan --pick 1,3-9`.

**5. أول تشغيل:** قول للـ agent: «استخدم سكيل mbset-module-curator على فولدر الموديول ده». أول مرة هيعمل تهيئة
ويسألك أسئلة قليلة، والإجابات بتتحفظ فما بيسألش تاني:
- **كليتك:** نظام تاجز دمياط وأسيوط جاهز. لو كليتك تانية، هيسألك ملفاتكم بتتسمّى إزاي (فاينال، ميدترم، فورماتيف،
  كويزات، كتب الأقسام، الدكاترة...)، ويعمل نظام التاجز بتاع كليتك معاك ويجرّبه على أسامي ملفاتك الحقيقية لحد ما توافق.
- **مين يشتغل:** Claude subagents، أو Codex أو Antigravity لو عندك، أو هو لوحده.
- **تليجرام:** هتستخدمه ولا لأ.
- **لغة الرد:** عربي ولا إنجليزي.

ولو حبيت تغيّر أي حاجة بعد كده: `python3 <skill>/scripts/mbset.py init`.
