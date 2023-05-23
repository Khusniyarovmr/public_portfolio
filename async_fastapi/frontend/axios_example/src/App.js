import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {
  const handlePost = () => {
      axios.post(
          'http://localhost:8000/api/v1/auth/jwt/login',
          {
            username: 'myemail@gmail.com',
            password: 'qwe'
          },
          {
            headers: {
              "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            withCredentials: true
          }
      ).then(function (response) {
        console.log(response);
      }).catch(function (error) {
        console.log(error);
      });
  }
  return (
    <div className="App">
      <button onClick={handlePost}>
        CLICK ME!!!
      </button>
    </div>
  );
}

export default App;
