host = os.popen('hostname -I').read()
app.run(host=host, port=5000, debug=False)