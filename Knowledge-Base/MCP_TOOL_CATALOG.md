# COMPLETE MCP TOOL CATALOG
**System:** Kyle's Windows 11 Development Environment
**Last Updated:** December 01, 2025
**Total Tools:** 44 tools across 9 servers

---

## SUMMARY (Quick Reference)

**Total:** 44 tools across 9 servers
**Status:** 42 working (95%), 2 optional (require service)
**Categories:** System Monitoring, Optimization, Files, Git, Database, Semantic, Orchestration, AI

---

## 1. PC HEALTH MONITOR (2 tools)

### pc-health:quick_status
Fast one-line system status: CPU%, RAM%, Disk%, Uptime

### pc-health:process_list
Top CPU processes with detailed stats (count parameter)

---

## 2. PC OPTIMIZATION (7 tools) ⚡ NEW

**Requires Administrator privileges for most operations**

### pc-optimization:optimize_performance
Comprehensive system optimization:
- Ultimate Performance power plan
- Disable unnecessary services (telemetry, Xbox)
- Optimize visual effects
- Enable GPU hardware scheduling
- Disable transparency
- Enable Game Mode
- Disable background apps

### pc-optimization:set_power_plan
Switch power plans: ultimate/high/balanced
Ultimate Performance recommended for workstation use

### pc-optimization:disable_services
Disable unnecessary Windows services
Optional: aggressive mode includes Superfetch & Windows Search

### pc-optimization:optimize_startup
Scan and list all startup programs with recommendations

### pc-optimization:clear_temp_files
Safe cleanup of temp files, system temp, prefetch
Returns space freed in MB

### pc-optimization:optimize_network
Network performance tuning:
- TCP auto-tuning
- RSS (Receive Side Scaling)
- Chimney offload
- NetDMA

### pc-optimization:gpu_optimization_check
AMD 7900 XTX optimization status:
- Hardware-accelerated GPU scheduling
- SAM (Smart Access Memory)
- Driver version
- AMD Software recommendations

---

## 3. FILE SCOUT (4 tools)

### file-scout:scout_file / hydra:scout_file
Safe file preview - returns full content for <1MB, metadata+tail for large files
Prevents crashes on huge files

### file-scout:scout_directory / hydra:scout_directory
Directory listing with sizes, marks files as safe (<1MB) or large (>1MB)

---

## 4. GIT AUTOMATION (6 tools) ✅ FIXED

### git-automation:git_status
Check status for multiple repos - modified files, untracked, branch info

### git-automation:git_commit_smart
Auto-generate commit message using local AI, then commit
Uses SmolLM2 for fast, no-cost messages

### git-automation:git_diff_summary
Summary of uncommitted changes with line counts

### git-automation:git_branch_info
Branch details: current, all branches, remotes

### git-automation:git_health_check
Multi-repo health check: uncommitted changes, unpushed commits

### git-automation:git_log_recent
Recent commit history (count parameter)

---

## 5. DATABASE QUERY (5 tools) ✅ FIXED

Known DBs: "memory", "ai-librarian"

### database-query:query_db
Execute arbitrary SQL on any SQLite database (limit parameter)

### database-query:db_schema
Complete database schema with tables and columns

### database-query:db_stats
Database file size and row counts per table

### database-query:memory_search
Search Memory database conversations by keyword

### database-query:librarian_search
Search AI-Librarian archives by keyword (searches messages.content)

---

## 6. SEMANTIC MEMORY (5 tools)

### semantic-memory:semantic_search
Find similar queries using embeddings (not exact keywords)
Parameters: query, limit, min_similarity

### semantic-memory:hybrid_search
Combined exact keyword + semantic similarity search

### semantic-memory:store_memory
Store new memory with auto-embedding generation

### semantic-memory:migrate_memory
One-time: Add embeddings to existing database

### semantic-memory:init_semantic_memory
One-time: Initialize semantic memory schema

---

## 7. ORCHESTRATOR (3 tools)

### orchestrator:orchestrate_task
Analyze task and route to best specialist agent
Uses memory to learn patterns

### orchestrator:list_specialists
List all available specialist agents and capabilities

