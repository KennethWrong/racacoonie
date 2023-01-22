import axios from 'axios';

const racaApp = axios.create({
  // baseURL: 'https://prod.letspondr.com/'
  baseURL: 'http://localhost:8000/'
});

export default racaApp;
