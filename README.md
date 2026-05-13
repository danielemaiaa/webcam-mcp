# Webcam MCP — Controle sua câmera pelo Claude Desktop

Permite conversar com o Claude Desktop para capturar imagens da webcam e ajustar brilho, contraste, exposição e outras configurações em tempo real.

**Sistemas operacionais:** Windows 10/11, macOS 12+, Linux (Ubuntu/Debian)
**Câmera:** Webcam USB externa (melhor compatibilidade) ou câmera interna

---

## O que você pode fazer

Depois de instalar, basta digitar no Claude Desktop:

- *"Tire uma foto pela minha câmera e me diz como está a iluminação"*
- *"Está muito escuro, aumente o brilho para 20 e veja se melhorou"*
- *"Desative o auto-exposure e coloque exposição em -4"*
- *"Quais câmeras estão conectadas no meu computador?"*
- *"Redefina as configurações da câmera para o padrão"*

---

## Pré-requisitos

1. **Python 3.10 ou superior**
   - Baixe em: https://python.org/downloads
   - Durante a instalação, marque **"Add Python to PATH"**

2. **Claude Desktop** (app instalado, não o navegador)
   - Baixe em: https://claude.ai/download

---

## Instalação

### Windows

1. Baixe ou clone este repositório
2. Abra a pasta no Explorador de Arquivos
3. Clique duas vezes em **`install.bat`**
4. Siga as instruções que aparecem no terminal

### macOS / Linux

```bash
chmod +x install.sh
./install.sh
```

No macOS, o script cria o `claude_desktop_config.json` automaticamente.
No Linux, instala `libgl1` e `libglib2.0-0` se necessário (dependências do OpenCV).

### Manual (qualquer OS)

Abra o **Prompt de Comando** na pasta do projeto e execute:

```cmd
pip install -r requirements.txt
```

---

## Configuração do Claude Desktop

Após instalar as dependências, configure o Claude Desktop:

1. Abra o Claude Desktop
2. Vá em **File > Settings > Developer**
3. Clique em **Edit Config** — abre o arquivo `claude_desktop_config.json`
4. Adicione o bloco abaixo (substitua o caminho pelo caminho real do `server.py` no seu computador):

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

5. Salve o arquivo
6. **Feche e reabra** o Claude Desktop

**Como saber se funcionou:** aparece um ícone de martelo (🔨) na janela de chat. Clique nele para ver as ferramentas disponíveis.

---

## Ferramentas disponíveis

| Ferramenta | O que faz |
|---|---|
| `system_info` | Mostra OS detectado, backend OpenCV e faixas de valores |
| `list_cameras` | Lista todas as câmeras conectadas |
| `capture_frame` | Tira uma foto e mostra ao Claude |
| `get_camera_settings` | Mostra as configurações atuais |
| `adjust_camera` | Ajusta brilho, contraste, exposição, etc. |
| `reset_camera` | Volta para as configurações padrão |

> Dica: comece sempre com `system_info()` para confirmar que o backend correto foi detectado.

---

## Referência de valores

| Configuração | Faixa típica | Padrão |
|---|---|---|
| `brightness` | -64 a 64 | 0 |
| `contrast` | 0 a 64 | 32 |
| `saturation` | 0 a 100 | 64 |
| `exposure` | Windows/Mac: -11 a -1 \| Linux: 1-10000µs | automático |
| `sharpness` | 0 a 100 | 50 |
| `gain` | 0 a 100 | 0 |

> Os valores exatos variam por modelo de câmera. Se um ajuste não funcionar, a câmera pode não suportar aquele controle via software.

---

## Dica para gravar aulas

Sequência recomendada antes de gravar:

1. *"Tire uma foto e me diz o que está ruim na imagem"*
2. *"Desative o auto-exposure"*
3. *"Coloque exposure em -5 e brightness em 10"*
4. *"Tire outra foto — melhorou?"*
5. Repita até ficar bom

---

## Limitações conhecidas

- Webcams **USB externas** têm muito mais controles disponíveis do que câmeras internas de notebook
- Alguns modelos de webcam ignoram certas propriedades via software (limitação do driver)
- Para câmeras Blackmagic (BMPCC etc.), use a [REST API oficial](https://documents.blackmagicdesign.com/DeveloperManuals/RESTAPIforBlackmagicCameras.pdf)

---

## Problemas comuns

**"Nenhuma câmera encontrada"**
- Verifique se a webcam está conectada e aparece no Gerenciador de Dispositivos
- Tente fechar outros programas que podem estar usando a câmera (Teams, Zoom, OBS)

**Ícone de martelo não aparece no Claude Desktop**
- Verifique o caminho do `server.py` no config — deve ser o caminho completo com barras duplas `\\`
- Reinicie o Claude Desktop após salvar o config

**Erro ao instalar dependências**
- Execute o Prompt de Comando como Administrador
- Tente: `pip install --upgrade pip` e depois `pip install -r requirements.txt`
