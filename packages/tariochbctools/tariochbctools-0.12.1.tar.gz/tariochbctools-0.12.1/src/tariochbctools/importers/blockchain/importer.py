import yaml
from os import path


from beancount.core import prices
from beancount.ingest import importer
from beancount.core import data
from beancount.core import amount
from beancount.core.number import D

import blockcypher


class Importer(importer.ImporterProtocol):
    """An importer for Blockchain data."""

    def identify(self, file):
        return 'blockchain.yaml' == path.basename(file.name)

    def file_account(self, file):
        return ''

    def extract(self, file, existing_entries):
        config = yaml.safe_load(file.contents())
        self.config = config
        self.priceMap = prices.build_price_map(existing_entries)
        baseCcy = config['base_ccy']

        entries = []
        for address in self.config['addresses']:
            currency = address['currency']
            addressDetails = blockcypher.get_address_details(address['address'], coin_symbol=currency.lower())
            for trx in addressDetails['txrefs']:
                metakv = {
                    'ref': trx['tx_hash'],
                }
                meta = data.new_metadata(file.name, 0, metakv)

                date = trx['confirmed'].date()
                price = prices.get_price(self.priceMap, tuple([currency, baseCcy]), date)
                cost = data.Cost(
                    price[1],
                    baseCcy,
                    None,
                    None
                )

                outputType = 'eth' if currency.lower() == 'eth' else 'btc'
                amt = blockcypher.from_base_unit(trx['value'], outputType)

                entry = data.Transaction(
                    meta,
                    date,
                    '*',
                    '',
                    address['narration'],
                    data.EMPTY_SET,
                    data.EMPTY_SET,
                    [
                        data.Posting(
                            address['asset_account'],
                            amount.Amount(D(str(amt)), currency),
                            cost,
                            None,
                            None,
                            None),
                    ]
                )
                entries.append(entry)

        return entries
