const axios = require('axios');

const BASE_API_URL = 'http://localhost:9000/api/v1';

axios.defaults.baseURL = BASE_API_URL;


const DataServices = {
    Init: function(){
        // Any application initialization logic comes here
    },
    GetArticles : async function(){
        return await axios.get(BASE_API_URL+"/articles");
    }
}

export default DataServices;