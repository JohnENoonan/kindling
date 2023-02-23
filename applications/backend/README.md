# Backend
The backend server manages the "database" of trees. It provides http endpoints that can be used to access the data.

## Installation
* [Install go](https://go.dev/doc/install)
* Download [NVM for Windows](https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip)
* Unzip, and install
* Open a CMD window as Admin
* Run `nvm install 16.14.2`
* Run `nvm use 16.14.2`
* Run `npm install pm2@latest -g`

## How to launch the backend
The backend uses JSON files to store all of its data. It requires: a file with all of the trees, a file storing the selected trees, and a file with all of the tree bios.

### Development
For testing purpose you can launch the backend with the following command
```
go run main.go --data-file-path=/path/to/data/file --selected-file-path=/path/to/selected/tree/file --bios-file=/path/to/bios/file
```

This will launch a sever listening on port `8090`.

The selected file path will be created if there is not an existing file there.

### Production
In production the backend should be run with pm2.
* Compile the go app into an executable with `go build`
* Run the file `startServer.bat`

## Closing the backend
### Development
Simply type `ctrl+c` in the terminal running the backend.

### Production
To close you must kill the pm2 instance. Either run `pm2 kill` or run `killServer.bat`.

## API Calls

### Get all trees (15 is the default return for now) trees in a radius from a point
```
curl 'localhost:8090/all-trees?latitude=x&longitude=y&radius=z'
```
The radius should be a floating point number in miles.

### Get a random tree
```
curl localhost:8090/random-tree
```

### Add a tree to the selected list
```
curl -X POST localhost:8090/selected-trees -d '{front end tree object}'
```
The posted JSON object must be in the format that you would like to receive it again when making the get request.

### Get a list of all selected trees so far
```
curl localhost:8090/selected-trees
```
