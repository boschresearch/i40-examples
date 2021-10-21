const bodyParser = require('body-parser')
const axios = require('axios').default
const app = require('express')()
const session = require('express-session')
const nodeutil = require('util');

const SCHEMA_ID = process.env.SCHEMA_ID || 'HK8EKmz5Ses1KwMVcuojyd:2:basic_schema:1.0.0' // first such schema on test.bcovrin network
const CONNECTION_ESTABLISHED_STATES = ['active', 'response']

app.use(session({
  secret: 'do-not-use-in-production-secret',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}))
app.use(bodyParser.json())

const ACAPY_URL = process.env.ACAPY_URL || 'http://acapyissuer:10001'

// mapping to find session id for a given connection id
app.locals.connection_sid = new Map()
app.locals.credDefIds = {}

app.post('/credential/request', (req, res) => {

  sid = req.session.id
  cid = req.session.connection_id
  if(cid) {
    // connection available, let's directly issue the credential
    credentialDefinitionId = app.locals.credDefIds[SCHEMA_ID]
    console.log('credentialDefinitionId: ', credentialDefinitionId)
    const data = {
      connection_id: cid,
      credential_definition_id: credentialDefinitionId,
      credential_proposal: {
        '@type': 'issue-credential/1.0/credential-preview',
        attributes: [
          {
            name: 'first_name',
            value: req.body.first_name
          },
          {
            name: 'last_name',
            value: req.body.last_name
          },
          {
            name: 'email',
            value: req.body.email
          }
        ]
      }
    }

    return axios.post(ACAPY_URL + '/issue-credential/send', data)
      .then((data) => {
        console.log(data.data)
        return res.json({message: 'Credential sent'})
      })
      .catch((err) => {
        console.log(err)
        return res.json({error: 'Could not send credential. Please contact an admin.'})
      })

  } else {
    // establish new connection
    return axios.post(ACAPY_URL + '/connections/create-invitation', {})
      .then((data) => {
        console.log(data.data)
        req.session.connection_id = data.data.connection_id
        app.locals.connection_sid.set(data.data.connection_id, req.session.id)
        res.status = 403
        return res.json( {
          "data": data.data,
          "error": "Browser session not yet connected with a SSI connection. Please establish a connection first and try again. Please find the connection invitation attached."
        })
      })
      .catch((error) => {
        console.error(error)
        return res.json({ error: 'could not create invitation' })
      })
    }
  })

/* DO NOT USE THIS IN PRODUCTION */
app.post('/webhooks/*', (req, res) => {
  console.log(req.originalUrl)
  console.log(req.url)
  console.log(req.body)

  const cid = req.body.connection_id
  const sid = app.locals.connection_sid.get(cid)
  console.log('mapping ids:', cid, sid)

  return res.json({})
})

async function initCredentialDefinitionWithSchema (schemaId) {
  // TODO: this needs a lot of cleaning - very hacky code
  // general issue: create cred_def_id if not exists
  // we use unique tags, but it happens that we create multiple such credDefIds
  // if one exists, we always return the fist and ignore the others

  const { data: existingCredDefId } = await axios.get(ACAPY_URL + '/credential-definitions/created?schema_id=' + encodeURI(schemaId))
  if (existingCredDefId?.credential_definition_ids.length > 0) {
    app.locals.credDefIds[schemaId] = existingCredDefId.credential_definition_ids[0]
    return app.locals.credDefIds[schemaId]
  }
  // ok, no cred_def_id, let's create one
  // whenever the wallet is deleted, we need to create a new cred_def_id on the ledger
  // it seems we can not fetch and reuse. Thus, let's use a unique tag
  const { data: created } = await axios.post(ACAPY_URL + '/credential-definitions', {
    schema_id: schemaId,
    support_revocation: false,
    tag: Date.now().toString() // sufficient here
  })
    .catch((err) => {
      console.error(err)
      return 0
    })
  if (created) {
    app.locals.credDefIds[schemaId] = created
    return app.locals.credDefIds[schemaId]
  }
  // ok, last but not least, some kind of an error
  return 0
}

const initServer = function () {
  console.log('server started.')
  // once server has started, make sure we have a credential definition available in case we plan to issue credentials
  console.log('initializing credential definition...')
  initCredentialDefinitionWithSchema(SCHEMA_ID)
}

initServer()

module.exports = app