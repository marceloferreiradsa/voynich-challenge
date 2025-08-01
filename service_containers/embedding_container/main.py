from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch
import time  # Add this import

print(f"\n=== GPU STATUS ===")
print(f"• CUDA available: {torch.cuda.is_available()}")
print(f"• GPU count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"• Current device: {torch.cuda.current_device()} → {torch.cuda.get_device_name(0)}")
    print(f"• CUDA version: {torch.version.cuda}")
    print(f"• PyTorch CUDA supported: {torch.cuda.is_available()}")
    print(f"• GPU memory: {torch.cuda.get_device_properties(0).total_memory/1e9:.2f} GB")
print("=================\n")

app = FastAPI()

# Check GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('/app/models/mpnet', device=device)
print(f"Model loaded on device: {device}")

class EmbedRequest(BaseModel):
    texts: list[str]

@app.post("/embed")
def embed(req: EmbedRequest):
    try:
        # ===== GPU DIAGNOSTICS START =====
        print("\n=== EMBEDDING START ===")
        print(f"Processing {len(req.texts)} texts")
        
        # Pre-execution diagnostics
        if torch.cuda.is_available():
            initial_mem_alloc = torch.cuda.memory_allocated()
            initial_mem_reserved = torch.cuda.memory_reserved()
            initial_utilization = torch.cuda.utilization()
            print(f"Pre-execution GPU memory: {initial_mem_alloc/1e6:.2f} MB allocated, {initial_mem_reserved/1e6:.2f} MB reserved")
            print(f"GPU utilization: {initial_utilization}%")
        
        start_time = time.perf_counter()
        # ===== MAIN EMBEDDING OPERATION =====
        embeddings = model.encode(req.texts, convert_to_tensor=False)
        processing_time = time.perf_counter() - start_time
        # ===== END EMBEDDING OPERATION =====
        
        # Post-execution diagnostics
        print(f"Embedding completed in {processing_time:.4f} seconds")
        print(f"Avg time per text: {processing_time/len(req.texts):.4f} sec")
        
        if torch.cuda.is_available():
            final_mem_alloc = torch.cuda.memory_allocated()
            final_mem_reserved = torch.cuda.memory_reserved()
            final_utilization = torch.cuda.utilization()
            
            print(f"Post-execution GPU memory: {final_mem_alloc/1e6:.2f} MB allocated, {final_mem_reserved/1e6:.2f} MB reserved")
            print(f"Memory delta: {(final_mem_alloc - initial_mem_alloc)/1e6:.2f} MB allocated, {(final_mem_reserved - initial_mem_reserved)/1e6:.2f} MB reserved")
            print(f"GPU utilization: {final_utilization}%")
            
            # Verify tensor operations device
            try:
                test_tensor = torch.tensor([1.0, 2.0, 3.0], device=device)
                print(f"Test tensor created on: {test_tensor.device}")
                if test_tensor.device.type == 'cuda':
                    print("✅ GPU tensor operations confirmed")
            except Exception as e:
                print(f"❌ Tensor test failed: {str(e)}")
        
        print("========================\n")
        # ===== GPU DIAGNOSTICS END =====
        
        return {"vectors": [vec.tolist() for vec in embeddings]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))