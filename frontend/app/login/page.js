import React from 'react'

const Login = () => {
  return (
    <div className='flex justify-center items-center flex-col ' >
      <input text="name" name='email' type='text' className='text-lg text-red-400 w-[50%] m-2' />
      <input text="password" name='password' type='password' className='w-1/2 m-2' />
      <button className='bg-amber-200 text-amber-800 font-bold p-2  w-1/3 m-2'>
        Login
      </button>
       
    </div>
  )
}

export default Login