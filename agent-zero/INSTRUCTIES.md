# Instructies om de App te Starten

De installatie van dependencies is momenteel bezig op de achtergrond.

> ⚠️ **Belangrijk:** Er zijn bekende compatibiliteitsproblemen met **Python 3.13** en sommige libraries (zoals `numpy` en `langchain`). 
> Als de installatie faalt, wordt aangeraden om **Python 3.11** of **3.12** te gebruiken.

Zodra de installatie voltooid is, kun je de applicatie starten met de volgende commando's:

### 0. Configuratie
Er is een `.env` bestand aangemaakt in `agent-zero/`.
**Je moet hierin je API keys invullen** (bijv. `GOOGLE_API_KEY` of `OPENAI_API_KEY`) voordat je de app start.

### 1. Web UI (Aanbevolen)
```powershell
python run_ui.py
```
Dit start de web interface. Open vervolgens je browser op de getoonde URL (meestal `http://localhost:5000` of `http://127.0.0.1:5000`).

### 2. Terminal Interface (CLI)
```powershell
python run_cli.py
```

### Let op
- Zorg dat **Docker** draait als je gebruik wilt maken van de veilige container omgeving.
- De eerste keer opstarten kan even duren omdat modellen of resources gedownload moeten worden.
