# CSI-275-01 Final Project

## How to Run the Application

### Server
1. Navigate to the directory containing the server file
2. Run the server using:
   ```
   python final_server.py
   ```
3. The server will start 

### Client
1. After starting the server, open new terminal windows for each client
2. Navigate to the client file which should be in the same folder
3. Run the client using:
   ```
   python final_client.py
   ```
4. Enter a unique username when prompted
5. You will be connected to the chat server

## Server Ports

The server listens on two ports:
- **7778 (READ_PORT)**: For handling client message sending
- **7779 (WRITE_PORT)**: For client registrations (START messages)

## How to Use the Chat Client

When you start the client, you will be prompted to enter a username. 
Then you will be prompted to enter the message type. See below for message types:


### Sending Broadcast Messages
To send a message to all connected users:
1. Type `BROADCAST` at the message type prompt
2. Enter your message when prompted
3. The message will be sent to all connected users

### Sending Private Messages
To send a message to a specific user:
1. Type `PRIVATE` at the message type prompt
2. Enter the username of the recipient when prompted
3. Enter your message when prompted
4. The message will be sent only to the specified user

### Exiting the Chat
To disconnect from the server:
1. Type `EXIT` at the message type prompt
2. You will be disconnected and other users will be notified of your departure

## Example Session

Here's an example of a chat session with users Test and Hi. 
(The input and output is exactly how it looks on the console):


### Hi's Terminal
```
Please enter a username: Hi
Please enter the message type you want to send: <BROADCAST, PRIVATE> OR <EXIT> to exit:
SERVER: Hi has joined the chat.

SERVER: Test has joined the chat.

Test: Hello everyone!

Test(private): Hey Hi, how are you?
BROADCAST
Please enter the message type you want to send: <BROADCAST, PRIVATE> OR <EXIT> to exit:
Please enter the message you want to broadcast: Hi Test!

Hi: Hi Test!

Test has left.
EXIT

Process finished with exit code 0
```

### Test's Terminal
```
Please enter a username: Test
Please enter the message type you want to send: <BROADCAST, PRIVATE> OR <EXIT> to exit: 
SERVER: Test has joined the chat.
BROADCAST
Please enter the message you want to broadcast: Hello everyone!
Please enter the message type you want to send: <BROADCAST, PRIVATE> OR <EXIT> to exit: 
Test: Hello everyone!
PRIVATE
Please enter the username of the person you want to message: Hi
Please enter the message you want to send: Hey Hi, how are you?
Please enter the message type you want to send: <BROADCAST, PRIVATE> OR <EXIT> to exit: EXIT
Test(private): Hey Hi, how are you?

Hi: Hi Test!
EXIT

Process finished with exit code 0
```