## Usage

Build a container to run the script, with dependencies installed:
```
docker build -t fetch-dewikipedia-data .
```

Run the script in the container: (outputs results to stdout)
```
docker run -it --rm --name fetch-data -v "$PWD":/usr/src/app -w /usr/src/app fetch-dewikipedia-data python fetch-german-wikipedia-excellent-articles.py
```
