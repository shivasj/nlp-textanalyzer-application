const axios = require('axios');

const BASE_API_URL = 'http://localhost:9000/api/v1';

axios.defaults.baseURL = BASE_API_URL;


const DataServices = {
    Init: function(){
        // Any application initialization logic comes here
    },
    GetArticles : async function(day,hours, summarize_ratio, summarize_word_count){
        return await axios.get(BASE_API_URL+"/articles?summarize=true&day="+day+"&hours="+hours+"&summarize_ratio="+summarize_ratio+"&summarize_word_count="+summarize_word_count);
    }
}

export default DataServices;