# OBJECTIVE 6 - Hardware Hacking 101 (Part 1) #

## OBJECTIVE : ##
>Ready your tools and sharpen your wits—only the cleverest can untangle the wires and unlock Santa’s hidden secrets!#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 6</summary>
>-	Hey, I just caught wind of this neat way to piece back shredded paper! It's a fancy heuristic detection technique—sharp as an elf’s wit, I tell ya! Got a sample Python script right here, courtesy of Arnydo. Check it out when you have a sec: [heuristic_edge_detection.py]((https://gist.github.com/arnydo/5dc85343eca9b8eb98a0f157b9d4d719)).
>-	Have you ever wondered how elves manage to dispose of their sensitive documents? Turns out, they use this fancy shredder that is quite the marvel of engineering. It slices, it dices, it makes the paper practically disintegrate into a thousand tiny pieces. Perhaps, just perhaps, we could reassemble the pieces?

</details>

#  

## PROCEDURE : ##
### SILVER MEDAL ###

We are given a “Santa’s little Helper (SLH) Access Card Maintenance Tool” UART-Bridge device that needs to be connected correctly to the terminal in order to access it.  We have a manual showing us the pinouts of the SLH but nothing more.
![image](https://github.com/user-attachments/assets/f5217501-95cb-470b-abf8-ff883a6549cb)

This information is enough to correctly connect the UART to the terminal and open up the console that is provided.  The correct connections are as follows:

- `GND` on the SLH goes to `G` on the terminal (preferably use a Green jumper wire for this)

- `VCC` on the SLH goes to `V` on the terminal (preferably use a Red jumper wire for this)

- `Rx` on the SLH needs to be connected to the transmitting pin `T` on the terminal

- `Tx` on the SLH need to be connected to the receiving pin `R` on the terminal

- The USB Type-C Connector goes on the USB port on the right-hand side of the SLH.
  
If we power on the terminal using the **P** button and try to establish a serial connection by pressing the **S** button, smoke comes out of one of the ICs on the terminal.  So we’ve most probably provided too much voltage.  Luckily there’s no permanent damage and we can just switch the DIP switch on the SLH to **3V**.

Now we no longer get smoke if we try to establish a serial connection but the terminal window tells us that our settings are incorrect.  Looking at the settings, we already know that the port to use is `USB0`.  However we need to determine the settings to use for the `Baud rate`, `Parity`, `Data`, `Stop bits` and `Flow Control` parameters.  

It’s clear now that we should be able to determine these settings from the pile of paper shreds we collected in the previous objective.  If only there was a way to reconstruct the original document!

The hints make this task quite easy for us by pointing us towards a Python script called `heuristic_edge_detection.py`.  Just by running this script and pointing it towards the folder with the paper slices in it, we are given a reconstructed image.  It needs to be flipped horizontally and edited very slightly, but the end result is a very useful document which just so happens to have all the information we’re looking for.  
![image](https://github.com/user-attachments/assets/a1ae7a87-4577-41d2-aa41-0959347bd6ba)

- Port: USB0
- Baud: 115200
- Parity: Even
- Data: 7 Bits
- Stop Bits: 1 bit
- Flow Ctrl: RTS

When we press the **S** button we get a successful serial connection 😊

![image](https://github.com/user-attachments/assets/ef3f7b47-41f2-4908-b76f-20cd6395c051)


