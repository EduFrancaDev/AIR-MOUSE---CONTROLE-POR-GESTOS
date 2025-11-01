# AirMouse

Projeto em Python que transforma sua mão em um mouse virtual usando visão computacional. Uma webcam comum detecta os principais pontos da mão com o MediaPipe e, a partir deles, o cursor é movido em tempo real e gestos controlam os cliques.

## Recursos

- Rastreamento de mão com MediaPipe e OpenCV.
- Movimentação suave do cursor por filtro exponencial configurável.
- Gesto de pinça (polegar + indicador) simula clique do mouse.
- Visualização opcional das landmarks para depuração.
- Ajustes de sensibilidade e espelhamento direto no código.

## Requisitos

- Python 3.10 ou superior.
- Webcam funcional.
- Sistema operacional com suporte ao `pyautogui` (Windows, macOS ou Linux com X11).

## Instalação

1. Clone ou faça download do repositório.
   ```bash
   git clone https://github.com/<seu-usuario>/AIRMOUSE.git
   cd AIRMOUSE
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Instale as dependências.
   ```bash
   pip install -r requirements.txt
   ```

## Como usar

1. Conecte a webcam e garanta boa iluminação.
2. Ative o ambiente virtual, caso tenha criado:
   ```bash
   .\.venv\Scripts\activate
   ```
3. Execute o aplicativo:
   ```bash
   python main.py
   ```
4. Movimente o indicador para controlar o cursor. Faça um gesto de pinça (aproxime polegar e indicador) para pressionar o botão esquerdo; solte para liberar. Pressione `ESC` para encerrar.

### Ajustes úteis

- `alpha`: define quão responsivo é o filtro suavizador (valores maiores reagem mais rápido).
- `DRAW_LANDMARKS`: habilita/desabilita o desenho dos pontos da mão no vídeo.
- `cap.set(...)`: permita alterar a resolução de captura caso precise equilibrar desempenho e precisão.

## Problemas comuns

- **Movimento lento ou travado**: diminua a resolução (`cap.set`) ou aumente `alpha`. Feche programas que usem muito CPU/GPU.
- **Cursor não se move**: confirme se a câmera está ativa e se apenas uma mão está sendo detectada (o script opera com uma mão).
- **Clique permanente**: afaste levemente o polegar do indicador ou ajuste o limiar dentro da função `pinch_gesto`.

Sinta-se à vontade para adaptar o código a novos gestos ou combinar com automações mais avançadas!
