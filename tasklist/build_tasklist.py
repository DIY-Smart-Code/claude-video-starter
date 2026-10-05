#!/usr/bin/env python3
"""Write tasklist/claude-code-video-starter.json, the follow-along checklist for
https://tasklist.smartcode.diy/list/claude-code-video-starter

Format: Task List Advanced import file, {"name": ..., "data": [task, ...]}.
A task is a headline (isHeadline) or a step; a step can carry one code block
(the app shows a copy button on it) and an HTML note (richText, opens in a modal).
Task text is inserted as HTML, so `<` and `>` in it must be escaped. Code blocks are plain text.

Run: python tasklist/build_tasklist.py
"""
import html
import json
from pathlib import Path

NAME = "Claude Code Video Starter"
OUT = Path(__file__).with_name("claude-code-video-starter.json")

tasks = []


def _add(text, headline=False, code=None, lang="bash", note=None, optional=False):
    n = len(tasks) + 1
    task = {
        "id": f"cc5v0000-0000-4000-8000-{n:012d}",
        "text": text if headline else html.escape(text, quote=False),
        "completed": False,
        "isHeadline": headline,
        "createdAt": f"2026-10-04T12:{n // 60:02d}:{n % 60:02d}.000Z",
    }
    if not headline:
        task["optional"] = optional
    if code is not None:
        task["codeBlock"] = {"language": lang, "code": code}
    if note:
        task["richText"] = note
    tasks.append(task)


def head(text):
    _add(text, headline=True)


def step(text, code=None, lang="bash", note=None, optional=False):
    _add(text, code=code, lang=lang, note=note, optional=optional)


def prompt(text, code, note=None, optional=False):
    """Something you type into Claude Code, not into the terminal."""
    _add(text, code=code, lang="javascript", note=note, optional=optional)


# ── intro ──────────────────────────────────────────────────────────────────
head("What you build")
step("One real explainer video, built start to finish with Claude Code and HyperFrames: a brief, a "
     "fact-checked script, a storyboard you review before anything moves, illustrations in one locked "
     "style, a synced voice and a review loop. Every command and prompt from the video is below, in order.")
step("Starter repo (everything from the video)",
     code="https://github.com/DIY-Smart-Code/claude-video-starter", lang="javascript")
step("Commands with <slug> mean the video folder Claude created under videos/. "
     "List them with: ls videos")

BRIEF_PROMPT = (
    "/hyperframes Make a 2-minute explainer about prompt caching for developers who use Claude Code.\n"
    "Use the standard explainer pipeline. Collaborative: show me the storyboard before you build.\n"
    "My take: most of your Claude Code bill is Claude re-reading the same context, and caching is the\n"
    "kitchen where the prep is already done. The idea scenes use that kitchen as illustrations; the\n"
    "numbers stay diagrams.\n"
    "Sources: https://platform.claude.com/docs/en/build-with-claude/prompt-caching and\n"
    "https://code.claude.com/docs/en/prompt-caching\n"
    "Look: cream paper #F4F1EA, charcoal ink #1A1815, one clay accent #C15F3C. Playfair Display\n"
    "headlines, Inter body, JetBrains Mono labels.\n"
    "Voice: ElevenLabs. No music. YouTube, 16:9."
)

# -- 1 set up ---------------------------------------------------------------
head("1 Set up")
step("Windows: install Node.js (22 or newer)", code="winget install OpenJS.NodeJS.LTS", lang="powershell")
step("macOS: install Node.js (22 or newer)", code="brew install node")
step("Windows: install ffmpeg", code="winget install Gyan.FFmpeg", lang="powershell")
step("macOS: install ffmpeg", code="brew install ffmpeg")
step("Windows (PowerShell): install Claude Code", code="irm https://claude.ai/install.ps1 | iex", lang="powershell",
     note="<p>Official installer from the Claude Code docs. Open a <strong>new</strong> terminal afterwards.</p>"
          "<p>Claude Code needs a Pro, Max, Team, Enterprise or Console account. The free claude.ai plan does not include it.</p>"
          "<p>Docs: <a href=\"https://code.claude.com/docs/en/setup\">code.claude.com/docs/en/setup</a></p>")
