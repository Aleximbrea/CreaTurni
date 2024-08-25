def dictionary_query(cur, query):
    cur.execute(query)

    data = []
    column_names = [i[0] for i in cur.description]
    rows = cur.fetchall()
    for row in rows:
        row_dict = {}
        for i in range(len(row)):
            row_dict[column_names[i]] = row[i]
        data.append(row_dict)
    return data
    