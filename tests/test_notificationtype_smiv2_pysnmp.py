#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
import sys

try:
    import unittest2 as unittest

except ImportError:
    import unittest

from pysmi.parser.smi import parserFactory
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.codegen.symtable import SymtableCodeGen
from pysnmp.smi.builder import MibBuilder


class NotificationTypeTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      NOTIFICATION-TYPE
        FROM SNMPv2-SMI;

    testNotificationType NOTIFICATION-TYPE
       OBJECTS         {
                            testChangeConfigType,
                            testChangeConfigValue
                        }
        STATUS          current
        DESCRIPTION
            "A collection of test notification types."
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testNotificationTypeSymbol(self):
        self.assertTrue("testNotificationType" in self.ctx, "symbol not present")

    def testNotificationTypeName(self):
        self.assertEqual(self.ctx["testNotificationType"].getName(), (1, 3), "bad name")

    def testNotificationTypeDescription(self):
        self.assertEqual(
            self.ctx["testNotificationType"].getDescription(),
            "A collection of test notification types.",
            "bad DESCRIPTION",
        )

    def testNotificationTypeClass(self):
        self.assertEqual(
            self.ctx["testNotificationType"].__class__.__name__,
            "NotificationType",
            "bad SYNTAX class",
        )


class NotificationTypeHyphenTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      NOTIFICATION-TYPE
        FROM SNMPv2-SMI;

    test-notification-type NOTIFICATION-TYPE
       OBJECTS         {
                            testChangeConfigType,
                            testChangeConfigValue
                        }
        STATUS          current
        DESCRIPTION
            "A collection of test notification types."
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testNotificationTypeSymbol(self):
        self.assertTrue("test_notification_type" in self.ctx, "symbol not present")

    def testNotificationTypeLabel(self):
        self.assertEqual(
            self.ctx["test_notification_type"].getLabel(),
            "test-notification-type",
            "bad name",
        )


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
