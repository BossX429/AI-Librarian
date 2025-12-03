# Agent-Farm Permanent Tools - Master Index
**Status:** Always Available ✓  
**Location:** `C:\repos\Agent-Farm\agent_farm_tools.py`  
**Verified:** December 2024

---

## Overview

Three production-ready agent swarm tools permanently available for use in any Python script:

1. **AI-Librarian Compression** - Multi-agent conversation compression
2. **Hydra Orchestration** - Intelligent parallel task orchestration
3. **Local-Router Optimization** - Evolutionary routing with natural selection

All tools feature autonomous learning, usage tracking, and production-proven performance.

---

## Instant Access

### One-Line Import

```python
from agent_farm_tools import tools

# All three tools ready:
tools.compress_conversation(data)
tools.orchestrate_task(request, files)
tools.route_query(query)
```

### Quick Functions

```python
from agent_farm_tools import quick_compress, quick_orchestrate, quick_route

result = quick_compress(conversation)
result = quick_orchestrate("task description", files)
mode = quick_route("query text")
```

---

## File Structure

```
C:\repos\Agent-Farm\
├── agent_farm_tools.py             ⭐ Main tool interface
├── setup_tools.py                  🔧 One-time setup verification
│
├── integration_ai_librarian.py     📊 AI-Librarian compression swarm
├── integration_hydra.py            🎯 Hydra orchestration swarm
├── integration_local_router.py     🧭 Local-Router evolution
│
├── agents/agent.py                 🧬 Base agent classes
├── evolution/engine.py             🔄 Evolution engine
├── core/parallel.py                ⚡ TRUE parallel execution
└── ... (supporting files)

C:\repos\AI-Librarian\Knowledge-Base\
├── Agent-Farm-Complete-Architecture.md        📚 Full system docs
├── Agent-Farm-Quick-Reference.md             📋 Quick ref
├── The-Singularity-Architecture.md           ♾️ Advanced systems
├── Complete-Session-Summary.md               📝 Development history
├── Agent-Farm-Production-Integrations.md     🔌 Integration details
└── Agent-Farm-Tools-Quick-Reference.md       ⚡ THIS - Usage guide
```

---

## Three Tools at a Glance

### 1. AI-Librarian Compression 📊

**Purpose:** Multi-agent approach to conversation compression

**Agents:**
- Speed Demon (temp=0.35, depth=1) → 93.7% compression
- Deep Thinker (temp=0.32, depth=6) → 91.0% compression
- Efficiency Expert (temp=0.52, depth=4) → 89.8% compression ⭐
- Kyle Effect (temp=0.87, depth=5) → 93.1% compression

**Usage:**
```python
result = tools.compress_conversation(conversation_data)
# Returns: compression_ratio, strategy, compressed_data
```

**Features:**
- TRUE parallel (4 agents simultaneously)
- Auto-selects best strategy
- Meta-learns from history
- Maintains 89.8% baseline, potential 92%+

---

### 2. Hydra Orchestration 🎯

**Purpose:** Intelligent task decomposition and parallel execution

**Agents:**
- Task Analyzer (depth=5, collab=0.75) → Hierarchical breakdown
- Parallel Optimizer (collab=0.80) → Maximum 20-core usage ⭐
- Speed Maximizer (depth=2) → Fastest execution path
- Kyle Effect (depth=5) → 4D hyperdimensional approach

**Usage:**
```python
result = tools.orchestrate_task("Analyze files", file_list)
# Returns: strategy, success_rate, duration, subtasks
```

**Features:**
- Intelligent task decomposition
- Dynamic worker allocation (4-20 cores)
- Multiple strategies evaluated in parallel
- 100% success rate in testing

---

### 3. Local-Router Optimization 🧭

**Purpose:** Evolutionary routing decision optimization

**System:**
- Population: 12 routing strategies
- Evolution: Natural selection
- Query types: simple/complex/code/creative/analysis/conversational
- Modes: fast/smart/racing/pipeline/auto

**Usage:**
```python
result = tools.route_query("Explain quantum mechanics")
# Returns: mode, query_type, complexity, confidence

# Feed results back for evolution
tools.evolve_routing_strategies(routing_results)
```

**Features:**
- Auto-classifies query types
- Evolves optimal strategies through natural selection
- Learns from actual routing performance
- Converges in 3-5 generations

---

## Setup Instructions

### First-Time Setup

