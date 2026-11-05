<div align="center">

<a href="https://mosrobotics.github.io/materials7-8/"><img src="https://img.shields.io/badge/%F0%9F%9A%80%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8C%20%D1%81%D0%B0%D0%B9%D1%82-mosrobotics.github.io-0f9d8a?style=for-the-badge" alt="Открыть сайт"></a>

<a href="https://github.com/Mosrobotics/materials7-8/actions/workflows/deploy.yml"><img src="https://github.com/Mosrobotics/materials7-8/actions/workflows/deploy.yml/badge.svg" alt="Публикация сайта"></a>
<img src="https://img.shields.io/badge/MkDocs-Material-1565c0?logo=materialformkdocs&logoColor=white" alt="MkDocs Material">
<img src="https://img.shields.io/badge/Arduino-скетчи-00979D?logo=arduino&logoColor=white" alt="Arduino">

**Конспекты, схемы и скетчи с занятий по робототехнике для групп А и С.**

</div>

---

> [!TIP]
> Это страница с исходниками. **Сам сайт — по кнопке выше:** https://mosrobotics.github.io/materials7-8/
>
> Сайт собирается автоматически из папки `docs/`. После любого изменения в ветке `main` он обновляется сам примерно за 1–2 минуты.

## Как исправить страницу

1. Откройте страницу на сайте и нажмите **карандаш** справа от заголовка.
2. Войдите в GitHub (нужно быть участником организации Mosrobotics).
3. Исправьте текст и нажмите **Commit changes**.

## Как добавить новую страницу

1. В нужной папке (например, `docs/group-c/theory/`) нажмите **Add file → Create new file**.
2. Назовите файл латиницей, например `servo.md`.
3. Добавьте строку о странице в `mkdocs.yml` в раздел `nav:`:
   ```yaml
   - Сервопривод: group-c/theory/servo.md
   ```
4. Добавьте ссылку в таблицу на странице раздела (`index.md`).

## Как добавить ссылку на оборудование

Откройте файл [`equipment-links.txt`](equipment-links.txt) → карандаш → допишите строку и нажмите **Commit changes**:

```
Паяльник: https://www.ozon.ru/product/...
```

Ссылка сама встанет в строку «Паяльник» на странице «Оборудование». Название пишите как в таблице;
если такого инструмента нет — он появится в разделе «Другое». Ещё проще — через Telegram-бота: `/material` → «Оборудование».

## Шпаргалка по разметке

| Что нужно | Как написать |
|-----------|--------------|
| Заголовок | `## Заголовок` |
| **Жирный** | `**текст**` |
| Ссылка | `[текст](https://адрес)` |
| Картинка | `![подпись](../../assets/images/файл.png)` |
| Код | три обратные кавычки и `cpp`, в конце снова три кавычки |
| Формула | `$R = U / I$` |

Цветные блоки:

```markdown
!!! tip "Совет"
    Текст с отступом в 4 пробела.

!!! warning "Внимание"
    Текст предупреждения.

??? question "Вопрос (раскрывается по клику)"
    Ответ.
```

Готовые примеры всех приёмов: `docs/group-c/theory/led-resistor.md` и `docs/group-c/programming/blink.md`.

## Где что лежит

- `docs/assets/images/` — картинки;
- `docs/assets/files/` — небольшие файлы для скачивания;
- большие файлы и видео храним на Яндекс Диске, на сайт ставим ссылку.

## Проверка на своём компьютере (необязательно)

```bash
pip install -r requirements.txt
mkdocs serve
```
Сайт откроется по адресу http://127.0.0.1:8000.
