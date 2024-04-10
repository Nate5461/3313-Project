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
#include <memory>
#include <thread>

struct Game
{
    int id;
    Board board;
    std::vector<Socket> players;
    std::vector<Semaphore*> semaphores;

    Game(std::string const &name) : id(0), board()
    {}
};

std::vector<Game *> games;

class GameThread : public Thread
{
private:
    Game &game;

public:

    GameThread(Game &g) : Thread(true), game(g) {}

    int ThreadMain(void)
    {

        std::cout << "Game thread started" << std::endl;
        std::cout << "players size: " << game.players.size() << std::endl;

        while (!game.board.checkForGameOver() && game.players.size() == 2)
        {

            std::cout << "Game not over" << std::endl;
            int currentPlayer = game.board.getLastPlayer() == P2 ? P1 : P2;
            switch (currentPlayer)
            {
            case P1:
            {
                std::cout << "Player 1's turn" << std::endl;
                std::string boardStr = game.board.getGameBoardAsString();
                
                ByteArray bytes(boardStr);
                if (!game.players[0].Write(bytes))
                {
                    std::cout << "no message" << std::endl;
                }

                ByteArray response;

                game.players[0].Read(response);

                if (response.ToString().empty())
                {
                    std::cout << "Player disconnected" << std::endl;
                    
                    
                    std::string message = "Player1 disconnected";
                    ByteArray bytes(message);
                    game.players[1].Write(bytes);
                    
                    game.semaphores[1]->Signal();

                    games.erase(std::remove(games.begin(), games.end(), &game), games.end());

                    return 0;
                }

                std::string msg = response.ToString();

                int column;
                try
                {
                    column = std::stoi(msg);
                }
                catch (std::invalid_argument &e)
                {
                    std::cout << "Invalid input" << std::endl;
                    continue;
                }
                catch (std::out_of_range &e)
                {
                    std::cout << "Invalid input" << std::endl;
                    continue;
                }

                game.board.makeMove(column - 1, P1);
                break;
            }

            case P2:
            {
                std::cout << "Player 2's turn" << std::endl;
               std::string boardStr = game.board.getGameBoardAsString();
                
                ByteArray bytes(boardStr);
                game.players[1].Write(bytes);

                ByteArray response;

                game.players[1].Read(response);

                if (response.ToString().empty())
                {
                    std::cout << "Player disconnected" << std::endl;
                    
                    
                    std::string message = "Player1 disconnected";
                    ByteArray bytes(message);
                    game.players[0].Write(bytes);
                    
                    game.semaphores[0]->Signal();

                    games.erase(std::remove(games.begin(), games.end(), &game), games.end());
                    
                    return 0;
                }

                std::string msg = response.ToString();

                int column;
                try
                {
                    column = std::stoi(msg);
                }
                catch (std::invalid_argument &e)
                {
                    std::cout << "Invalid input" << std::endl;
                    continue;
                }
                catch (std::out_of_range &e)
                {
                    std::cout << "Invalid input" << std::endl;
                    continue;
                }

                game.board.makeMove(column - 1, P2);
                break;
            }
            default:
                break;
            }
        }

        std::cout << "Game over" << std::endl;

        ByteArray bytes;
        if (game.board.getWinner() == P1)
        {

            bytes = ByteArray(game.board.getGameBoardAsString() + "Player 1 wins");
        }
        else if (game.board.getWinner() == P2)
        {
            bytes = ByteArray(game.board.getGameBoardAsString() + "Player 2 wins!");
        }
        else
        {
            bytes = ByteArray(game.board.getGameBoardAsString() + "It's a draw!");
        }

        for (int i = 0; i < game.players.size(); ++i)
        {
            game.players[i].Write(bytes);
            game.semaphores[0]->Signal();
            game.semaphores[1]->Signal();
            
        }
        
        games.erase(std::remove(games.begin(), games.end(), &game), games.end());
        return 0;
    }
};

std::vector<std::unique_ptr<GameThread>> gameThreads;

class CommThread : public Thread
{

private:
    Socket theSocket;
    Semaphore semaphore;

public:
    CommThread(Socket const &p)
        : Thread(true), theSocket(p), semaphore("CommSemaphore", 0, true)
    {
        ;
    }

