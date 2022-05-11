import unittest
from src import decypher


class TestDecipher(unittest.TestCase):
    def test_decipher_baskerville_aristocrat(self):
        """
        Based on a text that the initial version of this program could decipher. Anything that does not decipher it is
        necessarily worse.
        """
        text = 'Pu. Vkhuorfn Krophv, zkr zdv xvxdoob yhub odwh lq wkh pruqlqjv, vdyh xsrq wkrvh qrw lqiuhtxhqw ' \
               'rffdvlrqvzkhq kh zdv xs doo qljkw, zdv vhdwhg dw wkh euhdnidvw wdeoh. L vwrrg xsrq wkh khduwk-uxj ' \
               'dqg slfnhg xs wkh vwlfn zklfk rxu ylvlwru kdg ohiw ehklqg klp wkh qljkw ehiruh. Lw zdv d ilqh, wklfn ' \
               'slhfh ri zrrg, exoerxv-khdghg, ri wkh vruw zklfk lv nqrzq dv d "Shqdqj odzbhu." Mxvw xqghu wkh khdg ' \
               'zdv d eurdg vloyhu edqg qhduob dq lqfk dfurvv. "Wr Mdphv Pruwlphu, P.U.F.V., iurp klv iulhqgv ri wkh ' \
               'F.F.K.," zdv hqjudyhg xsrq lw, zlwk wkh gdwh "1884." Lw zdv mxvw vxfk d vwlfn dv wkh rog-idvklrqhg ' \
               'idplob sudfwlwlrqhu xvhg wr fduub—dgljqlilhg svrolg adqgruhdvvxulqj.'
        plain = 'Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent ' \
                'occasions when he was up all night, was seated at the breakfast table. I stood upon the hearth-rug ' \
                'and picked up the stick which our visitor had left behind him the night before. It was a fine, ' \
                'thick piece of wood, bulbous-headed, of the sort which is known as a “Penang lawyer.” Just under ' \
                'the head was a broad silver band nearly an inch across. “To James Mortimer, M.R.C.S., from his ' \
                'friends of the C.C.H.,” was engraved upon it, with the date “1884.” It was just such a stick as ' \
                'the old-fashioned family practitioner used to carry—dignified, solid, and reassuring.'
        deciphered = decypher.decipher(50, 'abcdefghijklmnopqrstuvwxyz', 'en', 'a', 10000, ciphertext=text)
        self.assertTrue(deciphered, plain)


if __name__ == '__main__':
    unittest.main()
