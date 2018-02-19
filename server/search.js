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

    var prefix = term.split(':')[0].trim() 
    if (prefix === 'sys'){
      query_body = {
        "match" : {
            "syscalls" : {
		"query": term.split(':')[1].trim() ,
		"fuzziness": 0
	    }
        }
      }
    } else if (prefix === 'reg'){
      query_body = {
        "match" : {
            "registry" : {
		"query": term.split(':')[1].trim(),
		"fuzziness": 0
	    }
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
