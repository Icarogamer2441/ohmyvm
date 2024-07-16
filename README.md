# ohmyvm
my own vm in python

## how to compile the python files
if you're in linux you can run [build.sh file](./build.sh) and if you use windows you can build using windows commands<br>
you need to create the "bin" folder to compile and put the output files in it

## how to compile and run a file
### compile
example of file (you can use any extension but i use .oasm for no reason):
```console
./bin/omasm hello.oasm out.om
```
you can only create output files with .om extension!
### run
example of file:
```
./bin/om out.om
```
