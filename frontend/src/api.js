import axios from "axios";

const api = axios.create({
  baseURL: "https://docu-dive.com/api",
});

export default api;

// import axios from "axios";

// const api = axios.create({
//   // local
//   // baseURL: "http://127.0.0.1:8000",
//   // EC2 instance
//   // baseURL: "http://44.202.55.152:8000",
//   // My domain
//   // baseURL: "https://docu-dive.com",
// baseURL: "http://localhost:8000",
//   // Use your domain name for the baseURL
//   baseURL: "https://docu-dive.com:8000",
//   // baseURL: "https://docu-dive.com/api", // Updated to reflect the proxy pass setup
// });

// export default api;
