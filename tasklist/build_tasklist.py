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
step("An empty folder to a narrated MP4 with Claude Code and HyperFrames: a title card, "
     "a narrated explainer synced to its voice, and a /brag launch clip. Every command and "
     "prompt from the video is below, in order.")
step("Starter repo (everything from the video)",
     code="https://github.com/DIY-Smart-Code/claude-video-starter", lang="javascript")
step("Commands with <slug> mean the video folder Claude created under videos/. "
     "List them with: ls videos")

# ── step 1 ─────────────────────────────────────────────────────────────────
head("Step 1: Install the tools")
step("Windows: install Node.js (22 or newer)", code="winget install OpenJS.NodeJS.LTS", lang="powershell")
step("macOS: install Node.js (22 or newer)", code="brew install node")
step("Windows: install ffmpeg", code="winget install Gyan.FFmpeg", lang="powershell")
step("macOS: install ffmpeg", code="brew install ffmpeg")
step("Windows (PowerShell): install Claude Code", code="irm https://claude.ai/install.ps1 | iex", lang="powershell",
     note="<p>Official installer from the Claude Code docs. Open a <strong>new</strong> terminal afterwards.</p>"
          "<p>Claude Code needs a Pro, Max, Team, Enterprise or Console account. The free claude.ai plan does not include it.</p>"
          "<p>Docs: <a href=\"https://code.claude.com/docs/en/setup\">code.claude.com/docs/en/setup</a></p>")
step("macOS / Linux / WSL: install Claude Code", code="curl -fsSL https://claude.ai/install.sh | bash",
     note="<p>Official installer from the Claude Code docs. Open a <strong>new</strong> terminal afterwards.</p>"
          "<p>Claude Code needs a Pro, Max, Team, Enterprise or Console account.</p>")
step("Check the three tools", code="node -v\nffmpeg -version\nclaude --version")
step("Python 3.8+ (only for the ElevenLabs voice in step 5)", optional=True,
     note="<p>Windows: <code>winget install Python.Python.3.12</code></p><p>macOS: <code>brew install python</code></p>")
step("Check your machine", code="npx hyperframes@latest doctor",
     note="<p><code>@latest</code> runs the current release. whisper-cpp shows as missing: that is optional and only "
          "needed for the free voice route in step 5.</p><p>No graphics card needed: without one, the browser renders in software.</p>")
step("Teach Claude Code how HyperFrames builds videos", code="npx hyperframes@latest skills")

# ── step 2 ─────────────────────────────────────────────────────────────────
head("Step 2: Clone the starter")
step("Clone the repo", code="git clone https://github.com/DIY-Smart-Code/claude-video-starter.git")
step("Go into the folder", code="cd claude-video-starter")
step("Install (pins one HyperFrames version for the repo)", code="pnpm install",
     note="<p>No pnpm? <code>npm install</code> works too.</p>")
step("Start Claude Code inside the folder", code="claude",
     note="<p>The first start opens your browser to log in.</p>")
step("Read the three rules at the top of CLAUDE.md",
     note="<ol><li>Use HyperFrames for every video.</li>"
          "<li>Same input, same frame: no random numbers, clocks or network calls inside a composition, so a render never changes.</li>"
          "<li>Lint after every edit, and a video is not finished until you have run <code>/review</code> on it.</li></ol>")

# ── step 3 ─────────────────────────────────────────────────────────────────
head("Step 3: The first prompt")
prompt("Type into Claude Code",
       "Using /hyperframes, make a 15-second title card for claude-video-starter, 16:9.",
       note="<p>Claude copies the template into <code>videos/&lt;slug&gt;/</code> and writes the composition. "
            "Naming the skill makes sure it loads.</p>")
step("Preview it in the studio", code="npx hyperframes preview videos/<slug>")
step("Lint it (catches broken timing before you render)", code="npx hyperframes lint videos/<slug>")
step("Render it", code="npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4")

# ── step 4 ─────────────────────────────────────────────────────────────────
head("Step 4: Let Claude review its own frames")
prompt("Type into Claude Code", "/review videos/<slug>",
       note="<p>Turns the render into a grid of 18 stills, scores Hook, Readability, Motion and Variety out of 10, "
            "and names the three worst problems with timestamps. It changes nothing until you say so.</p>")
prompt("Apply the fixes", "fix them")
step("Render again, then run /review again. Repeat until the timestamped problems are gone.",
     note="<p>Don't chase the scores. The timestamped list is the useful part.</p>"
          "<p>If <code>npx hyperframes check</code> still fails after a fix, believe the check: pull a full-size frame from the render and look.</p>")

# ── step 5 ─────────────────────────────────────────────────────────────────
head("Step 5: Give it a voice (ElevenLabs)")
step("Pick a voice in the voice library and copy its voice ID",
     code="https://elevenlabs.io/voice-library", lang="javascript",
     note="<p>The example in the video uses the stock voice <strong>Sarah</strong>: <code>EXAVITQu4vr4xnSDxMaL</code></p>")
step("Create an API key", code="https://elevenlabs.io/app/developers/api-keys", lang="javascript",
     note="<p>The key is a secret. It goes into <code>.env</code>, never into a prompt or a screenshot.</p>"
          "<p><a href=\"https://elevenlabs.io/docs/api-reference/authentication\">ElevenLabs docs: authentication</a></p>")
