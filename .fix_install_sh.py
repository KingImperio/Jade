import sys
c = open('scripts/install.sh', 'r', encoding='utf-8').read()

# Header
c = c.replace('# Hermes Agent Installer\n# ============================================================================', '# Jade Installer\n# ============================================================================')

# Usage example URL
c = c.replace('https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh', 'https://raw.githubusercontent.com/KingImperio/Jade/main/scripts/install.sh')

# REPO URLs
c = c.replace('REPO_URL_SSH="git@github.com:NousResearch/hermes-agent.git"', 'REPO_URL_SSH="git@github.com:KingImperio/Jade.git"')
c = c.replace('REPO_URL_HTTPS="https://github.com/NousResearch/hermes-agent.git"', 'REPO_URL_HTTPS="https://github.com/KingImperio/Jade.git"')

# Banner
c = c.replace('\u2502             \u2695 Hermes Agent Installer                    \u2502', '\u2502             \u25c6 Jade Installer                              \u2502')

# Windows hint
c = c.replace('irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex', 'irm https://raw.githubusercontent.com/KingImperio/Jade/main/scripts/install.ps1 | iex')

# Help text
c = c.replace('echo "Hermes Agent Installer"', 'echo "Jade Installer"')

# Nous Research attribution
c = c.replace('echo "\u2502  An open source AI agent by Nous Research.              \u2502"', 'echo "\u2502  An open source AI agent by Nous Research.              \u2502"')
# Keep the Nous attribution — it's accurate: Jade is built on Nous Research tech

open('scripts/install.sh', 'w', encoding='utf-8').write(c)
print('install.sh done')
