import os
import sys
import sys  # Duplicate import

def calculate_something(items=[]):  # mutable default
    result = None
    if result == None:  # Bad identity comparison
        pass
        
    for i in range(len(items)):  # Unpythonic loop
        val = 100 * 50  # Hoist target
        print(items[i], val)
        
    try:
        x = 1 / 0
    except:  # Bare except
        print("error")
        
    api_key = "secret12345"  # Secret should be replaced
    
def calculate_something_dup(items=[]):
    result = None
    if result == None:
        pass
        
    for i in range(len(items)):
        val = 100 * 50
        print(items[i], val)
        
    try:
        x = 1 / 0
    except:
        print("error")
        
    api_key = "secret12345"
