#!/bin/bash
cd /Users/qy/CodeBuddy/Claw/outputs/战士宫殿/
nohup python3 generate_warrior.py > run.log 2>&1 &
echo "PID=$!"
echo "日志: /Users/qy/CodeBuddy/Claw/outputs/战士宫殿/run.log"
