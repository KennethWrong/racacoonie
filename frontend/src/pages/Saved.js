import React, { useEffect, useState } from "react";
import Container from '@mui/material/Container';
import axios from 'axios'
import {useParams} from 'react-router-dom';
import { Grid } from "@mui/material";
import RecipeBlock from "../components/RecipeBlock";

export default function Recipe () {
    const [recipes, setRecipes] = useState(null);

    useEffect(() => {
        getSavedRecipe()
    }, [])

    const getSavedRecipe = async () => {
        try{
            const config = {
                headers:{
                  authorization: localStorage.getItem("racacoonie-auth-token")
                }
              };
            axios.get(`http://localhost:8000/user/liked`, config).then(
                (res) => {
                    console.log(res['data'])
                    setRecipes(res['data'])
                }
            )
        } catch (err){
            console.log(err)
            return "Error"
        }
    }

    return (
        <Container>
            {recipes? 
            <div>
                <ol className="pl-5 mt-2 space-y-1 list-decimal list-inside">
                    {recipes?recipes.map((rec, index) => (
                        <li key={index} className="font-bold text-xl m-2">{rec['name']}</li>
                    )): "NaN"}
                 </ol>
            </div> 
            :
            <p>No saved yet tho</p>}
        </Container>
    )
}
