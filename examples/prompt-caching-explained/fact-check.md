# Fact check — SCRIPT.md

Sources (downloaded 2026-10-04 into `capture/sources/`):
- **CC** = https://code.claude.com/docs/en/prompt-caching
- **API** = https://platform.claude.com/docs/en/build-with-claude/prompt-caching

| # | Claim (frame) | Value on screen / spoken | Source | Status |
|---|---|---|---|---|
| 1 | Every message re-sends the whole session (F1, F2) | "reads your whole session again" | CC: "The model doesn't remember anything between requests, so Claude Code re-sends the full context: the system prompt, your project context, every prior message and tool result, and your new message." | verified |
| 2 | New content goes at the end; most of each request is repeated (F2) | "Most of every request is text Claude has already read" | CC: "New content is appended at the end, which means most of each request is identical to the one before it." | verified |
| 3 | "Most of what you pay for is the re-read" (F3) | thesis | The user's take. Supported by #2 (most of each request is repeated input). The sources give no figure for share of the bill, so the video shows no percentage. | opinion, framed as the take |
| 4 | Cache write = prep done once; cache hit = reuse (F5, F6) | "cache write", "cache hit" | CC: `cache_creation_input_tokens` = "Tokens written to the cache"; `cache_read_input_tokens` = "Tokens served from cache". | verified |
| 5 | Match is exact and starts at the top (F7) | "exact… starts at the top" | CC: "The API caches by matching the start of each request, called the prefix… The match is exact, so a change anywhere in the prefix recomputes everything after it." | verified |
| 6 | Layers: system prompt · project context · conversation (F7) | three layer labels | CC layer table: System prompt / Project context / Conversation. | verified |
| 7 | Change conversation → prep stays; change above → everything below re-cooks (F7) | spoken | CC: "A change to the conversation layer leaves the system prompt and project context cached. A change to the system prompt invalidates everything." | verified |
| 8 | Normal input = 1× (F8) | 1× | API pricing table, "Base input tokens". | verified |
| 9 | Cache write = 1.25× (F8) | 1.25× | API: "5-minute cache write tokens are 1.25 times the base input tokens price". | verified (5-min TTL; 1-hour writes are 2×, not shown) |
| 10 | Cache read = 0.1× (F8) | 0.1× / "one tenth" | API: "Cache read tokens are 0.1 times the base input tokens price". Footnote: "All other models use the standard 0.1x multiplier." | verified |
| 11 | Opus 5.5 read = 0.05× (F8) | 0.05× / "one twentieth" | API footnote 2: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price." | verified |
| 12 | Cache lives five minutes (F9) | 5 min | API: "By default, the cache has a 5-minute lifetime." CC: five-minute TTL for usage credits, API key or cloud provider. | verified |
| 13 | An hour on a Claude subscription (F9) | 1 h | CC: "Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage" (main conversation). | verified, with caveat: main conversation only, within plan usage. The on-screen label carries the caveat |
| 14 | Every hit resets the clock (F9) | spoken | CC: "Each request that hits the cache resets the timer." API: "refreshed for no additional cost each time the cached content is used." | verified |
| 15 | Switching models throws the cache out (F10) | "/model" | CC: "Each model has its own cache. Switching… the next request reads the entire conversation history with no cache hits." | verified |
| 16 | Turning on fast mode throws the cache out (F10) | "fast mode" | CC: "the first request Claude Code sends with fast mode on reads the entire conversation history with no cache hits." It happens once per conversation. | verified |
| 17 | Compacting throws out the conversation cache (F10) | "/compact" | CC: "this invalidates the conversation layer, since the next request has a new, shorter history." The system prompt layer is reused. | verified. The narration says "compacting" generally; the label says "mid-task", following the CC tip |
| 18 | Pick model at the start; compact between tasks (F11) | habits | CC tip: "Pick your model and effort level at the top of a session, then save /compact for natural breaks between tasks." | verified |
| 19 | `/usage` shows a prompt cache line (F11) | "Prompt cache (main) — hit ratio · misses · warm" | CC: "run /usage… a Prompt cache (main) line… showing the session's hit ratio, miss count, and whether the cache is warm right now." Requires v2.1.251+. | verified. No invented values on screen, labels only |

Corrections made while writing:
- Removed "connecting an MCP server" from the spoilers list. With tool search on (the default on supported models), it does not invalidate the cache (CC § Connecting or removing an MCP server).
- Removed "changing effort". On Opus 5.5, Sonnet 5.5 and Fable 5.1 (API key or subscription), changing effort keeps the cache, so the claim isn't true in general.
