
// ==UserScript==
// @name         Push Scratch wsvar to Local WS IID
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Source: https://github.com/EloiStree/2024_05_10_TamperMonkeyToRsaTunnelingIID/blob/main/ScratchToLocalWebsocket/ScratchVarToLocalWebsocket.js
// @description  Test zone: https://scratch.mit.edu/projects/1018462085
// @author       Eloi stree
// @match        https://scratch.mit.edu/projects/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=integergames.be
// @require      http://code.jquery.com/jquery-1.8.3.min.js

// @grant        none

// ==/UserScript==
//TO LOOK LATER
//https://github.com/travist/jsencrypt
(function() {
    'use strict';

/*
What this code do ?
This code overlook at the HTML code when you are on https://scratch.mit.edu/projects/*
It searches about the HTML of a variable display in the scratch game that are a HTML Div code.
The div Id are
- name: .monitor_label_ci1ok
- value: .monitor_value_3Yexa

It add the key value in a dictionary if the value changed only to avoid spam when send outside of the script.

With the help of a unsecure websocket client it send the value as a integer converted to 4 bytes in little format.
To use this script you need to recover it with a websocket server of your own and turn back the 4 bytes to integer.

*/


//Just show in console that the script is injected
console.log("Hello Tamper to Integer :).\n Websocket client will try to connect to websocket server. \n  ")

// Creating url to push on local computer at the port 7073 the integer that changed.
var socketUrl= 'ws://localhost:7072';
    
    
// If you use relay server on your computer
socketUrl= 'ws://localhost:7072';
/////////////////////////////////////////////// SWICH THOSE LINE BASED ON YOUR GOAL.
// If you use the default pi server behind ddns
socketUrl= 'wss://apint.ddns.net:4725/';

console.log("Server link : "+socketUrl);

// Defined the var of the future websocket client
var socket = null;
// Will be use to have a way to know that the server is still in theory connected
var isConnectionValide=false;
// Dictionnary that is storing the previous state when a change happened
// Used to detect any change in the Scratch variable
var previousData = {};

// Do we want to display console log in the browser or not.
var useConsoleDebug=false;

/* This function is use to make some test. It allow to push randomply a integer if the connection is still active */
   function PushMessageToServerRandomInteger(){
       if(!isConnectionValide){
           return;
       }
       const randomInt = Math.floor(Math.random() * 1000000000) + 1;
       PushMessageToServerInteger(randomInt)

   }
    /*This function send an integer into a exportable value with the date of when it was detected as a ulong format */
   function PushMessageToServerIntegerDate(integer){
    if(!isConnectionValide){return;}
      var value =integer;
       // Get the current UTC time in milliseconds
     const currentTimeMillis = Date.now();

     // Convert to an unsigned long (assuming 64-bit)
     const ulongVar = BigInt(currentTimeMillis);

     // Create a byte array of length 12
     const byteArray = new Uint8Array(12);
     // Set the first 4 bytes of the array from the value in little-endian format
     byteArray[0] = value & 0xFF;
     byteArray[1] = (value >> 8) & 0xFF;
     byteArray[2] = (value >> 16) & 0xFF;
     byteArray[3] = (value >> 24) & 0xFF;

     // Set the next 8 bytes of the array from ulongVar in little-endian format
     const view = new DataView(byteArray.buffer);
     view.setBigUint64(4, ulongVar, true);
     socket.send(byteArray);
    if(useConsoleDebug)
     console.log("Random date with date:", value)
}


/*This function send an integer into a exportable value and don't attach to it a date value */
function PushMessageToServerInteger(integer){
    if(!isConnectionValide){return;}

      var value =integer;
     const byteArray = new Uint8Array(4);
     byteArray[0] = value & 0xFF;
     byteArray[1] = (value >> 8) & 0xFF;
     byteArray[2] = (value >> 16) & 0xFF;
     byteArray[3] = (value >> 24) & 0xFF;
     socket.send(byteArray);
    if(useConsoleDebug)
     console.log("Int Pushed to web local server:", value)
}




var server_is_offline=false;

/*Try to reconnect with a new websocket client if it detect that the current is for any reason not there */
function ReconnectIfOffline(){

    if (socket !=null && socket && socket.readyState === WebSocket.OPEN) {
    }
    else{
        isConnectionValide=false
        try{
            if(useConsoleDebug)
            console.log('Try estabalish connection with: '+socketUrl);
            socket = new WebSocket(socketUrl);
            //socket = new WebSocket(socketUrl, null, { rejectUnauthorized: false });
            // Event listener for when the connection is established
            socket.addEventListener('open', () => {
                console.log('WebSocket connection established');
                isConnectionValide=true
            });

            // Event listener for incoming messages
            socket.addEventListener('message', (event) => {
                console.log('Received message from server:', event.data);

            });

            // Event listener for when the connection is closed
            socket.addEventListener('close', () => {
                console.log('WebSocket connection closed');
                isConnectionValide=false

            });

            // Event listener for errors
            socket.addEventListener('error', (error) => {
                console.error('WebSocket error:', error);
            });
            server_is_offline=false;
            console.log("Server Online");
        }catch(Exception){
            server_is_offline=true;
        }
    }
}



    /*This will send key value as integer if it detect the variable start with "wsvar " and connection is open */
    function sentKeyValueToOpenWebsocket(label, value) {

        if (socket && socket.readyState === WebSocket.OPEN) {
            const lowerStr = label.toLowerCase().trim();

            if (lowerStr.startsWith("wsvar ")) {
                const number = parseInt(value);
                //console.log("The string starts with 'wsvar'");
                if (!isNaN(number)) {

                    console.log("Change detectected wsvar int: "+value)
                    PushMessageToServerInteger(number);
                    //console.log("The string is a valid integer:", number);
                } else {
                    //console.log("The string is not a valid integer");
                }
            }

        }
    }


    /*This will look in the HTML code for the Scratch variable as HTML.
    If it find the div of the key value that start with "wsvar ". It will set them in the dictionary and notify if it changed*/
    function extractAndSendData() {
        var dataString = '';
        // Find all elements with class 'react-contextmenu-wrapper'
        var elements = document.getElementsByClassName('react-contextmenu-wrapper');
        // Iterate through each element
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            // Find elements with classes 'monitor_label_ci1ok' and 'monitor_value_3Yexa' within current element

            var labelElement = element.querySelector('[class^="monitor_label_"]');
            var valueElement = element.querySelector('[class^="monitor_value_"]');

            // Extract text content from label and value elements
            var label = labelElement ? labelElement.textContent.trim() : '';
            var value = valueElement ? valueElement.textContent.trim() : '';

            if (label && value) {
                if(label.startsWith("wsvar ") ){
                   dataString += label + ': ' + value + '\n';
                    if (!previousData[label]) {
                        previousData[label] = value;
                        sentKeyValueToOpenWebsocket(label, value);
                    } else {
                        if (previousData[label] !== value) {
                            previousData[label] = value;

                            console.log("Change detectected: "+value)
                            sentKeyValueToOpenWebsocket(label, value);
                        }
                    }
                }
            }
        }
    }

    if(useConsoleDebug)
        console.log("Interval :) Start ")

    setInterval(ReconnectIfOffline, 1000);
    setInterval(extractAndSendData,15);
    if(useConsoleDebug)
        console.log('Code end reach');

})();
