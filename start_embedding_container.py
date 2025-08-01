import subprocess
import time

container_name = "voynich_api"

# Start the container in detached mode
print("Starting container...")
subprocess.run([
    "docker", "run", "-d", "--rm", "--gpus", "all",
    "--ipc=host", "--ulimit", "memlock=-1", "--ulimit", "stack=67108864",
    "--platform", "linux/amd64",
    "-e", "NVIDIA_VISIBLE_DEVICES=all",
    "-p", "8000:8000",
    "--name", container_name,
    "voynich-embed:cuda12-1"
])

# Wait briefly to allow container to boot up
time.sleep(2)

# Show initial logs (non-blocking)
print("\nContainer logs:")
log_process = subprocess.run([
    "docker", "logs", container_name
], text=True, capture_output=True)

print(log_process.stdout)