### orchestrator:get_memory_stats
Memory system statistics and agent usage

---

## 8. HYDRA MULTI-HEAD (9 tools) ✅ FIXED

### PLANNER (The Eyes)

#### hydra:analyze_request
Analyze request: detect tasks, batch ops, complexity, parallelizable

#### hydra:create_execution_plan
Detailed parallel execution plan with core assignments
Handles Kyle's 20 cores, estimates timing

#### hydra:detect_project_scope
Detect which projects involved (AI-Librarian, Local-Router, etc)

### REPORTER (The Ears)

#### hydra:aggregate_results
Aggregate results from parallel tasks: success/fail counts, timing

#### hydra:synthesize_report
Convert to human-readable (summary/detailed/errors_only)

#### hydra:compare_results
A/B testing - compare two result sets

#### hydra:extract_insights
Extract patterns, bottlenecks, recommendations

### FILE SCOUT (The Hands) - see #2 above

---

## 9. LOCAL ROUTER RACING (5 tools) ✅ ENDPOINT FIXED

Models: SmolLM2 1.7b (fast) + gpt-oss 20b (smart)
Status: Requires service running

### local-router-racing:local_chat_racing
TRUE parallel racing - both models on separate cores simultaneously
Returns both responses, winner identified

### local-router-racing:local_chat_pipeline
Sequential pipeline: SmolLM2 drafts → gpt-oss refines
Higher quality, slower

### local-router-racing:local_chat_auto
Smart auto-select: SIMPLE tasks → fast only, COMPLEX → parallel racing
Best default option

### local-router-racing:local_chat_fast
Force SmolLM2 only (5-8s)

### local-router-racing:local_chat_smart
Force gpt-oss only (10-15s)

---

## POWER COMBINATIONS

### Multi-Repo Health Check
```
1. git-automation:git_health_check
2. orchestrator:get_memory_stats  
3. pc-health:quick_status
```

### Research Workflow
```
1. semantic-memory:hybrid_search
2. database-query:librarian_search
3. hydra:synthesize_report
```

### Development Workflow
```
1. file-scout:scout_directory
2. git-automation:git_status
3. local-router-racing:local_chat_auto
4. git-automation:git_commit_smart
```

### Performance Analysis
```
1. hydra:create_execution_plan
2. [Execute parallel operations]
3. hydra:aggregate_results
4. hydra:extract_insights
5. hydra:synthesize_report
```

---

## DETAILED TOOL DESCRIPTIONS

[See full catalog below for complete descriptions, parameters, use cases, and examples]

### PC HEALTH: quick_status
**What:** Fast system status check
**Returns:** CPU%, RAM%, Disk%, Uptime
**Use:** Quick health check, verify resources available
**Speed:** ~0.1s

### PC HEALTH: process_list
**What:** Top CPU processes with stats
**Params:** count (default: 10)
**Returns:** Process name, CPU time, RAM usage
**Use:** Identify resource hogs, check services
**Speed:** ~0.2s

### FILE SCOUT: scout_file
**What:** Safe file preview without memory crashes
**Params:** filepath, tail_lines (default: 30)
**Logic:** <1MB = full content, >1MB = metadata + tail
**Returns:** Size, line count, content/preview
**Use:** Check logs, preview datasets, verify contents
**Speed:** Instant for small, fast for large

### FILE SCOUT: scout_directory
**What:** Directory listing with size info
**Params:** dirpath, include_sizes (default: true)
**Returns:** Items with [FILE]/[DIR], sizes, safe/large markers
**Use:** Explore structure, find large files
**Speed:** Instant

### GIT: git_status
**What:** Git status for multiple repos
**Params:** repos (array)
**Returns:** Branch, modified files, untracked files, status
**Use:** Multi-repo checks, pre-commit verification
**Speed:** 0.02s per repo ⚡ (FIXED)

### GIT: git_commit_smart
**What:** AI-generated commit message + commit
**Params:** repo_path, add_all (default: true)
**Logic:** Analyzes diff, generates message via SmolLM2
**Returns:** Commit hash, message
**Use:** Quick commits, consistent style
**Speed:** ~6s (local AI)