step("macOS / Linux / WSL: install Claude Code", code="curl -fsSL https://claude.ai/install.sh | bash",
     note="<p>Official installer from the Claude Code docs. Open a <strong>new</strong> terminal afterwards.</p>")
step("Python 3.8+ (for the ElevenLabs voice script)",
     note="<p>Windows: <code>winget install Python.Python.3.12</code></p><p>macOS: <code>brew install python</code></p>")
step("Check your machine", code="npx hyperframes@latest doctor",
     note="<p>whisper-cpp shows as optional: you only need it for the free voice route.</p>")
step("Install the official HyperFrames skills for Claude Code", code="npx hyperframes@latest skills",
     note="<p>They install into your user folder, so every project sees them.</p>")
step("Clone the starter", code="git clone https://github.com/DIY-Smart-Code/claude-video-starter.git\ncd claude-video-starter")
step("Install (pins one HyperFrames version for the repo)", code="pnpm install")
step("Pick a voice in the ElevenLabs voice library and copy its voice ID",
     code="https://elevenlabs.io/voice-library", lang="javascript",
     note="<p>The explainer in the video uses the stock voice <strong>Sarah</strong>: <code>EXAVITQu4vr4xnSDxMaL</code></p>")
step("Create an ElevenLabs API key", code="https://elevenlabs.io/app/developers/api-keys", lang="javascript",
     note="<p>The key is a secret. It goes into <code>.env</code>, never into a prompt or a screenshot.</p>")
step("Copy the example env file and paste in your key and voice ID",
     code="cp .env.example .env",
     note="<p><code>.env</code> is already in <code>.gitignore</code>. The free ElevenLabs plan is non-commercial only; "
          "a monetized channel needs a paid plan "
          "(<a href=\"https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform\">ElevenLabs on publishing</a>).</p>")
step("Connect the Higgsfield MCP server (needs a paid Higgsfield plan)",
     code="claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp",
     note="<p>Or add <code>https://mcp.higgsfield.ai/mcp</code> as a connector on claude.ai (Settings, Connectors).</p>"
          "<p><a href=\"https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp\">Higgsfield: what is the MCP</a></p>")
step("Start Claude Code in the repo folder", code="claude")
prompt("Log in to Higgsfield once: run /mcp and pick higgsfield", "/mcp")

# -- 2 brief ----------------------------------------------------------------
head("2 The brief")
prompt("Type into Claude Code (swap in your topic, take, sources and look)", BRIEF_PROMPT,
       note="<p>\"Use the standard explainer pipeline\" routes it to /faceless-explainer. It recommends an angle, "
            "may offer a few additions, and asks what's missing.</p>")
prompt("Answer its questions in a line each (the tutorial's answers)",
       "1. Yes, the narrative concept.\n"
       "2. Both. Keep one kitchen across the idea scenes: empty, prepped, serving.\n"
       "3. No, only the two docs pages.",
       note="<p>The answers land in <code>BRIEF.md</code>.</p>")

# -- 3 script ---------------------------------------------------------------
head("3 The script")
step("Read fact-check.md: one row per claim, with the sentence from the source it rests on",
     note="<p>In the tutorial run it dropped two claims the docs didn't support and marked the take as an opinion.</p>")
prompt("No fact-check.md in your run? Ask for it",
       "Check every number in SCRIPT.md against the sources and write fact-check.md with one row per\n"
       "claim: value, source URL, verified or wrong. Fix any wrong ones in the script.", optional=True)
step("CLAUDE.md makes Claude write the narration for the ear",
     note="<p>Commas or full stops instead of dashes, file names written the way they're said "
          "(<code>CLAUDE.md</code> becomes \"Claude dot M D\"). The voice reads exactly what's on the page.</p>")

# -- 4 design system --------------------------------------------------------
head("4 The design system")
step("Check frame.md once: the preset the workflow picked, remixed onto your colours and fonts",
     note="<p>Every frame inherits it. Fix anything that is off now, before the storyboard is drawn on it.</p>")
prompt("Confirm it and let Claude draw the sketches", "The frames look right. Draw the sketches.")