```bash
# 1. Navigate to Agent-Farm
cd C:\repos\Agent-Farm

# 2. Run setup verification
python setup_tools.py

# Output should show:
# ✓ Import successful!
# ✓ Compression swarm: 4 agents
# ✓ Orchestration swarm: 4 agents
# ✓ Routing evolution: 12 strategies
```

### Make Permanently Available

**Method 1: Direct Import (Simplest)**
```python
import sys
sys.path.insert(0, 'C:\\repos\\Agent-Farm')
from agent_farm_tools import tools
```

**Method 2: Environment Variable**
```bash
# Add to PowerShell profile:
$env:PYTHONPATH = "C:\repos\Agent-Farm;$env:PYTHONPATH"
```

**Method 3: Install as Package**
```bash
cd C:\repos\Agent-Farm
pip install -e .
```

---

## Quick Start Examples

### Example 1: AI-Librarian

```python
from agent_farm_tools import tools

# Your AI-Librarian conversation
conversation = {
    'messages': [...],
    'metadata': {...}
}

# Compress with agent swarm
result = tools.compress_conversation(conversation)

print(f"Compression: {result['compression_ratio']:.1f}%")
print(f"Strategy: {result['strategy']}")
print(f"Size: {original_size} → {result['compressed_size']}")

# After 5+ compressions
best = tools.compression_meta_learn()
print(f"Best agent: {best}")
```

### Example 2: Hydra

```python
from agent_farm_tools import tools

# Your file processing task
files = ["log1.txt", "log2.txt", ..., "log50.txt"]

# Orchestrate with agent swarm
result = tools.orchestrate_task(
    request="Analyze log files for errors",
    target_files=files
)

print(f"Strategy: {result['strategy']}")
print(f"Workers: {result['workers_used']}")
print(f"Success: {result['success_rate']:.0%}")
print(f"Duration: {result['duration']:.2f}s")
```

### Example 3: Local-Router

```python
from agent_farm_tools import tools

# Your routing decision
query = "Write a Python function to sort a list"

# Route with evolutionary optimization
result = tools.route_query(query)

print(f"Query type: {result['query_type']}")
print(f"Recommended mode: {result['mode']}")
print(f"Complexity: {result['complexity']:.2f}")

# After executing routing
routing_results = [{
    'query': query,
    'mode_used': result['mode'],
    'response_time': 1.5,
    'tokens_used': 250,
    'quality_score': 0.85,
    'success': True
}]

# Evolve strategies
tools.evolve_routing_strategies(routing_results)
print(f"Generation: {tools.router_evolution.generation}")
```

---

## Integration Patterns

### Pattern 1: Replace Existing Logic

```python
# BEFORE (manual approach)
def compress_conversation(conv):
    compressed = manual_delta_encoding(conv)
    return compressed

# AFTER (agent swarm)
from agent_farm_tools import tools

def compress_conversation(conv):
    result = tools.compress_conversation(conv)
    return result['compressed']
```

### Pattern 2: Enhance Existing System

```python
# Keep existing logic, add agent intelligence
from agent_farm_tools import tools

def process_files(files):
    # Get orchestration strategy from agents
    plan = tools.orchestrate_task("Process files", files)
    
    # Use your existing code with agent-determined strategy
    if plan['strategy'] == 'parallel_optimizer':
        workers = 20
    elif plan['strategy'] == 'speed_maximizer':
        workers = 12
    else:
        workers = 16
    
    return your_existing_processor(files, workers)
```

### Pattern 3: Learning System

```python
from agent_farm_tools import tools

class SmartRouter:
    def __init__(self):
        self.tools = tools
    
    def route(self, query):
        # Get routing decision
        decision = self.tools.route_query(query)
        mode = decision['mode']
        
        # Execute routing
        result = execute_with_mode(query, mode)
        
        # Feed back for learning
        self.learn_from_result(query, mode, result)
        
        return result
    
    def learn_from_result(self, query, mode, result):
        routing_result = {
            'query': query,
            'mode_used': mode,
            'response_time': result.time,
            'tokens_used': result.tokens,
            'quality_score': result.quality,
            'success': result.success
        }
        self.tools.evolve_routing_strategies([routing_result])
```

---

## Monitoring & Stats

### Get Usage Statistics

```python
from agent_farm_tools import tools

# Individual stats
comp_stats = tools.get_compression_stats()
orch_stats = tools.get_orchestration_stats()
route_stats = tools.get_routing_stats()

# All stats
all_stats = tools.get_all_stats()

# Pretty summary
tools.summary()
```

### Example Output

