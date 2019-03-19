import unittest
import binascii

from torba.server.tx import BlockDeserializer  # Deserializer


class BlockDeserializeTest(unittest.TestCase):

    def test_btc_genesis(self):
        genesis = ('010000000000000000000000000000000000000000000000000000000000000000000000'
                   '3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49'
                   'ffff001d1dac2b7c01010000000100000000000000000000000000000000000000000000'
                   '00000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f'
                   '4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f'
                   '6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104'
                   '678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f'
                   '4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000')
        deserializer = BlockDeserializer(binascii.unhexlify(genesis), start=80)
        txs = deserializer.read_tx_block()
        self.assertEqual(binascii.hexlify(txs[0][0].raw).decode(), genesis[-408:])

    def test_lbc_claim(self):
        lbc_block = ('00000020e498728593fb78744fd52985bcc8777526190f56d3f9f94309bbf6aa016d3b'
                     'a0823552b8be8adae7a1fd20e7a6881d583eb7c169a57d20c18dfac41e0b752802f7372'
                     'c4fb24782d74a3d5cc8dfc877077285b75b20fb397110c66d2e3c9e639999576b57ba4f'
                     '131dce5ff70002010000000100000000000000000000000000000000000000000000000'
                     '00000000000000000ffffffff0401660102ffffffff0184fdf50500000000232102fd5d'
                     '6190be11a3f007643cc1e8cf3f6fd88805349ce6047348577a436e6c45c3ac000000000'
                     '100000001ba888e2f9c037f831046f8ad09f6d378f79c728d003b177a64d29621f481da'
                     '5d0000000049483045022100edb84a6cea712811eb6cfb9c83ee185dd92a8dbb1a9477a'
                     '5ccf39dfef456ecde0220215bff58cdfa14e50f10b61856ca4da7c15ca020a2442f3877'
                     '253e3edf1d154f01feffffff02fcd3fa02000000001976a91436c63c9af872095dc7bc5'
                     'a6adab80b54f7a12e3c88ac80f0fa0200000000c6b5096d696e64626c6f776e4c9e7b22'
                     '736f7572636573223a207b226c6272795f73645f68617368223a2022643162616538326'
                     '66534616431613934613865363930303930303335353737393332643838616461646634'
                     '64653437313134636335343632336462663633666562633130373565313962386438626'
                     '13563633961633534393166313530653936227d2c20226465736372697074696f6e223a'
                     '2022696d706f737369626c65227d6d7576a914731acaf68fb1642bdbb1cd5ea7f247318'
                     '96256ef88ac5e000000')
        deserializer = BlockDeserializer(binascii.unhexlify(lbc_block), start=112)
        txs = deserializer.read_tx_block()
        self.assertEqual(binascii.hexlify(txs[0][0].raw).decode(), lbc_block[-730-198:-730])  # len: 198
        self.assertEqual(binascii.hexlify(txs[-1][0].raw).decode(), lbc_block[-730:])
