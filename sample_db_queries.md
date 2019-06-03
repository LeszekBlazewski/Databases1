# SQL Commands for databases project

Pracownicy z czwartku z basenów 2, 6 i 11:

```SQL
SELECT s.name, s.surname, s.job, sc.id_pool
FROM staff s
JOIN schedules sc ON (s.id_s = sc.id_staff)
WHERE sc.id_pool IN (2, 6, 11) AND sc.dayofweek = 'THU'
ORDER BY sc.id_pool
```

Pięcioro ludzi który mają najwięcej rezerwacji w sierpniu:

```SQL
SELECT *
FROM (SELECT c.name, c.surname, COUNT(*) AS reservations
      FROM clients c
      JOIN reservations r ON (c.id_c = r.id_client)
      WHERE r.reservationdate BETWEEN '19/08/01' AND '19/08/31'
      GROUP BY c.name, c.surname
      ORDER BY reservations DESC)
WHERE ROWNUM <= 5
```

Dwudziestu klientów, którzy wydali najwięcej na rezerwacje:

```SQL
SELECT *
FROM (SELECT c.name, c.surname, SUM(r.price) AS total_spent
      FROM clients c
      JOIN reservations r ON (c.id_c = r.id_client)
      GROUP BY c.name, c.surname
      ORDER BY total_spent DESC)
WHERE ROWNUM <= 20
```

Ludzie który pracują przy 4 basenach z najwiekszym stosunkiem ilości rezerwacji do dostępnych miejsc:

```SQL
SELECT s.name, s.surname, sc.id_pool
FROM staff s
JOIN schedules sc ON (s.id_s = sc.id_staff)
WHERE sc.id_pool IN (SELECT id_p
    FROM (SELECT p.id_p, (COUNT(*)/p.numberofplaces) AS rtop_ratio
          FROM reservations r
          JOIN pools p ON (r.id_pool = p.id_p)
          GROUP BY p.id_p, p.numberofplaces
          ORDER BY rtop_ratio DESC)
    WHERE ROWNUM <= 4)
ORDER BY id_pool
```

Zwiększyć wypłatę o 100 ludziom pracującym na basenie na którym najwięcej unikalnych klientów zrobilo rezerwacje

```SQL
UPDATE staff
SET salary = salary + 100
WHERE id_s IN (SELECT s.id_s
    FROM staff s
    JOIN schedules sc ON (s.id_s = sc.id_staff)
    WHERE sc.id_pool = (SELECT id_pool
        FROM (SELECT p.id_p AS id_pool, COUNT(DISTINCT c.id_c) AS uniq_clients
            FROM pools p
            JOIN reservations r ON (p.id_p = r.id_pool)
            JOIN clients c ON (c.id_c = r.id_client)
            GROUP BY p.id_p
            ORDER BY uniq_clients DESC)
        WHERE ROWNUM = 1))
```

Dać 10% podwyżki osobom, które pracują w weekend na wieczornej zmianie, a ich płaca jest niższa od średniej płacy na ich stanowisku:

```SQL
UPDATE staff
SET salary = 1.1 * salary
WHERE id_s IN (SELECT DISTINCT s.id_s
             FROM staff s
             JOIN schedules sc ON (s.id_s = sc.id_staff)
             WHERE sc.dayofweek IN ('SAT', 'SUN')
             AND sc.starttime = '15.00'
             AND s.salary < (SELECT avgsal
                             FROM (SELECT job, avg(salary) AS avgsal
                                   FROM staff
                                   GROUP BY job)
                             WHERE job = s.job)
             GROUP BY s.id_s)
```
