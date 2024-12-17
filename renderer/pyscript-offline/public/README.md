# UNLWS Renderer
A tool to specify UNLWS texts in code and display them.

## Setup

1. Clone the repo
2. Open a terminal in `.../unlws/renderer/pyscript-offline/`
3. Start a local web server. If you have Python installed, this can be done by running the shell script `run_local_server.sh`
4. Go to `http://localhost:8000` in your browser

Each time the site is loaded, it will download a WebAssembly-based Python runtime (via PyScript), so expect to wait a while.
If you make changes to the code but don't see the updates in the browser, the issue may be due to caching (browsers store files to improve performance). You can disable caching in your browser's developer tools to ensure you're loading the latest version of your code.
