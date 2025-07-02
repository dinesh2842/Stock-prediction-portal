import axios from "axios";

const baseURL = import.meta.env.VITE_BACKEND_BASE_API

const axiosInstance = axios.create({
    baseURL: baseURL,
    headers:{
        'Content-type':'application/json',
    }
})


//request Interceptor
axiosInstance.interceptors.request.use(
    function(config){
       
        const accessToken = localStorage.getItem('accessToken')
        if (accessToken){
            config.headers['Authorization'] = `Bearer ${accessToken}`
        }
        
        
        return config;
    },
    function(error){
        return Promise.reject(error)
    }

)

//Axios Interceptors

axiosInstance.interceptors.response.use(
    function(response){
        return response
    },
    //handle failed reponses
    async function(error){
        const originalRequest = error.config;
        if(error.response.status === 401 && !originalRequest.retry){ // if there is 401 in the response we are seting originalRequest.retry = true
            originalRequest.retry = true; //if you dont put this will go into a infinte loop
            const refreshToken = localStorage.getItem('refreshToken')//then we are taking refresh token from localstorage
            try{
                const response =  await axiosInstance.post('/token/refresh/',{refresh: refreshToken})// sending the refresh token to the server
                
                
                localStorage.setItem('accessToken',response.data.access)//server will give us the new token and new token will be set inside the localstorage
                originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`//and it also be set inside the authorization header
                return axiosInstance(originalRequest)//once this is set to the authorization header of the original request and then the original request will again establish and give success response
                
            }catch(error){
               localStorage.removeItem('accessToken')
               localStorage.removeItem('refreshToken')
               

            }
        }
        return Promise.reject(error);
    }
)

export default axiosInstance