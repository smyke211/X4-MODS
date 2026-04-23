---
name: claude-code-insights
description: Techniques from Claude Code system prompt leaks — dynamic prompt assembly, subagent prompts, system reminders, and output efficiency patterns for Hermes X4.
category: devops
---

## Claude Code Prompt Architecture — Insights for Hermes X4

Источник: репозиторий Piebald-AI/claude-code-system-prompts (до v2.1.118, апрель 2026).

### Ключевые принципы архитектуры промтов

1. **Динамическая сборка (композиция)** — промт не монолитный, а собирается из модульных блоков:
   - Базовые правила (роль, стиль общения)
   - Контекст задачи (git, текущая директория)
   - Активные инструменты (tool descriptions)
   - System Reminders (контекстные напоминания)
   - Специфика задачи (software engineering, data science, etc.)

2. **Template Variables** — все промты используют `${VAR}` плейсхолдеры, интерполируемые при runtime.

3. **System Reminders** — короткие (1-3 строки) напоминания, вставляемые систем-сообщением в середине разговора для:
   - Напоминания о стиле вывода
   - Уведомления о изменении файлов
   - Информации о потреблении токенов
   - Реакции на хуки

4. **Субагент-промты** — каждый субагент имеет отдельный промт с:
   - Чёткой ролью
   - Списком доступных/запрещённых инструментов
   - Процессом работы
   - Обязательным форматом вывода

5. **Output Efficiency** — минимальный, но достаточный вывод:
   - "Lead with answers over reasoning"
   - 1-2 предложения саммери в конце поворота
   - Одно предложение на обновление
   - НЕ создавать документы без запроса

### Файлы в этом skill

- `references/communication-style.md` — адаптированный Output Efficiency промт
- `references/system-reminders.md` — каталог System Reminders
- `templates/subagent-plan.md` — План субагент промт
- `templates/subagent-explore.md` — Explore субагент промт
- `templates/subagent-worker.md` — Worker субагент промт

### Когда использовать

При создании новых субагентов, настройке стилей вывода, проектировании system reminder хуков для Hermes.
