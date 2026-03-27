# =============================================================================
# Browntone — FEniCSx Development Environment
# =============================================================================
# Based on the official DOLFINx Docker image with additional project deps.
#
# Build:  docker build -f docker/Dockerfile -t browntone:latest .
# Run:    docker run --rm -it -v $(pwd):/work browntone:latest bash
# =============================================================================

FROM dolfinx/dolfinx:v0.8.0

LABEL maintainer="jon"
LABEL description="Browntone: FEniCSx environment for abdominal cavity simulations"

# System packages for mesh generation and visualisation
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglu1-mesa \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /work

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Install browntone with all dependencies (FEniCSx already in base image)
RUN pip install --no-cache-dir -e ".[dev,notebooks]"

# Copy remaining project files
COPY . .

# Default command
CMD ["bash"]
