# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git (needed for some pip installs if applicable)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . .

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# Expose the default port for HTTP transport
EXPOSE 8000

# Set environment variables (defaults, can be overridden)
ENV MCP_TRANSPORT=http

# Default command to run the server in HTTP mode
# Use 0.0.0.0 to allow external access within the container network
ENTRYPOINT ["upstox-mcp"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
