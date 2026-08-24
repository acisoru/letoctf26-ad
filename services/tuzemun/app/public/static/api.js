class BackendAPI {
    constructor(addr) {
      this._addr = addr;
    }
  
    async register(username, email, password) {
      const data = {
        username: username,
        email: email,
        password1: password,
        password2: password,
      };
  
      const response = await fetch(`${this._addr}/api/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Registration failed');
      }
    }
  
    async login(username, password) {
      const data = {
        username: username,
        password: password,
      };
  
      const response = await fetch(`${this._addr}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Login failed');
      }
    }
  
    async info() {
      const response = await fetch(`${this._addr}/api/info`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch info');
      }
  
      return response.json();
    }

    async user() {
        const response = await fetch(`${this._addr}/api/user`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
    
        if (!response.ok) {
          throw new Error('Failed to fetch info');
        }
    
        return response.json();
      }
  
    async sendRequest(fio, passport) {
      const data = {
        fio: fio,
        passport: passport,
      };
  
      const response = await fetch(`${this._addr}/api/send-request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Sending request failed');
      }
    }
  
    async recoveryCode() {
      const response = await fetch(`${this._addr}/api/recovery-code`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch recovery code');
      }
  
      return response.json();
    }
  
    async resetPassword(code, newpassword) {
      const data = {
        code: code,
        newpassword: newpassword,
      };
  
      const response = await fetch(`${this._addr}/api/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Password reset failed');
      }
    }
  
    async logout() {
      const response = await fetch(`${this._addr}/api/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error('Logout failed');
      }
    }
  }
  
  // Example usage:
 /* const backend = new BackendAPI('https://your-backend-server.com');
  backend.register('john_doe', 'john@example.com', 'password123')
    .then(() => {
      // Registration successful
    })
    .catch((error) => {
      console.error(error);
    }); */
  
  // You can similarly call other methods like login, info, sendRequest, recoveryCode, resetPassword, and logout as needed.
  