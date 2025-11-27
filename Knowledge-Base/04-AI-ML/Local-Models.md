# Local Models & Ollama

## Ollama Setup
**Status:** Not yet installed

### Installation
```powershell
# Download from https://ollama.ai
# Install and verify
ollama --version
```

### Common Commands
```bash
# List installed models
ollama list

# Pull a model
ollama pull llama2
ollama pull codellama
ollama pull mistral

# Run a model
ollama run llama2

# Remove a model
ollama rm modelname
```

## Model Selection for AMD 7900XTX (24GB VRAM)

### Recommended Models
- **7B models:** Fast, efficient for most tasks
- **13B models:** Good balance of capability and speed
- **34B models:** Maximum capability within VRAM limits
