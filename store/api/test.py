# import base64

# encoded = base64.b64encode(b'learner@codio.com:admin')
# decoded = base64.b64decode(encoded)
# print(f'{encoded}->{decoded}')
# username,password = str(decoded,'utf-8').split(':')
# print(f'username:{username}\npassword:{password}')


def verify_dict(func):
    def inner_func(*args,**kwargs):
        for key,val in args[0].items():
            print(f'{key}:{val}')
        print('original function')
        return func(*args,**kwargs)
    return inner_func

def my_func(a_dict):
    for key,val in a_dict.items():
        print(f'{key}:{val}')

func_name = verify_dict(my_func)
func_name({'key1':'val1'})