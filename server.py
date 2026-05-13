import base64
import json
import cv2
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Webcam Controller")


def _open_camera(index: int):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise ValueError(f"Não foi possível abrir a câmera {index}. Verifique se ela está conectada.")
    return cap


@mcp.tool()
def list_cameras() -> str:
    """Lista todas as webcams conectadas ao computador."""
    cameras = []
    for i in range(6):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            cameras.append({
                "index": i,
                "resolucao": f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
                "fps": int(cap.get(cv2.CAP_PROP_FPS)),
            })
            cap.release()

    if not cameras:
        return "Nenhuma câmera encontrada. Verifique se a webcam está conectada."

    return json.dumps(cameras, indent=2, ensure_ascii=False)


@mcp.tool()
def capture_frame(camera_index: int = 0) -> list:
    """
    Tira uma foto pela webcam e retorna a imagem para análise.
    Use isso para ver como está a iluminação, enquadramento e qualidade da imagem.
    """
    cap = _open_camera(camera_index)

    # Descarta frames iniciais para a câmera estabilizar
    for _ in range(10):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Falha ao capturar frame. Tente novamente.")

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".jpg", frame_rgb, [cv2.IMWRITE_JPEG_QUALITY, 90])
    img_b64 = base64.b64encode(buffer).decode("utf-8")

    return [{"type": "image", "data": img_b64, "mimeType": "image/jpeg"}]


@mcp.tool()
def get_camera_settings(camera_index: int = 0) -> str:
    """
    Mostra as configurações atuais da webcam:
    brilho, contraste, saturação, exposição, nitidez, ganho.
    """
    cap = _open_camera(camera_index)

    settings = {
        "brilho (brightness)": cap.get(cv2.CAP_PROP_BRIGHTNESS),
        "contraste (contrast)": cap.get(cv2.CAP_PROP_CONTRAST),
        "saturacao (saturation)": cap.get(cv2.CAP_PROP_SATURATION),
        "exposicao (exposure)": cap.get(cv2.CAP_PROP_EXPOSURE),
        "auto_exposicao": cap.get(cv2.CAP_PROP_AUTO_EXPOSURE),
        "nitidez (sharpness)": cap.get(cv2.CAP_PROP_SHARPNESS),
        "ganho (gain)": cap.get(cv2.CAP_PROP_GAIN),
        "resolucao": f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
        "fps": cap.get(cv2.CAP_PROP_FPS),
    }

    cap.release()
    return json.dumps(settings, indent=2, ensure_ascii=False)


@mcp.tool()
def adjust_camera(
    camera_index: int = 0,
    brightness: float = None,
    contrast: float = None,
    saturation: float = None,
    exposure: float = None,
    auto_exposure: bool = None,
    sharpness: float = None,
    gain: float = None,
) -> str:
    """
    Ajusta as configurações da webcam.

    Faixas de valores típicas (variam por modelo de câmera):
    - brightness: -64 a 64  (0 = padrão)
    - contrast: 0 a 64      (32 = padrão)
    - saturation: 0 a 100   (64 = padrão)
    - exposure: -11 a -1    (ex: -5 = médio; desative auto_exposure primeiro)
    - sharpness: 0 a 100
    - gain: 0 a 100
    - auto_exposure: true = automático, false = manual

    Dica: desative auto_exposure (false) antes de ajustar exposure manualmente.
    """
    cap = _open_camera(camera_index)

    aplicado = {}

    if auto_exposure is not None:
        # 0.75 = automático, 0.25 = manual (padrão DirectShow Windows)
        val = 0.75 if auto_exposure else 0.25
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, val)
        aplicado["auto_exposure"] = auto_exposure

    if brightness is not None:
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        aplicado["brightness"] = brightness

    if contrast is not None:
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        aplicado["contrast"] = contrast

    if saturation is not None:
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        aplicado["saturation"] = saturation

    if exposure is not None:
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        aplicado["exposure"] = exposure

    if sharpness is not None:
        cap.set(cv2.CAP_PROP_SHARPNESS, sharpness)
        aplicado["sharpness"] = sharpness

    if gain is not None:
        cap.set(cv2.CAP_PROP_GAIN, gain)
        aplicado["gain"] = gain

    # Lê os valores reais que o driver aplicou (podem diferir do solicitado)
    reais = {
        "brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
        "contrast": cap.get(cv2.CAP_PROP_CONTRAST),
        "saturation": cap.get(cv2.CAP_PROP_SATURATION),
        "exposure": cap.get(cv2.CAP_PROP_EXPOSURE),
        "sharpness": cap.get(cv2.CAP_PROP_SHARPNESS),
        "gain": cap.get(cv2.CAP_PROP_GAIN),
    }

    cap.release()

    return json.dumps({
        "solicitado": aplicado,
        "valores_reais_apos_ajuste": reais,
        "aviso": "Alguns modelos de webcam ignoram certas configurações via software. Se um valor não mudou, a câmera não suporta esse controle programático.",
    }, indent=2, ensure_ascii=False)


@mcp.tool()
def reset_camera(camera_index: int = 0) -> str:
    """
    Redefine as configurações da câmera para o padrão de fábrica.
    Útil quando a imagem ficou muito escura, lavada ou distorcida após ajustes.
    """
    cap = _open_camera(camera_index)

    # Reativa auto-exposure e zera os ajustes manuais
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    cap.set(cv2.CAP_PROP_CONTRAST, 32)
    cap.set(cv2.CAP_PROP_SATURATION, 64)
    cap.set(cv2.CAP_PROP_SHARPNESS, 50)
    cap.set(cv2.CAP_PROP_GAIN, 0)

    cap.release()
    return "Configurações redefinidas para o padrão. Use capture_frame para verificar o resultado."


if __name__ == "__main__":
    mcp.run()
