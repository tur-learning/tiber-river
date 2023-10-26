import xml.etree.ElementTree as ET

def extract_and_write_complete_relation_data(original_osm_file, new_osm_file, relation_id):
    """
    Extract specific relation data, including all relevant nodes, ways, and bounds,
    from an OSM file and write to a new OSM file.

    :param original_osm_file: path to the original .osm file.
    :param new_osm_file: path to the new .osm file to be written.
    :param relation_id: ID of the relation to extract.
    """

    # Parse the original .osm file
    tree = ET.parse(original_osm_file)
    root = tree.getroot()

    # Create a new root for the new .osm file
    new_root = ET.Element('osm')
    new_root.attrib = root.attrib  # Copy the attributes of the original .osm file

    # Copy the 'bounds' element (if present) to preserve geographical context
    bounds = root.find('bounds')
    if bounds is not None:
        new_root.append(bounds)

    # To store IDs of nodes and ways that are part of the relation
    node_ids = set()
    way_ids = set()

    # Find the target relation and extract related node and way IDs
    for relation in root.findall('relation'):
        if relation.get('id') == relation_id:
            # Copy the relation element to the new root
            new_root.append(relation)

            for member in relation.findall('member'):
                if member.get('type') == 'node':
                    node_ids.add(member.get('ref'))
                elif member.get('type') == 'way':
                    way_ids.add(member.get('ref'))

            # No need to check other relations
            break

    # Find and copy the related ways and their associated nodes
    for way in root.findall('way'):
        if way.get('id') in way_ids:
            new_root.append(way)

            # Add the nodes referenced by this way
            for nd in way.findall('nd'):
                node_ids.add(nd.get('ref'))

    # Find and copy the related nodes
    for node in root.findall('node'):
        if node.get('id') in node_ids:
            new_root.append(node)

    # Create a new ElementTree with the new root
    new_tree = ET.ElementTree(new_root)

    # Write the new .osm file
    new_tree.write(new_osm_file, encoding='utf-8', xml_declaration=True)

# Usage
original_osm_path = 'tiber.osm'  # replace with your original .osm file path
new_osm_path = 'tiber_converted.osm'  # replace with path where you want to save the new .osm file
relation_id_to_extract = '5071'  # replace with the relation ID you're interested in

extract_and_write_complete_relation_data(original_osm_path, new_osm_path, relation_id_to_extract)
