const elasticsearch = require('elasticsearch')

// Core ES variables for this project
const index = 'malwords'
const type = 'samples'
const port = 9200
const host = process.env.ES_HOST || 'localhost'
const client = new elasticsearch.Client({ host: { host, port } })

/** Check the ES connection status */
async function checkConnection () {
  let isConnected = false
  while (!isConnected) {
    console.log('Connecting to ES')
    try {
      const health = await client.cluster.health({})
      console.log(health)
      isConnected = true
    } catch (err) {
      console.log('Connection Failed, Retrying...', err)
    }
  }
}

// checkConnection()

/** Clear the index, recreate it, and add mappings */
async function resetIndex () {
  if (await client.indices.exists({ index })) {
    await client.indices.delete({ index })
  }

  await client.indices.create({ 
    index,
    body: { 
      settings: {
      "index.mapping.total_fields.limit": 500000,
      // "index.codec": "best_compression"
      } 
    }
  })

  await putMalwordsMapping()
}

/** Add book section schema mapping to ES */
async function putMalwordsMapping () {
  const schema = {
    content: { type: 'nested' },
    family: {type: 'keyword'}
  }

  return client.indices.putMapping({ index, type, body: { properties: schema } })
}

module.exports = {
  client, index, type, checkConnection, resetIndex
}