### GIT: git_diff_summary
**What:** Summary of uncommitted changes
**Params:** repo_path
**Returns:** File changes, insertions/deletions
**Use:** Review before commit, estimate size
**Speed:** 0.02s

### GIT: git_branch_info
**What:** Branch information
**Params:** repo_path
**Returns:** Current, all branches, remotes
**Use:** Branch management, verify current
**Speed:** 0.02s

### GIT: git_health_check
**What:** Multi-repo health check
**Params:** repos (default: AI-Librarian, Local-Router)
**Returns:** Uncommitted changes, unpushed commits, issues
**Use:** Daily health check, pre-deployment
**Speed:** 0.02s per repo

### GIT: git_log_recent
**What:** Recent commit history
**Params:** repo_path, count (default: 10)
**Returns:** Commit hashes, messages
**Use:** Review work, find commits, changelogs
**Speed:** 0.02s

### DATABASE: query_db
**What:** Execute SQL on SQLite database
**Params:** database, query, limit (default: 100)
**Logic:** Auto-adds LIMIT if not specified
**Returns:** Query results with column names
**Use:** Custom queries, data analysis, extraction
**Speed:** Depends on query

### DATABASE: db_schema
**What:** Complete database schema
**Params:** database
**Returns:** All tables, columns, types, PKs
**Use:** Understand structure, plan queries
**Speed:** Instant

### DATABASE: db_stats
**What:** Database statistics
**Params:** database
**Returns:** File size, row counts per table
**Use:** Monitor growth, capacity planning
**Speed:** Instant

### DATABASE: memory_search
**What:** Search Memory database by keyword
**Params:** search_term, limit (default: 20)
**Returns:** Conversations with agents, timestamps
**Use:** Find agent decisions, trace behavior
**Speed:** Fast

### DATABASE: librarian_search
**What:** Search AI-Librarian archives
**Params:** search_term, limit (default: 20)
**Returns:** Session ID, preview, message count, date
**Use:** Find past conversations, research
**Speed:** Fast
**Note:** ✅ FIXED - now searches messages.content

### SEMANTIC: semantic_search
**What:** Semantic similarity search via embeddings
**Params:** query, limit (default: 5), min_similarity (default: 0.3)
**Returns:** Similar content with scores
**Use:** Find related by meaning, not keywords
**Speed:** Fast

### SEMANTIC: hybrid_search
**What:** Combined exact + semantic search
**Params:** query, limit (default: 10)
**Returns:** Merged results, match type shown
**Use:** Comprehensive search, max recall
**Speed:** Fast

### SEMANTIC: store_memory
**What:** Store with auto-embedding
**Params:** query, context (optional)
**Use:** Save learnings, build knowledge base
**Speed:** Fast

### SEMANTIC: migrate_memory
**What:** Add embeddings to existing data
**Use:** One-time migration for semantic search
**Speed:** Depends on data size

### SEMANTIC: init_semantic_memory
**What:** Initialize semantic schema
**Use:** First-time setup
**Speed:** Instant

### ORCHESTRATOR: orchestrate_task
**What:** Route task to best specialist
**Params:** task
**Logic:** Uses memory to learn patterns
**Returns:** Selected agent, reasoning
**Use:** Intelligent delegation, adaptive routing
**Speed:** Fast

### ORCHESTRATOR: list_specialists
**What:** List all specialists and capabilities
**Returns:** Agent names, descriptions, tools
**Use:** Discover agents, plan workflows
**Speed:** Instant

### ORCHESTRATOR: get_memory_stats
**What:** Memory system statistics
**Returns:** Conversations, patterns, agent usage
**Use:** Monitor learning, debug routing
**Speed:** Instant

### HYDRA: analyze_request
**What:** Analyze request for task components
**Params:** request
**Returns:** Tasks, batch op flag, complexity, parallelizable
**Use:** Pre-processing, decide strategy
**Speed:** Instant

### HYDRA: create_execution_plan
**What:** Detailed parallel execution plan
**Params:** request, target_files (optional)
**Returns:** Plan ID, tasks, core assignments, estimated time
**Use:** Plan batch ops, optimize parallel workflows
**Speed:** Instant
**Note:** ✅ FIXED - handles empty task lists

