const { client, index, type } = require('./connection')

module.exports = {
  /** Query ES index for the provided term */
  queryTerm (term, offset = 0) {

    query_body = {
      "multi_match" : {
          "query" : term,
          "fields": ["content", "raw"],
          "fuzziness": 0
      } 
    }

    if (term.split(':')[0].trim() === 'sys'){
      query_body = {
        "match" : {
            "syscalls" : term
        }
      }
    } else if (term.split(':')[0].trim() === 'reg'){
      query_body = {
        "match" : {
            "registry" : term
        }
      }
    }

    const body = {
      from: offset, 
      "_source": {
          "exclude": ["content", "syscalls", "raw", "registry"]
      },

      "query": query_body,

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
