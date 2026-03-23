# KeyboardMod

## Mission
Our goal is to allow users to create their own keyboard shortcuts that
have python-integrated functionality such as running other sub-modules with the press of a 
button or rebinding keys to complete complex tasks using other python modules. 

This application features several different keyboard layers called "modes" that typists can 
move between, each with their own unique keybindings.


<img width="1298" height="697" alt="image" src="https://github.com/user-attachments/assets/59843d50-53cc-4522-8632-bb9e36e4808a" />

<img width="1295" height="695" alt="image" src="https://github.com/user-attachments/assets/d9094380-99ba-4bb7-bca9-ab1fd2dd7907" />

<img width="1006" height="692" alt="image" src="https://github.com/user-attachments/assets/70bed7e9-5cc7-45a4-94d2-f496bafb75ea" />


## Motivation 
I, Lawrence, wanted to increase my productivity with a keyboard and reduce the time 
my hands spend moving away from the home row while using proper typing form. I believed
it would be excellent to bind the scripts I write to make me more powerful on my machines.
After scoping out the problem I identified some key weaknesses with existing solutions and settled
on my own keyboard layering system with a centralized server for passing and storing data between 
subroutines. This allows for more flexibility and supreme integration with native windows operating 
systems and I'm proud to bring this to you all.


## Functionalities:
- Pressing and holding the caps-lock key rebinds every key on the keyboard, entering 'CapMode'
- Releasing both Lshift and Rshift at the same time rebinds every key on the keyboard separately in 'ShiftMode'
- ShiftMode can be toggled via the same shortcut or by entering and leaving 'CapMode'
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
|  '  | alt+tab (view previously focused window)                                       |
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




## Known issues

- The crtl mode cannot handle the typing of some characters (emojis). typeCharacter() needs some work. Currently values are hardcoded and that's limited.




TODO:
- Focus on both multi-person collaboration and single person tech separately
- Think about how we scale could scale api keys to integrate AI workflows