    Semaphore &getSemaphore()
    {
        return semaphore;
    };
    int ThreadMain(void)
    {

        ByteArray bytes;
        std::cout << "Created a socket thread!" << std::endl;
        for (;;)
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
                if (theString == "start")
                {
                    std::string gameName = "game" + std::to_string(games.size());
                    Game *newGame = new Game(gameName);


                    newGame->id = games.size();

                    std::cout << "Creating new game" << std::endl;
                    newGame->players.push_back(theSocket);
                    newGame->semaphores.push_back(&this->getSemaphore());
                    std::cout << "Player 1 added" << std::endl;
                    

                    games.push_back(newGame);
                    std::string message = "Game " + gameName + " created. Waiting for player 2...";
                    ByteArray bytes(message);
                    //theSocket.Write(bytes);
                    semaphore.Wait();
                    // Avaialable games
                }
                else if (theString == "join")
                {

                    std::vector<int> availableGames;
                    std::string availableGamesString;

                    for (int i = 0; i < availableGames.size(); i++) {
                        if (i != 0) {
                            availableGamesString += " ";
                        }
                        availableGamesString += std::to_string(availableGames[i]);
                    }

                    
                    ByteArray bytes(availableGamesString);
                    theSocket.Write(bytes);
                }
                else if (theString.substr(0, 4) == "join")
                {
                    try
                    {
                        int gameId = std::stoi(theString.substr(5));

                        std::cout << "Joining game " << gameId << std::endl;
                        for (Game *game : games)
                        {
                            std::cout << "Checking game " << game->id << std::endl;
                            if (game->id == gameId && game->players.size() < 2)
                            {
                                std::cout << "Game found" << std::endl;
                                game->players.push_back(theSocket);
                                game->semaphores.push_back(&this->getSemaphore());
                                std::cout << "Signalling Semaphore" << std::endl;

                                gameThreads.emplace_back(new GameThread(*game));
                                //game->semaphores[0]->Signal();

                                std::cout << "Player 2 added. Game " << gameId << " started." << std::endl;
                                semaphore.Wait();
                                break;
                            }
                        }
                    }
                    catch (std::invalid_argument &)
                    {
                        std::cout << "Invalid command: game ID is not a number" << std::endl;
                    }
                    catch (std::out_of_range &)
                    {
                        std::cout << "Invalid command: game ID is out of range" << std::endl;
                    }
                }

                else if (theString == "end")
                {
                    // Find the game this socket is part of and remove it
                    auto it = std::find_if(games.begin(), games.end(), [&](Game *game) {                                // Change this line
                        return std::find(game->players.begin(), game->players.end(), theSocket) != game->players.end(); // Change this line
                    });
                    if (it != games.end())
                    {
                        games.erase(it);
                    }
                } else{
                    std::string message = "Invalid command";
                    ByteArray bytes(message);
                    theSocket.Write(bytes);
                }
            }
        }
        std::cout << "Thread is gracefully ending" << std::endl;
    }
};

class KillThread : public Thread

{
private:
    SocketServer &theServer;

public:
    KillThread(SocketServer &t)
        : Thread(true), theServer(t)
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
            if (s == "quit")
            {
                theServer.Shutdown();
                break;
            }
        }
    }
};

int main(void)
{

    try
    {
        std::cout << "I am a socket server" << std::endl;
        SocketServer theServer(3000);
        KillThread killer(theServer);
        std::cout << "Starting the server" << std::endl;
        std::vector<CommThread *> threads;

        for (;;)
        {
            try
            {
                Socket newSocket = theServer.Accept();
                std::cout << "Received a socket connection!" << std::endl;
                threads.push_back(new CommThread(newSocket));
            }
            catch (TerminationException e)
            {
                std::cout << "The socket server is no longer listening. Exiting now." << std::endl;
                break;
            }
            catch (std::string s)
            {
                std::cout << "thrown " << s << std::endl;
                break;
            }
            catch (...)
            {
                std::cout << "caught  unknown exception" << std::endl;
                break;
            }
        }

        std::cout << "End of main" << std::endl;
        for (int i = 0; i < threads.size(); i++)
            delete threads[i];
    }
    catch (const std::string &s)
    {
        std::cout << "caught string exception: " << s << std::endl;
    }
    catch (...)
    {
        std::cout << "Caught unexpected exception" << std::endl;
    }
}
