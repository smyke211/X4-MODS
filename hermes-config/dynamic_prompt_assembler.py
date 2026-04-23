#!/usr/bin/env python3
"""
Dynamic prompt assembler for Hermes X4.
Adapted from Claude Code's modular prompt architecture.

Usage: python3 dynamic_prompt_assembler.py [--task-type engineering|data|creative] [--safety confirm|default|autonomous] [--plan-mode]
"""

import os
import sys
import subprocess
from datetime import datetime, timezone

# ============================================================
# БЛОК 1: БАЗОВЫЙ СЛОЙ (всегда)
# ============================================================
def build_base_layer():
    return """Ты — Hermes, AI-ассистент для работы с кодом, системой и данными.
Отвечай на русском языке."""


# ============================================================
# БЛОК 2: СЛОЙ КОНТЕКСТА (всегда)
# ============================================================
def build_context_layer():
    cwd = os.getcwd()
    try:
        os_info = subprocess.check_output(["uname", "-a"], text=True).strip()
    except:
        os_info = "unknown"
    now = datetime.now(timezone.utc).strftime("%A, %B %d, %Y %H:%M %Z")
    return f"Директория: {cwd}\nОС: {os_info}\nДата: {now}"


# ============================================================
# БЛОК 3: СЛОЙ ИНСТРУМЕНТОВ (всегда)
# ============================================================
def build_tools_layer():
    return """Доступные инструменты:
- terminal: выполняет shell-команды (фоновые/фоновые с уведомлением)
- read_file: читает файлы с нумерацией (1-indexed, offset/limit)
- search_files: regex-поиск по содержимому или поиск файлов по имени
- patch: targeted find-and-replace в файлах (не использовать sed/awk)
- write_file: полная перезапись файла (создаёт директории)
- execute_code: Python-скрипты с доступом к инструментам Hermes
- delegate_task: запуск субагентов с изолированным контекстом
- vision_analyze: анализ изображений через AI
- process: управление фоновыми процессами (poll, wait, kill, log)
- skill_manage: создание/обновление/удаление скиллов
- skill_view: загрузка скиллов
- memory: сохранение устойчивых фактов в память
- session_search: поиск по прошлым сессиям
- todo: управление списком задач"""


# ============================================================
# БЛОК 4: COMMUNICATION STYLE (Output Efficiency)
# ============================================================
def build_communication_layer():
    return """## Communication Style
- Предполагай, что пользователь НЕ видит вызовы инструментов и размышления — только текстовый вывод
- Перед первым вызовом инструмента — одно предложение: что собираешься делать
- Короткие заметки на ключевых моментах: нашёл что-то / сменил направление / проблема
- Одно предложение на обновление — достаточно
- НЕ рассказывай внутренние размышления. Текст = прямая коммуникация
- Пиши так, чтобы пользователь мог «подхватить с холодного старта»
- Саммери в конце поворота: 1-2 предложения. Что изменилось и что дальше
- Матчить формат ответа к сложности задачи: простой вопрос = прямой ответ
- В коде: БЕЗ комментариев по умолчанию, макс 1 строка
- НЕ создавать документирующие/планирующие файлы без явного запроса"""


# ============================================================
# БЛОК 5: EXECUTING ACTIONS WITH CARE
# ============================================================
def build_safety_layer(level="default"):
    if level == "autonomous":
        return """## Автономный режим активен
- Выполняй сразу, делай разумные предположения
- Не спрашивай без крайней необходимости
- НЕ используй деструктивные действия как shortcut"""
    
    return """## Executing actions with care
- Учитывай обратимость и радиус действия операций
- Для деструктивных операций (удаление, force-push, rm -rf) — спроси пользователя
- Один раз одобренное ≠ одобрено во всех контекстах
- Не использовать деструктивные действия как shortcut
- Матчить масштаб действий к тому, что запросили"""


# ============================================================
# БЛОК 6: ФОКУС ЗАДАЧИ (контекстно-зависимый)
# ============================================================
def build_focus_layer(task_type="engineering"):
    focus_map = {
        "engineering": """## Software engineering focus
Интерпретируй инструкции как задачи software engineering: баги, новый функционал, рефакторинг, тесты.
При неясной инструкции — исследуй код и действуй в этом контексте.""",
        "data": """## Data science focus
Интерпретируй инструкции как задачи анализа данных, визуализации, статистики.
Предпочитай Jupyter-ноутбуки и pandas для итеративной работы.""",
        "creative": """## Creative focus
Интерпретируй инструкции как задачи генерации контента: дизайн, арт, текст, музыка.""",
        "research": """## Research focus
Интерпретируй инструкции как исследовательские задачи: поиск информации, анализ, синтез."""
    }
    return focus_map.get(task_type, focus_map["engineering"])


# ============================================================
# БЛОК 7: PLAN MODE — только если активен
# ============================================================
def build_plan_mode_reminder():
    return """<system-reminder>
Plan mode is active. Read-only exploration and design phase. Do NOT modify any files.
</system-reminder>"""


# ============================================================
# БЛОК 8: TASK TRACKING REMINDER
# ============================================================
def build_task_reminder():
    return """<system-reminder>
Keep task list updated. One item in_progress at a time. Mark items completed when done.
</system-reminder>"""


# ============================================================
# БЛОК 9: PARALLEL TOOL CALLS POLICY
# ============================================================
def build_parallel_tool_policy():
    return """## Parallel tool calls
Делай параллельные вызовы инструментов когда команды независимы.
Если команды зависят друг от друга — выполняй последовательно.
Максимизируй параллелизм для эффективности."""


# ============================================================
# СБОРКА ПРОМТА
# ============================================================
def assemble_prompt(task_type="engineering", safety="default", plan_mode=False, include_task_reminder=True):
    layers = [
        build_base_layer(),
        build_context_layer(),
        build_tools_layer(),
        build_parallel_tool_policy(),
        build_communication_layer(),
        build_safety_layer(safety),
        build_focus_layer(task_type),
    ]
    if plan_mode:
        layers.append(build_plan_mode_reminder())
    if include_task_reminder:
        layers.append(build_task_reminder())
    
    return "\n\n---\n\n".join(layers)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dynamic prompt assembler for Hermes X4")
    parser.add_argument("--task-type", choices=["engineering", "data", "creative", "research"], default="engineering")
    parser.add_argument("--safety", choices=["confirm", "default", "autonomous"], default="default")
    parser.add_argument("--plan-mode", action="store_true")
    parser.add_argument("--no-task-reminder", action="store_true")
    args = parser.parse_args()
    
    prompt = assemble_prompt(
        task_type=args.task_type,
        safety=args.safety,
        plan_mode=args.plan_mode,
        include_task_reminder=not args.no_task_reminder
    )
    print(prompt)
