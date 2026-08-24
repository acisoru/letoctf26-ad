const fs = require('fs')
const bcrypt = require('bcrypt')
const saltRounds = 13;

const Pool = require('pg').Pool
const POSTGRES_HOST = process.env.POSTGRES_HOST || 'postgres'
const POSTGRES_PORT = process.env.POSTGRES_PORT || 5432
const POSTGRES_USER = process.env.POSTGRES_USER || 'user'
const POSTGRES_DBNAME = process.env.POSTGRES_DBNAME || 'tuzemun'
const POSTGRES_PASS = process.env.POSTGRES_PASS || 'PJwPl8v6YlQ87Qzd'

const pool = new Pool({
	user: POSTGRES_USER,
	host: POSTGRES_HOST,
	database: POSTGRES_DBNAME,
	password: POSTGRES_PASS,
	port: POSTGRES_PORT,
})

function addExtraData(userid, fio, passport, approved) {
  return pool.query('INSERT INTO users_extra_data(userid, fio, passport, approved) VALUES($1, $2, $3, $4)', [userid, fio, passport, approved])
      .then((result) => {return true})
      .catch(err => {return console.error('Error storing extra data', err.stack)})
}

function addExtraDataDict(userid, data) {
  return pool.query('INSERT INTO users_extra_data(userid, fio, passport, approved) VALUES($1, $2, $3, $4)', 
            [userid, data.fio, data.passport, data.approved])
      .then((result) => {return true})
      .catch(err => {return console.error('Error storing extra data', err.stack)})
}

function getExtraData(username, email) {
  return pool.query('SELECT * FROM users_extra_data WHERE userid IN (SELECT id FROM users WHERE username LIKE $1 AND email LIKE $2)',
       [username, email]).then(result => {
    return result.rows
  }).catch(err => {return console.error('Error getting user extra data', err.stack)})
}

function extraDataExists(userid) {
  return pool.query('SELECT * FROM users_extra_data WHERE userid=$1', [userid]).then(result => {
    if (result.rows.length != 1) {
      return false
    }
    return true
  }).catch(err => {return console.error('Error checking extra data existence', err.stack)})
}

function createUser(username, email, password) {
  return bcrypt.hash(password, saltRounds).then(hashpassword => {
    return pool.query('INSERT INTO users(username, email, password) VALUES($1, $2, $3)', [username, email, hashpassword])
      .then((result) => {return true})
      .catch(err => {return console.error('Error storing a user', err.stack)})
  }).catch(err => {return console.log(err.stack)})
}

function changePassword(userid, newpassword) {
  return bcrypt.hash(newpassword, saltRounds).then(hashpassword => {
    return pool.query('UPDATE users SET password=$1 WHERE id=$2', [hashpassword, userid])
      .then((result) => {return true})
      .catch(err => {return console.error('Error changing a password', err.stack)})
  }).catch(err => {return console.log(err.stack)})
}

function checkUser(username, password) {
  return pool.query('SELECT password FROM users WHERE username=$1', [username]).then(result => {
    if (result.rows.length != 1) {
      return false
    }
    return bcrypt.compare(password, result.rows[0].password)
      .then(result => {return result})
      .catch(err => {return console.error('Error comparing bcrypt', err.stack)})
  }).catch(err => {return console.error('Error checking user', err.stack)})
}

function userExists(username) {
  return pool.query('SELECT * FROM users WHERE username=$1', [username]).then(result => {
    if (result.rows.length != 1) {
      return false
    }
    return true
  }).catch(err => {return console.error('Error checking user existence', err.stack)})
}

function getUserID(username) {
  return pool.query('SELECT id FROM users WHERE username=$1', [username]).then(result => {
    if (result.rows.length != 1) {
      return -1
    }
    return result.rows[0].id
  }).catch(err => {return console.error('Error getting user id', err.stack)})
}

function getUserByID(uid) {
  return pool.query('SELECT * FROM users WHERE id=$1', [uid]).then(result => {
    return result.rows[0]
  }).catch(err => {return console.error('Error getting user by id', err.stack)})
}

function getUsers() {
  return pool.query('SELECT username, email FROM users').then(result => {
    return result.rows
  }).catch(err => {return console.error('Error getting users', err.stack)})
}

function createRequest(userid) {
  return pool.query('INSERT INTO requests(userid) VALUES($1)', [userid])
      .then((result) => {return true})
      .catch(err => {return console.error('Error creating a request', err.stack)})
}

function getRequestByUserId(uid) {
  return pool.query('SELECT * FROM requests WHERE userid=$1', [uid]).then(result => {
    return result.rows
  }).catch(err => {return console.error('Error getting user by id', err.stack)})
}

function init() {
  let DB = Object()
  pool.connect((err, client, release) => {
    if (err) {
      return console.error('Error acquiring client', err.stack)
    }
    let sql = fs.readFileSync('init_db.sql').toString()
    
    client.query(sql, (err, result) => {
      release()
      if (err) {
        return console.error('Error executing query', err.stack)
      }
    })
  })
  
  DB.createUser = createUser
  DB.checkUser = checkUser
  DB.userExists = userExists
  DB.getUserID = getUserID
  DB.getUserByID = getUserByID
  DB.addExtraData = addExtraData
  DB.getExtraData = getExtraData
  DB.getRequestByUserId = getRequestByUserId
  DB.createRequest = createRequest
  DB.extraDataExists = extraDataExists
  DB.getUsers = getUsers
  DB.addExtraDataDict = addExtraDataDict
  DB.changePassword = changePassword
  DB.DEFAULT_DATA = {'approved': false}
  return DB
}

exports = module.exports = init
