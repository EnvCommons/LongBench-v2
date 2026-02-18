from pathlib import Path
import os
# Production (default)
# ENV_PATH = Path("/orwd_data")

# Local development (uncomment for testing)

if os.path.exists("/orwd_data"):
    ENV_PATH = Path("/orwd_data")
else:
    ENV_PATH = Path(__file__).parent

