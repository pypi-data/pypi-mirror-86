# SharedCollections

SharedCollections contains, some commonly used data structure collections like queue and stack, which can be accessed by multiple access managers, individually. Currently it is alpha stage.

## Version

The current version of this module is `0.0.2`.

Check it by below command.

```bash
python3 -m sharedcollections.version
```

## Dependencies

No such external dependencies, and currently it is supported in python 3.5+ only.

## Installation

### Using git

```bash
git clone https://github.com/antaripchatterjee/SharedCollections
cd SharedCollections
python3 setup.py install
```

### Using pip
```bash
pip3 install SharedCollections
```

## Uninstallation

```bash
pip3 uninstall SharedCollections
```

## Usage

Example of using `SharedQueue` is given below as a reference.

```python
from sharedcollections.queue import SharedQueue

if __name__ == "__main__":
    q = SharedQueue()
    # Constructor of SharedQueue can take two named aruguments
    # maxsize, default is None, decideds the maximum length of
    # items of the queue.
    # maxmgr. default is None, decideds the maximum count of the
    # managers of the queue.
    mgr1 = q.new_manager()
    q.put(1)
    mgr2 = q.new_manager()
    q.put(2)
    q.put(3)
    print('Length of mgr1', len(mgr1))
    print('Length of mgr2', len(mgr1))
    for i in mgr1:
        print(i, end=' ')
    print('\n------------------------')
    print(next(mgr2))
    print(mgr2.have_values())
    print(next(mgr2))
```

The above code will generate the below output.

```output
Length of mgr1 3
Length of mgr2 2
1 2 3
------------------------
2
True
3
```

## License

This library is licensed under [MIT](https://github.com/antaripchatterjee/SharedCollections/blob/master/LICENSE) license.

## Development

This is currently in Alpha stage, soon I will release a newer version with shared stack.
