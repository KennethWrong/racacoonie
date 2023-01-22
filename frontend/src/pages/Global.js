import React from "react";
import { useEffect, useState, useRef } from 'react';
import ReactDOM from "react-dom";
import GoogleMapReact from 'google-map-react';
import FavoriteIcon from '@mui/icons-material/Favorite';
import axios from 'axios';
import CountryMarker from "../components/CountryMarker";
 
export default function Global(){
    const [recipes, setRecipes] = useState([])
    useEffect(() => {
        axios.get('http://localhost:8000/recipe/all').then((res) => {
            const data = res['data']
            setRecipes(data['recipes'])
        })
    }, [])

    const longlatdic = {
        "cn": [35.86166, 104.195397],
        "mx": [23.634501, -102.552784],
        "it": [41.87194, 12.56738],
        "us": [37.09024, -95.712891]
    }

    const defaultProps = {
      center: {
        lat: 10.99835602,
        lng: 77.01502627
      },
      zoom: 0
    };

    const getLongLat = (countryCode) => {
        if (!(countryCode in longlatdic)) {
            return [20.337, 30.337]
        }
        return longlatdic[countryCode];
    }
  
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: "AIzaSyDlCjCQsCWUEZng7BwjWom5u95vvlORrW8" }}
          defaultCenter={defaultProps.center}
          defaultZoom={-4}
        >
        {recipes? 
        recipes.map((rec, index) => (
            <CountryMarker 
                key={index}
                lat={getLongLat(rec['region'])[0]}
                lng={getLongLat(rec['region'])[1]}
                recipe ={rec}
            /> 
        )) : ""
        }
        </GoogleMapReact>
      </div>
    );
  }