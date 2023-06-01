Тестовое задание.

Первая часть.

Приложение имеет три эндпоинта:
1. create_user_by_phone - добавление пользователя в БД в виде "номер": "адрес". 
    При получении сигнала запускается crud "CRUDUser.upinsert_address_by_phone".
    В БД сохраняется в виде хеша по ключу 'user' с полем "номер" и значением "адрес"
    Возвращается только статус 200
2. update_address_by_phone - обновление пользователя в БД по номеру телефона.
    Работает аналогично create_user_by_phone
    Возвращается только статус 200
3. get_address_by_phone - получение информации из БД по номеру телефона.
    При получении сигнала запускается crud "CRUDUser.get_address_by_phone"
    Возвращается либо объект pydantic модели "UserModel" либо dict

Запуск приложения:

```bash
git clone https://github.com/Khusniyarovmr/public_portfolio.git
cd public_portfolio/job_tasks/job_tasks_2/app
docker-compose build
docker-compose up
```


Вторая часть.

Этот код отрабатывает за 2,5 секунды.

```sql
update test_1
set num = c.num
from (
    with t1 as (
    select fullname, split_part(fullname, '.', 1) norm_name from test_1
    )

select t1.fullname fullname_t1, t1.norm_name, b.num from t1
left join test_2 b on t1.norm_name=b.partname
) c where c.fullname_t1=fullname
;
```

Этот код когда-нибудь отработает:)

```sql
update test_1
set num = b.num
from test_2 b
where fullname like b.partname||'.';
```

Этот код отрабатывает за 3,5 секунды.
```sql
update test_1
set num=b.num
from test_2 b
where substring(fullname,1,position('.' in fullname)-1) = b.partname;
```
