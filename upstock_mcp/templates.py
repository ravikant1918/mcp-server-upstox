HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upstox MCP Server | Modern AI Day</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --code-bg: #1e293b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 0% 0%, rgba(37, 99, 235, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, rgba(37, 99, 235, 0.1) 0%, transparent 50%);
            overflow-x: hidden;
        }

        .container {
            max-width: 800px;
            width: 90%;
            padding: 2.5rem;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border-radius: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            animation: fadeIn 0.8s ease-out;
            margin: 2rem 0;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo {
            font-size: 3.5rem;
            margin-bottom: 1rem;
        }

        h1 {
            font-size: 2.25rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p {
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }

        .badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: rgba(37, 99, 235, 0.2);
            color: #60a5fa;
            border-radius: 2rem;
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(37, 99, 235, 0.3);
        }

        .links {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        @media (max-width: 600px) {
            .links { grid-template-columns: 1fr; }
        }

        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s;
            border: 1px solid transparent;
            cursor: pointer;
            font-family: inherit;
        }

        .btn-primary {
            background-color: var(--primary);
            color: white;
            grid-column: span 2;
        }

        @media (max-width: 600px) {
            .btn-primary { grid-column: span 1; }
        }

        .btn-primary:hover {
            background-color: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        }

        .btn-outline {
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(255, 255, 255, 0.1);
            color: var(--text);
        }

        .btn-outline:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .mcp-config-section {
            display: none;
            text-align: left;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideDown 0.5s ease-out;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .mcp-config-section.active {
            display: block;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #60a5fa;
        }

        .code-block-container {
            position: relative;
            background: var(--code-bg);
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        pre {
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            color: #e2e8f0;
            line-height: 1.5;
        }

        .copy-btn {
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: var(--text);
            padding: 0.4rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        .instructions {
            background: rgba(37, 99, 235, 0.05);
            border-radius: 0.75rem;
            padding: 1.25rem;
            font-size: 0.95rem;
        }

        .instructions h3 {
            font-size: 1rem;
            margin-bottom: 0.75rem;
            color: var(--text);
        }

        .instructions ol {
            padding-left: 1.25rem;
            color: var(--text-muted);
        }

        .instructions li {
            margin-bottom: 0.5rem;
        }

        .footer {
            margin-top: 2.5rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }

        .footer a {
            color: #60a5fa;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📈</div>
        <div class="badge">Modern AI Day Edition</div>
        <h1>Upstox MCP Server</h1>
        <p>A high-performance Model Context Protocol server enabling AI agents to reason over real-time Indian market data.</p>
        
        <div class="links">
            <button onclick="toggleConfig()" class="btn btn-primary">
                🔌 Connect to MCP Endpoint
            </button>
            <a href="https://medium.com/@ravikantyadav1918/the-usb-port-for-ai-how-the-upstox-mcp-server-connects-claude-to-real-time-market-data-ba179358e891" target="_blank" class="btn btn-outline">
                📖 Read Article
            </a>
            <a href="https://github.com/ravikant1918/mcp-server-upstox" target="_blank" class="btn btn-outline">
                ⭐ GitHub
            </a>
        </div>

        <div id="mcpConfig" class="mcp-config-section">
            <h2 class="section-title">MCP Configuration (Remote BYOK)</h2>
            <div class="code-block-container">
                <button class="copy-btn" onclick="copyConfig(this)">Copy JSON</button>
                <pre id="configJson">{
  "mcpServers": {
    "Upstox-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp-server-upstox.onrender.com/mcp",
        "--header", "X-Upstox-API-Key:YOUR_API_KEY",
        "--header", "X-Upstox-API-Secret:YOUR_API_SECRET",
        "--header", "X-Upstox-Access-Token:YOUR_ACCESS_TOKEN"
      ]
    }
  }
}</pre>
            </div>

            <div class="instructions">
                <h2 class="section-title">How to Connect</h2>
                
                <p style="margin-bottom: 1rem; font-size: 0.95rem;">This server supports <strong>Bring Your Own Key (BYOK)</strong>. You can use your own credentials without configuring them on the server side.</p>

                <h3>Claude Desktop (Remote)</h3>
                <ol>
                    <li>Open Claude Desktop configuration file:
                        <ul>
                            <li>macOS: <code>~/Library/Application Support/Claude/claude_desktop_config.json</code></li>
                            <li>Windows: <code>%APPDATA%\\Claude\\claude_desktop_config.json</code></li>
                        </ul>
                    </li>
                    <li>Paste the JSON configuration above.</li>
                    <li>Replace the <code>YOUR_...</code> placeholders with your actual Upstox credentials.</li>
                    <li>Restart Claude Desktop.</li>
                </ol>

                <h3 style="margin-top: 1.5rem;">Local Connection (stdio)</h3>
                <ol>
                    <li>If you are running the server locally, you can pass credentials via the <code>env</code> block in your config.</li>
                    <li>The server will automatically detect and use these variables.</li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            Built with ❤️ for the AI & FinTech community.
        </div>
    </div>

    <script>
        function toggleConfig() {
            const section = document.getElementById('mcpConfig');
            section.classList.toggle('active');
            if (section.classList.contains('active')) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }

        async function copyConfig(btn) {
            const config = document.getElementById('configJson').innerText;
            try {
                await navigator.clipboard.writeText(config);
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                btn.style.background = '#059669';
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.background = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy: ', err);
            }
        }
    </script>
</body>
</html>
"""
