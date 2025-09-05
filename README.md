# Onion Architecture Demo (Refactor)

**Слои:**
- `app/domain` — Pydantic-модели (Domain)
- `app/application/services` — бизнес-логика (Application)
- `app/infrastructure` — адаптеры/интеграции: LLM, парсинг PDF, конфиг (Infrastructure)
- `main.py` — точка входа (Interface)

## Установка
```bash
pip install pydantic python-dotenv
```

## Запуск
```bash
python main.py
```

### Совместимость с исходными функциями
- `when_start_workig`, `compare_cities`, `analysis_legend`, `CoreML.get_score` — тела сохранены (только `pass` → мок `return`).
- Ошибка в функции обработки ФИО исправлена: теперь `analysis_fio(llm, data: NameParts)` принимает ФИО из резюме.
- Конфиг и промпты сохранены: `app/config/`, `app/infrastructure/llm/prompts/`.