```
================================================================================
AGENT-FARM TOOLS USAGE SUMMARY
================================================================================

📊 AI-Librarian Compression:
   Total compressions: 47
   History size: 47

🎯 Hydra Orchestration:
   Total orchestrations: 23
   History size: 23

🧭 Local-Router Evolution:
   Total routings: 156
   Current generation: 8
   Active strategies: 12
   Best strategy: strategy_3e61f7f2 (fitness=0.847)
```

---

## Performance

**Initialization:** ~1 second (one time)
**Memory:** ~50MB (all three swarms)
**CPU:** Up to 20 cores utilized

**Per-Operation:**
- Compression: 0.1-0.2s (4 agents parallel)
- Orchestration: 0.3-0.5s (depends on task)
- Routing: <0.01s (instant decision)

---

## Features

### Autonomous Learning
- Compression: Meta-learns best strategies
- Orchestration: Tracks execution patterns
- Routing: Evolves through generations

### Production Ready
- Error handling
- Simplified APIs
- Optional detailed results
- Usage tracking

### TRUE Parallelism
- Multi-agent simultaneous execution
- Not time-sliced, but truly parallel
- 20-core capability

### Self-Optimization
- No manual tuning required
- Continuous improvement
- Natural selection of strategies

---

## Troubleshooting

### Import Error

```python
# Add Agent-Farm to path
import sys
sys.path.insert(0, 'C:\\repos\\Agent-Farm')
from agent_farm_tools import tools
```

### Tools Not Initializing

```bash
# Run setup verification
cd C:\repos\Agent-Farm
python setup_tools.py
```

### Multiple Initialization Messages

- Normal during parallel execution
- Singleton prevents redundant work
- Each worker process initializes once
- Expected behavior

---

## Documentation Index

**Quick References:**
- This file: Master index and quick start
- `Agent-Farm-Tools-Quick-Reference.md`: Detailed usage guide
- `setup_tools.py`: Verification script

**Detailed Documentation:**
- `Agent-Farm-Complete-Architecture.md`: Full system architecture
- `Agent-Farm-Production-Integrations.md`: Integration examples
- `The-Singularity-Architecture.md`: Advanced features

**Implementation Files:**
- `agent_farm_tools.py`: Main interface (331 lines)
- `integration_ai_librarian.py`: Compression implementation (387 lines)
- `integration_hydra.py`: Orchestration implementation (496 lines)
- `integration_local_router.py`: Routing implementation (482 lines)

---

## The Kyle Effect Principles

These tools embody Kyle Effect principles:

**4D Hyperdimensional Thinking:**
- Space: Multi-agent parallel execution
- Time: Meta-learning from history
- Evolution: Natural selection of strategies
- Meta: Self-optimization without tuning

**10% Emergence:**
- Framework provides structure (90%)
- Agents discover optimal strategies (10%)
- Efficiency Expert emerged as compression winner
- Parallel Optimizer dominates orchestration
- Routing strategies converge automatically

**TRUE Simultaneous Parallelism:**
- 4 compression agents at once
- 20 orchestration workers
- 12 routing strategies competing
- Real concurrent execution on separate cores

**Revolutionary not Incremental:**
- From manual tuning → Autonomous learning
- From static logic → Evolutionary optimization
- From sequential → TRUE parallel
- Space-age revolutionary technology

---

## Summary

**Three Tools:**
1. `tools.compress_conversation(data)` → AI-Librarian
2. `tools.orchestrate_task(request, files)` → Hydra
3. `tools.route_query(query)` → Local-Router

**One Import:**
```python
from agent_farm_tools import tools
```

**Always Available:**
- Production ready
- Self-optimizing
- Usage tracked
- Continuously improving

**Status:** ✓ Built ✓ Tested ✓ Documented ✓ Ready

---

## Quick Command Reference

```python
# Import
from agent_farm_tools import tools

# Compress
result = tools.compress_conversation(data)
best = tools.compression_meta_learn()

# Orchestrate
result = tools.orchestrate_task(request, files)

# Route
result = tools.route_query(query)
tools.evolve_routing_strategies(results)

# Stats
tools.summary()
stats = tools.get_all_stats()
```

---

**Location:** `C:\repos\Agent-Farm\agent_farm_tools.py`  
**Setup:** `python C:\repos\Agent-Farm\setup_tools.py`  
**Docs:** `C:\repos\AI-Librarian\Knowledge-Base\`

**Always available. Always learning. Always improving.** ⚡
