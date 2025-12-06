# 🐳 Agent Zero - Docker/Ubuntu Setup voor Android

## 📋 OVERZICHT

Je hebt nu **twee manieren** om Agent Zero te draaien op je Android device:

### 1. **Native Termux** ⚡ (Aanbevolen voor dagelijks gebruik)
- ✅ Snelste performance
- ✅ Direct access tot Termux environment
- ✅ Minimaal geheugen gebruik
- ✅ Alle upgrades werken perfect

### 2. **Ubuntu Container** 🐧 (Voor Docker/container features)
- ✅ Volledige Linux omgeving
- ✅ Toegang tot meer packages
- ✅ Kan later Docker-in-Docker doen
- ⚠️ Iets langzamer (PRoot overhead)

---

## 🚀 QUICK START

### Optie A: Run in Native Termux (Snel)
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./run-termux.sh
```

### Optie B: Run in Ubuntu Container
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./run-ubuntu.sh
```

### Optie C: Open Ubuntu Shell (Development)
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./ubuntu-shell.sh
```

---

## 📁 SETUP DETAILS

### Wat is geïnstalleerd:

**Ubuntu Container:**
- Ubuntu 25.10 (Questing) ARM64
- Python 3.13.7
- Build tools (gcc, g++, make)
- Git, curl, wget
- Virtual environment met Agent Zero dependencies

**Agent Zero:**
- Gelinkt vanuit Termux naar Ubuntu
- Alle upgrades beschikbaar in beide omgevingen
- Gedeelde data en logs

---

## 🔧 TECHNICAL DETAILS

### Ubuntu Location
```
/data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/ubuntu
```

### Agent Zero in Ubuntu
```
/root/agent-zero-link -> /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
```

### Virtual Environment
```
/root/agent-zero-link/venv
```

### How It Works
- **proot-distro**: Chroot-like environment zonder root access
- **Symlink**: Agent Zero files gedeeld tussen Termux en Ubuntu
- **venv**: Isolated Python environment binnen Ubuntu

---

## 💡 WANNEER WELKE GEBRUIKEN?

### Gebruik Native Termux Voor:
- ✅ Normale Agent Zero taken
- ✅ Snelle responses
- ✅ Minimaal battery/memory gebruik
- ✅ Alle huidige functionaliteit

### Gebruik Ubuntu Container Voor:
- ✅ Packages die alleen in Linux werken
- ✅ Development met volledige build tools
- ✅ Testing Docker images (future)
- ✅ Experimenten zonder Termux te riskeren

---

## 📊 PERFORMANCE COMPARISON

| Aspect | Native Termux | Ubuntu Container |
|--------|--------------|------------------|
| **Startup Time** | <1s | ~3s |
| **Memory** | ~300MB | ~500MB |
| **CPU** | 100% | ~85% (PRoot overhead) |
| **Package Access** | Termux only | All Ubuntu packages |
| **Stability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔍 TROUBLESHOOTING

### Ubuntu Container Start Fails
```bash
# Check if Ubuntu is installed
ls $PREFIX/var/lib/proot-distro/installed-rootfs/ubuntu

# Reinstall if needed
proot-distro remove ubuntu
proot-distro install ubuntu
```

### Python Dependencies Missing
```bash
# Enter Ubuntu shell
./ubuntu-shell.sh

# Reinstall dependencies
cd /root/agent-zero-link
source venv/bin/activate
pip install langchain langchain-core langchain-community langchain-openai
```

### Symlink Broken
```bash
# In Ubuntu shell
cd /root
rm agent-zero-link
ln -s /data/data/com.termux/files/home/AI-EcoSystem/agent-zero agent-zero-link
```

### Performance Issues
```bash
# Ubuntu containers use more resources
# Switch back to native Termux if needed:
./run-termux.sh
```

---

## 🎯 ADVANCED USAGE

### Run Specific Commands in Ubuntu
```bash
proot-distro login ubuntu -- bash -c "your-command-here"
```

### Install Additional Packages in Ubuntu
```bash
./ubuntu-shell.sh
apt update
apt install package-name
```

### Access Ubuntu Files from Termux
```bash
# Ubuntu filesystem is at:
cd $PREFIX/var/lib/proot-distro/installed-rootfs/ubuntu/root
```

### Mount Additional Directories
Edit: `/data/data/com.termux/files/usr/etc/proot-distro/ubuntu.sh`

---

## 🔐 SECURITY NOTES

- Ubuntu container heeft GEEN root access op Android
- PRoot simuleert root binnen container
- Alle file access beperkt tot Termux home directory
- Safe voor experimenten zonder Android systeem te beschadigen

---

## 📈 FUTURE POSSIBILITIES

Met deze Ubuntu setup kun je later:
- [ ] Docker-in-Docker installeren (met root-repo)
- [ ] Kubernetes tools (minikube, k3s)
- [ ] Database servers (PostgreSQL, MySQL)
- [ ] Web servers (Nginx, Apache)
- [ ] Development tools (VSCode server, Jupyter)

---

## 🆘 NEED HELP?

### Check Status
```bash
# Ubuntu installed?
proot-distro list

# Python version in Ubuntu
proot-distro login ubuntu -- python3 --version

# Agent Zero files accessible?
proot-distro login ubuntu -- ls /root/agent-zero-link
```

### Logs
```bash
# Ubuntu container logs
ls $PREFIX/var/lib/proot-distro/dlcache/

# Agent Zero logs (shared)
ls /data/data/com.termux/files/home/AI-EcoSystem/agent-zero/logs/
```

---

## 📚 RESOURCES

- [proot-distro GitHub](https://github.com/termux/proot-distro)
- [Ubuntu on Termux Guide](https://wiki.termux.com/wiki/PRoot)
- [Docker on Android (root required)](https://github.com/cyberkernelofficial/docker-in-termux)

---

## ✅ QUICK REFERENCE

| Task | Command |
|------|---------|
| **Run Agent Zero (Termux)** | `./run-termux.sh` |
| **Run Agent Zero (Ubuntu)** | `./run-ubuntu.sh` |
| **Open Ubuntu shell** | `./ubuntu-shell.sh` |
| **Check Ubuntu status** | `proot-distro list` |
| **Remove Ubuntu** | `proot-distro remove ubuntu` |
| **Update Ubuntu** | `proot-distro login ubuntu -- apt update && apt upgrade` |

---

## 🎉 CONCLUSIE

Je hebt nu het **beste van beide werelden**:

✅ **Snelle native Termux** voor dagelijks gebruik
✅ **Volledige Ubuntu container** voor advanced features
✅ **Gedeelde Agent Zero installatie** - geen dubbel werk
✅ **Makkelijk switchen** met helper scripts

**Start Agent Zero zoals je wilt:**
```bash
./run-termux.sh    # Snel en efficient
# of
./run-ubuntu.sh    # Volledige Linux environment
```

---

*Agent Zero v2.0 - Hybrid Termux/Ubuntu Setup*
*Geïnstalleerd: 29 November 2025*
*Platform: Android ARM64*
