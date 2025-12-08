import sys
import time
import psutil
# TITAN-Powered MCP Health Monitor
# Parallel health checks across all 16 MCP servers


MCP_SERVERS = [
    "nexus",
    "agent-farm",
    "semantic-memory",
    "pc-health",
    "pc-optimization",
    "log-surgeon",
    "git-automation",
    "database-query",
    "file-scout",
    "titan-analyzer",
    "titan-fs",
    "codebase-intelligence",
    "code-generator",
    "network-monitor",
    "auto-orchestrator",
    "autonomous-sales-agent"
]

def check_server_health(server_name):
    """Check if MCP server is running - parallel check"""
    try:
        # Look for python process running this server
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] in ['python.exe', 'python3.exe']:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if server_name in cmdline.lower():
                        return ('alive', server_name, proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return ('dead', server_name, None)
        
    except Exception as e:
        return ('error', server_name, str(e))

def main():
    start = time.time()
    
    # PARALLEL HEALTH CHECKS - All 16 servers checked simultaneously
    results = {
        'alive': [],
        'dead': [],
        'error': []
    }
    
    with ProcessPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_server_health, server): server for server in MCP_SERVERS}
        
        for future in as_completed(futures):
            status, server, info = future.result()
            results[status].append((server, info))
    
    duration = time.time() - start
    
    # Log results
    log_path = Path('C:/repos/AI-Librarian/logs/mcp_health.log')
    log_path.parent.mkdir(exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_path, 'a') as f:
        if results['dead'] or results['error']:
            f.write(f"{timestamp} - TITAN: ⚠️ Issues detected in {duration:.2f}s:\\n")
            f.write(f"   Alive: {len(results['alive'])}\\n")
            f.write(f"   Dead: {len(results['dead'])} - {[s for s, _ in results['dead']]}\\n")
            f.write(f"   Errors: {len(results['error'])} - {[s for s, _ in results['error']]}\\n")
        else:
            f.write(f"{timestamp} - TITAN: ✅ All {len(results['alive'])} servers healthy (checked in {duration:.2f}s)\\n")
    
    print(f"✅ TITAN MCP Health Check ({duration:.2f}s):")
    print(f"   Alive: {len(results['alive'])}")
    print(f"   Dead: {len(results['dead'])}")
    print(f"   Errors: {len(results['error'])}")
    
    if results['dead']:
        print(f"   ⚠️ Dead servers: {[s for s, _ in results['dead']]}")

if __name__ == "__main__":
    main()
