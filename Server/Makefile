Client: Client.o socket.o
	g++ -o Client Client.o socket.o -pthread -l rt

Client.o : Client.cpp socket.h
	g++ -c Client.cpp 

Server : Server.o thread.o socket.o socketserver.o Board.o Move.o
	g++ -o Server Server.o thread.o socket.o socketserver.o Board.o Move.o -pthread -l rt

Server.o : Server.cpp socket.h socketserver.h thread.h Board.h Move.h Constants.h
	g++ -c Server.cpp

thread.o : thread.cpp thread.h ThreadSem.h
	g++ -c thread.cpp

socket.o : socket.cpp socket.h
	g++ -c socket.cpp

socketserver.o : socketserver.cpp socket.h socketserver.h
	g++ -c socketserver.cpp

Board.o : Board.cpp Board.h Move.h Constants.h
	g++ -c Board.cpp

Move.o : Move.cpp Move.h
	g++ -c Move.cpp

constants.o : Constants.cpp Constants.h
	g++ -c Constants.cpp

Cleaner : CleanThreadSem.cpp
	g++ -o Cleaner CleanThreadSem.cpp -pthread -l rt