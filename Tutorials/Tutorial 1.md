# Tutorial 1
###### Getting Started
In this tutorial you will learn how to initialize the engine and create an empty window. At first, you have to import the game engine.
```py
from heat2d import *
```

## Initializing
You have to initialize the engine to begin using it's elements.
```py
engine = Engine()
``` 

## Window
Now you have to setup a window which your game will be displayed in. This time it will be 800x600 and named "My first game!"
```py
engine.window.size = (800, 600)
engine.window.title = "My first game!"
```

Let's make our window's background color white.
```py
engine.window.color = (255, 255, 255)
```

## Run
Everything is ready, just tell the engine to run it's main loop.
```py
engine.run()
```

## Final
Your code should be looking like this
```py
from heat2d import *

engine = Engine()

engine.window.size = (800, 600)
engine.window.title = "My first game!"
engine.window.color = (255, 255, 255)

engine.run()
```

---

In [Tutorial 2](https://github.com/kadir014/heat2d/blob/master/Tutorials/Tutorial%202.md), you will learn about stages.
