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


### TODO:

- Make some stupid way of saving config like ls.config = {'local_path': 'here/there/folder/local_storage', 'use_pickle':False}
