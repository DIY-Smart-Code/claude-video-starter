# Fact-check — prompt-caching-kitchen

Sources (fetched 2026-10-05):
- **[API]** https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- **[CC]** https://code.claude.com/docs/en/prompt-caching

| # | Claim in SCRIPT.md | Source quote | Frame |
|---|---|---|---|
| 1 | Claude Code sends everything again each message: system prompt, Claude dot M D, every message, every tool result, the new message | [CC] "Claude Code re-sends the full context: the system prompt, your project context, every prior message and tool result, and your new message." | 02 |
| 2 | Most of each request is a re-read ("most of your bill is re-reading" — the user's take) | [CC] "New content is appended at the end, which means most of each request is identical to the one before it." | 01 |
| 3 | The cache matches the start of each request, the prefix; only the newest turn is processed fresh | [CC] "The API caches by matching the start of each request, called the prefix … On a normal turn, the prefix is the entire previous request and only the latest exchange is new." | 05 |
| 4 | A cache read costs one tenth of normal input | [API] "Cache read tokens are 0.1 times the base input tokens price" (some newer models are cheaper still: Opus 5.5 0.05x, Fable 5.1 0.025x) | 06 |
| 5 | Writing the cache costs a quarter more, once | [API] "5-minute cache write tokens are 1.25 times the base input tokens price" | 06 |
| 6 | 100,000-token context × 40 turns: 4,000,000 full-price tokens uncached; ≈ 515,000 cached | Arithmetic from #4/#5: 100,000 × 40 = 4,000,000. Cached: 1 write × 100,000 × 1.25 = 125,000 + 39 reads × 100,000 × 0.1 = 390,000 → 515,000 full-price-equivalent. Simplified: context held constant, new-turn tokens ignored. On screen labelled "illustrative". 100,000 cache read mirrors the [API] usage example (`cache_read_input_tokens: 100000`). | 07 |
| 7 | Stack order: system prompt and tools, then project context, then the conversation | [CC] layer table: System prompt (core instructions, tool definitions) → Project context (CLAUDE.md, auto memory, unscoped rules) → Conversation | 08 |
| 8 | Change near the top and everything below is recomputed | [CC] "The match is exact, so a change anywhere in the prefix recomputes everything after it." / "A change to the system prompt invalidates everything" | 08 |
| 9 | Switching models breaks the cache | [CC] "Each model has its own cache. Switching with /model means the next request reads the entire conversation history with no cache hits" | 09 |
| 10 | Changing effort breaks it, on most models | [CC] "On most models, changing the effort level mid-session means the next request reads the entire conversation history with no cache hits." (Opus 5.5, Sonnet 5.5, Fable 5.1 on API key/subscription keep it) | 09 |
| 11 | Turning on fast mode breaks it (once) | [CC] "the first request Claude Code sends with fast mode on reads the entire conversation history with no cache hits" / "The cost applies once per conversation." | 09 |
| 12 | Slash compact rebuilds the conversation layer | [CC] "Compaction … By design, this invalidates the conversation layer" | 09 |
| 13 | Upgrading Claude Code rebuilds the cache | [CC] "the first conversation you start after an upgrade builds its cache from the top" | 09 |
| 14 | Each break = one slower, full-price turn, then cached again | [CC] "You see a one-time slower, more expensive turn, after which the new prefix is cached." | 09 |
| 15 | API key: cache lasts five minutes without use; each use resets the timer | [CC] table: "Usage credits, API key, or cloud provider — Five minutes"; [API] "The cache is refreshed for no additional cost each time the cached content is used" | 10 |
| 16 | Subscription: Claude Code keeps the main conversation warm for an hour | [CC] "Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage. There it requests the hour for the main conversation" | 10 |
| 17 | Editing files, invoking skills, switching permission modes, slash rewind keep the cache | [CC] "Actions that keep the cache": Editing files in your repository · Changing permission mode · Invoking skills and commands · Rewinding the conversation | 11 |
| 18 | Pick model and effort at the start; compact between tasks | [CC] Tip: "Pick your model and effort level at the top of a session, then save /compact for natural breaks between tasks." | 12 |
| 19 | Check your hit rate with slash usage | [CC] "For a per-session summary, run /usage … a Prompt cache (main) line … showing the session's hit ratio, miss count, and whether the cache is warm right now." | 12 |

Deliberately left out (true but too conditional for 2 minutes): MCP server changes (only break the cache when tool search is off), image accumulation, gateways, 20-block lookback, minimum cacheable lengths.
