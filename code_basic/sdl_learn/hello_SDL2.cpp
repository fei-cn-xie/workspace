#include <iostream>
#include <SDL.h>
#include <chrono>
#include <thread>

constexpr int gWindowWidth = 800;
constexpr int gWindowHeight = 600;

int main(int argc, char* argv[]) {
    // 初始化 SDL 视频子系统
    SDL_Init(SDL_INIT_VIDEO);

    // 创建一个 SDL 窗口
    SDL_Window *window = SDL_CreateWindow("Hello SDL2", 
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, gWindowWidth, gWindowHeight, SDL_WINDOW_RESIZABLE);
    
    // 等待 2 秒钟
    // std::chrono::milliseconds ms(2000);
    // std::this_thread::sleep_for(ms);

    // 创建Renderer, Renderer: 渲染器
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    // 加载一张图片
    SDL_Surface *imageSurface = SDL_LoadBMP("../assets/hello.bmp");

    if(imageSurface == nullptr) {
        std::cerr << __PRETTY_FUNCTION__ << ":" << __LINE__ << std::endl;
        return -1;
    }

    // 由surface创建texture; Surface 是“那块存放像素的内存”，Texture 是“GPU 如何读取那块内存的规则和接口”。
    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, imageSurface);

    // 释放surface
    SDL_FreeSurface(imageSurface);

    bool quit = false;
    SDL_Event event;
    while (!quit) {
        // 处理事件
        SDL_PollEvent(&event);
        // if (event.type == SDL_QUIT) {
        //     quit = true;
        // }
        switch (event.type) {
            case SDL_QUIT:
                std::cout << __PRETTY_FUNCTION__ << ":" << __LINE__ << std::endl;
                quit = true;
                break;
            default:
                break;
        }
        SDL_RenderCopy(renderer, texture, nullptr, nullptr);
        SDL_RenderPresent(renderer);
    }

    // 销毁纹理和渲染器
    SDL_DestroyTexture(texture);
    SDL_DestroyRenderer(renderer);

    // 销毁窗口并退出 SDL
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}