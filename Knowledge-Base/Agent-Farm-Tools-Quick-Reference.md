# Agent-Farm Tools - Always Available Quick Reference
**Location:** `C:\repos\Agent-Farm\agent_farm_tools.py`  
**Status:** Production Ready - Use Anytime

---

## Quick Import

```python
# Option 1: Full access
from agent_farm_tools import AgentFarmTools
tools = AgentFarmTools()

# Option 2: Quick functions
from agent_farm_tools import quick_compress, quick_orchestrate, quick_route

# Option 3: Pre-initialized global instance
from agent_farm_tools import tools
```

---

## Three Tools Always Available

### 1. AI-Librarian Compression 📊

**Compress conversations with multi-agent swarm:**

```python
from agent_farm_tools import tools

# Basic compression
result = tools.compress_conversation(conversation_data)
print(f"Compression: {result['compression_ratio']:.1f}%")
print(f"Strategy: {result['strategy']}")

# With full analysis
result = tools.compress_conversation(
    conversation_data, 
    use_parallel=True,
    return_analysis=True
)

# Meta-learning (run after 5+ compressions)
best_agent = tools.compression_meta_learn()
print(f"Best agent: {best_agent}")

# Get stats
stats = tools.get_compression_stats()
print(f"Total compressions: {stats['total_compressions']}")
```

**Quick version:**
```python
from agent_farm_tools import quick_compress

result = quick_compress(conversation_data)
```

### 2. Hydra Orchestration 🎯

**Intelligent parallel task orchestration:**

```python
from agent_farm_tools import tools

# Basic orchestration
result = tools.orchestrate_task(
    request="Analyze log files for errors",
    target_files=list_of_files
)
print(f"Strategy: {result['strategy']}")
print(f"Success: {result['success_rate']:.0%}")

# With full details
result = tools.orchestrate_task(
    request="Complex analysis task",
    target_files=files,
    return_details=True
)

# Get stats
stats = tools.get_orchestration_stats()
print(f"Total orchestrations: {stats['total_orchestrations']}")
```

**Quick version:**
```python
from agent_farm_tools import quick_orchestrate

result = quick_orchestrate("Process files", file_list)
```

### 3. Local-Router Optimization 🧭

**Evolutionary routing with natural selection:**

```python
from agent_farm_tools import tools

# Basic routing
result = tools.route_query("Explain quantum mechanics")
print(f"Mode: {result['mode']}")
print(f"Query type: {result['query_type']}")
print(f"Confidence: {result['confidence']:.2f}")

# With reasoning
result = tools.route_query(
    query="Write a Python function",
    query_type="code",  # Optional: simple/complex/code/creative/analysis/conversational
    return_reasoning=True
)
print(f"Reasoning: {result['reasoning']}")

# Evolve strategies (after routing execution)
routing_results = [
    {
        'query': 'test',
        'mode_used': 'fast',
        'response_time': 1.0,
        'tokens_used': 100,
        'quality_score': 0.8,
        'success': True
    }
]
tools.evolve_routing_strategies(routing_results)

# Get stats
stats = tools.get_routing_stats()
print(f"Generation: {stats['generation']}")
print(f"Best strategy: {stats['best_strategy']}")
```

**Quick version:**
```python
from agent_farm_tools import quick_route

mode = quick_route("What is 2+2?")  # Returns just the mode
```

---

## Get All Stats

```python
from agent_farm_tools import tools

# Summary of all usage
tools.summary()

# Or get structured stats
stats = tools.get_all_stats()
print(stats['compression'])
print(stats['orchestration'])
print(stats['routing'])
```

---

## Integration Examples

### AI-Librarian Integration

```python
# In your AI-Librarian code:
from agent_farm_tools import tools

def compress_conversation(conversation):
    # Old manual compression
    # compressed = manual_compress(conversation)
    
    # New agent swarm compression
    result = tools.compress_conversation(conversation)
    
    return result['compressed'], result['compression_ratio']

# Periodic meta-learning
if compression_count % 10 == 0:
    best = tools.compression_meta_learn()
    print(f"Optimal agent: {best}")
```

### Hydra Integration

```python
# In your Hydra code:
from agent_farm_tools import tools

def execute_parallel_task(request, files):
    # Old manual decomposition
    # tasks = manual_decompose(request, files)
    # results = execute_tasks(tasks, workers=20)
    
    # New agent orchestration
    result = tools.orchestrate_task(request, files)
    
    return result['results'], result['success_rate']
```

### Local-Router Integration

```python
# In your Local-Router code:
from agent_farm_tools import tools

def route_query(query):
    # Old manual routing
    # if is_simple(query):
    #     mode = "fast"
    # elif is_complex(query):
    #     mode = "racing"
    
    # New evolutionary routing
    result = tools.route_query(query)
    mode = result['mode']
    
    return mode

# After execution, feed results back
def post_execution_callback(query, mode, performance):
    results = [{
        'query': query,
        'mode_used': mode,
        'response_time': performance['time'],
        'tokens_used': performance['tokens'],
        'quality_score': performance['quality'],
        'success': performance['success']
    }]
    tools.evolve_routing_strategies(results)
```

