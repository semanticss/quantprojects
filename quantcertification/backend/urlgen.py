base_url = "www.qrack.space"

def generate_url(user_name):
    assert type(user_name) == str
    custom_url = f'{base_url}/{user_name}/certification'
    return custom_url