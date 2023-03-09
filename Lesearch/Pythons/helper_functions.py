def get_attribute(header, groups):
    '''ヘッダーからgroupの属性を返す.'''
    attributes = {}
    for group in groups:
        lst = []
        for h in header:
            if group in h:
                lst.append(h)
        attributes[group] = lst
    return attributes

def get_labels(header, groups):
    '''ヘッダーからgroupの属性を返す.'''
    attributes = {}
    for group in groups:
        lst = []
        for h in header:
            if group in h:
                lst.append(h.replace(f'{group}_', ''))
        attributes[group] = lst
    return attributes