import React, { useEffect, useState } from "react";
import Container from '@mui/material/Container';
import axios from 'axios'
import {useParams} from 'react-router-dom';
import { Grid } from "@mui/material";
import RecipeBlock from "../components/RecipeBlock";

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
                }
            )
        } catch (err){
            console.log(err)
            return "Error"
        }
    }

    return (
        <Container>
            {
                recipe ? 
                <div>
                    <h1 className="text-6xl m-9 font-black"> {recipe['name']}</h1>
                    <img src="https://mdbootstrap.com/img/new/slides/041.jpg" className="max-w-full h-auto" alt="..." />
                    <div className="grid grid-cols-3 gap-4">
                        <RecipeBlock title="Time needed:" text={recipe['minutes']} />
                        <RecipeBlock title="Calories:" text={recipe['calories']} />
                        <RecipeBlock title="Total Steps:" text={recipe['n_steps']} />
                    </div>
                    <div>
                        <h1 className="text-4xl m-9 font-black">Description</h1>
                        <p>
                            {recipe['description']}
                        </p>
                    </div>
                    <div>
                        <h1 className="text-4xl m-9 font-black">Description</h1>
                        <ol className="list-decimal">
                        {recipe['steps'].map((step, index) => (
                            <li key={index}>{step}</li>
                        ))}
                        </ol>
                    </div>
                </div> :
                <h1 className="text-6xl m-9 font-black"> Loading...</h1>
            }
        </Container>
    )
}
