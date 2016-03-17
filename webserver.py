from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import cgi
    
#The web server code can be classified into two main categories - main and handler
#The main code initializes the web server by specifying which port it is listening
#on and the handler code contains the functionality that needs to be run depending
#on the request received by the Server
class webserverHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                
                #Server tells the client the request is successfully processed
                self.send_response(200)
                
                #Server will be sending html text
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = "<html><body>"
                output += "<b><a href='/restaurant/new'>Make a new Restaurant</a>"

                restaurants = getRestaurantDetails()
                for restaurant in restaurants:
                   output += "<p> {0} </p>".format(restaurant.name) 
                   output += "<a href='/restaurant/{0}/edit'>Edit</a>".format(restaurant.id)
                   output += "</br>"
                   output += "<a href='/restaurant/{0}/delete'>Delete</a>".format(restaurant.id)

                output += "</body></html>"
                
                #Server sends the output to the client
                self.wfile.write(output)
                return
            
            elif self.path.endswith("/restaurant/new"):
                print("Display form to create a new restaurant")

                #Server tells the client the request is successfully processed
                self.send_response(200)
                
                #Server will be sending html text
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += '''<form method = "POST" enctype = "multipart/form-data" action="/restaurant">
                             Enter name of new restaurant: <input name = "name" type = "text"> <br/>
                             <input type = "submit" value = "Create"> </form>'''
                output += "</body></html>"

                #Server sends the output to the client
                self.wfile.write(output)
                return

            elif self.path.endswith("/edit"):
                print("Editing restaurant name")
                id = self.path.split('/')[2]

                #Server tells the client the request is successfully processed
                self.send_response(200)
                
                #Server will be sending html text
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += '''<form method = "POST" enctype = "multipart/form-data" action="/restaurant/{0}/edit">
                             Enter new name: <input name = "new_name" type = "text"> <br/>
                             <input type = "submit" value = "Rename"> </form>'''.format(id)
                output += "</body></html>"

                #Server sends the output to the client
                self.wfile.write(output)
                return

            elif self.path.endswith("/delete"):
                print("Deleting restaurant")
                id = self.path.split('/')[2]

                #Server tells the client the request is successfully processed
                self.send_response(200)
                
                #Server will be sending html text
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += '''<form method = "POST" enctype = "multipart/form-data" action="/restaurant/{0}/delete">
                             Are you sure you want to delete this restaurant? </br>
                             <input type = "submit" value = "Delete"> </form>'''.format(id)
                output += "</body></html>"

                #Server sends the output to the client
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found {0}'.format(self.path))

    def do_POST(self):
        try:
           
            if self.path.endswith('/restaurant'):

                #Retrieving the data from the name field of the form
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('name')

                    #Creating a restaurant
                    createRestaurant(message_content[0])

                    #Redirect back to the restaurant page
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

                    return

            elif self.path.endswith('/edit'):

                #Retrieving the data from the name field of the form
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('new_name')

                    #Editing the restaurant name in the database
                    restaurant = getRestaurantById(self.path.split('/')[2])
                    restaurant.name = message_content[0]
                    session = createSession()
                    session.add(restaurant)
                    session.commit()

                    #Redirect back to the restaurant page
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            elif self.path.endswith('/delete'):

                #Retrieving the data from the name field of the form
                ctype, _ = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    
                    #Deleting the restaurant from the database
                    restaurant = getRestaurantById(self.path.split('/')[2])
                    session = createSession()
                    session.delete(restaurant)
                    session.commit()

                    #Redirect back to the restaurant page
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
        except:
            pass

def createSession():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind=engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session

def getRestaurantDetails():
    session = createSession()
    restaurants = session.query(Restaurant).all()
    session.close()
    return restaurants

def createRestaurant(new_name):
    session = createSession()
    newRestaurant = Restaurant(name = new_name)
    session.add(newRestaurant)
    session.commit()
    print("Committed {0} to the list of restaurants".format(new_name))
    session.close()

def getRestaurantById(id):
    session = createSession()
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.close()
    return restaurant

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print("Web server running on port {0}".format(port))
        server.serve_forever() 
        
    #This exception is triggered when the user holds Control + C on the keyboard
    except KeyboardInterrupt:
        print("Web server interrupted by user")
        server.socket.close()

if __name__ == '__main__':
    main()