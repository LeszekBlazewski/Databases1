# Sample SQL commands for pool database

Employees who work at thursdays at pools with IDs = 2, 6, 11.

```SQL
SELECT s.name, s.surname, s.job, sc.id_pool
FROM staff s
JOIN schedules sc ON (s.id_s = sc.id_staff)
WHERE sc.id_pool IN (2, 6, 11) AND sc.dayofweek = 'THU'
ORDER BY sc.id_pool
```

Five clients who made most reservations in august.

```SQL
SELECT *
FROM (SELECT c.name, c.surname, COUNT(*) AS reservations
      FROM clients c
      JOIN reservations r ON (c.id_c = r.id_client)
      WHERE r.reservationdate BETWEEN '01-AUG-2019' AND '31-AUG-2019'
      GROUP BY c.name, c.surname
      ORDER BY reservations DESC)
WHERE ROWNUM <= 5
```

Twenty clients who have spent the most on reservations.

```SQL
SELECT *
FROM (SELECT c.name, c.surname, SUM(r.price) AS total_spent
      FROM clients c
      JOIN reservations r ON (c.id_c = r.id_client)
      GROUP BY c.name, c.surname
      ORDER BY total_spent DESC)
WHERE ROWNUM <= 20
```

Employees who work at four pools with the most number of reservations made on given pool.

```SQL
SELECT s.name, s.surname, sc.id_pool
FROM staff s
JOIN schedules sc ON (s.id_s = sc.id_staff)
WHERE sc.id_pool IN (SELECT id_p
    FROM (SELECT p.id_p, (COUNT(*)) AS res_amt
          FROM reservations r
          JOIN pools p ON (r.id_pool = p.id_p)
          GROUP BY p.id_p, p.numberofplaces
          ORDER BY res_amt DESC)
    WHERE ROWNUM <= 4)
ORDER BY id_pool
```

Increase the salary of employees who work at pools on which most uniq clients have made reservations.

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

Give 10% bonus to employees who work night shifts at weekends and their salary is lower than average salary on their position.

```SQL
UPDATE staff
SET salary = 1.1 * salary
WHERE id_s IN (SELECT DISTINCT s.id_s
             FROM staff s
             JOIN schedules sc ON (s.id_s = sc.id_staff)
             WHERE sc.dayofweek IN ('SAT', 'SUN')
             AND sc.endtime = 23.00
             AND s.salary < (SELECT avgsal
                             FROM (SELECT job, avg(salary) AS avgsal
                                   FROM staff
                                   GROUP BY job)
                             WHERE job = s.job)
             GROUP BY s.id_s)
```
