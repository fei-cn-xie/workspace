
> 本内容基于：https://www.bilibili.com/video/BV1iz4y1L7tA  
> [https://github.com/jinfeihan57/start_A_c_cpp_project ](https://github.com/jinfeihan57/learn_SDL2) 
# 1. SDL简介

## 1.1 简介
> SDL（Simple DirectMedia Layer） 是一套开源的、跨平台的多媒体开发库，专门为游戏和多媒体应用程序提供底层硬件访问的抽象层。  
> 可以把 SDL 理解为一个 “硬件抽象层”，它屏蔽了不同操作系统之间的差异（Windows、macOS、Linux、iOS、Android 等），让你可以用同一套 C/C++ 代码实现：
> - 窗口创建与管理
> - 2D/3D 图形渲染
> - 键盘、鼠标、游戏手柄输入
> - 音频播放
> - 多线程与定时器  
> ### 核心功能模块
> - 模块: 功能
> - 视频: 渲染	创建窗口、2D 图形加速、纹理渲染，也可与 OpenGL/Vulkan/Metal 配合
> - 输入事件: 键盘、鼠标、游戏手柄、触屏、加速计
> - 音频: 音频播放、简单混音（独立音频线程）
> - 系统工具: 跨平台线程、高精度计时器、文件 I/O、字节序处理

## 1.2 SDL安装

> https://libsdl.org/  
> https://github.com/libsdl-org/SDL/releases/tag/release-3.4.8  


```sh
# 通过命令行安装，提前安装msys2，ucrt64窗口中操作
pacman -S mingw-w64-ucrt-x86_64-SDL2


# 通过源码，手动编译安装
# 1. 下载源码压缩包 SDL-release-3.4.8.tar.gz
# 2. 进入ucrt64窗口，解压
tar -zxf SDL-release-3.4.8.tar.gz
# 3. 进入目录, 创建编译目录，手动编译
cd SDL-release-3.4.8/
mkdir build
cd build
cmake .. -L -G"MSYS Makefiles" -DCMAKE_INSTALL_PREFIX=`pwd`/install

# 编译
make -j16

# 安装
make install

```

```sh
# 通过编译测试，运行测试内容
cmake .. -L -G"MSYS Makefiles" -DCMAKE_INSTALL_PREFIX=`pwd`/install -DSDL_TESTS=ON

```

## 1.3 helloworld

### 1.3.1 定义cpp文件
```cpp
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
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, gWindowWidth, gWindowHeight, 0);
    
    // 等待 2 秒钟
    std::chrono::milliseconds ms(2000);
    std::this_thread::sleep_for(ms);

    // 销毁窗口并退出 SDL
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
```

### 1.3.2 定义CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16.3)
project(sdl_learn)

enable_testing()

option(BUILD_DEBUG "Build Debug" OFF)
if(BUILD_DEBUG)
    add_compile_options("-g")
endif()

set(SDL_LEARN_PROJECT_ROOT ${CMAKE_CURRENT_SOURCE_DIR})
set(SDL_LEARN_BIN_ROOT ${CMAKE_CURRENT_BINARY_DIR})

add_executable(sdl_learn
    ${CMAKE_CURRENT_SOURCE_DIR}/hello_SDL2.cpp
)

find_package(SDL2)

if(${SDL2_FOUND})
    message(STATUS "SDL2 found: ${SDL2_INCLUDE_DIRS}")
    message(STATUS "SDL2 libraries: ${SDL2_STATIC_LIBRARIES}")
    target_include_directories(sdl_learn PUBLIC ${SDL2_INCLUDE_DIRS})
    target_link_libraries(sdl_learn PUBLIC ${SDL2_STATIC_LIBRARIES})
else()
    message(STATUS "SDL2 not found, building from source" )
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/lib/SDL-release-2.28.3)
    target_link_libraries(sdl_learn PUBLIC SDL2::SDL2-static SDL2::SDL2main)
endif()


# 设置编译测试选项

option(BUILD_TESTS "Build Tests" OFF)
if(BUILD_TESTS)
    add_subdirectory(tests)
endif()
```


### 1.3.3 编译执行
```sh
mkdir build
cd build
cmake .. -LH -G"MSYS Makefiles" -DCMAKE_INSTALL_PREFIX=d/Users/fei/workspace/code_basic/sdl_learn/lib/SDL-release-2.28.3/build/install

make -j64

```

