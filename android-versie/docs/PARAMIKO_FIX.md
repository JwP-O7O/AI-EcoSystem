# Paramiko Installation Fix voor Android/Termux

**Datum:** 28 November 2025
**Status:** ✅ Opgelost

---

## Probleem

Wanneer Agent Zero code probeert uit te voeren, krijg je deze error:
```
ModuleNotFoundError: No module named 'paramiko'
```

Dit gebeurt in `python/tools/code_execution_tool.py` wanneer het probeert te importeren van `python/helpers/shell_ssh.py`.

---

## Waarom Niet Simpel `pip install paramiko`?

Normaal zou `pip install paramiko` voldoende zijn, maar op Android/Termux faalt dit omdat:

1. Paramiko vereist **pynacl** als dependency
2. PyNaCl moet native C code compileren tegen **libsodium**
3. De pip installer probeert libsodium zelf te compileren
4. Dit faalt op Termux omdat de linker (`ld`) niet gevonden wordt in het pad

**Error die je krijgt:**
```
configure: error: no acceptable ld found in $PATH
subprocess.CalledProcessError: Command '[.../configure', ...] returned non-zero exit status 1.
ERROR: Failed building wheel for pynacl
```

---

## De Oplossing (3 stappen)

### Stap 1: Installeer libsodium via Termux package manager
```bash
pkg install libsodium -y
```

Dit installeert een pre-compiled versie van libsodium speciaal voor Android/ARM.

### Stap 2: Installeer pynacl met system libsodium
```bash
SODIUM_INSTALL=system pip install pynacl --no-binary :all:
```

De `SODIUM_INSTALL=system` environment variable vertelt pynacl om de system libsodium te gebruiken in plaats van zelf te compileren.

### Stap 3: Installeer paramiko
```bash
pip install paramiko
```

Nu pynacl beschikbaar is, installeert paramiko zonder problemen!

---

## Verificatie

Test of paramiko correct is geïnstalleerd:

```bash
python -c "import paramiko; print('✅ Paramiko werkt!'); print(f'Version: {paramiko.__version__}')"
```

**Expected output:**
```
✅ Paramiko werkt!
Version: 4.0.0
```

---

## Waarom is Paramiko Nodig?

Paramiko is een SSH2 protocol library die Agent Zero gebruikt voor:

1. **Code Execution Tool** - Voert terminal commands uit
2. **SSH Connections** - Verbindt met remote machines (optioneel)
3. **Secure Communication** - Encrypted communication voor tools

Zonder paramiko kan Agent Zero geen code uitvoeren, wat een core functionaliteit is!

---

## Installed Versies

Na deze fix heb je:
- **libsodium:** 1.0.20-1 (via Termux pkg)
- **pynacl:** 1.6.1 (via pip, gecompileerd tegen system libsodium)
- **paramiko:** 4.0.0 (via pip)
- **invoke:** 2.2.1 (dependency van paramiko)

---

## Troubleshooting

### "ERROR: Command '[.../configure', ...] returned non-zero exit status 1"
**Oplossing:** Je probeert pynacl te installeren zonder eerst libsodium via pkg te installeren. Volg Stap 1 hierboven.

### "ModuleNotFoundError: No module named 'paramiko'" (na installatie)
**Oplossing:**
1. Verify installation: `pip show paramiko`
2. Check je in de juiste Python environment bent
3. Herstart je terminal session

### "ImportError: cannot import name 'ShellSSH'"
Dit is normaal als je buiten Agent Zero's directory probeert te importeren. Zolang paramiko zelf importeert, werkt het.

---

## One-Liner voor Fresh Install

Als je Agent Zero op een nieuwe Termux install zet:

```bash
pkg install libsodium -y && SODIUM_INSTALL=system pip install pynacl --no-binary :all: && pip install paramiko
```

---

## Technische Details

### Waarom faalt compilation op Android?

1. **Toolchain issues:** Android NDK heeft een andere toolchain setup dan reguliere Linux
2. **Missing linker:** De autoconf configure script zoekt `ld` maar Termux gebruikt `aarch64-linux-android-ld`
3. **PATH issues:** De compiler (clang) wordt gevonden, maar de linker niet

### Waarom werkt system install wel?

Termux's pkg manager heeft pre-compiled binaries voor ARM64:
- Speciaal gebouwd voor Android/Termux environment
- Correct gelinkt tegen Android's libc (Bionic)
- Klaar om te gebruiken, geen compilation nodig

### Alternative: Waarom niet Paramiko via pkg?

Termux heeft geen `pkg install paramiko` package. Python packages worden verwacht via pip te installeren, maar native dependencies (zoals libsodium) komen via pkg.

---

## Related Files

- **Code execution tool:** `/python/tools/code_execution_tool.py`
- **SSH helper:** `/python/helpers/shell_ssh.py`
- **Dependencies:** Zie `android-versie/requirements-android.txt`

---

✅ **Met deze fix werkt Agent Zero volledig op Android/Termux!**

*Laatste update: 28 November 2025*