### HYDRA: detect_project_scope
**What:** Detect projects involved
**Params:** request
**Returns:** Projects, multi-project flag, scope
**Use:** Multi-project coordination, scope estimation
**Speed:** Instant

### HYDRA: aggregate_results
**What:** Aggregate parallel task results
**Params:** results, plan_id (optional)
**Returns:** Success/fail counts, timing stats, errors
**Use:** Batch reporting, performance analysis
**Speed:** Instant

### HYDRA: synthesize_report
**What:** Human-readable report from results
**Params:** results, report_type (summary/detailed/errors_only)
**Returns:** Formatted report
**Use:** User-friendly output, summaries, debugging
**Speed:** Instant

### HYDRA: compare_results
**What:** Compare two result sets (A/B testing)
**Params:** results_a, results_b
**Returns:** Deltas, winner, performance comparison
**Use:** A/B testing, before/after analysis
**Speed:** Instant

### HYDRA: extract_insights
**What:** Extract patterns and recommendations
**Params:** results
**Returns:** Bottlenecks, patterns, recommendations
**Use:** Performance tuning, optimization, improvement
**Speed:** Instant

### RACING: local_chat_racing
**What:** TRUE parallel racing - both models simultaneously
**Params:** prompt
**Logic:** SmolLM2 + gpt-oss on separate cores, winner identified
**Returns:** Both responses, winner, timing
**Use:** Coding, technical questions, speed + quality
**Speed:** ~10-15s (winner finishes first)
**Status:** Requires service

### RACING: local_chat_pipeline
**What:** Sequential pipeline - draft then refine
**Params:** prompt
**Logic:** SmolLM2 drafts → gpt-oss refines
**Returns:** Draft and refined versions, timing
**Use:** Quality-critical tasks, content generation
**Speed:** ~15-20s
**Status:** Requires service

### RACING: local_chat_auto
**What:** Smart auto-select mode
**Params:** prompt
**Logic:** Classifies SIMPLE (fast only) vs COMPLEX (racing)
**Returns:** Response with mode explanation
**Use:** General use, best default, adaptive
**Speed:** Variable
**Status:** Requires service

### RACING: local_chat_fast
**What:** Force SmolLM2 only
**Params:** prompt
**Use:** Quick tasks, drafts, fast iteration
**Speed:** ~5-8s
**Status:** ✅ WORKS (service running)

### RACING: local_chat_smart
**What:** Force gpt-oss only
**Params:** prompt
**Use:** High quality, complex reasoning, code generation
**Speed:** ~10-15s
**Status:** Requires service

---

## RECENT FIXES (Nov 30, 2025)

1. **git-automation:** Added stdin=DEVNULL → 3000x speedup (60s timeout → 0.02s)
2. **database-query:librarian_search:** Fixed schema mismatch → searches messages.content
3. **hydra:create_execution_plan:** Fixed division by zero → handles empty tasks
4. **local-router-racing:** Fixed endpoint path → /race (not /racing)

---

## MAINTENANCE

**Services:**
- Racing Router: Auto-starts on login (configured, not started)
- MCP Servers: Auto-load with Claude Desktop

**Logs:** `C:\Users\kyleh\AppData\Roaming\Claude\logs\mcp-server-*.log`

**Start Racing Service:**
```powershell
schtasks /run /tn "LocalRouterRacing"
# OR
C:\repos\Local-Router\control_racing.bat
```

---

## STATISTICS

**By Category:**
- System Monitoring: 2
- System Optimization: 7
- File Operations: 4 (2 in hydra)
- Git Operations: 6
- Database: 5
- Semantic: 5
- Orchestration: 3
- Planning/Reporting: 7
- Local AI: 5

**Performance:**
- Fastest: pc-health:quick_status (~0.1s)
- Slowest: local_chat_smart (~10-15s)
- Most complex: hydra:create_execution_plan

**Status:**
- ✅ Working: 42/44 (95%)
- ⊘ Optional: 2/44 (5% - require racing service)

---

**END OF CATALOG**
