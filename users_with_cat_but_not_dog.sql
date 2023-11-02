-- true = 1 ,false = 0

SELECT
  *
FROM
  classification
WHERE
  (
    contains_cat = 1
    AND contains_dog = 0
  );