# LLM Manager

## Introduction

Utilization of llm's in projects may offer unique functionality and user experience, but avaiability of online services providing ready to use solutions should not be taken for granted.
Goal of this project is to make utilization of downloaded llm's easy in projects locally or in local network.

## Pipeline

Client sends request with request id, model id (requested beforehand) and user prompt. Server scans for requests and processes them accordingly into llm. When finished, response is avaiable from server at /get/[request id]

## Client implementation

With offloading of all AI related tasks to server, client is required basic network compatabilities only to send and receive requests from api. /client contains an example of client implementation in python.  

## Use Cases

Having access to llm's in local area to any wireless device, gives many capabilities including, but not limited to:

- Smart home AI controller,
- Chat bots / daily home assistants,
- Local coding helper,
- Smart NPC's in Singleplayer or LAN games
