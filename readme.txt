запустить uswgi:

waitress-serve --port=8000 src.falcon_app.app:app

Пример post запроса:

curl -X POST -H "Content-Type: application/json" -d "@products.json"  http://DESKTOP-B0EGCJA:8000/

products.json:
{
  "мясо": 500,
  "огурец": 5,
  "картофель": 5
}