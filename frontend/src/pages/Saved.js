import React, { useEffect, useState } from "react";
import Container from '@mui/material/Container';
import axios from 'axios'
import {useParams} from 'react-router-dom';
import { Grid } from "@mui/material";
import RecipeCards from "../components/RecipeCards";

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
                    setRecipes(res['data'])
                }
            )
        } catch (err){
            console.log(err)
            return err
        }
    }

    return (
        <Container>
            {recipes? 
            <div>
                <RecipeCards recipes={recipes} />
            </div> 
            :
            <p>No saved yet tho</p>}
        </Container>
    )
}
