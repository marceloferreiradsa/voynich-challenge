from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LLM_API")

app = FastAPI()

# --- Device Configuration ---
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")
logger.info(f"PyTorch version: {torch.__version__}")
logger.info(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    logger.info(f"CUDA version: {torch.version.cuda}")

# --- Load LLM Model ---
llm_model = None
llm_tokenizer = None
llm_pipeline = None

def load_llm():
    global llm_model, llm_tokenizer, llm_pipeline
    try:
        logger.info("Loading LLM model...")
        llm_model_name = "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
        
        # Clear cache before loading
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Load model with basic configuration
        llm_model = AutoModelForCausalLM.from_pretrained(
            llm_model_name,
            device_map="auto",
            trust_remote_code=False
        )
        
        llm_tokenizer = AutoTokenizer.from_pretrained(
            llm_model_name, 
            use_fast=True
        )
        
        # Create text generation pipeline
        llm_pipeline = pipeline(
        "text-generation",
        model=llm_model,
        tokenizer=llm_tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15,
        do_sample=True,  
        pad_token_id=llm_tokenizer.eos_token_id  
        )
        logger.info("LLM pipeline ready")
        return True
    except Exception as e:
        logger.error(f"LLM load failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

# Load the model at startup
if torch.cuda.is_available():
    if not load_llm():
        logger.error("Failed to load LLM. Exiting...")
        exit(1)
else:
    logger.error("No GPU available. LLM requires CUDA.")
    exit(1)

# --- Pydantic Models ---
class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 256

# --- LLM Generation Endpoint ---
@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        logger.info(f"\n=== GENERATING {req.max_new_tokens} TOKENS ===")
        
        # Format for Mistral instruction following
        formatted_prompt = f"[INST] {req.prompt} [/INST]"
        
        start_time = time.perf_counter()
        
        # Generate response
        outputs = llm_pipeline(
            formatted_prompt,
            max_new_tokens=req.max_new_tokens
        )
        response = outputs[0]['generated_text']
        
        # Extract only the response after [/INST]
        if "[/INST]" in response:
            response = response.split("[/INST]", 1)[1].strip()
        
        processing_time = time.perf_counter() - start_time
        
        logger.info(f"Generated {len(response)} chars in {processing_time:.2f}s")
        return {"response": response}
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ready" if llm_pipeline else "error",
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available()
    }