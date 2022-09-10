"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""


def htable(nbuckets):
    """Return a list of nbuckets lists"""
    return [[] for _ in range(nbuckets)]


def hashcode(o):
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value. For strings, perform 
    operation h = h*31 + ord(c) for all characters in the string
    """
    if isinstance(o, int):
        return o
    elif isinstance(o, str):
        h = ord(o[0])
        for c in o[1:]:
            h = h * 31 + ord(c)
        return h
    else:
        return None


def bucket_indexof(table, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the index of the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    for idx, (bucket_key, _) in enumerate(table[hashcode(key) % len(table)]):
        if key == bucket_key:
            return idx
    return None


def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append (key,value)
    to that bucket if the (key,value) pair doesn't exist yet in that bucket.
    If the bucket for key already has a (key,value) pair with that key,
    then replace the tuple with the new (key,value).
    Make sure that you are only adding (key,value) associations to the buckets.
    The type(value) can be anything. Could be a set, list, number, string, anything!
    """
    bucket_idx = hashcode(key) % len(table)
    for idx, (bucket_key, _) in enumerate(table[bucket_idx]):
        if key == bucket_key:
            table[bucket_idx][idx] == (key, value)
            break
    else:
        table[bucket_idx].append((key, value))
    return table


def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    for i, (k, v) in enumerate(table[hashcode(key) % len(table)]):
        if key == k:
            return v
    return None


def htable_buckets_str(table):
    """
    Return a string representing the various buckets of this table.
    The output looks like:
        0000->
        0001->
        0002->
        0003->parrt:99
        0004->
    where parrt:99 indicates an association of (parrt,99) in bucket 3.
    """
    output = ""
    for table_idx, bucket in enumerate(table):
        output += "0" * (4 - len(str(table_idx))) + str(table_idx) + "->"
        if len(bucket) == 0:
            output += "\n"
        else:
            for bucket_idx, (key, val) in enumerate(bucket):
                output += f"{key}:{val}"
                if bucket_idx != len(bucket) - 1:
                    output += ", "
                elif table_idx != len(table) - 1:
                    output += "\n"
    return output


def htable_str(table):
    """
    Return what str(table) would return for a regular Python dict
    such as {parrt:99}. The order should be in bucket order and then
    insertion order within each bucket. The insertion order is
    guaranteed when you append to the buckets in htable_put().
    """
    output = "{"
    for bucket in table:
        for key, value in bucket:
            output += f"{key}:{value}, "
    output = output.strip(", ") + "}"
    return output
