from webAPi import create_app
# 用于部署启动项目:
# python main.py
# flask run (FLASK_APP=main)
app = create_app()
config = app.config


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get("HOST", 5000))
