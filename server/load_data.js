const fs = require('fs')
const path = require('path')
const esConnection = require('./connection')


/** Read an individual book text file, and extract the title, author, and paragraphs */
function parseFile (filePath) {
  // Read json file
  const words = JSON.parse(fs.readFileSync(filePath, 'utf8'))

  // Find uuid
  const uuid = filePath.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, "")

  console.log(`Reading file - ${uuid}`)
  console.log(`Parsed ${Object.keys(words).length} Words`)
  
  return {uuid, words}
}


/** Bulk index the book data in ElasticSearch */
async function insertData (files, labels) {
  let bulkOps = [] // Array to store bulk operations
  var i = 1;

  // Scan the folder
  for (let file of files) {
    const filePath = path.join('./malwords', file)

    // Get the file info
    const {uuid, words} = parseFile(filePath)
    const label = labels[uuid]
    console.log(label)

    bulkOps.push({ index: { _index: esConnection.index, _type: esConnection.type } })

    // Add document
    bulkOps.push({
      id: uuid,
      body: {
        content: words, 
        family: label
      }
    })
    i += 1

    // Do bulk insert after every 10 files
    if (i > 0 && i % 2 === 0) { 
      console.log('Indexing...')
      await esConnection.client.bulk({ 
        refresh: "wait_for",
        requestTimeout: 0, 
        body: bulkOps 
      })
      bulkOps = []
      console.log(`Indexed files ${i - 1} - ${i}`)
    }
  }

  // Insert remainder of bulk ops array
  console.log('Indexing...')
  await esConnection.client.bulk({
    refresh: "wait_for",
    requestTimeout: 0,
    body: bulkOps 
 })
  console.log(`Indexed files ${i}\n\n\n`)
}


/** Clear ES index, parse and index all files from the directory */
async function readAndInsert () {
  try {
    // Clear previous ES index
    await esConnection.resetIndex()

    esConnection.client.indices.putSettings({
      body: {"refresh_interval" : "-1"}
    }); 

    // Read books directory
    let files = fs.readdirSync('./malwords')
    console.log(`Found ${files.length} Files`)

    const labels = JSON.parse(fs.readFileSync('./labels.json', 'utf8'))

    // Read and index files in batches
    insertData (files, labels)
  
  } catch (err) {
    console.error(err)
  }
}

readAndInsert()
