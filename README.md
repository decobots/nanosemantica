Сборка докер контейнера:
docker build -t name
docker run  -e DATABASE_URL=sqlite:///foo.db -p 8080:8080  name


Пример post запроса:

curl -X POST -H "Content-Type: application/json" -d "@products.json"  http://localhost:8080/

products.json:
{
  "мясо": 500,
  "огурец": 5,
  "картофель": 5
}