import axios from "axios";

const api = axios.create({
  // local
  // baseURL: "http://127.0.0.1:8000",

  // EC2 instance
  // baseURL: "http://44.202.55.152:8000",

  // My domain
  baseURL: "https://docu-dive.com/",
});

export default api;
