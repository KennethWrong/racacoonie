import IconButton from '@mui/material/IconButton';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import React, { useEffect, useState } from "react";
import axios from 'axios'
import { Box } from '@mui/system';


export default function SaveButton ({rid}) {

    const [liked, setLiked] = useState()

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
                    const savedRecipes = res['data']
                    if(savedRecipes){
                        savedRecipes.forEach((r) => {
                            if(r['id'] == rid) {
                                setLiked(true);
                                return;
                            }
                        })
                    }
                }
            )
        } catch (err){
            console.log(err)
            return err
        }
    }


    const handleLikefunction = (e) => {
        e.preventDefault();
        const config = {
            headers:{
              authorization: localStorage.getItem("racacoonie-auth-token")
            }}
        axios.post('http://localhost:8000/recipe/like', {'rid':rid}, config).then((res) => {
            setLiked(true)
        })
    }

    const handleUnlikefunction = (e) => {
        e.preventDefault();

        const config = {
            headers:{
              authorization: localStorage.getItem("racacoonie-auth-token")
            }}
            
            axios.post('http://localhost:8000/recipe/unlike', {'rid':rid}, config).then((res) => {
            setLiked(false)
        })
    }

    return (
        <div>
        {liked?
        <IconButton onClick={handleUnlikefunction}>
            <FavoriteIcon color="error"/>
        </IconButton> :
        <IconButton onClick={handleLikefunction}>
            <FavoriteBorderIcon color="error"/>
        </IconButton>
        }
        </div>
    )
}