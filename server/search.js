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
      "multi_match" : {
          "query" : term,
          "fields": ["content", "syscalls", "raw"]
      } 
    },
    highlight: { fields: { content: {} } }
    }

    return client.search({ index, type, body })
  },

  /** Get the specified range of paragraphs from a book */
  getDetails (param) {
    console.log(param)
    const body = {
      "query": {
        "terms": {
          "_id": [param['docId']]
        }
      }
    }

    return client.search({ index, type, body })
  }
}
