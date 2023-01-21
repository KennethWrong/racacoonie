import React, { useEffect, useState } from "react";
import Container from '@mui/material/Container';
import axios from 'axios'
import {useParams} from 'react-router-dom';

export default function Recipe () {
    const [recipe, setRecipe] = useState(null);
    const {rid} = useParams();

    useEffect(() => {
        getRecipe()
    }, [])

    const getRecipe = async () => {
        try{
            axios.get(`http://localhost:8000/recipe/${rid}`).then(
                (res) => {
                    console.log(res['data']['recipe'])
                    setRecipe(res['data']['recipe'])
                    console.log('lmao')
                    return "recipe received"
                }
            )
        } catch (err){
            console.log(err)
            return "Error"
        }
    }

    return (
        <Container>
            {recipe ?
            <h1> {recipe['name']}</h1>
            :
            <h1>Recipe</h1>
            }
        </Container>
    )
}
