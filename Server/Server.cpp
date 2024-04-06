#include "SharedObject.h"
#include "Semaphore.h"
#include "thread.h"
#include "socketserver.h"
#include <stdlib.h>
#include <time.h>
#include <list>
#include <pthread.h>
#include <vector>
#include "Board.h"
#include <algorithm>

struct Game {
    int id;
    Board board;
    std::vector<Socket> players;
};

std::vector <Game> games;


class CommThread : public Thread
{

private:
    Socket theSocket;
public:
    CommThread(Socket const & p)
        : Thread(true),theSocket(p)
    {
        ;
    }
    int ThreadMain(void)
    {
        ByteArray bytes;
        std::cout << "Created a socket thread!" << std::endl;
        for(;;)
        {
            int read = theSocket.Read(bytes);

            if (read == -1)
            {
                std::cout << "Error in socket detected" << std::endl;
                break;
            }
            else if (read == 0)
            {
                std::cout << "Socket closed at remote end" << std::endl;
                break;
            }
            else

            {
                std::string theString = bytes.ToString();
                std::cout << "Received: " << theString << std::endl;

                // Handle game-related commands
                if (theString == "start") {
                    Game newGame;
                    newGame.players.push_back(theSocket);
                    games.push_back(newGame);

                //Avaialable games
                } else if (theString == "join") {
                
                    std::vector<int> availableGames;
                    for (const Game& game : games) {
                        if (game.players.size() < 2) {
                            availableGames.push_back(game.id);
                            break;
                        }
                    }

                    std::string availableGamesString = "Available games: " + std::to_string(availableGames.size());
                
                    for (int id : availableGames) {
                        availableGamesString += " " + std::to_string(id);
                    }
                    ByteArray bytes(availableGamesString);
                    theSocket.Write(bytes);
                
                } else if (theString.substr(0,4) == "join"){
                    int gameId = std::stoi(theString.substr(5));

                    for (Game& game : games) {
                        if (game.id == gameId && game.players.size() < 2) {
                            game.players.push_back(theSocket);
                            break;
                        }
                    }
                }
                
                else if (theString == "end") {
                    // Find the game this socket is part of and remove it
                    auto it = std::find_if(games.begin(), games.end(), [&](const Game& game) {
                    return std::find(game.players.begin(), game.players.end(), theSocket) != game.players.end();
                    });
                    if (it != games.end()) {
                        games.erase(it);
                    }
                }

                theSocket.Write(bytes);
            }
        }
        std::cout << "Thread is gracefully ending" << std::endl;
    }
};

class KillThread  : public Thread

{
private:
    SocketServer & theServer;
public:
    KillThread(SocketServer & t)
        : Thread(true),theServer(t)
    {
        ;
    }
    int ThreadMain(void)
    {
        std::cout << "Type 'quit' when you want to close the server" << std::endl;
        for (;;)
        {
            std::string s;
            std::cin >> s;
            if(s=="quit")
            {
                theServer.Shutdown();
                break;
            }
        }
    }

};

int main(void)
{
    std::cout << "I am a socket server" << std::endl;
    SocketServer theServer(3000);
    KillThread killer(theServer);
    std::vector<CommThread *> threads;

    for(;;)
    {
        try
        {
            Socket newSocket = theServer.Accept();
            std::cout << "Received a socket connection!" << std::endl;
            threads.push_back(new CommThread(newSocket));
        }
        catch(TerminationException e)
        {
            std::cout << "The socket server is no longer listening. Exiting now." << std::endl;
            break;
        }
        catch(std::string s)
        {
            std::cout << "thrown " << s << std::endl;
            break;
        }
        catch(...)
        {
            std::cout << "caught  unknown exception" << std::endl;
            break;
        }
    }

    std::cout << "End of main" << std::endl;
    for (int i=0;i<threads.size();i++)
        delete threads[i];
}
