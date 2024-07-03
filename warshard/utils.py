def ensure_lowest_key(dictionary):
    # Keep an element only in the list of smallest key
    # Input : a dictionary like {1:[A],2:[A,B]}
    # Output : a dictionary like input but where
    # each element is present only in the list of lowest
    # key that contained it originally. For the input
    # example, the output would be {1:[A],2:[B]}
    seen_objects = set()
    for key in sorted(dictionary.keys()):
        unique_objects = []
        for obj in dictionary[key]:
            if obj not in seen_objects:
                unique_objects.append(obj)
                seen_objects.add(obj)
        dictionary[key] = unique_objects
    return dictionary
