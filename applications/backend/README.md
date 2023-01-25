# How to launch the backend

For testing purpose you can launch the backend with the following command

```
go run main.go --data-file-path=/path/to/data/file --selected-file-path=/path/to/selected/tree/file
```

This will launch a sever listening on port `8090`.

The selected file path will be created if there is not an existing file there.

## API Calls

### Get all trees (15 is the default return for now) trees in a radius from a point
```
curl 'localhost:8090/all-trees?latitude=x&longitude=y&radius=z'
```

### Add a tree to the selected list
```
curl -X POST localhost:8090/selected-trees -d '{#front end tree object}'
```

### Get a list of all selected trees so far
```
curl localhost:8090/selected-trees
```
