from lxml import html

def get_children_text(tree, xpath_parent_selector, xpath_child_selector):
    parent_elements = tree.xpath(xpath_parent_selector)
    children_texts = []

    for element in iter(parent_elements):
        # for each parent, try to find 1 child with that selector
        child = element.xpath(xpath_child_selector)

        if child:
            children_texts.append(child[0].text_content())
        else:
            # we add None to indicate the item at this index had no match
            children_texts.append(None)

    return children_texts

def get_nodes(tree, xpath_selector):
    return tree.xpath(xpath_selector)

def get_tree(html_content):
    return html.fromstring(html_content)


def get_text(tree, xpath_selector):
    elements = tree.xpath(xpath_selector)
    return list(map(lambda element: element.text_content(), elements))


def get_attributes(tree, xpath_selector, attribute):
    elements = tree.xpath(xpath_selector)
    return list(map(lambda element: element.get(attribute), elements))