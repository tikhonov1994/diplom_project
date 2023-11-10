from functional.test_data.db_data import test_user_info, test_user_profile_create_info

test_user_profile = {
    'id': test_user_info['id'],
    'name': 'test_user, surname',
    'surname': 'test_user_surname',
    'country': 'Zimbabwe',
    'time_zone': 'UTC+2',
    'phone_number': '26324234123',
    'avatar_link': None,
    'avatar_status': 'WITHOUT'
}

test_user_profile_create = {
    'id': test_user_profile_create_info['id'],
    'name': 'test_create_name',
    'surname': 'test_create_surname',
    'country': 'Countryname',
    'time_zone': 'UTC+4',
    'phone_number': '+79123123123',
    'avatar_link': None,
    'avatar_status': 'WITHOUT'
}
