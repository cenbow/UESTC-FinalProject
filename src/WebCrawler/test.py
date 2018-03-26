class AError(Exception):
     """AError---exception"""
     print('AError')

try:
     #raise AError
     a = 1
except AError:
     print("Get AError")
except:
     print("exception")
else:
     print("else")
finally:
     print("finally")
print("hello wolrd")
