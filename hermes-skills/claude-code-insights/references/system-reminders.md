# Hermes System Reminders Catalog

Оригинал: 47 файлов `system-reminder-*.md` из репозитория Piebald-AI/claude-code-system-prompts.

## Что такое System Reminders

Короткие (1-3 строки) напоминания, вставляемые харнессом как `<system-reminder>` теги в середине разговора. Это НЕ сообщения от пользователя — это инструкции для агента, которые НЕ нужно упоминать вслух.

## Паттерн вставки

```
<system-reminder>
{текст напоминания}
</system-reminder>
```

## Каталог готовых реминдеров

### Стили вывода
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| output-style-active | Пользователь включил режим стиля | "{имя_стиля} output style is active. Remember to follow the specific guidelines for this style." |
| thinking-frequency-tuning | Всегда при вставке | "System reminders are instructions to you, not from the user. On simple messages, respond directly without thinking. On complex tasks, reason as much as needed but don't overthink." |

### Контекст сессии
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| session-continuation | После переключения устройства/провайдера | "This session is being continued. Application state may have changed. Current working directory: {dir}" |
| token-usage | При компактизации контекста | "Tokens used: {used}/{total}; {remaining} remaining" |

### Файлы
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| file-truncated | Файл обрезан через offset/limit | "The file was truncated. Only lines {from}-{to} were shown." |
| file-shorter-than-offset | offset > total_lines | "The file has only {n} lines. Your offset {off} was beyond the end." |
| file-modified-by-user-or-linter | После редактирования пользователем/линтером | "The file '{path}' was modified since you last read it. Re-read before further edits." |

### Планы
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| verify-plan-reminder | После создания плана | "Before implementing, verify your plan against the codebase." |
| plan-mode-is-active | Когда план-режим активен | "Plan mode is active. Read-only phase. Do not modify files." |

### Хуки
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| hook-blocking-error | Хук заблокировал операцию | "The operation was blocked by a hook: {reason}" |
| hook-stopped-continuation | Хук остановил процесс | "The process was stopped by a hook. Context: {context}" |

### Команды задач
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| task-tools-reminder | При работе с todo | "One item in_progress at a time. Mark items completed immediately when done." |

### Мульти-агент
| Название | Когда вставлять | Текст |
|----------|----------------|-------|
| team-coordination | При мульти-агент сессии | "Coordinate with other agents. Delegate clearly, provide full context." |
| team-shutdown | При завершении мульти-агент | "Team session shutting down. Report final status." |

## Как использовать

Харнесс вставляет реминдеры автоматически:
- После переключения модели → session-continuation
- При компактизации → token-usage, thinking-frequency-tuning
- При обрезке файла → file-truncated
- При блокировке хуком → hook-blocking-error
- После создания плана → verify-plan-reminder
- При работе с todo → task-tools-reminder
