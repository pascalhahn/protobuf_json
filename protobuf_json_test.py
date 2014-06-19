#!/usr/bin/python
#
# Test the protobuf json library


__author__ = 'Pascal Hahn <ph@lxd.bz>'


import protobuf_json
import unittest

from testdata import node_pb2
from testdata import repeated_field_pb2
from testdata import embedded_msg_pb2

class Json2ProtoTest(unittest.TestCase):
  def test_alldataset(self):
    node_name = 'host1.berlin'
    node_state = 'AVAILABLE'

    node = protobuf_json.json2proto(
        '{"nodeid": "%s", "state": "%s"}' % (node_name, node_state),
        node_pb2.Node)
    self.assertEquals(node.nodeid, node_name)
    self.assertEquals(node.state, node.AVAILABLE)
    self.assertTrue(node.IsInitialized())

  def test_defaultdata(self):
    node_name = 'host1.berlin'

    node = protobuf_json.json2proto(
        '{"nodeid": "%s"}' % node_name, node_pb2.Node)
    self.assertEquals(node.nodeid, node_name)
    self.assertEquals(node.state, node.PLANNED)
    self.assertTrue(node.IsInitialized())

  def test_raisesJsonDataMissingError(self):
    self.assertRaises(
      protobuf_json.JsonDataMissingError,
      protobuf_json.json2proto, '{}', node_pb2.Node)

  def test_repeated_field(self):
    msg = protobuf_json.json2proto('{"notes": ["testnote", "testnotes"]}', repeated_field_pb2.TestMessage)
    self.assertEquals(msg.notes, ['testnote', 'testnotes'])

  def test_raisesProtoEnumValueNotFoundError(self):
    node_name = 'host1.berlin'
    self.assertRaises(
      protobuf_json.ProtoEnumValueNotFoundError,
      protobuf_json.json2proto,
      '{"nodeid": "%s", "state": "%s"}' % (node_name, "WROONG"), node_pb2.Node)

  def test_raisesUnsupportedFieldTypeError(self):
    self.assertRaises(
      protobuf_json.UnsupportedFieldTypeError,
      protobuf_json.json2proto,
      '{"testmessage": {"test": "test"}}', embedded_msg_pb2.TestMessage)


class Proto2JsonTest(unittest.TestCase):
  def test_complete_node(self):
    node = node_pb2.Node(nodeid='testnode', state=node_pb2.Node.AVAILABLE)
    self.assertEquals(protobuf_json.proto2json(node), '{"state": "AVAILABLE", "nodeid": "testnode"}')

  def test_node_defaults(self):
    node = node_pb2.Node(nodeid='testnode')
    self.assertEquals(protobuf_json.proto2json(node), '{"state": "PLANNED", "nodeid": "testnode"}')

  def test_repeated_field(self):
    msg = repeated_field_pb2.TestMessage()
    msg.notes.extend(['testnote', 'testnote2'])
    self.assertEquals(protobuf_json.proto2json(msg), '{"notes": ["testnote", "testnote2"]}')

  def test_node_raisesProtoEnumValueNotFoundError(self):
    node = node_pb2.Node(nodeid='testnode', state=node_pb2.Node.AVAILABLE)
    node.state = 20
    self.assertRaises(
      protobuf_json.ProtoEnumValueNotFoundError,
      protobuf_json.proto2json,
      node)

  def test_embedded_msg(self):
    msg = embedded_msg_pb2.TestMessage()
    self.assertEquals(protobuf_json.proto2json(msg), '{"testmessage": {"test": "test"}}')


if __name__ == '__main__':
  unittest.main()

# vim: set tabstop=2 softtabstop=2 shiftwidth=2 textwidth=80 syntax=python smarttab expandtab:
