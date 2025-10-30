import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Inicialização da câmera e do MediaPipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Definir as dimensões da tela
scr_w, scr_h = pyautogui.size()  # Pega a resolução da tela do usuário

# Suavização para a posição do cursor (para evitar movimentos bruscos)
alpha = 0.25  # Fator de suavização
prev = np.array([0.0, 0.0])


# Função para mapear coordenadas normalizadas para coordenadas da tela
def norm_to_screen(xn, yn):
    x = np.clip(xn, 0, 1) * scr_w
    y = np.clip(yn, 0, 1) * scr_h
    return np.array([x, y])


# Função para verificar se o "pinch" (gesto de apertar os dedos) foi feito
def pinch_gesto(lm):
    # Verifica a distância entre o polegar (índice 4) e o indicador (índice 8)
    th_tip, idx_tip = lm[4], lm[8]
    return np.hypot(th_tip.x - idx_tip.x, th_tip.y - idx_tip.y) < 0.05


while True:
    # Captura o frame da câmera
    ret, frame = cap.read()
    if not ret:
        break

    # Inverte a imagem para visualização correta
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
    result = hands.process(rgb)  # Processa o frame

    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0].landmark  # Pega a mão detectada

        # Pega a posição do indicador (landmark 8) e mapeia para a tela
        ix, iy = landmarks[8].x, landmarks[8].y
        target = norm_to_screen(ix, iy)
        prev = prev * (1 - alpha) + target * alpha  # Suavização da posição
        pyautogui.moveTo(
            prev[0], prev[1], _pause=False
        )  # Mover o mouse para a nova posição

        # Verifica se o "pinch" foi feito (polegar e indicador próximos)
        pinch = pinch_gesto(landmarks)
        if pinch:
            pyautogui.mouseDown()  # Clica com o botão do mouse
        else:
            pyautogui.mouseUp()  # Solta o botão do mouse

        # Desenha as landmarks da mão na tela (para debug)
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
