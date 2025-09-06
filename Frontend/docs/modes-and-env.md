## Режимы (modes) и переменные окружения (env)

Проект использует Vite и режимы: `development`, `staging`, `production`.
Режим влияет на загружаемые `.env*` файлы, `import.meta.env.MODE`, sourcemaps и параметры сборки.

### Файлы окружения

Кладём в корень `WolfEye_/Frontend/`:
- `.env` — дефолты
- `.env.development`, `.env.staging`, `.env.production` — значения для режимов
- `.env.example` — шаблон для команды/CI (без секретов)

Приоритет (сильнее справа): `.env` < `.env.[mode]` < `.env.local` < `.env.[mode].local`.
В клиент попадают только переменные, начинающиеся с `VITE_`.

Пример:
```
VITE_APP_NAME=WolfEye
VITE_API_URL=http://localhost:5173/api
```

Стейджинг/прод:
```
# .env.staging
VITE_API_URL=https://staging.api.example.com

# .env.production
VITE_API_URL=https://api.example.com
```

Рекомендуется в `.gitignore`:
```
.env*
!.env.example
```

### Скрипты

- Dev (development):
```
npm run dev
```
- Dev (staging):
```
npm run dev:staging
```
- Build (production / staging):
```
npm run build
npm run build:staging
```
- Preview из `dist` (после соответствующего build):
```
npm run preview
npm run preview:staging
```
- Дополнительно:
```
npm run typecheck
npm run lint
```

### Доступ к переменным в коде

```ts
const mode = import.meta.env.MODE
const apiUrl = import.meta.env.VITE_API_URL
```

Глобалы из `define` (см. `vite.config.ts`):
```ts
console.log(__APP_ENV__, __API_URL__)
```

Типы окружения находятся в `src/vite-env.d.ts`.

### Смоук‑тест режимов

- Development: `npm run dev` → в консоли браузера `import.meta.env.VITE_API_URL` = `http://localhost:5173/api`; HMR и inline sourcemaps работают.
- Staging (dev): `npm run dev:staging` → URL из `.env.staging`; sourcemaps: hidden.
- Production: `npm run build && npm run preview` → нет sourcemaps; `react` вынесен в отдельный чанк; значения переменных прод.

### Переопределение из CLI

```bash
VITE_API_URL=https://override.example.com npm run dev:staging
```

### Добавление нового режима (например, `qa`)

1. Создать `.env.qa`:
```
VITE_API_URL=https://qa.api.example.com
```
2. Запуск:
```
vite --mode qa
# или добавить npm-скрипт "dev:qa": "vite --mode qa"
```

### Частые ошибки

- Переменные без префикса `VITE_` не попадут в клиент.
- `preview` использует значения, «запечённые» на этапе `build` — билдить под тот же `--mode`.
- После изменения `.env*` перезапускайте dev‑сервер.
- Секреты для Node не должны иметь префикс `VITE_` и не импортируются в клиент.


