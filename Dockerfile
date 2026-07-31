# SWAL Skills — Development Container
# Portable environment for skill validation, POML linting, and benchmark runs.
#
# Build:
#   docker build -t swal-skills .
#
# Run interactively:
#   docker run -it --rm -v $(pwd):/app swal-skills bash
#
# Run skill provider:
#   docker run --rm swal-skills node _registry/skill-provider.js list --public
#
# Run POML validation:
#   docker run --rm -v $(pwd):/app swal-skills python scripts/check_poml_headers.py -- poml/**/*.poml

FROM python:3.11-slim

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=20.x

# Install system deps: git, curl, node.js 20
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify versions
RUN python --version && node --version && npm --version && git --version

# Set working directory
WORKDIR /app

# Copy dependency manifests first (layer caching)
COPY package*.json ./
COPY scripts/ ./scripts/

# Install Node dependencies (husky, lint-staged)
RUN npm install

# Install Python optional dependencies used by scripts
RUN pip install --no-cache-dir pyyaml

# Copy the rest of the project
COPY . .

# Run init.sh if the user wants a full bootstrap, but do not auto-execute it
# so that .env creation remains an explicit choice.
RUN chmod +x init.sh

# Default command: show skill provider help
CMD ["node", "_registry/skill-provider.js"]
