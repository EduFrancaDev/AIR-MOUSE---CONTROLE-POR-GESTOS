import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Inicialização da câmera e do MediaPipe
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 424)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,  # Complexidade menor reduz custo mantendo estabilidade
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
)
mp_draw = mp.solutions.drawing_utils

# Definir as dimensões da tela
scr_w, scr_h = pyautogui.size()  # Pega a resolução da tela do usuário

# Suavização para a posição do cursor (para evitar movimentos bruscos)
alpha = 0.35  # Filtro exponencial mais responsivo
prev = None
DRAW_LANDMARKS = True  # Mostrar landmarks na mão para facilitar o tracking visual
MIRROR_FEED = False  # Define se o frame deve ser espelhado horizontalmente


def smooth_position(new_pos):
    """Aplicar filtro exponencial para suavizar sem adicionar muito atraso"""
    global prev
    new_arr = np.asarray(new_pos, dtype=np.float64)
    if prev is None:
        prev = new_arr
    else:
        prev = prev + alpha * (new_arr - prev)
    return prev


# Função para mapear coordenadas normalizadas para coordenadas da tela
def norm_to_screen(xn, yn):
    x = np.clip(xn, 0, 1) * scr_w
    y = np.clip(yn, 0, 1) * scr_h
    return np.array([x, y])


# Função para verificar se o "pinch" (gesto de apertar os dedos) foi feito
def pinch_gesto(lm):
    th_tip, idx_tip = lm[4], lm[8]  # Pega as posições do polegar e indicador
    return np.hypot(th_tip.x - idx_tip.x, th_tip.y - idx_tip.y) < 0.05


while True:
    # Captura o frame da câmera
    ret, frame = cap.read()
    if not ret:
        break

    if MIRROR_FEED:
        frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
    result = hands.process(rgb)  # Processa o frame

    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0].landmark  # Pega a mão detectada

        # Pega a posição do indicador (landmark 8) e mapeia para a tela
        ix, iy = landmarks[8].x, landmarks[8].y
        target = norm_to_screen(ix, iy)  # Mapeia para a tela

        # Suavização de movimento com filtro exponencial
        smooth_target = smooth_position(target)
        pyautogui.moveTo(
            smooth_target[0], smooth_target[1], _pause=False
        )  # Mover o mouse para a nova posição

        # Verifica se o "pinch" foi feito (polegar e indicador próximos)
        pinch = pinch_gesto(landmarks)
        if pinch:
            pyautogui.mouseDown()  # Clica com o botão do mouse
        else:
            pyautogui.mouseUp()  # Solta o botão do mouse

        # Desenha as landmarks da mão na tela (para debug)
        if DRAW_LANDMARKS:
            mp_draw.draw_landmarks(
                frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS
            )

    # Exibe a imagem
    cv2.imshow("Air Mouse", frame)

    # Para encerrar, pressione a tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
