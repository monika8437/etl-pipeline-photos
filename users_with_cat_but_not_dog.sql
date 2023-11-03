-- Write a query to find all users who have a photo of a cat in their library but not a dogWrite a query to find all users who have a photo of a cat in their library but not a dog
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