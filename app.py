from factory import creat_app

app = creat_app()

app.run(
    host = '0.0.0.0',
    port = '5000'
)