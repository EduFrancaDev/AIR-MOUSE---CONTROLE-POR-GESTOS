# Configuração do ambiente

- Criar ambiente virtual (Windows):
  ```powershell
  python -m venv .venv
  ```
- Ativar ambiente virtual (Windows PowerShell):
  ```powershell
  .\.venv\Scripts\Activate
  ```
- Instalar dependências:
  ```powershell
  pip install -r requirements.txt
  ```

# Execução do projeto

- Rodar o AirMouse:
  ```powershell
  python main.py
  ```

# Ajustes rápidos no código

- Alternar desenho das landmarks: editar `DRAW_LANDMARKS` em `main.py`.
- Espelhar ou não o vídeo: editar `MIRROR_FEED` em `main.py`.
- Ajustar sensibilidade do movimento: alterar `alpha` ou a resolução em `main.py`.
