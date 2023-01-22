import React from "react";
import { useEffect, useState, useRef } from 'react';
import ReactDOM from "react-dom";
import GoogleMapReact from 'google-map-react';
import FavoriteIcon from '@mui/icons-material/Favorite';
import axios from 'axios';
 
export default function Global(){
    const [recipes, setRecipes] = useState([])

    useEffect(() => {
        axios.get('http://localhost:8000/recipe/all').then((res) => {
            console.log(res)
        })
    }, [])

    const defaultProps = {
      center: {
        lat: 10.99835602,
        lng: 77.01502627
      },
      zoom: 0
    };
  
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: "AIzaSyDlCjCQsCWUEZng7BwjWom5u95vvlORrW8" }}
          defaultCenter={defaultProps.center}
          defaultZoom={-4}
        >
          <FavoriteIcon
            lat={59.955413}
            lng={30.337844}
          />
        </GoogleMapReact>
      </div>
    );
  }