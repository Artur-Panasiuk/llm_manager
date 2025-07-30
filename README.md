# LLM Manager

## Introduction

Utilization of llm's in projects may offer unique functionality and user experience, but avaiability of online services providing ready to use solutions should not be taken for granted.
Goal of this project is to make utilization of downloaded llm's easy in projects locally or in local network.

## General Idea

Client sends request with id, prompt, model data and status to database. Server scans for requests and processes them accordingly into llm. When finished, collection in database is updated with response and status. Client scans and fetches database for its updated request marked by id and status.

## Use cases

Having access to llm's in local area to any wireless device, gives many capabilities including, but not limited to:

- Smart home AI controller,
- Chat bots / daily home assistants,
- Local coding helper ,
- Smart NPC's in Singleplayer or LAN games
