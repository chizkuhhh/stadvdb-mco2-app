import axios from 'axios'
import { useEffect, useState } from 'react'


function App() {
  const [message, setMessage] =useState('')

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/test')
      .then(response => setMessage(response.data.message))
      .catch(error => console.error(error))
  }, [])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">MCO2 React + Flask App</h1>
      <p>{message}</p>
    </div>
  )
}

export default App
