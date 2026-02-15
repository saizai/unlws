def remove_whitespace_nodes(node):
  """
  Recursively remove text nodes that contain only whitespace.
  """
  remove_list = []
  for child in node.childNodes:
    if child.nodeType == child.TEXT_NODE and not child.data.strip():
      remove_list.append(child)
    elif child.hasChildNodes():
      remove_whitespace_nodes(child)
  for child in remove_list:
    node.removeChild(child)
