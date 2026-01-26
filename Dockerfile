# Use official Python slim image (3.12+ required for new pandas-ta)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install git (needed for some pip installs if applicable)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . .

# Upgrade pip and install the package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Expose the default port for HTTP transport
EXPOSE 8000

# Set environment variables (defaults, can be overridden)
ENV MCP_TRANSPORT=http

# Default command to run the server in HTTP mode
# Use 0.0.0.0 to allow external access within the container network
ENTRYPOINT ["upstox-mcp"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
