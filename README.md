# bitshovel-memo
An installable plug-in service that implements the Memo protocol for BitShovel.

## Dependencies
* BitShovel must be running on your network.
* redis-cli must be install on your local machine

## Installation
Install and run the Memo component
```
docker run --network=host dfoderick/bitshovel-memo
```
## Usage
Post a message to Memo.cash
```
redis-cli publish memo.send "Test from BitShovel Memo"
```
Post a message to Memo with a topic.
```
redis-cli publish memo.send 'posttopic "BitShovel" "Test Topic"'
```
Change your Memo name
```
redis-cli publish memo.send 'setname "BitShovel Test"'
```