---

## Making It Permanently Available

### Method 1: Add to Python Path

```python
# Add to your .bashrc or .zshrc or PowerShell profile
export PYTHONPATH="C:\repos\Agent-Farm:$PYTHONPATH"

# Then from anywhere:
from agent_farm_tools import tools
```

### Method 2: Install as Package (Recommended)

```bash
# In C:\repos\Agent-Farm
pip install -e .

# Then from anywhere:
from agent_farm_tools import tools
```

### Method 3: Direct Import

```python
import sys
sys.path.insert(0, 'C:\\repos\\Agent-Farm')
from agent_farm_tools import tools
```

---

## Usage Patterns

### Pattern 1: One-Off Usage

```python
from agent_farm_tools import quick_compress, quick_orchestrate, quick_route

# Quick compression
result = quick_compress(conversation)

# Quick orchestration
result = quick_orchestrate("Analyze files", files)

# Quick routing
mode = quick_route("What is AI?")
```

### Pattern 2: Persistent Session

```python
from agent_farm_tools import tools

# Tools initialize once
# Reuse throughout session

result1 = tools.compress_conversation(conv1)
result2 = tools.compress_conversation(conv2)
result3 = tools.compress_conversation(conv3)

# Meta-learn after multiple uses
tools.compression_meta_learn()
tools.summary()
```

### Pattern 3: Production Integration

```python
# In your main application
from agent_farm_tools import AgentFarmTools

class MyApp:
    def __init__(self):
        self.agent_tools = AgentFarmTools()
    
    def process_data(self, data):
        # Use throughout app lifetime
        compressed = self.agent_tools.compress_conversation(data)
        return compressed
```

---

## Features

**Singleton Pattern:**
- Tools initialize once, reuse forever
- No redundant initialization
- Maintains state across calls

**Auto-Learning:**
- Compression: Meta-learns best strategies
- Orchestration: Tracks execution patterns
- Routing: Evolves through generations

**Statistics Tracking:**
- Usage counts
- Best performers
- History sizes
- Evolution progress

**Production Ready:**
- Error handling
- Simplified results
- Optional detailed analysis
- Flexible return formats

---

## Performance

**Initialization:** ~1 second (one time)
**Compression:** 0.1-0.2s (parallel)
**Orchestration:** 0.3-0.5s (depends on tasks)
**Routing:** <0.01s (instant)

**Memory:** ~50MB (all three swarms loaded)
**CPU:** Uses up to 20 cores in parallel

---

## Tips

**For AI-Librarian:**
- Run meta-learning every 5-10 compressions
- Monitor which agent wins most often
- System converges on optimal strategy

**For Hydra:**
- Let agents determine worker count
- Don't override parallel_optimizer choice
- Trust agent analysis

**For Local-Router:**
- Feed routing results back regularly
- Evolution improves after 3-5 generations
- Watch fitness scores increase

---

## Troubleshooting

**Import Error:**
```python
# Make sure Agent-Farm is in path
import sys
sys.path.insert(0, 'C:\\repos\\Agent-Farm')
from agent_farm_tools import tools
```

**Multiple Initializations:**
- Normal during parallel execution
- Singleton prevents redundant work
- Each worker process initializes once

**Slow First Call:**
- Tools initialize on first import (~1s)
- Subsequent calls are instant
- Expected behavior

---

## Summary

**Three tools, always available:**

1. **tools.compress_conversation(data)** → AI-Librarian compression
2. **tools.orchestrate_task(request, files)** → Hydra orchestration  
3. **tools.route_query(query)** → Local-Router optimization

**All with:**
- Automatic learning
- Usage tracking
- Statistics reporting
- Production-ready APIs

**Import once, use forever.**

---

## Example Session

```python
# Start Python
>>> from agent_farm_tools import tools

# Compress
>>> result = tools.compress_conversation(my_conversation)
>>> print(f"Saved {result['compression_ratio']:.1f}%")

# Orchestrate
>>> result = tools.orchestrate_task("Analyze logs", log_files)
>>> print(f"Strategy: {result['strategy']}, Success: {result['success_rate']:.0%}")

# Route
>>> result = tools.route_query("Write a Python script")
>>> print(f"Mode: {result['mode']}, Type: {result['query_type']}")

# Stats
>>> tools.summary()

# That's it - all three tools ready to use!
```

---

**Location:** `C:\repos\Agent-Farm\agent_farm_tools.py`  
**Documentation:** `C:\repos\AI-Librarian\Knowledge-Base\Agent-Farm-Tools-Quick-Reference.md`

**Ready to use. Always available. Production proven.** ✓
