# Webcam MCP — Controle sua câmera pelo Claude Desktop

Permite conversar com o Claude Desktop para capturar fotos pela webcam e ajustar brilho, contraste, exposição e outras configurações em tempo real.

**Sistemas operacionais:** Windows 10/11, macOS 12+, Linux (Ubuntu/Debian)
**Câmera:** Webcam USB externa (melhor compatibilidade) ou câmera interna

---

## O que você pode fazer

Depois de instalar, basta digitar no Claude Desktop como se fosse uma conversa normal:

- *"Tire uma foto pela minha câmera e me diz como está a iluminação"*
- *"Está muito escuro, aumente o brilho para 20 e veja se melhorou"*
- *"Desative o auto-exposure e coloque exposição em -4"*
- *"Quais câmeras estão conectadas no meu computador?"*
- *"Redefina as configurações da câmera para o padrão"*

---

## Pré-requisitos

1. **Python 3.10 ou superior**
   - Baixe em: https://python.org/downloads
   - **Windows:** durante a instalação, marque **"Add Python to PATH"**

2. **Claude Desktop** (o app instalado no computador, não o site)
   - Baixe em: https://claude.ai/download

---

## Instalação

### Passo 1: Baixar o projeto

Se você não usa Git, clique no botão verde **"Code"** no topo desta página e escolha **"Download ZIP"**. Extraia a pasta em algum lugar fácil de encontrar (ex: `C:\Users\SeuUsuario\webcam-mcp`).

Se usa Git:
```bash
git clone https://github.com/danielemaiaa/webcam-mcp.git
```

### Passo 2: Executar o instalador

**Windows:** abra a pasta e clique duas vezes em **`install.bat`**

**macOS / Linux:** abra o Terminal na pasta do projeto e execute:
```bash
chmod +x install.sh && ./install.sh
```

O script instala as dependências e mostra (ou cria automaticamente) o bloco de configuração do Claude Desktop.

---

## Configuração do Claude Desktop

> Se usou o `install.bat` no Windows, ele já mostrou as instruções. Siga o que apareceu no terminal.
> Se usou o `install.sh` no Mac, o config já foi criado automaticamente — pule para o passo 5.

1. Abra o Claude Desktop
2. Vá em **File > Settings > Developer**
3. Clique em **Edit Config** — abre o arquivo `claude_desktop_config.json`
4. Cole o conteúdo abaixo (ajuste o caminho do `server.py` para onde você salvou a pasta):

**Windows:**
```json
{
  "mcpServers": {
    "webcam": {
      "command": "python",
      "args": ["C:\\Users\\SeuUsuario\\webcam-mcp\\server.py"]
    }
  }
}
```

**macOS / Linux:**
```json
{
  "mcpServers": {
    "webcam": {
      "command": "python3",
      "args": ["/Users/SeuUsuario/webcam-mcp/server.py"]
    }
  }
}
```

5. Salve o arquivo
6. **Feche e reabra** o Claude Desktop

**Como confirmar que funcionou:** aparece um ícone de martelo na parte inferior da janela de chat. Clique nele para ver as ferramentas disponíveis. Se não aparecer, veja a seção de problemas comuns abaixo.

---

## Como usar

Não há comandos para decorar. Basta conversar normalmente com o Claude Desktop. Exemplos:

**Para verificar a câmera:**
> "Quais câmeras estão conectadas?"
> "Me mostra as configurações atuais da câmera"

**Para tirar uma foto e analisar:**
> "Tire uma foto e me diz o que está ruim"

**Para ajustar:**
> "Aumente o brilho para 20"
> "Desative o auto-exposure e coloque exposição em -5"
> "Aumente o contraste para 50"

**Para voltar ao padrão:**
> "Redefina a câmera para as configurações padrão"

---

## Referência de valores

| Configuração | Faixa típica | Padrão |
|---|---|---|
| `brightness` | -64 a 64 | 0 |
| `contrast` | 0 a 64 | 32 |
| `saturation` | 0 a 100 | 64 |
| `exposure` | Windows/Mac: -11 a -1 · Linux: 1–10000µs | automático |
| `sharpness` | 0 a 100 | 50 |
| `gain` | 0 a 100 | 0 |

> Os valores exatos variam por modelo de webcam. Se um ajuste não surtir efeito, a câmera não suporta aquele controle via software.

---

## Sequência recomendada para gravar aulas

1. "Tire uma foto e me diz o que está ruim na imagem"
2. "Desative o auto-exposure"
3. "Coloque exposure em -5 e brightness em 10"
4. "Tire outra foto — melhorou?"
5. Repita até ficar bom

---

## Problemas comuns

**Ícone de martelo não aparece**
- Verifique se o caminho do `server.py` no config está correto e completo
- Windows: use barras duplas `\\` no caminho
- Reinicie o Claude Desktop após salvar o config

**"Nenhuma câmera encontrada"**
- Confirme que a webcam aparece no Gerenciador de Dispositivos (Windows) ou em Preferências do Sistema > Câmera (Mac)
- Feche outros programas que podem estar usando a câmera (Teams, Zoom, OBS)

**Erro ao instalar dependências**
- Windows: execute o Prompt de Comando como Administrador
- Tente `pip install --upgrade pip` antes de instalar os requisitos

**Ajustes não funcionam mesmo conectando**
- Webcams internas de notebook têm suporte limitado a controles via software
- Webcams USB externas (Logitech, Razer etc.) têm muito mais compatibilidade

---

## Limitações

- Para câmeras Blackmagic profissionais (URSA, PYXIS etc.), use a [REST API oficial](https://documents.blackmagicdesign.com/DeveloperManuals/RESTAPIforBlackmagicCameras.pdf)
- Pocket Cinema Camera não tem REST API — só Bluetooth/SDI
