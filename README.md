# ez-local-storage

 Python library filled with bad practises! Great for saving data and loading it anywhere asap. Perfect for saving and loading fixture test data

## Usage

```
import local_storage as ls

# creates a json file and saves it locally with the name "my_new_file.json" 
ls.my_new_file = [{"foo":"bar"}]  

print(ls.my_new_file.load())  
# prints [{"foo":"bar"}]

print(ls.my_new_file.append_({"bar":"foo"}))
# prints [{"foo":"bar"}, {"bar":"foo"}] and saves it locally
```
