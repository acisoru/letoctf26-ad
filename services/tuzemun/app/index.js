const express = require('express')
const bodyParser = require('body-parser')
const hbs = require('express-hbs')
const app = express()
const morgan = require('morgan')
const cookieParser = require('cookie-parser')
const session = require('express-session')
const { encodeInt, decodeInt } = require('./utils')
const DB = require('./postgres')()

const PORT = process.env.PORT || 8137
const BIND_ADDR = process.env.BIND_ADDR || '0.0.0.0'

app.use(morgan('dev'))

app.engine('hbs', hbs.express4({}))
app.use(bodyParser.json())
app.use(cookieParser())
app.set('views', './public')
app.set('view engine', 'hbs')
app.use("/static", express.static(__dirname + "/public/static"))
app.use(session({
		keys: ['user'],
		secret: 'nobody knows it 1 believe',
		resave: true,
		saveUninitialized: true,
	}))

async function auth(req, res, next) {
	if (req.session.uid) {
		if (await DB.getUserByID(req.session.uid)) {
			next()
		} else {
			res.redirect("/")
			return
		}
	} else {
		res.redirect("/")
		return
	}
}

app.get('/', function(req, res){
	res.render('main.hbs')
})

app.get('/home', auth, async function(req,res) {
	res.render('home.hbs')
})


// API

app.post('/api/login', async (req, res) => {
	let { username, password } = req.body
	if (await DB.checkUser(username, password)) {
		req.session.uid = await DB.getUserID(username)
		res.sendStatus(200)
	} else {
		res.sendStatus(401)
	}
})

app.post('/api/register', async (req, res) => {
	let { username, email, password1, password2} = req.body
	if (password1 != password2) {
		res.sendStatus(400)
		return
	}
	if (await DB.userExists(username)) {
		res.sendStatus(403)
		return
	}
	if (await DB.createUser(username, email, password1)) {
		res.sendStatus(200)
	} else {
		res.sendStatus(500)
	}
})

app.get('/api/user', auth, async(req, res) => {
	var userid = req.session.uid
	let { username, email } = await DB.getUserByID(userid)
	res.json({username: username, email: email})
})

app.get('/api/info', auth, async (req, res) => {
	var userid = req.session.uid
	if (!(await DB.extraDataExists(userid))) {
		res.json({})
		return
	}
	let { username, email } = await DB.getUserByID(userid)
	let extraData = await DB.getExtraData(username, email)
	if (extraData.approved) {
		res.json(await DB.getUsers())
	} else {
		res.json(extraData)
	}
})

app.post('/api/send-request', auth, async (req, res) => {
	let data = req.body
	let full_data = {...DB.DEFAULT_DATA, ...data}
	let userid = req.session.uid
	if (!(await DB.extraDataExists(userid))){
		if (!(await DB.addExtraDataDict(userid, full_data))) {
			res.sendStatus(500)
			return
		}
	}
	if (await DB.createRequest(userid)) {
		res.sendStatus(200)
	} else {
		res.sendStatus(500)
	}
})

app.get('/api/recovery-code', auth, async(req, res) => {
	let userid = req.session.uid
	res.json({'code': encodeInt(userid)})
})

app.post('/api/reset-password', async (req, res) => {
	let { code, newpassword } = req.body
	let id = decodeInt(code)
	if (await DB.changePassword(id, newpassword)) {
		res.sendStatus(200)
	} else {
		res.sendStatus(500)
	}
})

app.post('/api/logout', async (req, res) => {
	req.session.destroy(err => {
		if (err) {
			res.status(400).send('Unable to log out')
		} else {
			res.sendStatus(200)
		}
	});
})

app.get('/logout', async (req, res) => {
	req.session.destroy(err => {
		if (err) {
			res.status(400).send('Unable to log out')
		} else {
			res.sendStatus(200)
		}
	});
})

app.listen(PORT, BIND_ADDR, () => {
	console.log('Running on ' + BIND_ADDR + ':' + PORT)
})