# -- 5 storyboard review ----------------------------------------------------
head("5 The storyboard review")
step("Open the sketch sheet in your browser", code="videos/<slug>/storyboard.html", lang="javascript",
     note="<p>Every frame as a static sketch, in the real fonts, colours and text. Nothing moves yet.</p>")
prompt("Ask for changes frame by frame (the tutorial's change)",
       "Frame 11 has too much text on screen. Cut it to the /usage card and let the voice say the two "
       "habits. Show me the sheet again.")
prompt("Confirm when it looks right", "Looks right. Go on.",
       note="<p>CLAUDE.md tells Claude never to build before you confirm the sheet.</p>")

# -- 6 art direction --------------------------------------------------------
head("6 Art direction")
step("Claude runs /art-direction for the metaphor scenes and shows you the first plate",
     note="<p>One prompt per scene with a locked style block, the first kept plate as a reference for the rest, "
          "a checklist for redoing plates, and a ledger of every prompt in <code>assets/art/</code>. "
          "Every image costs Higgsfield credits.</p>")
prompt("If it doesn't start on its own", "/art-direction for videos/<slug>", optional=True)
prompt("Put a fix into the style lock so every later plate gets it (the tutorial's redo)",
       "Redo it. Add full-bleed, no plate border to the style lock so plates B and C get it too.")
prompt("Keep the plate and let it make the rest", "Keep it. Go on with B and C.")

# -- 7 voice ----------------------------------------------------------------
head("7 The voice")
step("The workflow makes the narration with the ElevenLabs voice from .env", code="python scripts/tts.py videos/<slug>",
     note="<p>Writes <code>narration.wav</code> and <code>transcript.json</code>: the start time of every word.</p>")
step("Free route instead: Kokoro voice + word timings", optional=True,
     code="npx hyperframes tts videos/<slug>/script.txt --voice af_heart -o videos/<slug>/narration.wav\n"
          "npx hyperframes transcribe videos/<slug>/narration.wav -d videos/<slug>",
     note="<p>Word timings need whisper.cpp: <code>brew install whisper-cpp</code> on macOS; on Windows download "
          "<code>whisper-bin-x64.zip</code> from the <a href=\"https://github.com/ggml-org/whisper.cpp/releases\">whisper.cpp releases</a> "
          "and point <code>HYPERFRAMES_WHISPER_PATH</code> at <code>whisper-cli.exe</code>.</p>")

# -- 8 build ----------------------------------------------------------------
head("8 The build")
prompt("Approve the plates and start the build", "They look right. Start the build.",
       note="<p>One sub-agent per frame, then Claude assembles the video and runs the checks.</p>")
step("Run the checks", code="npx hyperframes check videos/<slug>")
step("Watch it in the studio", code="npx hyperframes preview videos/<slug>")
step("Render it", code="npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4",
     note="<p>If Claude's own render can't start Chrome from its shell, run this command yourself.</p>")

# -- 9 review loop ----------------------------------------------------------
head("9 The review loop")
prompt("Let Claude review its own frames", "/review videos/<slug>",
       note="<p>A grid of 18 stills, scores out of 10 and the three worst problems with timestamps. "
            "Don't chase the scores; fix the timestamped problems.</p>")
prompt("Apply the fixes", "Yes, apply all three.")
step("Render again, then run /review again",
     note="<p>Stop when the list gets shorter and the problems get smaller. If <code>npx hyperframes check</code> "
          "still fails after a fix, believe the check: pull a full-size frame from the render and look.</p>")
step("The finished project from the tutorial", code="examples/prompt-caching-explained/", lang="javascript",
     optional=True)

# -- going further ----------------------------------------------------------
head("Going further")
step("Official GSAP skills for richer motion", code="npx skills add https://github.com/greensock/gsap-skills", optional=True)
step("Ready-made blocks from the HyperFrames registry", code="npx hyperframes catalog --query \"<the look you want>\"", optional=True)
step("Camera moves and punch-ins: /hyperframes-keyframes. Sound effects: /media-use.", optional=True)

OUT.write_text(json.dumps({"name": NAME, "data": tasks}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{OUT.name}: {len(tasks)} items, {sum(1 for t in tasks if t.get('codeBlock'))} code blocks")
