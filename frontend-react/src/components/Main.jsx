import React from 'react'
import Button from './Button'




const Main = () => {
  return (
   <>
   
   
   <div className='container'>
        <div className='p-5 text-center bg-light-dark rounded'>
            <h1 className='text-light'>Stock Prediction Portal</h1>
            <p className='text-light lead'>This Stock prediction application utilizes machine learning techniques , specifically employing keras
                , and lstm model , integrated within the django framework.it <br />forecasts future stock prices by analyzing 100-day and 200-day moving 
                averages , essential indicators widely used by stock analysis to inform trading and investment decisions.
            </p>
            <Button text='Login' class="btn-outline-info" />

        </div>
   </div>
   
   </>
  )
}

export default Main
