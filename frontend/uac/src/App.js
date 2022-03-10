import './App.css';
import API from "./api.js"


import { useEffect, useState } from 'react'

function App() {
  const [userData, setUserData] = useState(null);
  const [paginationData, setPagination] = useState(null);


  useEffect(() => {
    API.get('user/get_users').then((res) => {
      console.log(res.data['data'])
      setUserData(res.data['data'])
      setPagination(res.data['info'])
    }).catch(error => {
      console.log(error)
    })
  }, [])

  if (!userData) return [];

  return (
    <div className="App" style={{ marginTop: 100, marginLeft:100, marginRight:100 }}>
      <table class="table table-dark table-striped">
        <thead>
          <tr>
            <th scope="col">First Name</th>
            <th scope="col">Last Name</th>
            <th scope="col">HIV Status</th>
            <th scope="col">Phone Number</th>
            <th scope="col">Creation Date</th>
          </tr>
        </thead>
        <tbody>
          {userData.map((d) => (
            <tr>
              <td scope="col">{d.first_name}</td>
              <td scope="col">{d.surname}</td>
              <td scope="col">{d.HIV_status.split(".")[1]}</td>
              <td scope="col">{d.Phone_number.toString()}</td>
              <td scope="col">{d.creation_date}</td>
          </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
