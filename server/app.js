const Koa = require('koa')
const Router = require('koa-router')
const joi = require('joi')
const validate = require('koa-joi-validate')
const search = require('./search')

const app = new Koa()
const router = new Router()

// Log each request to the console
app.use(async (ctx, next) => {
  const start = Date.now()
  await next()
  const ms = Date.now() - start
  console.log(`${ctx.method} ${ctx.url} - ${ms}`)
})

// Log percolated errors to the console
app.on('error', err => {
  console.error('Server Error', err)
})

// Set permissive CORS header
app.use(async (ctx, next) => {
  ctx.set('Access-Control-Allow-Origin', '*')
  return next()
})


// ENDPOINTS

router.get('/search',
  validate({
    query: {
      term: joi.string().max(60).required(),
      offset: joi.number().integer().min(0).default(0)
    }
  }),
  async (ctx, next) => {
    const { term, offset } = ctx.request.query
    ctx.body = await search.queryTerm(term, offset)
  }
)


router.get('/details',
  validate({
    query: {
      docId: joi.string().max(256).required()
    }
  }),
  async (ctx, next) => {
    const docId = ctx.request.query
    ctx.body = await search.getDetails(docId)
  }
)


const port = process.env.PORT || 3000

app
  .use(router.routes())
  .use(router.allowedMethods())
  .listen(port, err => {
    if (err) throw err
    console.log(`App Listening on Port ${port}`)
  })

