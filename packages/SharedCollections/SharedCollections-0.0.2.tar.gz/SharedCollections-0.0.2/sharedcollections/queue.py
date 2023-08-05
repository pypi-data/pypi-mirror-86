class SharedQueue:
    pass

class SharedQueueAccessManager(object):
    def __repr__(self):
        return '{0}({1}, {2})'.format(type(self).__name__,
            id(self), 'initialized' if self.__initialized else 'deinitialized')

    def __init__(self, sharedqueue: SharedQueue):
        super(SharedQueueAccessManager, self).__init__()
        self.__sharedqueue = sharedqueue
        self.__initialized = False

    def initialize(self):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        self.__initialized = True
        return self
    
    def is_initialized(self):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        return self.__initialized == True
    
    def de_initialize(self):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        self.__initialized = False

    def __iter__(self):
        while True:
            try:
                yield self.__next__()
            except StopIteration:
                break

    def __next__(self):
        if not self.__initialized:
            raise StopIteration('The manager object has not been initialized for data access or deinitialized.')
        return self.__sharedqueue.get(self)
    
    def __len__(self):
        return self.__sharedqueue.qsize(self)
    
    def have_values(self):
        '''
        returns True if manager have access to any value of the queue
        '''
        return len(self) != 0
    
    def detouch_queue(self):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        self.de_initialize()
        self.__sharedqueue = None
    

class SharedQueueValue():
    def __repr__(self):
        return '{0}(value={1}, managers={2})'.format(
            type(self).__name__, self.__value, self.__managers)

    def __init__(self, value: object, managers: list):
        self.__value = value
        for manager in managers:
            if not isinstance(manager, SharedQueueAccessManager):
                raise TypeError('positional argument `managers` must be a set of SharedQueue object')
        self.__managers = managers
    
    @property
    def value(self):
        '''
        returns value of this item
        '''
        return self.__value
    
    def is_valid_for(self, manager: SharedQueueAccessManager):
        '''
        returns True if manager is valid for this item
        '''
        if not isinstance(manager, SharedQueueAccessManager):
            raise TypeError('positional argument `manager` must be a SharedQueue object')
        return manager in self.__managers
    
    def remove_access(self, manager: SharedQueueAccessManager):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        manager.de_initialize()
        self.__managers.remove(manager)

    def add_access(self, manager: SharedQueueAccessManager):
        '''
        Do not call this function. It is made only for internal purpose.
        '''
        manager.initialize()
        self.__managers.add(manager)
    
    def is_empty(self):
        '''
        returns True if this item does not have any manager who can access it's value
        '''
        return len(self.__managers) == 0


class SharedQueue():
    def __repr__(self):
        return 'SharedQueue(items={0}, managers={1})'.format(
            self.__items,
            self.__current_managers
        )
    def __init__(self, maxsize=None, maxmgr=None):
        if isinstance(maxsize, int):
            if maxsize < 1:
                raise ValueError('positional argument maxsize must be greater than 0 or None')
        elif maxsize is not None:
            raise TypeError('positional argument maxsize must be int type or None')
            
        if isinstance(maxmgr, int):
            if maxmgr < 1:
                raise ValueError('positional argument maxmgr must be greater than 0 or None')
        elif maxmgr is not None:
            raise TypeError('positional argument maxmgr must be int type or None')
        
        self.__maxsize = maxsize
        self.__maxmgr = maxmgr
        self.__items = list()
        self.__current_managers = set()

    def put(self, item: SharedQueueValue, no_manager_ok=False):
        '''
        put value inside the queue
        '''
        if len(self.__items) == self.__maxsize:
            raise OverflowError('Max limit({0}) of the count of item has been exceeded.'.format(self.__maxsize))
        if len(self.__current_managers) == 0:
            if not no_manager_ok:
                raise ValueError('Can not add value with empty managers')
            return None
        else:
            managers = {manager.initialize() for manager in self.__current_managers if not manager.is_initialized()}
            self.__items.append(SharedQueueValue(item, managers))
            self.__current_managers.update(managers)
            return item
    
    def get(self, manager: SharedQueueAccessManager, default=None):
        '''
        Get the data from the queue for the manager.
        '''
        data = default
        data_found = False
        should_delete_item = True
        for item in self.__items.copy():
            if item.is_valid_for(manager):
                data = item.value
                data_found = True
                item.remove_access(manager)
                if should_delete_item and item.is_empty():
                    self.__items.remove(item)
            elif data_found:
                item.add_access(manager)
                break
            else:
                should_delete_item = False
        return data
    

    def qsize(self, manager: SharedQueueAccessManager):
        '''
        returns the queue size for the manager
        '''
        size = 0
        manager_found = False
        for item in self.__items:
            if manager_found:
                size += 1
            else:
                if item.is_valid_for(manager):
                    manager_found = True
                    size = 1
        return size

    def new_manager(self):
        '''
        creates a new manager and returns it
        '''
        if len(self.__current_managers) == self.__maxmgr:
            raise OverflowError('Max limit({0}) of the count of managers has been exceeded.'.format(self.__maxmgr))
        manager = SharedQueueAccessManager(self)
        self.__current_managers.add(manager)
        return manager
    
    def remove_manager(self, manager: SharedQueueAccessManager):
        '''
        remove a manager from the queue
        '''
        for _ in manager:
            pass
        manager.detouch_queue()
        self.__current_managers.remove(manager)
    
    def get_maxsize(self):
        '''
        returns the maximum length of the queue
        '''
        return self.__maxsize
    
    def get_maxmgr(self):
        '''
        returns the maximum count of the managers of the queue
        '''
        return self.__maxmgr

