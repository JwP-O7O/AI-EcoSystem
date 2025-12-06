@echo off
title Solana Scalpingbot - Stop
echo ?? Stopping Solana Scalpingbot...
REM Change to the directory of this script to ensure correct working directory
cd /d "%~dp0"
pm2 stop solana-scalpingbot
pm2 delete solana-scalpingbot
echo ? Bot stopped!
pause
