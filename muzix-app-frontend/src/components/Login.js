import React from 'react'

const Login = () => {
  return (
    <div>
        <h1>Login</h1>
        <form>
            <div class="row mb-3">
                <label for="inputEmail3" class="col-sm-2 col-form-label">Username</label>
                <div class="col-sm-10">
                <input type="email" class="form-control" id="inputEmail3" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="inputPassword3" class="col-sm-2 col-form-label">Password</label>
                <div class="col-sm-10">
                <input type="password" class="form-control" id="inputPassword3" />
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Login in</button>
        </form>
    </div>
  )
}

export default Login