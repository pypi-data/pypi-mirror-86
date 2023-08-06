# Python Noodle Extensions Editor (PNEE)
*pronounced /nē/ (Ni)*
```
PPPPPPPPPPPPPPPPP   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
P::::::::::::::::P  N:::::::N       N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
P::::::PPPPPP:::::P N::::::::N      N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
PP:::::P     P:::::PN:::::::::N     N::::::NEE::::::EEEEEEEEE::::EEE::::::EEEEEEEEE::::E
  P::::P     P:::::PN::::::::::N    N::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
  P::::P     P:::::PN:::::::::::N   N::::::N  E:::::E               E:::::E             
  P::::PPPPPP:::::P N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE   
  P:::::::::::::PP  N::::::N N::::N N::::::N  E:::::::::::::::E     E:::::::::::::::E   
  P::::PPPPPPPPP    N::::::N  N::::N:::::::N  E:::::::::::::::E     E:::::::::::::::E   
  P::::P            N::::::N   N:::::::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE   
  P::::P            N::::::N    N::::::::::N  E:::::E               E:::::E             
  P::::P            N::::::N     N:::::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
PP::::::PP          N::::::N      N::::::::NEE::::::EEEEEEEE:::::EEE::::::EEEEEEEE:::::E
P::::::::P          N::::::N       N:::::::NE::::::::::::::::::::EE::::::::::::::::::::E
P::::::::P          N::::::N        N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
PPPPPPPPPP          NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
```
## What is it?
This is a Python Noodle Extensions Editor for Beat Saber levels. Manually editing a JSON file over a long period of time can get really annoying, so this should speed up the process!

## How do I use it?
The docs can be found [Here!](https://github.com/megamaz/NoodleExtensions-python/blob/master/docs/documentation.md) (needs to be finished!)\
Just go in the releases tab and download the latest version.

## Extra notes:
- Made entirely in python
- Pull requests are appreciated. Someone needs to fix up my horid code.
## Samples
```py
from noodle_extensions import Editor, Animator
from noodle_extensions.constants import EventType, Animations

editor = Editor("YourLevel.datPath")
animator = Animator(editor)

# Animations can go here.
# Basic position animation (that does nothing)
animator.animate(EventType().AnimateTrack, Animations().position, [[0, 0]], "DummyTrack", 0, 3)
```

## Current Issues:
None
#### Currently testing features (checked features have been tested and are working)
* [X] Editor.updateDependencies
* [X] Editor.editBlock
* [X] Editor.editWall
* [X] Editor.getBlock
* [X] Editor.getWall
* [X] Editor.removeEvent
* [X] Animator.animate
* [X] Animator.animateBlock
* [X] Animator.animateWall
* [X] Animator.editTrack
