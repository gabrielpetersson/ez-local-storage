# ez-local-storage

Python library filled with bad practises for how code should behave! Great for saving data and loading it anywhere asap. Perfect for saving and loading fixture test data.

### Usage

```
import local_storage as ls

ls.my_new_file = [{"foo":"bar"}] # creates a json and saves it  

print(ls.my_new_file.load())  # prints [{"foo":"bar"}]

print(ls.my_new_file.append_({"bar":"foo"})) # prints [{"foo":"bar"}, {"bar":"foo"}] and saves it locally
```

### Boring usage
```
import local_storage.local_storage as ls
import JsonFile from local_storage 

file = JsonFile('some_name', {1:2})
file.path = 'some/path'

ls.add_file(file)

print(ls.load('some_name'))  # prints {1:2}, can also be done with print(ls.some_name.load())
print(ls.some_name.path)  # prints 'some/path'
print(ls.path)  # prints path to local_storage
```


### TODO:
- complete sub directories functionality: ls.add_sub = 'sub_dir' and then ls.sub_dir.some_file = {1:2}. Very cool.
