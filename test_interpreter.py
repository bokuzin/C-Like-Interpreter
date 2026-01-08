import unittest
import io
import interpreter
import StringIO
import sys

ANS = {
    "test1.iml" : "2\n4\n1\n4\n2\n2",
    "test2.iml" : "7",
    "test3.iml" : "-200",
    "test4.iml" : "10\n8\n6\n4\n2\n0",
    "test5.iml" : "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19",
    "test_fib.iml" : "1\n1\n2\n3\n5\n8\n13\n21\n34\n55",
    "test_collatz.iml" : "3\n10\n5\n16\n8\n4\n2\n1",
    "test_euclid.iml" : "48\n18\n18\n12\n12\n6\n6\n0\n6",
    "test_longcollatz.iml" : "27\n82\n41\n124\n62\n31\n94\n47\n142\n71\n214\n107\n322\n161\n484\n242\n121\n364\n182\n91\n274\n137\n412\n206\n103\n310\n155\n466\n233\n700\n350\n175\n526\n263\n790\n395\n1186\n593\n1780\n890\n445\n1336\n668\n334\n167\n502\n251\n754\n377\n1132\n566\n283\n850\n425\n1276\n638\n319\n958\n479\n1438\n719\n2158\n1079\n3238\n1619\n4858\n2429\n7288\n3644\n1822\n911\n2734\n1367\n4102\n2051\n6154\n3077\n9232\n4616\n2308\n1154\n577\n1732\n866\n433\n1300\n650\n325\n976\n488\n244\n122\n61\n184\n92\n46\n23\n70\n35\n106\n53\n160\n80\n40\n20\n10\n5\n16\n8\n4\n2\n1",
    "test_longfib.iml" : "1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89\n144\n233\n377\n610\n987\n1597\n2584\n4181\n6765\n10946\n17711\n28657\n46368\n75025\n121393\n196418\n317811\n514229\n832040\n1346269\n2178309\n3524578\n5702887\n9227465\n14930352\n24157817\n39088169\n63245986\n102334155\n165580141\n267914296\n433494437\n701408733\n1134903170\n1836311903\n2971215073\n4807526976\n7778742049\n12586269025\n20365011074\n32951280099\n53316291173\n86267571272\n139583862445\n225851433717\n365435296162\n591286729879\n956722026041\n1548008755920\n2504730781961\n4052739537881\n6557470319842\n10610209857723\n17167680177565\n27777890035288\n44945570212853\n72723460248141\n117669030460994\n190392490709135\n308061521170129\n498454011879264\n806515533049393\n1304969544928657\n2111485077978050\n3416454622906707\n5527939700884757\n8944394323791464\n14472334024676221\n23416728348467685\n37889062373143906\n61305790721611591\n99194853094755497\n160500643816367088\n259695496911122585\n420196140727489673\n679891637638612258\n1100087778366101931\n1779979416004714189\n2880067194370816120\n4660046610375530309\n7540113804746346429\n12200160415121876738\n19740274219868223167\n31940434634990099905\n51680708854858323072\n83621143489848422977\n135301852344706746049\n218922995834555169026"
    }

def testbase(self,filename):
    saved_stdout = sys.stdout
    try:
        out = StringIO.StringIO()
        sys.stdout = out
        code = interpreter.decode_iml("testcase/iml/" + filename)
        interpreter.interpret(code)
        output = out.getvalue().strip()
        self.assertEqual(output, ANS[filename])
    finally:
        sys.stdout = saved_stdout

class TestInterpreter(unittest.TestCase):
    def test_1(self):
        testbase(self,"test1.iml")

    def test_2(self):
        testbase(self,"test2.iml")

    def test_3(self):
        testbase(self,"test3.iml")

    def test_4(self):
        testbase(self,"test4.iml")

    def test_5(self):
        testbase(self,"test5.iml")

    def test_fib(self):
        testbase(self,"test_fib.iml")

    def test_collatz(self):
        testbase(self,"test_collatz.iml")

    def test_euclid(self):
        testbase(self,"test_euclid.iml")

    # 1~100 fib
    def test_longfib(self):
        testbase(self,"test_longfib.iml")

    # long sequence of starting with 27
    def test_longfib(self):
        testbase(self,"test_longcollatz.iml")

if __name__ == "__main__":
    unittest.main()
