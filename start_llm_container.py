import subprocess
import time

container_name = "voynich_llm_api"

# Start the container in detached mode with volume and GPU access
print("Starting container...")

subprocess.run([
    "docker", "run", "-d", "--rm", "--gpus", "all",
    "--ipc=host", "--ulimit", "memlock=-1",
    "--ulimit", "stack=67108864",
    "--platform", "linux/amd64",
    "-e", "NVIDIA_VISIBLE_DEVICES=all",
    "-p", "8001:8001",
    "--name", container_name,
    "-v", "voynich-model-cache:/app/models/hf_cache",
    "voynich-llm"
])

# Wait briefly to allow container to boot up
time.sleep(2)

# Show initial logs (non-blocking)
print("\nContainer logs:")
log_process = subprocess.run([
    "docker", "logs", container_name
], text=True, capture_output=True)

print(log_process.stdout)
