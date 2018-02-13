const { client, index, type } = require('./connection')

module.exports = {
  /** Query ES index for the provided term */
  queryTerm (term, offset = 0) {
    const body = {
    from: offset, 
    "_source": {
        "exclude": [ "content" ]
    },

    "query": {
        "nested": {
          "path": "content",
          "query": {
            "function_score": {
              "query": {
                "bool": {
                  "must": [
                    {
                      "exists": {
                         "field": "content." + term
                        }
                    }
                  ]
                }
              },
              "boost_mode": "replace",
              "functions": [
                {
                  "field_value_factor": {
                    "field": "content." + term,
                    "factor": 1,
                    "missing": 0
                  }
                }
              ]
            }
          }
        }
      }

    }

    return client.search({ index, type, body })
  },

  /** Get the specified range of paragraphs from a book */
  getParagraphs (bookTitle, startLocation, endLocation) {
    const filter = [
      { term: { title: bookTitle } },
      { range: { location: { gte: startLocation, lte: endLocation } } }
    ]

    const body = {
      size: endLocation - startLocation,
      sort: { location: 'asc' },
      query: { bool: { filter } }
    }

    return client.search({ index, type, body })
  }
}
