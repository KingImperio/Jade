c = open('scripts/install.ps1', 'r', encoding='utf-8').read()

c = c.replace('\ = "git@github.com:NousResearch/hermes-agent.git"', '\ = "git@github.com:KingImperio/Jade.git"')
c = c.replace('\ = "https://github.com/NousResearch/hermes-agent.git"', '\ = "https://github.com/KingImperio/Jade.git"')

c = c.replace('\u2502             \u2695 Hermes Agent Installer                    \u2502', '\u2502             \u25c6 Jade Installer                              \u2502')
c = c.replace('https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1', 'https://raw.githubusercontent.com/KingImperio/Jade/main/scripts/install.ps1')
c = c.replace('https://github.com/NousResearch/hermes-agent/archive/refs/heads/', 'https://github.com/KingImperio/Jade/archive/refs/heads/')

open('scripts/install.ps1', 'w', encoding='utf-8').write(c)
print('install.ps1 done')
