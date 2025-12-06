@echo off
title Solana Scalpingbot - Logs
echo ?? Solana Scalpingbot Logs
REM Change to the directory of this script to ensure correct working directory
cd /d "%~dp0"
pm2 logs solana-scalpingbot
