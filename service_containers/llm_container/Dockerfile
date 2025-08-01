# Use your existing EMBEDDING image as base
FROM voynich-embed:cuda12-1

# Set working directory
WORKDIR /app

# Install system dependencies for LLM
RUN apt-get update && apt-get install -y g++ make cmake

# Copy LLM-specific requirements
COPY requirements_llm.txt .

# Install only LLM-specific dependencies
RUN pip install --no-cache-dir -r requirements_llm.txt

# Copy LLM application code
COPY llm_api.py .

# Set Hugging Face cache location
ENV HF_HOME=/app/models/hf_cache
ENV TRANSFORMERS_CACHE=/app/models/hf_cache
RUN mkdir -p /app/models/hf_cache

# Change port for LLM service
CMD ["uvicorn", "llm_api:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"]