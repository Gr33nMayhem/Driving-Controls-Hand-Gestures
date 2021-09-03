# Driving-Controls-Hand-Gestures

This project uses hand recognition with the help of TensorFlow to simulate keyboard inputs that can be used to drive cars in a generic car driving game.

How does it work?

1) A frame is taken as in input from the Webcam video stream.
2) Neural networks is used to detect the position of the hands (for details check https://github.com/victordibia/handtracking)
3) The controls work in two modes:
  - When two hands are detected, the locatio of both the hannds are used to drive and steer. 
  - When 1 hand is detected, the user can cchange gears to reverese.
4) The inputs are done with the help of pynput in python.
