#include <iostream>

#include <SDL2/SDL.h>


using namespace std;

int main(int argc, char ** argv)
{
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		std::cout << "SDL_Init Error :" << SDL_GetError()
			  << std::endl;
	}
	SDL_Window *win =
		SDL_CreateWindow(
			"Hello World!", 100, 100, 640, 480,
			SDL_WINDOW_SHOWN);

	if (win == nullptr) {
		std::cout << "SDL_CreateWindow Error: " << SDL_GetError()
			  << std::endl;
		SDL_Quit();
		return 1;
	}



	SDL_DestroyWindow(win);
	std::cout << "Done" << std::endl;

	return 0;
}
