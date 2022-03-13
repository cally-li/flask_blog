from blogpackage import create_app
# imports create_app function from  __init__.py 

app= create_app()
# use python to run the flask module directly instead of setting environment vars
# run in debug mode to prevent having to reload server 
if __name__ == '__main__':
    app.run(debug=True)
