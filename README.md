# KeyboardMod

## Mission
The mission of this project is to allow the user to create their own keyboard shortcuts that
can have python-integrated functionality such as running other sub-modules with the press of a
button or rebinding keys to complete complex tasks using other python modules.

Motivation: I, Lawrence, wanted to increase my productivity with a keyboard and reduce the time 
my hands spend moving away from the home row on my keyboard.

## Functionalities:
- Pressing and holding the caps-lock key rebinds every key on the keyboard, entering 'CapMode'
- Releasing both Lshift and Rshift at the same time rebinds every key on the keyboard separately in 'ShiftLock'
- ShiftLock can be toggled via the same shortcut or by entering and leaving 'CapMode'
- Provides a library of common-use functions for keyboard customization 


## Built in Functionality:

### CapMode 
By pressing and holding the caps lock key, CapMode is enabled and rebinds keys. Here are some
of the bindings implemented by default:

| Key | Action                                                                         |
|:---:|:-------------------------------------------------------------------------------|
|  j  | leftArrow                                                                      |
|  k  | downArrow                                                                      |
|  l  | upArrow                                                                        |
|  ;  | rightArrow                                                                     |
|  o  | move left one desktop                                                          |
|  p  | move right one desktop                                                         |
|  .  | shift one tab to the left                                                      |
|  /  | shift one tab to the right                                                     |
|  n  | capitalize the first non-cap letter <br> in a word to the left of your cursor  |
|  m  | capitalize the first non-cap letter <br> in a word to the right of your cursor |
|  s  | left one word                                                                  |
|  f  | right one word                                                                 |
|  e  | home (beginning of line)                                                       |
|  d  | end (end of line)                                                              |
|  r  | types a print statement with <br> a debug message                              |
| rAlt | highlight the word to the right of your cursor                                 |
| lAlt | highlight the word to the left of your cursor                                  |
| space | press and hold to act as shift <br> while in CapMode                           |







