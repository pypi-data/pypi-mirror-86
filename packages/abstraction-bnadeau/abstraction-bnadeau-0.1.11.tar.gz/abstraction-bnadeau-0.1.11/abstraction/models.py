


class ObjectManager(list):
  def __init__(self, *args, **kwargs):
    super (ObjectManager, self).__init__(*args, **kwargs)
    

class Object(object):
  
  def __init__(self):
      self.__class__.__addnew__(self)
      
  def __repr__(self):
    return '<%s>' % self.__class__.__name__      
      
      
  @classmethod
  def __addnew__(cls, obj, instance_cls=True):
    classname = cls.__name__
    
    # Add a list to the class with the class name attached to it.
    key = classname + '_objects'
    if (key not in cls.__dict__.keys()):
        setattr(cls, key, ObjectManager())
        
    # Map the list witht the class name to the classes objects variable
    #if (instance_cls):
    if ('objects' not in cls.__dict__.keys()):
          setattr(cls, 'objects', cls.__dict__[key])

    cls.objects.append(obj)
    
    # Add this instance to every base classes list of objects
    # Let the function know that we dont want to override the objects list for these classes.
    for base_cls in cls.__bases__:
        func = getattr(base_cls, '__addnew__', None)
        if callable(func):
            base_cls.__addnew__(obj, False)
            
            



            
        




### An object that can describe anything. 
### It accepts any parameter to initialize,
### including type, a variable that can be used to better describe this object
class AbstractObject(dict):
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            
    def __str__(self):
        string = "<" + self.type + ': '
        for variable, value in self.__dict__.items():
            string += variable + "=" + str(value) + ", "
        return string + ">"
            


