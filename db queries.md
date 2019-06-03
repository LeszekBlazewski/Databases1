# SQL Commands for databases project

Pracownicy z czwartku z basenów 2, 6 i 11:

```SQL
SELECT s.name, s.surname, s.job, sc.poolid
FROM staff s
JOIN schedules sc ON (s.id = sc.staffid)
WHERE sc.poolid IN (2, 6, 11) AND sc.dayofweek = 'THU'
ORDER BY sc.poolid
```

Pięcioro ludzi który mają najwięcej rezerwacji w sierpniu:

```SQL
SELECT *
FROM (SELECT c.name, c.surname, COUNT(*) AS reservations
      FROM clients c
      JOIN reservations r ON (c.id = r.clientid)
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
      JOIN reservations r ON (c.id = r.clientid)
      GROUP BY c.name, c.surname
      ORDER BY total_spent DESC)
WHERE ROWNUM <= 20
```

Ludzie który pracują przy 4 basenach z najwiekszym stosunkiem ilości rezerwacji do dostępnych miejsc:

```SQL
SELECT s.name, s.surname, sc.poolid AS pool_id
FROM staff s
JOIN schedules sc ON (s.id = sc.staffid)
WHERE sc.poolid IN (SELECT pool_id
    FROM (SELECT p.id AS pool_id, (COUNT(*)/p.numberofplaces) AS rtop_ratio
          FROM reservations r
          JOIN pools p ON (r.poolid = p.id)
          GROUP BY p.id, p.numberofplaces
          ORDER BY rtop_ratio DESC)
    WHERE ROWNUM <= 4)
ORDER BY pool_id
```

Zwiększyć wypłatę o 100 ludziom pracującym na basenie na którym najwięcej unikalnych klientów zrobilo rezerwacje

```SQL
UPDATE staff
SET salary = salary + 100
WHERE id IN (SELECT s.id
    FROM staff s
    JOIN schedules sc ON (s.id = sc.staffid)
    WHERE sc.poolid = (SELECT pool_id
        FROM (SELECT p.id AS pool_id, COUNT(DISTINCT c.id) AS uniq_clients
            FROM pools p
            JOIN reservations r ON (p.id = r.poolid)
            JOIN clients c ON (c.id = r.clientid)
            GROUP BY p.id
            ORDER BY uniq_clients DESC)
        WHERE ROWNUM = 1))
```

Dać 10% podwyżki osobom, które pracują w weekend na wieczornej zmianie, a ich płaca jest niższa od średniej płacy na ich stanowisku:

```SQL
UPDATE staff
SET salary = 1.1 * salary
WHERE id IN (SELECT DISTINCT s.id
             FROM staff s
             JOIN schedules sc ON (s.id = sc.staffid)
             WHERE sc.dayofweek IN ('SAT', 'SUN')
             AND sc.starttime = '15.00'
             AND s.salary < (SELECT avgsal
                             FROM (SELECT job, avg(salary) AS avgsal
                                   FROM staff
                                   GROUP BY job)
                             WHERE job = s.job)
             GROUP BY s.id)


```