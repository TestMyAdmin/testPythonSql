## Таблицы

#### Основные таблицы:

1. **`invoices` (Счета):** Основная таблица, где хранятся счета.
2. **`managers` (Менеджеры):** Таблица с информацией о менеджерах.
3. **`clients` (Контрагенты):** Таблица с данными о контрагентах.
4. **`invoice_items` (Товары/услуги в счете):** Содержимое каждого счета (товары или услуги).
5. **`payments` (Платежи):** Таблица для хранения информации о платежах по счетам.
6. **`shipments` (Отгрузки):** Таблица для хранения информации об отгрузках по счетам.

#### Таблица `invoices` (Счета):

- **id**: уникальный идентификатор счета.
- **invoice_number**: номер счета, который может повторяться с определенной даты.
- **client_id**: внешний ключ на таблицу `clients` (контрагент, для которого выставлен счет).
- **manager_id**: внешний ключ на таблицу `managers` (менеджер, выставивший счет).
- **issue_date**: дата выставления счета.
- **due_date**: дата, до которой должен быть оплачен счет.
- **status**: статус счета (открыт, оплачен, частично оплачен, отгружен, не отгружен и т.д.).
- **total_amount**: общая сумма счета.

#### Таблица `managers` (Менеджеры):

- **id**: уникальный идентификатор менеджера.
- **name**: имя менеджера.
- **department** Отдел, к которому принадлежит менеджер.

#### Таблица `clients` (Контрагенты):

- **id**: уникальный идентификатор контрагента.
- **name**: наименование контрагента.
- **TIN**: ИНН контрагента.

#### Таблица `invoice_items` (Товары/услуги в счете):

- **id**: уникальный идентификатор строки счета.
- **invoice_id**: внешний ключ на таблицу `invoices`.
- **product_name**: наименование товара/услуги.
- **quantity**: количество товара/услуги.
- **unit_price**: цена за единицу товара/услуги.
- **line_total**: итоговая сумма за строку количество * цена (можно вынести как функцию).

#### Таблица `payments` (Платежи):

- **id**: уникальный идентификатор платежа.
- **invoice_id**: внешний ключ на таблицу `invoices`.
- **payment_date**: дата платежа.
- **amount_paid**: сумма платежа.

#### Таблица `shipments` (Отгрузки):

- **id**: уникальный идентификатор отгрузки.
- **invoice_id**: внешний ключ на таблицу `invoices`.
- **shipment_date**: дата отгрузки.
- **shipment_status**: статус отгрузки (полная, частичная, не отгружено).

## Связи между таблицами

#### `clients` (Контрагенты) ↔ `invoices` (Счета)
#### `managers` (Менеджеры) ↔ `invoices` (Счета)
#### `invoices` (Счета) ↔ `invoice_items` (Товары/услуги в счете)
#### `invoices` (Счета) ↔ `payments` (Платежи)
#### `invoices` (Счета) ↔ `shipments` (Отгрузки)

## Индексы

```sql
-- Индекс на дату выставления счета для поиска последних счетов
CREATE INDEX idx_invoices_issue_date ON invoices (issue_date);

-- Индекс на номер счета для поиска по номеру
CREATE INDEX idx_invoices_invoice_number ON invoices (invoice_number);

-- Индекс на контрагента для поиска по контрагенту
CREATE INDEX idx_invoices_client_id ON invoices (client_id);

-- Индекс на менеджера для поиска счетов по менеджеру
CREATE INDEX idx_invoices_manager_id ON invoices (manager_id);

-- Индекс на статус счета для быстрого поиска по статусу
CREATE INDEX idx_invoices_status ON invoices (status);
```

## Запросы для типовых выборок

#### 1. Последние 20 счетов, выставленных менеджером:

```sql
SELECT *
FROM invoices
WHERE manager_id = ? -- ID менеджера
ORDER BY issue_date DESC LIMIT 20;
```

#### 2. Поиск счетов за прошлую неделю/месяц/год:

```sql
-- За прошлую неделю
SELECT *
FROM invoices
WHERE issue_date >= NOW() - INTERVAL '7 DAYS';

-- За прошлый месяц
SELECT *
FROM invoices
WHERE issue_date >= NOW() - INTERVAL '1 MONTH';

-- За прошлый год
SELECT *
FROM invoices
WHERE issue_date >= NOW() - INTERVAL '1 YEAR';
```

#### 3. Поиск всех счетов по контрагенту:

```sql
SELECT *
FROM invoices
WHERE client_id = ?; -- ID контрагента
```

#### 4. Поиск счета по номеру:

```sql
SELECT *
FROM invoices
WHERE invoice_number = ?;
```

#### 5. Просмотр содержимого счета:

```sql
SELECT i.*, ii.*
FROM invoices i
         JOIN invoice_items ii ON i.id = ii.invoice_id
WHERE i.id = ?; -- ID счета
```

## Бонус Уровень - Интеграция со статусами оплаты и отгрузки

#### Дополнительные поля:

1. В таблице `invoices` можно добавить:
    - **`payment_status`**: для хранения информации об оплате (полная, частичная, не оплачено).
    - **`shipment_status`**: для хранения информации об отгрузке (полная, частичная, не отгружено).

#### Запросы:

- **Оплаченные, но не отгруженные счета:**
  ```sql
  SELECT * FROM invoices
  WHERE payment_status = 'полная'
  AND shipment_status = 'не отгружено';
  ```

- **Отгруженные, но не оплаченные счета:**
  ```sql
  SELECT * FROM invoices
  WHERE shipment_status = 'полная'
  AND payment_status != 'полная';
  ```

#### Индексы для синхронизации:

```sql
-- Индекс для быстрого доступа к статусам оплаты
CREATE INDEX idx_invoices_payment_status ON invoices (payment_status);

-- Индекс для быстрого доступа к статусам отгрузки
CREATE INDEX idx_invoices_shipment_status ON invoices (shipment_status);
```