@echo off
title Solana Scalpingbot - Production Mode
echo ?? Starting Solana Scalpingbot in Production Mode...
REM Change to the directory of this script to ensure correct working directory
cd /d "%~dp0"
pm2 start ecosystem.config.json
pm2 save
pm2 list
echo.
echo ? Bot started in background!
echo ?? Dashboard: http://localhost:3000
echo ?? Commands:
echo    pm2 logs solana-scalpingbot  - View logs
echo    pm2 stop solana-scalpingbot  - Stop bot
echo    pm2 restart solana-scalpingbot - Restart bot
pause
