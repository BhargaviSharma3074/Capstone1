const { contextBridge } = require('electron');
const axios = require('axios');

contextBridge.exposeInMainWorld("backend", {
  captureFaces: async () => {
    let res = await axios.get("http://127.0.0.1:8000/capture");
    return res.data.faces;
  }
});
