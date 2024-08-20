# Game 
## Approach :
we are given an exe of the chrome dino game written in c++ \
It was given in description the game source was yanked from \
<a href=https://github.com/shlomnissan/trex-runner>`https://github.com/shlomnissan/trex-runner`</a>

looking at main.cpp in this
```cpp

#define SDL_MAIN_HANDLED

#include <memory>

#include "core/game.h"
#include "game/main_stage.h"
#include "game/shared.h"

int main() {
    Game game {"Trex Runner!", kWindowWidth, kWindowHeight};

    // load assets
    game.LoadAudio("sfx_achievement.wav", "achievement");
    game.LoadAudio("sfx_hit.wav", "hit");
    game.LoadAudio("sfx_jump.wav", "jump");
    game.LoadSpritesheet(
        "spritesheet",
        {"spritesheet.png", "spritesheet.json"}
    );

    // start game
    game.Start(std::make_unique<MainStage>());

    return 0;
}
```
and comparing it with main function in the IDA decompilation 
![image](https://github.com/user-attachments/assets/514bc4eb-99af-46e2-8b4f-fa2fc706e0ad)

we can confirm a few things. 
1. `sub_140004AD0` is Game class
2. `sub_140004C20` is LoadAudio function
3. `sub_140004C60` is LoadSpritesheet

there should also be the start game somewhere down below. \
found a function that sets up the map down below which was prolly `make_uniqueStage` \
THen found a very interesting function : \
![image](https://github.com/user-attachments/assets/44edf484-811e-47a2-a47f-643bec596ab5)

immediate thoughts were z3 z3

sadly this was too much to z3, involved more functions within. I was honestly lazy to z3 this. \
but going through the code. it became clear these were checks against something and this was definitely not in the trex runner game source code that was provided. \
mainly these checks gave it away \
![image](https://github.com/user-attachments/assets/31bb9c9f-af3a-4c4b-bfb1-a8927d37bb99)

it was comparing something with `1337` `6969` \
and in the case, triggering something more. \
Aakash tried patching these checks \
to bypass them in `x64dbg` but it didn't work for some reason.

now we know something = 6969 is triggering bullshite (most prolly flag)

so felt natural that something = score

so opened cheat engine to mess up score. \
but couldn't find score in the memory when searching the score value directly \
even with different data types. That meant the score that is being displayed on screen \
was probably being stored as the ` score_on_screen * something ` \
then there sshould be a function that was performing the same. \
in the github there was this \
![image](https://github.com/user-attachments/assets/b840940c-39f5-4cb6-8f88-02a8da1f5248)

so there probably is a similar function in the binary somewhere. \
and akas the goat finds it \
![image](https://github.com/user-attachments/assets/48da08c5-aea0-465f-b41e-ad408be4f7cd)

bam so `score = double(stored_val) * 0.025` \
so `score * 40 = double(stored_val)` \
looked for a value = score * 40 that was a double in cheat engine, set it to 6969 * 40 and gotit \
![image](https://github.com/user-attachments/assets/0fdfc5cf-67b2-49f2-8204-4052c9146152)


## takeaways :
- learnt how to map a function's base addr to ida and x64dbg at the same time (apologies, should've picked this up earlier)
- learnt new ways to set breakpoints in cheat-engine
- learnt cooler ways to search for functions and their names in IDA
- generally got slightly better at using IDA and x64dbg
