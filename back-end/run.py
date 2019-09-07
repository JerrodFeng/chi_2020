from app import app

# The port number should be the same as the front end
#try:
app.run(host='127.0.0.1', port=14004, use_reloader=False, debug=True)
#except:
    #print("Something wrong!")

