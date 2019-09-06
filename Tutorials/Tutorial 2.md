# Tutorial 2
###### Stage Management
In tutorial 1, you've learned about engine and setting a window. Here you'll learn managing your stages and why is this important.

## What is Stage?
Stage concept is the most important thing after the core engine in Heat2D. All elements of a game is a part of a stage, but there can be mulitple stages and this is the important part because you can create menus, levels, etc.. with this concept.

## Setting things up
After importing and building the engine, you can create a class and inherit `heat2d.Stage` base class and call it's constructor. **Important: Your class's name is your stage's name, not you instance object's.**
```py
class MyStage(Stage):
    def __init__(self):
        super().__init__()
```

You should let the engine know of your stage's existence.
```py
engine.add_stage(MyStage())
```
You are creating an instance of your stage and adding it to the engine.

Before finishing let's have a look at stage's `update()` method. It is called by engine every tick, let's print out game's fps in your stage's update method.
```py
def update(self):
    print(engine.window.fps)
```
output should continue like this
```
59.000
59.000
59.000
...
```
## Final
Your code should be looking like this
```py
from heat2d import *

engine = Engine()

engine.window.size = (800, 600)
engine.window.title = "My first game!"
engine.window.color = (255, 255, 255)

class MyStage(Stage):
    def __init__(self):
        super().__init__()
        
    def update(self):
        print(engine.window.fps)
        
engine.add_stage(MyStage())

engine.run()
```

---

Tutorial 3 is coming soon.
