# ez-local-storage

Python library filled with bad practises for how code should behave! Great for saving data and loading it anywhere asap. Perfect for saving and loading fixture test data.

### Usage

```
import local_storage as ls

# creates a json file and saves it locally with the name "my_new_file.json" (yeap just like that)
ls.my_new_file = [{"foo":"bar"}]  

print(ls.my_new_file.load())  
# prints [{"foo":"bar"}]

# prints [{"foo":"bar"}, {"bar":"foo"}] and saves it locally
print(ls.my_new_file.append_({"bar":"foo"}))
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
- Make it work. Pushed a folder from my repo so some stuff are left from there
- Make some stupid way of saving config like ls.config = {'local_path': 'here/there/folder/local_storage', 'use_pickle':False}
- Config to set save/load child-class? ls.config.save = S3Interface
- complete sub directories functionality: ls.add_sub = 'sub_dir' and then ls.sub_dir.some_file = {1:2}. Very cool.
