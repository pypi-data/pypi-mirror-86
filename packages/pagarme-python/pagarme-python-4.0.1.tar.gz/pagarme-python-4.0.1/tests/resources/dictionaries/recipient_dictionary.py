from pagarme import bank_account
from tests.resources.dictionaries import bank_account_dictionary

BANK_ACCOUNT = bank_account.create(bank_account_dictionary.BANK_ACCOUNT)

RECIPIENT = {
    'anticipatable_volume_percentage': '80',
    'automatic_anticipation_enabled': 'true',
    'transfer_day': '5',
    'transfer_enabled': 'true',
    'transfer_interval': 'weekly',
    'bank_account_id': BANK_ACCOUNT['id']
}

UPDATE_RECIPIENT = {
    'transfer_enabled': 'false',
    'anticipatable_volume_percentage': '85'
}