step("Copy the example env file", code="cp .env.example .env")
step("Paste your key and voice ID into .env",
     code="ELEVENLABS_API_KEY=your-key-here\nELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL\nELEVENLABS_MODEL_ID=eleven_v4",
     lang="javascript", note="<p><code>.env</code> is already in <code>.gitignore</code>.</p>")
step("Put the example script into a new video folder",
     code="mkdir videos/git-undo-explainer\ncp examples/git-undo-explainer/script.txt videos/git-undo-explainer/",
     note="<p>For your own video, write your lines into <code>videos/&lt;slug&gt;/script.txt</code>.</p>")
step("Make the voice", code="python scripts/tts.py videos/git-undo-explainer",
     note="<p>Writes <code>narration.wav</code> and <code>transcript.json</code>: the start time of every word. Step 7 runs on those times.</p>")
step("Licence check before you publish",
     note="<p>The free ElevenLabs plan has no commercial licence and asks you to credit ElevenLabs in the title. "
          "A channel that earns money needs a paid plan.</p>"
          "<p><a href=\"https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform\">ElevenLabs: can I publish what I generate?</a></p>")

head("Step 5 (free route): the built-in voice, no account")
step("Windows: install whisper.cpp for word timings", optional=True,
     code="setx HYPERFRAMES_WHISPER_PATH \"C:\\path\\to\\whisper-cli.exe\"", lang="powershell",
     note="<p>Download <code>whisper-bin-x64.zip</code> from the "
          "<a href=\"https://github.com/ggml-org/whisper.cpp/releases\">whisper.cpp releases</a>, unzip it, and point "
          "<code>HYPERFRAMES_WHISPER_PATH</code> at the <code>whisper-cli.exe</code> inside. Open a new terminal afterwards.</p>")
step("macOS: install whisper.cpp for word timings", code="brew install whisper-cpp", optional=True)
step("Make the voice on your own machine (Kokoro-82M)", optional=True,
     code="npx hyperframes tts videos/git-undo-explainer/script.txt --voice af_heart -o videos/git-undo-explainer/narration.wav",
     note="<p><code>npx hyperframes tts --list</code> shows all voices.</p>")
step("Add the word timings", optional=True,
     code="npx hyperframes transcribe videos/git-undo-explainer/narration.wav -d videos/git-undo-explainer",
     note="<p>Writes the same <code>transcript.json</code> as the ElevenLabs route, so step 7 works either way.</p>")

# ── step 6 ─────────────────────────────────────────────────────────────────
head("Step 6: Pictures with the Higgsfield MCP")
step("Connect the Higgsfield MCP server (needs a paid Higgsfield plan)",
     code="claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp",
     note="<p>Alternative used in the video: add <code>https://mcp.higgsfield.ai/mcp</code> as a connector on claude.ai "
          "(Settings, Connectors). Claude Code picks it up when you are logged in with that account.</p>"
          "<p><a href=\"https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp\">Higgsfield: what is the MCP</a></p>")
prompt("Log in once: start claude, run /mcp, pick higgsfield", "/mcp")
step("Check it shows as connected", code="claude mcp list")
prompt("Ask for an image with your colours in the prompt",
       "Generate a dark illustration of a cassette tape rewinding for my git explainer.\n"
       "Palette #0B0F18 and #68D9FF, no text, 16:9. Save it to videos/git-undo-explainer/assets/.",
       note="<p>Use generated images for illustrations and backgrounds, never to fake a product screen. Every image costs credits.</p>")

# ── step 7 ─────────────────────────────────────────────────────────────────
head("Step 7: A narrated explainer, synced to the voice")
prompt("Type into Claude Code",
       "Build a narrated explainer in videos/git-undo-explainer from script.txt and narration.wav, 16:9.\n"
       "Reveal each command card on the word where the voice says it, using transcript.json.\n"
       "Put assets/cassette-rewind.png behind the title. Render it when check passes.",
       note="<p>Use the file name your image got in step 6.</p>")
prompt("Review it", "/review videos/git-undo-explainer")
prompt("Fix what the review found", "fix them", optional=True)

# ── step 8 ─────────────────────────────────────────────────────────────────
head("Step 8: /brag, a launch video from one sentence")
step("Go to the demo app", code="cd examples/demo-app")
step("Add the brag marketplace (this folder only)", code="claude plugin marketplace add latent-spaces/brag --scope project",
     note="<p>Drop <code>--scope project</code> on both commands to install brag for every project.</p>")
step("Install the plugin", code="claude plugin install brag@brag --scope project")
step("Start Claude Code in the demo app", code="claude")
prompt("Ask for a launch clip", "let's /brag about this, no music",
       note="<p>On Opus 5.5 brag switches to /brag-slim and makes every decision itself. "
            "The results land in <code>brag-output/</code>.</p>")
prompt("The original brag workflow with music", "/brag --full", optional=True)

OUT.write_text(json.dumps({"name": NAME, "data": tasks}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{OUT.name}: {len(tasks)} items, {sum(1 for t in tasks if t.get('codeBlock'))} code blocks")
