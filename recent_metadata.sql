--Write a query to find the most recent metadata for each photo belonging to a user
SELECT
  *
FROM
  (
    SELECT
      *,
        row_number() over(
        PARTITION BY user_uuid
        ORDER BY
          updated_at
      ) AS rk
    FROM
      metadata
  ) meta
WHERE
  rk = 1;
