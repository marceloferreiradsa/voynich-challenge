# Use updated image with CUDA 12.1 support
FROM nvcr.io/nvidia/pytorch:24.02-py3

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Preload model (using Hugging Face cache directory)
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
model = SentenceTransformer('all-mpnet-base-v2'); \
model.save('/app/models/mpnet')"

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]