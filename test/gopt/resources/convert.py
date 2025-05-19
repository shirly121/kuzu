import yaml
import copy
import argparse

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def transform_vertex_types(vertex_types):
    for vt in vertex_types:
        vt['type_name'] = vt['type_name'].lower()
        properties = vt.get('properties', [])
        for p in properties:
            p['property_name'] = vt['type_name'][0] + '_' + p['property_name']
    return vertex_types

def transform_edge_types(edge_types):
    new_edge_types = []
    max_type_id = max(et['type_id'] for et in edge_types)
    for et in edge_types:
        base_type_name = et['type_name'].lower()
        relations = et.get('vertex_type_pair_relations', [])
        properties = et.get('properties', [])
        for p in properties:
            p['property_name'] = base_type_name[0] + '_' + p['property_name']
        if len(relations) <= 1:
            et['type_name'] = base_type_name
            new_relations = []
            for rel in relations:
                rel['source_vertex'] = rel['source_vertex'].lower()
                rel['destination_vertex'] = rel['destination_vertex'].lower()
                new_relations.append(rel)
            et['vertex_type_pair_relations'] = new_relations
            new_edge_types.append(et)
        else:
            for rel in relations:
                max_type_id += 1
                source = rel['source_vertex'].lower()
                dest = rel['destination_vertex'].lower()
                rel['source_vertex'] = source
                rel['destination_vertex'] = dest
                if all(r['source_vertex'].lower() == source for r in relations):
                    new_type_name = f"{base_type_name}_{dest}"
                else:
                    new_type_name = f"{source}_{base_type_name}"
                new_et = {
                    'type_id': max_type_id,
                    'type_name': new_type_name,
                    'vertex_type_pair_relations': [rel],
                    'properties': copy.deepcopy(properties)
                }
                new_edge_types.append(new_et)
    return new_edge_types

def transform_yaml(input_path, output_path):
    data = load_yaml(input_path)
    schema = data.get('schema', {})
    if 'vertex_types' in schema:
        schema['vertex_types'] = transform_vertex_types(schema['vertex_types'])
    if 'edge_types' in schema:
        schema['edge_types'] = transform_edge_types(schema['edge_types'])
    data['schema'] = schema
    save_yaml(data, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform YAML schema according to specified rules.")
    parser.add_argument('-i', '--input', required=True, help='Path to the input YAML file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output YAML file.')
    args = parser.parse_args()
    transform_yaml(args.input, args.output)
