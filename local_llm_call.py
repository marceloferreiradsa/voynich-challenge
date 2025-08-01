import requests
import time
import os
import json
from datetime import datetime

def llm_call_old(prompt, max_tokens=300):
    url = "http://localhost:8001/generate"
    payload = {
        "prompt": prompt,
        "max_new_tokens": max_tokens
    }
    
    try:
        start = time.perf_counter()
        response = requests.post(url, json=payload)
        response_time = time.perf_counter() - start
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response in {response_time:.2f}s | Tokens: {max_tokens}")
            print("Generated text:")
            print("-" * 80)
            print(result['response'])
            print("-" * 80)
            return len(result['response'])
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return 0
            
    except Exception as e:
        print(f"🚫 Connection failed: {str(e)}")
        return 0

def llm_call(prompt, max_tokens=300):
    url = "http://localhost:8001/generate"
    payload = {
        "prompt": prompt,
        "max_new_tokens": max_tokens
    }

    try:
        start = time.perf_counter()
        response = requests.post(url, json=payload)
        response_time = time.perf_counter() - start

        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            print(f"✅ Response in {response_time:.2f}s | Tokens: {max_tokens}")
            print("Generated text:")
            print("-" * 80)
            print(response_text)
            print("-" * 80)
            return response_text  # ✅ return actual string
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return ""
    except Exception as e:
        print(f"🚫 Connection failed: {str(e)}")
        return ""

def save_llm_response(response_text: str,
                      prompt_text: str,
                      output_folder: str,
                      metadata: dict = None,
                      as_jsonl: bool = True):
    """
    Save an LLM response with metadata for later analysis.

    Args:
        response_text (str): The response returned by the LLM.
        prompt_text (str): The input prompt text.
        output_folder (str): Destination folder to save output file.
        metadata (dict): Optional additional metadata to include.
        as_jsonl (bool): If True, save as .jsonl (one record per line). Else, save as .json.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create record with metadata
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt_length": len(prompt_text),
        "response_length": len(response_text),
        "prompt": prompt_text,
        "response": response_text,
        "metadata": metadata or {}
    }
    
    # Generate timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    ext = "jsonl" if as_jsonl else "json"
    filename = f"llm_response_{timestamp}.{ext}"
    filepath = os.path.join(output_folder, filename)
    
    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        if as_jsonl:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        else:
            json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Response saved to: {filepath}")
    return filepath



def append_llm_response(response_text: str,
                        prompt_text: str,
                        output_folder: str,
                        file_name: str = "llm_responses.jsonl",
                        metadata: dict = None):
    """
    Appends an LLM response to a .jsonl file with metadata.

    Args:
        response_text (str): The response returned by the LLM.
        prompt_text (str): The input prompt text.
        output_folder (str): Folder where the .jsonl file is stored.
        file_name (str): Name of the file to append to (default: "llm_responses.jsonl").
        metadata (dict): Optional metadata (e.g., language, tags).
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Prepare structured record
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt_length": len(prompt_text),
        "response_length": len(response_text),
        "prompt": prompt_text,
        "response": response_text,
        "metadata": metadata or {}
    }

    # File path
    file_path = os.path.join(output_folder, file_name)

    # Append to JSONL file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ Appended response to: {file_path}")
    return file_path


def print_gpu_report(api_url="http://localhost:8001/gpu_status"):
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if not data.get("gpu_available", False):
            print("No CUDA-enabled GPU found or GPU not available.")
            return
        
        print(f"Device: {data['device_name']}")
        print(f"PyTorch CUDA Version: {data['torch_cuda_version']}")
        print(f"Memory Allocated: {data['memory_allocated_MB']:.2f} MB")
        print(f"Memory Reserved: {data['memory_reserved_MB']:.2f} MB")
        print(f"Memory Free (reserved - allocated): {data['memory_free_MB']:.2f} MB")
        
        smi = data.get("nvidia_smi_info", {})
        if "error" in smi:
            print(f"nvidia-smi info not available: {smi['error']}")
        else:
            print("\nnvidia-smi info:")
            print(f"  GPU Utilization: {smi['gpu_utilization_percent']}%")
            print(f"  Memory Utilization: {smi['memory_utilization_percent']}%")
            print(f"  Total Memory: {smi['memory_total_MB']} MB")
            print(f"  Memory Free: {smi['memory_free_MB']} MB")
            print(f"  Memory Used: {smi['memory_used_MB']} MB")
            
    except Exception as e:
        print(f"Failed to get GPU status: {e}")

# Run it
print_gpu_report()
